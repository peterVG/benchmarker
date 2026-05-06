# Task B-2.3: Backend Orchestration API Walkthrough

## Goal Description
The objective of this task was to create a lightweight FastAPI application that wraps the existing headless execution engine and metrics collector, fulfilling the Orchestration API requirements.

## SRS Mappings
- **F-006: Backend Orchestration API**: An API is available at `/api/run` to trigger batch inference processes.
- **F-007: Log Streaming**: A WebSocket endpoint is available at `/api/logs/{job_id}` to stream the embedded `stdout/stderr` logs.

## Implementation Details
1. **Dependencies**: Added `fastapi`, `uvicorn`, and `websockets` to `apps/backend/requirements.txt`.
2. **Schemas**: Created Pydantic models in `app/api/schemas.py` to strongly type the `RunConfiguration` request and `RunResponse`.
3. **Orchestrator**: Developed `JobOrchestrator` in `app/api/orchestrator.py` which manages background threads. It connects the API to the existing `DatasetManager`, `OllamaRunner`, and `DatabaseManager`, allowing multiple jobs to run in isolated threads and pushing log output to Python queues.
4. **FastAPI App**: Developed `app/api/main.py` configuring CORS to allow connections from the future Phase 3 dashboard, mapping HTTP triggers and Websocket upgrades to the Orchestrator.

## Verification
- Added `orchestration_api_SRS-BENCH-006.feature` containing BDD scenarios to verify HTTP triggering and WebSocket connection semantics.
- Created `tests/features/steps/orchestration_api_steps.py` utilizing the `TestClient` and WebSocket `starlette` handlers.
- **Results**: All tests pass successfully, confirming that the orchestration layer operates seamlessly with the underlying execution harness.
