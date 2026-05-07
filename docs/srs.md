# Software Requirements Specification (SRS) - Benchmarker

## 1. Functional Requirements

### SRS-BENCH-001: Automated Dataset Ingestion
The system MUST download and format standard HuggingFace document datasets (e.g., RVL-CDIP, FUNSD, SROIE). The system MUST map the dataset ground-truth labels to expected evaluation outputs for downstream comparison.

**Technical Implementation:**
- Utilize the Python `datasets` library from HuggingFace to download and cache the datasets locally.

**Source**
- `[prd.md](./prd.md)` F-001 Automated Dataset Ingestion

**Tests**
- [`dataset_ingestion_SRS-BENCH-001.feature`](../apps/backend/tests/features/dataset_ingestion_SRS-BENCH-001.feature)

### SRS-BENCH-002: Pluggable Model Execution Harness
The script MUST iterate through the ingested dataset and query the active AI model runner's local API to execute vision/language models. The harness MUST support swapping out different local models and execution runners (e.g., Ollama, vLLM, llama.cpp) via configuration.

**Technical Implementation:**
- The system MUST define an abstract `AIRunner` interface to allow seamless switching between different backend execution strategies.
- Execute HTTP requests to the respective local runner API (e.g., `http://localhost:11434/api/generate` for Ollama).
- The script MUST manage the lifecycle of the embedded AI runner daemon (start/stop) during the benchmarking session.
- The daemon MUST be configured to download and cache local models into the root `models/` directory, and binaries into the root `bin/` directory, to keep the project self-contained.

**Source**
- `[prd.md](./prd.md)` F-002 Batch Model Execution Harness

**Tests**
- [`batch_execution_SRS-BENCH-002.feature`](../apps/backend/tests/features/batch_execution_SRS-BENCH-002.feature)

### SRS-BENCH-003: Metric Collection Engine
The system MUST track execution metrics including latency, time to first token, tokens/sec, and VRAM/RAM usage. The system MUST compare the model's generated output against the ground truth to calculate classification/OCR accuracy.

**Source**
- `[prd.md](./prd.md)` F-003 Metric Collection Engine

**Tests**
- [`metric_collection_SRS-BENCH-003.feature`](../apps/backend/tests/features/metric_collection_SRS-BENCH-003.feature)

### SRS-BENCH-004: Persistent Storage of Results
The system MUST write all gathered metrics and accuracy results to a local SQLite database. The schema MUST support querying by model name, runner type, hardware profile, and run date.

**Technical Implementation:**
- Use Python's built-in `sqlite3` module or `SQLAlchemy` for structured inserts.
- The database file MUST be stored in the root `data/` directory (e.g., `data/benchmarker.sqlite`).

**Source**
- `[prd.md](./prd.md)` F-004 Persistent Storage of Results

**Tests**
- [`persistent_storage_SRS-BENCH-004.feature`](../apps/backend/tests/features/persistent_storage_SRS-BENCH-004.feature)

### SRS-BENCH-005: Presentation-Ready Reporting
The system MUST generate an HTML report or dashboard from the SQLite data. The report MUST include graphical representations of performance and accuracy metrics.

**Technical Implementation:**
- Use a Vanilla JS frontend scaffolded via Vite to read the SQLite data (via API or static export) and render charts (e.g., Chart.js or D3.js).

**Source**
- `[prd.md](./prd.md)` F-005 Presentation-Ready Reporting

**Tests**
- [`presentation_reporting_SRS-BENCH-005.feature`](../apps/frontend/tests/features/presentation_reporting_SRS-BENCH-005.feature)

### SRS-BENCH-007: Concurrent Inference Load Testing
The system MUST support dispatching concurrent inference requests to the active AI runner. The system MUST stream metric results to the persistent SQLite datastore and the frontend dashboard in real-time as individual concurrent requests complete, rather than waiting for the entire batch to finish.

**Technical Implementation:**
- Utilize an asynchronous execution pool (e.g. `ThreadPoolExecutor` or `asyncio.gather`) within the Orchestrator.
- The UI MUST accept a concurrency level parameter.
- The `vLLMRunner` MUST be implemented to support this concurrency optimally using continuous batching.
- The SQLite database connection MUST use Write-Ahead Logging (WAL) and sufficient timeout configuration to avoid locking errors during rapid sequential writes.

**Source**
- `[prd.md](./prd.md)` F-008 Concurrent Inference Load Testing

**Tests**
- [`concurrent_inference_SRS-BENCH-007.feature`](../apps/backend/tests/features/concurrent_inference_SRS-BENCH-007.feature)

## 2. Non-Functional Requirements & Technical Constraints

### SRS-BENCH-NFR-001: Cross-Platform Execution
The system MUST run seamlessly on both Apple Silicon (M5) and Nvidia architectures (Asus GX10 DGX).

**Source**
- `[prd.md](./prd.md)` NFR-001 Cross-Platform Execution

**Tests**
- Validated via CI/CD execution matrices on different hardware nodes.

### SRS-BENCH-NFR-002: Local-First Processing
All model execution, data processing, and storage MUST occur locally. The system MUST NOT rely on external cloud APIs for model inference (TC-001).

**Source**
- `[prd.md](./prd.md)` NFR-002 Local-First Processing
- `[prd.md](./prd.md)` TC-001 Local Execution Only

**Tests**
- Validated via static code analysis verifying no external HTTP requests outside of `localhost:11434` (Ollama) and `huggingface.co` (Dataset download).

### SRS-BENCH-NFR-003: Minimal Dependencies & Scale-to-Zero
The application MUST use lightweight, mainstream tools. The database MUST use SQLite (TC-002). The benchmarking script and reporting tool MUST consume zero active resources when not running.

**Source**
- `[prd.md](./prd.md)` NFR-003 Minimal Dependencies
- `[prd.md](./prd.md)` NFR-004 Scale-to-Zero
- `[prd.md](./prd.md)` TC-002 SQLite Datastore

**Tests**
- Validated by the absence of background daemon services in the `docker-compose.yml` or installation scripts (the embedded AI runner daemons are only active during test execution).

## 3. Traceability Summary Matrix

| PRD Identifier | SRS Identifier | Status |
|---|---|---|
| F-001 | SRS-BENCH-001 | Mapped |
| F-002 | SRS-BENCH-002 | Mapped |
| F-003 | SRS-BENCH-003 | Mapped |
| F-004 | SRS-BENCH-004 | Mapped |
| F-005 | SRS-BENCH-005 | Mapped |
| F-008 | SRS-BENCH-007 | Mapped |
| NFR-001 | SRS-BENCH-NFR-001 | Mapped |
| NFR-002 | SRS-BENCH-NFR-002 | Mapped |
| NFR-003 | SRS-BENCH-NFR-003 | Mapped |
| NFR-004 | SRS-BENCH-NFR-003 | Mapped |
| TC-001 | SRS-BENCH-NFR-002 | Mapped |
| TC-002 | SRS-BENCH-NFR-003 | Mapped |
