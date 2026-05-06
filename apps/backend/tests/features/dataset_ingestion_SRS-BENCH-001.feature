# SRS-BENCH-001: Automated Dataset Ingestion
Feature: Dataset Ingestion
  As an AI developer
  I want the system to automatically download and format HuggingFace datasets
  So that I can evaluate models against standard benchmarks

  # Happy Path
  Scenario: Ingest a standard dataset successfully
    Given the system has internet access to HuggingFace
    When I specify the "rvl_cdip" dataset for ingestion
    Then the dataset should be downloaded and cached locally
    And the ground-truth labels should be mapped to the expected output format

  # Edge Case
  Scenario: Ingesting a large dataset with limited local storage
    Given the system has less than 2GB of available storage
    When I specify a 10GB dataset for ingestion
    Then the system should throw an insufficient storage error
    And the partial download should be cleaned up

  # Error Case
  Scenario: Ingesting a non-existent dataset
    Given the HuggingFace datasets library is configured
    When I specify a non-existent dataset name "fake_dataset_name"
    Then the system should catch the download error
    And log a "dataset not found" error message

  # Source
  # - srs.md SRS-BENCH-001: Automated Dataset Ingestion
  # - prd.md F-001: Automated Dataset Ingestion
