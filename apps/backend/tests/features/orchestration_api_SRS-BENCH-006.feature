Feature: Backend Orchestration API
  As a frontend dashboard
  I want to interact with the backend execution harness via an API
  So that I can trigger runs and stream logs

  Scenario: Trigger a benchmark run
    Given the orchestration API is running
    When I send a POST request to "/api/run" with a valid configuration
    Then the API should return a 200 status code
    And the response should contain a job_id

  Scenario: Stream execution logs via WebSocket
    Given a job has been triggered and returned a job_id
    When I connect to the WebSocket endpoint "/api/logs/{job_id}"
    Then I should receive log messages from the execution daemon
