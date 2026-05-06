# Task B-2.1: Ollama Batch Execution Harness Walkthrough

## SRS-BENCH-002: Batch Model Execution Harness

This task implemented the core logic to iteratively pass dataset items to a local Ollama daemon for inference, fulfilling the requirement for a Batch Model Execution Harness.

### Embedded Daemon & Observability Support
As part of the embedded architectural requirement (ADR 008), the `OllamaDaemon` context manager was implemented to:
1. Spawns the `ollama` executable locally.
2. Directs the downloaded model cache to `<project-root>/models/` via the `OLLAMA_MODELS` environment variable.
3. Exposes an `iter_logs()` generator that captures daemon `stdout` and `stderr` asynchronously. This allows the forthcoming Orchestration API (Task B-2.3) to securely stream logs directly to the new Interactive Control Dashboard, fulfilling the F-007 observability requirements.

### Harness Operations
The `OllamaHarness` provides the `execute_batch` functionality:
- **Model Check/Pull**: Validates that the requested model exists in the `models/` cache using `GET /api/tags`. If absent, automatically invokes `POST /api/pull`.
- **Generation**: Formats each dataset item and sends non-streaming requests to `POST /api/generate`, simplifying response aggregation for latency/tokens metrics.
- **Crash Recovery**: If the `requests` library encounters a connection timeout or refusal (e.g. the daemon crashes mid-run), it safely returns the array of generated results completed up to that exact point, preventing data loss.

### BDD Test Verification

The module was tested via `behave` covering the happy paths, automatic pull scenarios, and graceful daemon crash recovery.

```
Feature: Batch Model Execution # tests/features/batch_execution_SRS-BENCH-002.feature:2
  As an AI developer
  I want to run a batch of documents through local Ollama models
  So that I can test their capabilities efficiently
  
  Scenario: Execute batch inference against a local model
    Given the Ollama daemon is running locally on port 11434
    And a dataset has been successfully ingested
    Given the local model "llama3" is pulled and available
    When I trigger the batch execution harness for "llama3"
    Then the harness should iterate over the dataset items
    And query the Ollama API for each item
    And record the generated response

  Scenario: Execute batch inference with an unavailable model
    Given the Ollama daemon is running locally on port 11434
    And a dataset has been successfully ingested
    Given the local model "unpulled_model" is not available in Ollama
    When I trigger the batch execution harness for "unpulled_model"
    Then the system should attempt to pull the model automatically
    And if it fails, throw an explicit "model unavailable" error

  Scenario: Ollama daemon crashes during batch execution
    Given the Ollama daemon is running locally on port 11434
    And a dataset has been successfully ingested
    Given the batch execution harness is running
    When the Ollama daemon becomes unreachable at 50% completion
    Then the harness should log the connection error
    And safely save the results obtained so far
    And exit gracefully

1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
20 steps passed, 0 failed, 0 skipped
```
