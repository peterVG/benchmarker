Feature: Control Dashboard
  As a user
  I want to interact with the benchmarking system via a UI
  So that I can configure runs, view live logs, and analyze historical metrics

  Scenario: Render historical metrics chart
    Given the dashboard is loaded
    Then I should see the historical metrics chart rendered

  Scenario: Submit configuration form
    Given the dashboard is loaded
    When I select the "ollama" runner
    And I enter the model name "llama3.2"
    And I enter the dataset ID "ag_news"
    And I click the Run Benchmark button
    Then I should see a status indicating the run has started
    And the terminal should become visible

  Scenario: Stream logs to the terminal
    Given a benchmarking run has been started
    When the backend sends log messages via WebSocket
    Then the terminal should append the log messages to its output
