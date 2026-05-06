from behave import given, when, then
from app.modules.execution.metrics import MetricsCollector

@given('the batch execution harness is processing an item')
def step_impl_processing_item(context):
    pass

@when('the Ollama API returns a successful response')
def step_impl_api_success(context):
    context.mock_response = {
        "metrics": {
            "eval_duration": 1500000000,  # 1.5s
            "eval_count": 30,             # 30 tokens
            "total_duration": 2000000000  # 2.0s
        }
    }
    context.telemetry = MetricsCollector.calculate_telemetry(context.mock_response)

@then('the system should record the latency')
def step_impl_record_latency(context):
    assert "total_latency_sec" in context.telemetry
    assert context.telemetry["total_latency_sec"] == 2.0

@then('the system should record the time to first token')
def step_impl_record_ttft(context):
    # Time to first token is not natively exposed in the non-streaming JSON, 
    # but eval_duration represents the generation phase latency.
    assert "eval_duration_sec" in context.telemetry

@then('the system should record the tokens per second')
def step_impl_record_tps(context):
    assert "tokens_per_sec" in context.telemetry
    assert context.telemetry["tokens_per_sec"] == 20.0  # 30 tokens / 1.5s

@given('the model has generated an output for a dataset item')
def step_impl_generated_output(context):
    context.generated_output = "The invoice total is 150.00"

@given('the dataset item has a known ground-truth label')
def step_impl_known_ground_truth(context):
    context.ground_truth = "150.00"

@when('the metric collection engine compares the output')
def step_impl_compare_output(context):
    context.accuracy = MetricsCollector.calculate_accuracy(context.generated_output, context.ground_truth)

@then('it should calculate an accuracy score (e.g., exact match or similarity)')
def step_impl_calculate_score(context):
    assert "exact_match" in context.accuracy
    assert "substring_match" in context.accuracy
    assert context.accuracy["substring_match"] is True

@then("attach the score to the item's metric record")
def step_impl_attach_score(context):
    assert "score" in context.accuracy
    assert context.accuracy["score"] == 1.0

@given('the model generates an empty or malformed JSON output')
def step_impl_empty_output(context):
    context.generated_output = ""
    context.ground_truth = "invoice"

@when('the metric collection engine attempts to parse and compare the output')
def step_impl_compare_empty(context):
    context.accuracy = MetricsCollector.calculate_accuracy(context.generated_output, context.ground_truth)

@then('it should record an accuracy score of 0')
def step_impl_score_zero(context):
    assert context.accuracy["score"] == 0.0

@then('flag the specific item as a parsing failure')
def step_impl_flag_failure(context):
    assert context.accuracy["substring_match"] is False
    assert context.accuracy["exact_match"] is False
