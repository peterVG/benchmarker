Feature: Concurrent Inference Load Testing

  Scenario: User runs a benchmark with multiple concurrent requests
    Given the benchmarker is configured with a concurrency level of 4
    When the batch execution starts
    Then the orchestrator should dispatch 4 concurrent requests to the runner
    And the metric results should stream to the database as they complete
