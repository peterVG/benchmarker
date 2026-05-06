# Project Requirements Document: Benchmarker

# Executive Summary
Benchmarker is a lightweight, automated benchmarking harness designed to batch-test local AI models (specifically for OCR and text classification) across diverse hardware profiles. It evaluates system performance and model accuracy, outputting presentation-ready reports.

# Product Vision
Benchmarker solves the problem of manual, non-reproducible local AI testing by providing an automated benchmarking pipeline with persistent reporting.

## Problem Statement
AI developers need to evaluate different local AI models for OCR and text classification across different hardware architectures (e.g., Apple Silicon and Nvidia DGX). Current UI-based tools (like Open WebUI) are designed for interactive chat, making automated batch-testing, accuracy evaluation against ground truth, and metric tracking tedious, manual, and non-reproducible.

## Target Users
Solo AI developer/engineer prioritizing automated dataset pipelines, precise metric tracking, and exportable data visualizations over a polished consumer user interface.

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
**User Story:** As an AI developer, I want to run batches of documents through local vision/language models via Ollama so that I can evaluate them efficiently.
### Acceptance Criteria
- Script can iterate through a dataset and query the local Ollama API.
- Harness supports swapping out different local models via configuration.
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
- Database schema supports querying by model, hardware profile, and run date.
*(Source: docs/product-vision.md)*

## F-005: Presentation-Ready Reporting
**Priority:** Mandatory
**User Story:** As an AI developer, I want to view my test results via a simple HTML pager so that I can easily browse historical runs and export graphs for presentations.
### Acceptance Criteria
- System generates an HTML report or dashboard from SQLite data.
- Includes graphical representations of performance and accuracy metrics.
*(Source: docs/product-vision.md)*

## Technology Stack
- **Frontend:** HTML Pager/Dashboard
- **Backend:** Python (with HuggingFace `datasets`) and Ollama execution layer
- **Storage:** SQLite

# Non-Functional Requirements

## NFR-001: Cross-Platform Execution
**Requirement:** Must run seamlessly on both Apple Silicon (M5) and Nvidia architectures (Asus GX10 DGX).
**Rationale:** The user tests across diverse hardware profiles.

## NFR-002: Local-First Processing
**Requirement:** All model execution, data processing, and storage must occur locally.
**Rationale:** Ensures data privacy and sovereignty; complies with local-first principles.

## NFR-003: Minimal Dependencies
**Requirement:** Use lightweight, mainstream tools (Python, SQLite, Ollama) and avoid heavy UI frameworks or complex external databases.
**Rationale:** Reduces setup friction and ensures the tool remains a lightweight harness rather than a bloated application.

## NFR-004: Scale-to-Zero
**Requirement:** The benchmarking script and reporting tool consume zero active resources when not running.
**Rationale:** No always-on services (other than the base Ollama daemon).

# Technical Constraints

## TC-001: Local Execution Only
**Constraint:** Must not rely on external cloud APIs for model inference.
**Rationale:** Ensures privacy and accurate local hardware performance metrics.

## TC-002: SQLite Datastore
**Constraint:** Must use SQLite for the datastore.
**Rationale:** Follows the mandate for a zero-friction setup without requiring separate database server provisioning.

# Release Criteria

## RC-001: End-to-End Benchmark Run
**Criteria:** The system successfully ingests a sample HuggingFace dataset, runs it against an Ollama model, and records the metrics in SQLite.
**Verification:** Manual execution of the script and verification of SQLite database contents.

## RC-002: Report Generation
**Criteria:** The HTML reporting pager correctly displays the metrics of the completed benchmark run.
**Verification:** Open the HTML pager in a browser and verify graphical and text outputs.

# AGENTS.md Principles Integration

- **Minimize Dependencies → Feature Simplicity:** Uses standard Python, SQLite, and Ollama.
- **Scale-to-Zero → Performance Requirements:** Tool is an on-demand script/pager, no persistent server overhead.
- **Zero-Friction Setup:** SQLite database requires no manual initialization.
- **Local-First:** All data remains on the user's machine.
