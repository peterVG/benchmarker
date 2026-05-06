# SRS-BENCH-002: Batch Model Execution Harness
Feature: Batch Model Execution
  As an AI developer
  I want to run a batch of documents through local Ollama models
  So that I can test their capabilities efficiently

  Background:
    Given the Ollama daemon is running locally on port 11434
    And a dataset has been successfully ingested

  # Happy Path
  Scenario: Execute batch inference against a local model
    Given the local model "llama3" is pulled and available
    When I trigger the batch execution harness for "llama3"
    Then the harness should iterate over the dataset items
    And query the Ollama API for each item
    And record the generated response

  # Edge Case
  Scenario: Execute batch inference with an unavailable model
    Given the local model "unpulled_model" is not available in Ollama
    When I trigger the batch execution harness for "unpulled_model"
    Then the system should attempt to pull the model automatically
    And if it fails, throw an explicit "model unavailable" error

  # Error Case
  Scenario: Ollama daemon crashes during batch execution
    Given the batch execution harness is running
    When the Ollama daemon becomes unreachable at 50% completion
    Then the harness should log the connection error
    And safely save the results obtained so far
    And exit gracefully

  # Source
  # - srs.md SRS-BENCH-002: Batch Model Execution Harness
  # - prd.md F-002: Batch Model Execution Harness
