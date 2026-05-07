import os
import platform
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

class OllamaRunner(AIRunner):
    """
    Concrete implementation of the AIRunner interface for Ollama.
    Handles auto-installation, daemon lifecycle, and batch inference execution.
    """
    def __init__(self, models_dir: str = None, bin_dir: str = None, concurrency: int = 1):
        self.concurrency = concurrency
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 6 levels up from current_dir to get to project root
        project_root = os.path.abspath(os.path.join(current_dir, *['..']*6))
        
        self.models_dir = os.path.abspath(models_dir) if models_dir else os.path.join(project_root, 'models')
        self.bin_dir = os.path.abspath(bin_dir) if bin_dir else os.path.join(project_root, 'bin')
        
        self.executable_path = os.path.join(self.bin_dir, "ollama")
        self.base_url = "http://localhost:11434"
        self.session = requests.Session()
        
        self.process = None
        self.log_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._log_thread = None

    def install(self) -> None:
        if os.path.exists(self.executable_path) and os.access(self.executable_path, os.X_OK):
            version = self.get_version()
            console.print(f"[dim]Ollama binary (version {version}) already exists locally.[/dim]")
            return

        os.makedirs(self.bin_dir, exist_ok=True)
        
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":
            url = "https://github.com/ollama/ollama/releases/latest/download/ollama-darwin"
        elif system == "linux":
            if machine in ["x86_64", "amd64"]:
                url = "https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64"
            elif machine in ["aarch64", "arm64"]:
                url = "https://github.com/ollama/ollama/releases/latest/download/ollama-linux-arm64"
            else:
                console.print(f"[bold red]Unsupported Linux architecture: {machine}[/bold red]")
                return
        else:
            console.print(f"[bold yellow]Auto-install not supported for {system}. Please download Ollama manually and place it at {self.executable_path}.[/bold yellow]")
            return

        console.print(f"[bold cyan]Downloading Ollama binary from {url}...[/bold cyan]")
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(self.executable_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
            # Apply executable permissions (chmod +x)
            os.chmod(self.executable_path, 0o755)
            
            version = self.get_version()
            console.print(f"[bold green][SUCCESS] Ollama version {version} downloaded successfully.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to download Ollama: {e}[/bold red]")

    def get_version(self) -> str:
        try:
            result = subprocess.run([self.executable_path, "-v"], capture_output=True, text=True, check=True)
            # Output is typically "ollama version is X.Y.Z"
            return result.stdout.strip().replace("ollama version is ", "").replace("ollama version ", "")
        except Exception:
            return "unknown"

    def __enter__(self):
        self.install()
        
        os.makedirs(self.models_dir, exist_ok=True)
        env = os.environ.copy()
        env['OLLAMA_MODELS'] = self.models_dir
        env['OLLAMA_NUM_PARALLEL'] = str(self.concurrency)
        
        self.process = subprocess.Popen(
            [self.executable_path, "serve"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        self._log_thread = threading.Thread(target=self._read_logs)
        self._log_thread.daemon = True
        self._log_thread.start()
        
        # Give the daemon a moment to bind to the port
        time.sleep(2)
        console.print("[bold green][SUCCESS] Ollama daemon is locally available and ON.[/bold green]")
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
        console.print("[dim]Ollama daemon stopped.[/dim]")

    def check_model(self, model_name: str) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get('models', [])
            return any(m.get('name') == model_name for m in models)
        except requests.exceptions.RequestException:
            return False

    def pull_model(self, model_name: str) -> None:
        try:
            console.print(f"[bold cyan]Pulling model '{model_name}'...[/bold cyan]")
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name, "stream": False}
            )
            response.raise_for_status()
            console.print(f"[bold green]Successfully pulled model '{model_name}'.[/bold green]")
        except requests.exceptions.RequestException as e:
            raise ModelUnavailableError(f"Failed to pull model '{model_name}': {e}")

    def generate(self, model_name: str, prompt: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()

    def execute_batch(self, model_name: str, dataset_stream: Generator, prompt_template: str, concurrency: int = 1, on_result_cb = None) -> List[Dict[str, Any]]:
        results = []
        
        if not self.check_model(model_name):
            self.pull_model(model_name)
            
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
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = []
                for item in dataset_stream:
                    futures.append(executor.submit(process_item, item))
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        results.append(future.result())
                    except Exception as e:
                        console.print(f"[bold red]Item generation failed: {e}[/bold red]")
                        
        except requests.exceptions.ConnectionError as e:
            console.print(f"[bold red]Error during batch execution: Connection to Ollama failed. Safely saving results obtained so far. Details: {e}[/bold red]")
        finally:
            self.session.close()
            
        return results
