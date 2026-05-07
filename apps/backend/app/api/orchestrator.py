import asyncio
import uuid
import queue
import threading
from typing import Dict, Any, Generator
from .schemas import RunConfiguration
from app.modules.execution.runners.ollama_runner import OllamaRunner
from app.modules.execution.runners.vllm_runner import VLLMRunner
from app.modules.execution.metrics import MetricsCollector
from app.modules.ingestion.dataset_manager import DatasetManager
from app.modules.persistence.database import DatabaseManager
from datetime import datetime

import platform
import subprocess

def detect_hardware() -> str:
    sys_name = platform.system()
    machine = platform.machine()
    
    if sys_name == "Darwin" and machine == "arm64":
        return "MacOS Apple Silicon"
    
    try:
        # Check for NVIDIA GPU
        subprocess.check_output(["nvidia-smi"], stderr=subprocess.STDOUT)
        return "NVIDIA CUDA"
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
        
    return f"{sys_name} {machine} (CPU)"

class JobOrchestrator:
    def __init__(self):
        self.jobs = {}
        self.log_queues: Dict[str, queue.Queue] = {}
        self.db = DatabaseManager()

    def create_job(self, config: RunConfiguration) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "config": config,
            "status": "pending",
            "results": []
        }
        self.log_queues[job_id] = queue.Queue()
        
        # Start background thread
        thread = threading.Thread(target=self._run_job, args=(job_id, config))
        thread.daemon = True
        thread.start()
        
        return job_id

    def _run_job(self, job_id: str, config: RunConfiguration):
        self.jobs[job_id]["status"] = "running"
        q = self.log_queues[job_id]
        
        try:
            q.put(f"[INFO] Starting job {job_id}")
            
            # Load dataset
            q.put(f"[INFO] Loading dataset {config.dataset_name}...")
            loader = DatasetManager()
            dataset = loader.load_dataset_split(config.dataset_name, split="train")
            stream = loader.stream_documents(dataset)
            
            # Limited stream
            def limited_stream(s, limit):
                for i, item in enumerate(s):
                    if i >= limit:
                        break
                    yield item

            run_stream = limited_stream(stream, config.max_items)
            
            # Validate concurrency
            if config.concurrency < 1:
                q.put(f"[ERROR] Invalid concurrency level: {config.concurrency}")
                self.jobs[job_id]["status"] = "failed"
                return

            # Select runner
            if config.runner_type.lower() == "ollama":
                runner = OllamaRunner(concurrency=config.concurrency)
            elif config.runner_type.lower() == "vllm":
                runner = VLLMRunner(model_name=config.model_name, concurrency=config.concurrency)
            else:
                q.put(f"[ERROR] Unsupported runner type {config.runner_type}")
                self.jobs[job_id]["status"] = "failed"
                return

            q.put(f"[INFO] Starting runner {config.runner_type} with concurrency {config.concurrency}...")
            
            with runner as active_runner:
                # Initialize run in DB only after runner is successfully started
                self.db.initialize_schema()
                run_id = self.db.create_run(
                    run_date=datetime.utcnow().isoformat() + "Z",
                    hardware_profile=detect_hardware(),
                    model_name=config.model_name,
                    runner_type=config.runner_type
                )

                # Log forwarder thread
                stop_forwarder = threading.Event()
                def forward_logs():
                    for log_line in active_runner.iter_logs():
                        q.put(log_line)
                        if stop_forwarder.is_set():
                            break

                log_thread = threading.Thread(target=forward_logs)
                log_thread.daemon = True
                log_thread.start()

                q.put(f"[INFO] Executing batch...")
                
                # Setup callback for streaming results
                def handle_result(raw_res):
                    processed = MetricsCollector.process_result(raw_res)
                    metric_data = {
                        "dataset_item_id": str(processed["item"].get("id", "unknown")),
                        "latency_ms": int(processed["telemetry"]["total_latency_sec"] * 1000),
                        "tokens_per_sec": processed["telemetry"]["tokens_per_sec"],
                        "vram_usage_mb": 0,
                        "is_correct": 1 if processed.get("accuracy", {}).get("exact_match", False) else 0
                    }
                    try:
                        self.db.save_metric(run_id, metric_data)
                    except Exception as e:
                        q.put(f"[ERROR] Failed to save metric: {str(e)}")
                    self.jobs[job_id]["results"].append(processed)
                    q.put(f"[METRIC] Item complete: Latency={metric_data['latency_ms']}ms, TPS={metric_data['tokens_per_sec']:.2f}")

                active_runner.execute_batch(
                    config.model_name, 
                    run_stream, 
                    config.prompt_template, 
                    concurrency=config.concurrency, 
                    on_result_cb=handle_result
                )
                
                q.put(f"[INFO] Batch completed.")
                stop_forwarder.set()
                log_thread.join(timeout=1)
                
            self.jobs[job_id]["status"] = "completed"
            q.put(f"[INFO] Job {job_id} completed successfully.")
            
        except Exception as e:
            q.put(f"[ERROR] Job failed: {str(e)}")
            self.jobs[job_id]["status"] = "failed"

    async def iter_job_logs(self, job_id: str):
        if job_id not in self.log_queues:
            yield f"[ERROR] Unknown job ID {job_id}"
            return
            
        q = self.log_queues[job_id]
        
        while True:
            # Check if job is done and queue is empty
            status = self.jobs[job_id]["status"]
            if status in ["completed", "failed"] and q.empty():
                break
                
            try:
                # Use a small sleep to prevent blocking the async event loop
                log_line = q.get_nowait()
                yield log_line
            except queue.Empty:
                await asyncio.sleep(0.1)

orchestrator = JobOrchestrator()
