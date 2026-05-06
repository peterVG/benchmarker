import asyncio
import uuid
import queue
import threading
from typing import Dict, Any, Generator
from .schemas import RunConfiguration
from app.modules.execution.runners.ollama_runner import OllamaRunner
from app.modules.execution.metrics import MetricsCollector
from app.modules.ingestion.dataset_manager import DatasetManager
from app.modules.persistence.database import DatabaseManager
from datetime import datetime

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
            
            # Select runner
            if config.runner_type.lower() == "ollama":
                runner = OllamaRunner()
            else:
                q.put(f"[ERROR] Unsupported runner type {config.runner_type}")
                self.jobs[job_id]["status"] = "failed"
                return
                
            q.put(f"[INFO] Starting runner {config.runner_type}...")
            
            with runner as active_runner:
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
                results = active_runner.execute_batch(config.model_name, run_stream, config.prompt_template)
                
                q.put(f"[INFO] Batch completed. Processing metrics...")
                stop_forwarder.set()
                log_thread.join(timeout=1)
                
            # Process metrics and save
            processed_results = []
            metrics_list = []
            
            for res in results:
                processed = MetricsCollector.process_result(res)
                metrics_list.append({
                    "dataset_item_id": str(processed["item"].get("id", "unknown")),
                    "latency_ms": int(processed["telemetry"]["total_latency_sec"] * 1000),
                    "tokens_per_sec": processed["telemetry"]["tokens_per_sec"],
                    "vram_usage_mb": 0,
                    "is_correct": 1 if processed.get("accuracy", {}).get("is_exact_match", False) else 0
                })
                processed_results.append(processed)
                
            self.db.initialize_schema()
            self.db.save_run(
                run_date=datetime.utcnow().isoformat() + "Z",
                hardware_profile="unknown", # We can add this to config later
                model_name=config.model_name,
                metrics=metrics_list
            )
            
            self.jobs[job_id]["results"] = processed_results
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
