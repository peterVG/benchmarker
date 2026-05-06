from behave import given, when, then
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

@given('the orchestration API is running')
def step_impl_api_running(context):
    context.client = client

@when('I send a POST request to "/api/run" with a valid configuration')
def step_impl_post_run(context):
    payload = {
        "runner_type": "ollama",
        "model_name": "llama3",
        "dataset_name": "dummy/dataset",
        "max_items": 1
    }
    from unittest.mock import patch
    with patch('app.api.main.orchestrator.create_job', return_value="mock-job-123"):
        context.response = context.client.post("/api/run", json=payload)

@then('the API should return a 200 status code')
def step_impl_status_code(context):
    assert context.response.status_code == 200

@then('the response should contain a job_id')
def step_impl_has_job_id(context):
    data = context.response.json()
    assert "job_id" in data
    assert data["job_id"] == "mock-job-123"

@given('a job has been triggered and returned a job_id')
def step_impl_job_triggered(context):
    context.job_id = "mock-job-123"
    from app.api.main import orchestrator
    
    async def mock_iter_logs(job_id):
        yield "[INFO] Starting job"
        yield "[INFO] Loading dataset"
    
    context.original_iter = orchestrator.iter_job_logs
    orchestrator.iter_job_logs = mock_iter_logs

@when('I connect to the WebSocket endpoint "/api/logs/{job_id}"')
def step_impl_ws_connect(context, job_id):
    context.ws_messages = []
    from starlette.websockets import WebSocketDisconnect
    try:
        with client.websocket_connect(f"/api/logs/{context.job_id}") as websocket:
            context.ws_messages.append(websocket.receive_text())
            context.ws_messages.append(websocket.receive_text())
    except WebSocketDisconnect:
        pass
    except Exception as e:
        pass

@then('I should receive log messages from the execution daemon')
def step_impl_receive_logs(context):
    from app.api.main import orchestrator
    if hasattr(context, 'original_iter'):
        orchestrator.iter_job_logs = context.original_iter
        
    assert len(context.ws_messages) > 0
    assert "[INFO] Starting job" in context.ws_messages
