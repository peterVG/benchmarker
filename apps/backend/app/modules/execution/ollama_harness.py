import os
import subprocess
import threading
import queue
import time
import requests
from typing import Generator, List, Dict, Any

class ModelUnavailableError(Exception):
    pass

class OllamaDaemon:
    """
    Context manager that handles the lifecycle of an embedded Ollama daemon.
    It automatically routes Ollama models to the project's models/ directory
    and provides a thread-safe generator to yield stdout/stderr logs.
    """
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            # Resolve to the root of the benchmarker project (3 levels up from this file)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.models_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..', 'models'))
        else:
            self.models_dir = os.path.abspath(models_dir)
            
        self.process = None
        self.log_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._log_thread = None

    def __enter__(self):
        os.makedirs(self.models_dir, exist_ok=True)
        env = os.environ.copy()
        env['OLLAMA_MODELS'] = self.models_dir
        
        # Start the daemon
        self.process = subprocess.Popen(
            ["ollama", "serve"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # Pipe stderr to stdout
            text=True,
            bufsize=1
        )
        
        # Start a thread to read stdout and put it in the queue
        self._log_thread = threading.Thread(target=self._read_logs)
        self._log_thread.daemon = True
        self._log_thread.start()
        
        # Give the daemon a moment to bind to the port
        time.sleep(2)
        return self

    def _read_logs(self):
        """Reads lines from the subprocess stdout and puts them in a queue."""
        for line in iter(self.process.stdout.readline, ''):
            if line:
                self.log_queue.put(line.strip())
            if self._stop_event.is_set():
                break

    def iter_logs(self) -> Generator[str, None, None]:
        """Generator that yields log lines as they become available."""
        while not self._stop_event.is_set() or not self.log_queue.empty():
            try:
                # Timeout allows the loop to periodically check the stop event
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

class OllamaHarness:
    """
    Client for executing batches of inference requests against the Ollama API.
    """
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()

    def check_model(self, model_name: str) -> bool:
        """Checks if a model is locally available in the Ollama daemon."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get('models', [])
            return any(m.get('name') == model_name for m in models)
        except requests.exceptions.RequestException:
            return False

    def pull_model(self, model_name: str) -> None:
        """Pulls a model from the Ollama registry."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name, "stream": False}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ModelUnavailableError(f"Failed to pull model '{model_name}': {e}")

    def generate(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """Generates a response from the model (non-streaming)."""
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

    def execute_batch(self, model_name: str, dataset_stream: Generator, prompt_template: str) -> List[Dict[str, Any]]:
        """
        Iterates over a dataset generator, querying the Ollama API, and accumulating results.
        Returns the accumulated results. If a connection error occurs during batch execution,
        it gracefully returns the results collected up to that point.
        """
        results = []
        
        # Ensure the model is available before starting the batch
        if not self.check_model(model_name):
            self.pull_model(model_name)
            
        try:
            for item in dataset_stream:
                try:
                    # Try to format the prompt using keys in the item
                    prompt = prompt_template.format(**item)
                except KeyError:
                    # Fallback if the template doesn't match the item's keys
                    prompt = prompt_template
                    
                response = self.generate(model_name, prompt)
                
                results.append({
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
                })
        except requests.exceptions.ConnectionError as e:
            # Daemon crashed or became unreachable during execution
            print(f"Error during batch execution: Connection to Ollama failed. Safely saving results obtained so far. Details: {e}")
        finally:
            self.session.close()
            
        return results
