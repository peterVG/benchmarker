from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .schemas import RunConfiguration, RunResponse
from .orchestrator import orchestrator
import asyncio

app = FastAPI(title="Benchmarker Orchestration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/run", response_model=RunResponse)
async def trigger_run(config: RunConfiguration):
    """
    Triggers a new benchmark run in the background.
    Returns a Job ID that can be used to stream logs.
    """
    job_id = orchestrator.create_job(config)
    return RunResponse(job_id=job_id, status="pending")

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    """
    Gets the current status of a job.
    """
    if job_id not in orchestrator.jobs:
        return {"error": "Job not found"}
    
    return {"job_id": job_id, "status": orchestrator.jobs[job_id]["status"], "results_count": len(orchestrator.jobs[job_id]["results"])}

@app.get("/api/runs")
async def get_all_runs():
    """
    Retrieves all historical benchmarking runs and their aggregated metrics.
    """
    from app.modules.persistence.database import DatabaseManager
    db = DatabaseManager()
    runs = db.get_all_runs()
    return {"runs": runs}

@app.websocket("/api/logs/{job_id}")
async def websocket_logs(websocket: WebSocket, job_id: str):
    """
    Streams the stdout/stderr logs from the background job execution runner.
    """
    await websocket.accept()
    
    try:
        async for log_line in orchestrator.iter_job_logs(job_id):
            await websocket.send_text(log_line)
    except WebSocketDisconnect:
        print(f"Client disconnected from logs for job {job_id}")
    finally:
        pass
