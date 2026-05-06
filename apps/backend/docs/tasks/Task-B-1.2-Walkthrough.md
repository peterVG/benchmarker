# Task B-1.2 Walkthrough: Dataset Ingestion

## SRS-BENCH-001: Automated Dataset Ingestion

This document provides a walkthrough of the implementation for Task B-1.2, which introduces the HuggingFace `datasets` integration.

### Implementation Details

1. **`DatasetManager` Module:** Created `apps/backend/app/modules/ingestion/dataset_manager.py`. It provides the `DatasetManager` class that wraps `datasets.load_dataset()`.
2. **Offline Resilience:** The wrapper catches specific operating system and connection errors, re-throwing them as custom domain exceptions like `InsufficientStorageError` and `DatasetIngestionError` to decouple standard error handling from the HF library specificities.
3. **Data Standardization:** The `stream_documents()` method ensures datasets are transformed into a standard internal dictionary with `id`, `content`, and `label` keys, protecting the application from varied HF schemas.
4. **Centralized Logging:** Followed ADR 004 by using Python's standard `logging` to stream unbuffered logs directly to `stdout`.

### BDD Test Verification

The BDD feature tests were executed locally within the isolated virtual environment:

```text
Feature: Dataset Ingestion # tests/features/dataset_ingestion_SRS-BENCH-001.feature:2
  As an AI developer
  I want the system to automatically download and format HuggingFace datasets
  So that I can evaluate models against standard benchmarks

  Scenario: Ingest a standard dataset successfully                           # tests/features/dataset_ingestion_SRS-BENCH-001.feature:8
    Given the system has internet access to HuggingFace                    # tests/features/steps/dataset_ingestion_steps.py:10
    When I specify the "rvl_cdip" dataset for ingestion                    # tests/features/steps/dataset_ingestion_steps.py:14
    Then the dataset should be downloaded and cached locally               # tests/features/steps/dataset_ingestion_steps.py:25
    And the ground-truth labels should be mapped to the expected output format # tests/features/steps/dataset_ingestion_steps.py:30

  Scenario: Ingesting a large dataset with limited local storage           # tests/features/dataset_ingestion_SRS-BENCH-001.feature:15
    Given the system has less than 2GB of available storage                # tests/features/steps/dataset_ingestion_steps.py:38
    When I specify a 10GB dataset for ingestion                            # tests/features/steps/dataset_ingestion_steps.py:42
    Then the system should throw an insufficient storage error             # tests/features/steps/dataset_ingestion_steps.py:54
    And the partial download should be cleaned up                          # tests/features/steps/dataset_ingestion_steps.py:58

  Scenario: Ingesting a non-existent dataset                               # tests/features/dataset_ingestion_SRS-BENCH-001.feature:22
    Given the HuggingFace datasets library is configured                   # tests/features/steps/dataset_ingestion_steps.py:64
    When I specify a non-existent dataset name "fake_dataset_name"         # tests/features/steps/dataset_ingestion_steps.py:68
    Then the system should catch the download error                        # tests/features/steps/dataset_ingestion_steps.py:80
    And log a "dataset not found" error message                            # tests/features/steps/dataset_ingestion_steps.py:84

1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
12 steps passed, 0 failed, 0 skipped
```

The output validates that all ingestion scenarios execute correctly, robustly handle edge-case exceptions, and strictly follow the behavior outlined in the SRS requirements.
