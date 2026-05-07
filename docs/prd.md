# Project Requirements Document: Benchmarker

# Executive Summary
Benchmarker is an automated benchmarking harness designed to batch-test local AI models across diverse hardware profiles. It features an interactive Control Dashboard allowing users to dynamically configure runs, evaluate system performance, and monitor real-time execution logs.

# Product Vision
Benchmarker solves the problem of manual, non-reproducible local AI testing by providing a unified interface to configure dataset pipelines, execute model benchmarking locally, and persistently track metrics and logs.

## Problem Statement
AI developers need to evaluate different local AI models for OCR and text classification across different hardware architectures. Current UI-based tools are designed for interactive chat, making automated batch-testing, accuracy evaluation against ground truth, and metric tracking tedious, manual, and non-reproducible.

## Target Users
AI developers/engineers prioritizing automated dataset pipelines, precise metric tracking, exportable data visualizations, and full control over local execution environments through an integrated control dashboard.

# Functional Requirements

## F-001: Automated Dataset Ingestion
**Priority:** Mandatory
**User Story:** As an AI developer, I want to automatically ingest HuggingFace datasets (e.g., RVL-CDIP, FUNSD, SROIE) so that I can use standard testing benchmarks without manual data structuring.
### Acceptance Criteria
- System can download and format standard HuggingFace document datasets.
- System maps dataset ground-truth labels to expected evaluation outputs.
*(Source: docs/product-vision.md)*

## F-002: Batch Model Execution Harness
**Priority:** Mandatory
**User Story:** As an AI developer, I want to run batches of documents through local vision/language models via a pluggable AI runner (e.g., Ollama, vLLM, llama.cpp) so that I can evaluate them efficiently using the best execution engine for my hardware.
### Acceptance Criteria
- Script can iterate through a dataset and query the local API of the active AI model runner.
- Harness supports downloading and swapping out different AI model runners (Ollama, vLLM, etc.) and their respective models via configuration.
*(Source: docs/product-vision.md)*

## F-003: Metric Collection Engine
**Priority:** Mandatory
**User Story:** As an AI developer, I want to track system performance and accuracy metrics so that I can compare different models objectively.
### Acceptance Criteria
- Tracks latency, time to first token, tokens/sec, and VRAM/RAM usage.
- Compares model outputs against ground truth for classification/OCR accuracy.
*(Source: docs/product-vision.md)*

## F-004: Persistent Storage of Results
**Priority:** Mandatory
**User Story:** As an AI developer, I want to save test results to a SQLite database so that I can maintain a historical record of all benchmark runs.
### Acceptance Criteria
- All metrics are written to a local SQLite database.
- Database schema supports querying by model, runner type, hardware profile, and run date.
*(Source: docs/product-vision.md)*

## F-005: Presentation-Ready Reporting
**Priority:** Mandatory
**User Story:** As an AI developer, I want to view my test results via a dashboard so that I can easily browse historical runs and export graphs for presentations.
### Acceptance Criteria
- System generates an HTML report or dashboard from SQLite data.
- Includes graphical representations of performance and accuracy metrics.
*(Source: docs/product-vision.md)*

## F-006: Benchmark Configuration UI
**Priority:** Mandatory
**User Story:** As an AI developer, I want a starting point UI to select my benchmarking parameters so that I can quickly orchestrate runs without modifying scripts.
### Acceptance Criteria
- User can select the AI harness (e.g., Ollama, vLLM).
- User can specify the AI model to be benchmarked.
- User can select a HuggingFace dataset from the local cache or search online repositories directly from the UI.

## F-007: Execution Observability UI
**Priority:** Mandatory
**User Story:** As an AI developer, I want to track and recall daemon logs directly in the app so that I can debug inference issues.
### Acceptance Criteria
- The UI tracks, stores, and recalls logging (stdout, stderr) from the active AI model runner daemon.
- The implementation adheres to the project's centralized observability rules (routing streams appropriately).

## F-008: Concurrent Inference Load Testing
**Priority:** Mandatory
**User Story:** As an AI developer, I want to test model performance under concurrent load so that I can measure continuous batching efficiency.
### Acceptance Criteria
- User can specify a concurrency level.
- The orchestrator dispatches multiple simultaneous inference requests to the active AI runner.
- The UI receives real-time metric streaming as individual concurrent requests complete.

## Technology Stack
- **Frontend:** Interactive HTML Dashboard (Vite/Vanilla JS or framework as decided)
- **Backend:** Python (with HuggingFace `datasets`) and an embedded, pluggable AI execution layer (managed programmatically by the script).
- **Storage:** SQLite and local file cache (`models/` and `bin/` directories for runners and weights).

# Non-Functional Requirements

## NFR-001: Cross-Platform Execution
**Requirement:** Must run seamlessly on both Apple Silicon (M5) and Nvidia architectures (Asus GX10 DGX).
**Rationale:** The user tests across diverse hardware profiles.

## NFR-002: Local-First Processing
**Requirement:** All model execution, data processing, and storage must occur locally.
**Rationale:** Ensures data privacy and sovereignty; complies with local-first principles.

## NFR-003: Minimal Dependencies
**Requirement:** Use lightweight, mainstream tools (Python, SQLite) and avoid heavy UI frameworks or complex external databases. AI model runners must be managed as embedded binaries or local environments rather than system-wide dependencies.
**Rationale:** Reduces setup friction and ensures the tool remains a lightweight harness rather than a bloated application.

## NFR-004: Scale-to-Zero
**Requirement:** The benchmarking script and reporting tool consume zero active resources when not running.
**Rationale:** No always-on services. The embedded AI model runners are strictly started and stopped as part of the benchmark run lifecycle.

# Technical Constraints

## TC-001: Local Execution Only
**Constraint:** Must not rely on external cloud APIs for model inference.
**Rationale:** Ensures privacy and accurate local hardware performance metrics.

## TC-002: SQLite Datastore
**Constraint:** Must use SQLite for the datastore.
**Rationale:** Follows the mandate for a zero-friction setup without requiring separate database server provisioning.

# Release Criteria

## RC-001: End-to-End Benchmark Run
**Criteria:** The system successfully ingests a sample HuggingFace dataset, downloads the selected AI runner, runs it against a model, and records the metrics in SQLite.
**Verification:** Manual execution of the script and verification of SQLite database contents.

## RC-002: Report Generation
**Criteria:** The HTML reporting pager correctly displays the metrics of the completed benchmark run.
**Verification:** Open the HTML pager in a browser and verify graphical and text outputs.

# AGENTS.md Principles Integration

- **Minimize Dependencies → Feature Simplicity:** Uses standard Python, SQLite, and embedded AI binaries.
- **Scale-to-Zero → Performance Requirements:** Tool is an on-demand script/pager, no persistent server overhead.
- **Zero-Friction Setup:** SQLite database requires no manual initialization. AI runners and requested models are automatically downloaded and cached locally upon first run.
- **Local-First:** All data remains on the user's machine, including cached LLM weights and runner binaries.
