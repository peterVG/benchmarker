# Implementation Plan: Backend (Python)

This localized checklist dictates the implementation flow for the Backend module of the Benchmarker application.

## Phase 1: Foundational Database & Ingestion

- [x] **Task B-1.1: Initialize SQLite Database & Schema**
  - **Description:** Implement the base data layer to durably store telemetry and metrics. Configure the `data/` directory.
  - **Estimated Time:** 2 hours
  - **Dependencies:** None
  - **Related Requirements:** [SRS-BENCH-004](../../docs/srs.md), TC-002
  - **Related Tests:** [`persistent_storage_SRS-BENCH-004.feature`](../tests/features/persistent_storage_SRS-BENCH-004.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task B-1.1. Then begin development within apps/backend/ keeping in mind ADR 006. Additionally, invoke the @feature-writer skill to translate SRS requirements into executable BDD feature tests. Upon completion, YOU MUST generate apps/backend/docs/tasks/Task-B-1.1-Walkthrough.md directly in the project repository with clear SRS mapping (including BOTH the ID and full human-readable title text) in heading position 2 exclusively, and strictly delete any internal tracking Plan/ToDos documents before checking off the Markdown box locally in docs/plan.md and apps/backend/docs/plan.md. Then commit your changes and push the branch to origin.`

- [ ] **Task B-1.2: Implement HuggingFace Dataset Ingestion**
  - **Description:** Implement the `datasets` wrapper to download and format industry benchmarks (e.g., RVL-CDIP, FUNSD) locally.
  - **Estimated Time:** 2 hours
  - **Dependencies:** Task B-1.1
  - **Related Requirements:** [SRS-BENCH-001](../../docs/srs.md)
  - **Related Tests:** [`dataset_ingestion_SRS-BENCH-001.feature`](../tests/features/dataset_ingestion_SRS-BENCH-001.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task B-1.2. Then begin development within apps/backend/, integrating the HuggingFace datasets library per ADR 007. Invoke the @feature-writer skill for BDD testing. Upon completion, generate apps/backend/docs/tasks/Task-B-1.2-Walkthrough.md natively in the repository referencing the SRS, delete any scratchpads, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`

## Phase 2: Execution & Metric Engines

- [ ] **Task B-2.1: Ollama Batch Execution Harness**
  - **Description:** Write the core iteration logic to pass formatted dataset items to the local Ollama API via REST HTTP calls.
  - **Estimated Time:** 3 hours
  - **Dependencies:** Task B-1.2
  - **Related Requirements:** [SRS-BENCH-002](../../docs/srs.md), TC-001
  - **Related Tests:** [`batch_execution_SRS-BENCH-002.feature`](../tests/features/batch_execution_SRS-BENCH-002.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task B-2.1. Then begin development within apps/backend/ focusing on local-first processing via the Ollama REST API (ADR 005). Invoke the @feature-writer skill for BDD scenarios. Upon completion, generate apps/backend/docs/tasks/Task-B-2.1-Walkthrough.md with SRS mappings, delete internal tracking files, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`

- [ ] **Task B-2.2: Metric Collection & Accuracy Validation**
  - **Description:** Implement telemetry tracking (latency, tokens/sec, VRAM) and calculate accuracy scores against ground truth. Route data to SQLite.
  - **Estimated Time:** 3 hours
  - **Dependencies:** Task B-2.1
  - **Related Requirements:** [SRS-BENCH-003](../../docs/srs.md)
  - **Related Tests:** [`metric_collection_SRS-BENCH-003.feature`](../tests/features/metric_collection_SRS-BENCH-003.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task B-2.2. Then begin development within apps/backend/. Calculate the required performance and accuracy metrics. Invoke the @feature-writer skill for BDD testing. Upon completion, generate apps/backend/docs/tasks/Task-B-2.2-Walkthrough.md referencing the SRS, delete any scratchpads, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`
