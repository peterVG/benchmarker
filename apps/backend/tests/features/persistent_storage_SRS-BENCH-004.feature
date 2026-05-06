# SRS-BENCH-004: Persistent Storage of Results
Feature: Persistent Storage
  As an AI developer
  I want to save my benchmark results to a SQLite database
  So that I can maintain a historical record of all runs

  Background:
    Given a local SQLite database exists at "data/benchmarker.sqlite"

  # Happy Path
  Scenario: Save benchmark metrics to the database
    Given a batch execution run has completed successfully
    When the system persists the results
    Then a new run record should be created with the date and hardware profile
    And all individual metric records should be inserted and linked to the run
    And the database commit should succeed

  # Edge Case
  Scenario: Concurrent writes to SQLite database
    Given multiple benchmark harnesses are running simultaneously
    When they attempt to write results to the database at the exact same time
    Then the database layer should handle the concurrency gracefully using SQLite locks
    And no data should be lost

  # Error Case
  Scenario: Database file permissions error
    Given the "data/benchmarker.sqlite" file is read-only
    When the system attempts to persist the results
    Then it should catch the file permission error
    And log a warning
    And export the results to a fallback JSON file instead

  # Source
  # - srs.md SRS-BENCH-004: Persistent Storage of Results
  # - prd.md F-004: Persistent Storage of Results
