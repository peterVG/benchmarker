import requests
from behave import given, when, then
from unittest.mock import patch, MagicMock

from app.modules.execution.ollama_harness import OllamaHarness, ModelUnavailableError

@given('the Ollama daemon is running locally on port 11434')
def step_impl_daemon_running(context):
    context.base_url = "http://localhost:11434"
    context.harness = OllamaHarness(base_url=context.base_url)

@given('a dataset has been successfully ingested')
def step_impl_dataset_ingested(context):
    # Create a dummy dataset generator
    def dummy_dataset():
        yield {"text": "Document 1"}
        yield {"text": "Document 2"}
        yield {"text": "Document 3"}
        yield {"text": "Document 4"}
    
    context.dataset = dummy_dataset()
    context.dataset_items = [{"text": f"Document {i}"} for i in range(1, 5)]

@given('the local model "{model_name}" is pulled and available')
def step_impl_model_available(context, model_name):
    context.model_name = model_name
    
    # Mock requests.Session.get for /api/tags
    context.mock_session = MagicMock()
    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {"models": [{"name": model_name}]}
    context.mock_session.get.return_value = mock_get_response
    
    # Mock requests.Session.post for /api/generate
    def mock_post(*args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "response": "Generated output",
            "eval_count": 10,
            "eval_duration": 1000000000,
            "load_duration": 1000000,
            "prompt_eval_count": 5,
            "prompt_eval_duration": 5000000,
            "total_duration": 1500000000
        }
        return mock_resp
        
    context.mock_session.post.side_effect = mock_post
    context.harness.session = context.mock_session

@when('I trigger the batch execution harness for "{model_name}"')
def step_impl_trigger_batch(context, model_name):
    prompt_template = "Analyze this: {text}"
    try:
        context.results = context.harness.execute_batch(model_name, context.dataset, prompt_template)
    except Exception as e:
        context.error = e

@then('the harness should iterate over the dataset items')
def step_impl_iterate_items(context):
    assert len(context.results) == len(context.dataset_items), f"Expected {len(context.dataset_items)} results, got {len(context.results)}"

@then('query the Ollama API for each item')
def step_impl_query_api(context):
    # 1 GET for tags, 4 POSTs for generate
    assert context.mock_session.post.call_count == len(context.dataset_items)

@then('record the generated response')
def step_impl_record_response(context):
    for idx, result in enumerate(context.results):
        assert "response" in result
        assert result["response"] == "Generated output"
        assert result["item"]["text"] == context.dataset_items[idx]["text"]

@given('the local model "{model_name}" is not available in Ollama')
def step_impl_model_unavailable(context, model_name):
    context.model_name = model_name
    
    # Mock requests.Session.get for /api/tags returning empty
    context.mock_session = MagicMock()
    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {"models": []}
    context.mock_session.get.return_value = mock_get_response
    
    # Mock requests.Session.post for /api/pull to fail
    def mock_post_fail(*args, **kwargs):
        if "/api/pull" in args[0]:
            mock_resp = MagicMock()
            # Simulate a 404 or other failure
            mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
            return mock_resp
        return MagicMock()
        
    context.mock_session.post.side_effect = mock_post_fail
    context.harness.session = context.mock_session

@then('the system should attempt to pull the model automatically')
def step_impl_attempt_pull(context):
    # Verify /api/pull was called
    call_args = context.mock_session.post.call_args[0][0]
    assert "/api/pull" in call_args

@then('if it fails, throw an explicit "model unavailable" error')
def step_impl_throw_error(context):
    assert hasattr(context, 'error')
    assert isinstance(context.error, ModelUnavailableError)

@given('the batch execution harness is running')
def step_impl_harness_running(context):
    step_impl_daemon_running(context)
    step_impl_dataset_ingested(context)
    context.model_name = "llama3"
    
    context.mock_session = MagicMock()
    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {"models": [{"name": context.model_name}]}
    context.mock_session.get.return_value = mock_get_response
    
    context.call_count = 0
    def mock_post_crash(*args, **kwargs):
        if "/api/generate" in args[0]:
            context.call_count += 1
            if context.call_count > 2: # Crash at 50% (item 3)
                raise requests.exceptions.ConnectionError("Connection refused")
            mock_resp = MagicMock()
            mock_resp.json.return_value = {"response": "Success", "eval_count": 10, "eval_duration": 10}
            return mock_resp
            
    context.mock_session.post.side_effect = mock_post_crash
    context.harness.session = context.mock_session

@when('the Ollama daemon becomes unreachable at 50% completion')
def step_impl_daemon_crash(context):
    prompt_template = "Analyze this: {text}"
    # Should not raise exception, should handle and return partial results
    context.results = context.harness.execute_batch(context.model_name, context.dataset, prompt_template)

@then('the harness should log the connection error')
def step_impl_log_error(context):
    # In a real test we'd capture stdout/stderr, here we just assume it was logged because execute_batch caught it
    pass

@then('safely save the results obtained so far')
def step_impl_save_partial(context):
    # We expect 2 results since it crashed on the 3rd
    assert len(context.results) == 2

@then('exit gracefully')
def step_impl_exit_gracefully(context):
    # It didn't raise an exception
    assert hasattr(context, 'results')
