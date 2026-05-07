import os
import subprocess
import threading
import queue
import time
import requests
import concurrent.futures
from typing import Generator, List, Dict, Any
from rich.console import Console
from .base import AIRunner, ModelUnavailableError

console = Console()

class VLLMRunner(AIRunner):
    """
    Concrete implementation of the AIRunner interface for vLLM.
    Starts a local vLLM OpenAI-compatible server.
    """
    def __init__(self, model_name: str, concurrency: int = 1):
        self.concurrency = concurrency
        self.model_name = model_name
        self.base_url = "http://localhost:8000/v1"
        self.session = requests.Session()
        
        self.process = None
        self.log_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._log_thread = None

    def install(self) -> None:
        try:
            import vllm
            console.print(f"[dim]vLLM already installed locally.[/dim]")
        except ImportError:
            console.print(f"[bold cyan]Installing vLLM via pip...[/bold cyan]")
            subprocess.run(["pip", "install", "vllm"], check=True)
            console.print(f"[bold green][SUCCESS] vLLM installed successfully.[/bold green]")

    def get_version(self) -> str:
        try:
            import vllm
            return vllm.__version__
        except ImportError:
            return "unknown"

    def __enter__(self):
        self.install()
        
        env = os.environ.copy()
        # VLLM uses Ray for multi-gpu, we restrict to single GPU for local benchmark
        env["CUDA_VISIBLE_DEVICES"] = "0"
        
        cmd = [
            "python", "-m", "vllm.entrypoints.openai.api_server",
            "--model", self.model_name,
            "--port", "8000" # We will use 8000. Wait, our FastAPI uses 8000!
            # Let's use 8080 for vLLM to avoid collision with FastAPI
        ]
        
        # Override base_url to match the custom port
        self.base_url = "http://localhost:8080/v1"
        cmd[-1] = "8080"
        
        console.print(f"[bold cyan]Starting vLLM server on port 8080 with model {self.model_name}...[/bold cyan]")
        self.process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        self._log_thread = threading.Thread(target=self._read_logs)
        self._log_thread.daemon = True
        self._log_thread.start()
        
        # Wait for the server to be ready
        ready = False
        start_time = time.time()
        while time.time() - start_time < 300: # Wait up to 5 mins for large models
            try:
                res = requests.get("http://localhost:8080/health")
                if res.status_code == 200:
                    ready = True
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                
        if not ready:
            raise RuntimeError("vLLM server failed to start within timeout.")
            
        console.print("[bold green][SUCCESS] vLLM daemon is locally available and ON.[/bold green]")
        return self

    def _read_logs(self):
        for line in iter(self.process.stdout.readline, ''):
            if line:
                self.log_queue.put(line.strip())
            if self._stop_event.is_set():
                break

    def iter_logs(self) -> Generator[str, None, None]:
        while not self._stop_event.is_set() or not self.log_queue.empty():
            try:
                yield self.log_queue.get(timeout=0.5)
            except queue.Empty:
                continue

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        if self._log_thread:
            self._log_thread.join(timeout=1)
        console.print("[dim]vLLM daemon stopped.[/dim]")

    def check_model(self, model_name: str) -> bool:
        # vLLM automatically downloads HF models if missing
        return True

    def pull_model(self, model_name: str) -> None:
        pass

    def generate(self, model_name: str, prompt: str) -> Dict[str, Any]:
        start_time = time.time()
        response = self.session.post(
            f"{self.base_url}/completions",
            json={
                "model": model_name,
                "prompt": prompt,
                "max_tokens": 100,
                "temperature": 0.0
            }
        )
        response.raise_for_status()
        data = response.json()
        end_time = time.time()
        
        # Mock Ollama-like metrics from vLLM output since vLLM format is different
        return {
            "response": data["choices"][0]["text"],
            "eval_count": data["usage"]["completion_tokens"],
            "eval_duration": int((end_time - start_time) * 1e9), # nanoseconds
            "load_duration": 0,
            "prompt_eval_count": data["usage"]["prompt_tokens"],
            "prompt_eval_duration": 0,
            "total_duration": int((end_time - start_time) * 1e9)
        }

    def execute_batch(self, model_name: str, dataset_stream: Generator, prompt_template: str, concurrency: int = 1, on_result_cb = None) -> List[Dict[str, Any]]:
        results = []
        
        def process_item(item):
            try:
                prompt = prompt_template.format(**item)
            except KeyError:
                prompt = prompt_template
                
            response = self.generate(model_name, prompt)
            
            res = {
                "item": item,
                "response": response.get("response", ""),
                "metrics": {
                    "eval_count": response.get("eval_count"),
                    "eval_duration": response.get("eval_duration"),
                    "load_duration": response.get("load_duration"),
                    "prompt_eval_count": response.get("prompt_eval_count"),
                    "prompt_eval_duration": response.get("prompt_eval_duration"),
                    "total_duration": response.get("total_duration")
                }
            }
            if on_result_cb:
                on_result_cb(res)
            return res

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
                futures = []
                for item in dataset_stream:
                    futures.append(executor.submit(process_item, item))
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        results.append(future.result())
                    except Exception as e:
                        console.print(f"[bold red]Item generation failed: {e}[/bold red]")
                        
        except requests.exceptions.ConnectionError as e:
            console.print(f"[bold red]Error during batch execution: Connection to vLLM failed. {e}[/bold red]")
        finally:
            self.session.close()
            
        return results
