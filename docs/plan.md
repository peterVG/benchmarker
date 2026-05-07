# Implementation Plan: Benchmarker (Global Roadmap)

This document outlines the step-by-step implementation plan for the Benchmarker repository, synthesizing the PRD, SRS, ADRs, and BDD features into a holistic roadmap.

## Phase 1: Foundational Database & Ingestion (Backend)

- [x] **Task 1.1: Initialize SQLite Database & Schema**
  - **Description:** Implement the base data layer to durably store telemetry and metrics (using Python's `sqlite3` or `SQLAlchemy`). Configure the `data/` directory to store `benchmarker.sqlite`.
  - **Estimated Time:** 2 hours
  - **Dependencies:** None
  - **Related Requirements:** [SRS-BENCH-004](../docs/srs.md), TC-002
  - **Related Tests:** [`persistent_storage_SRS-BENCH-004.feature`](../apps/backend/tests/features/persistent_storage_SRS-BENCH-004.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task 1.1. Then begin development within apps/backend/ keeping in mind ADR 006. Additionally, invoke the @feature-writer skill to translate SRS requirements into executable BDD feature tests. Upon completion, YOU MUST generate apps/backend/docs/tasks/Task-1.1-Walkthrough.md directly in the project repository with clear SRS mapping (including BOTH the ID and full human-readable title text) in heading position 2 exclusively, and strictly delete any internal tracking Plan/ToDos documents before checking off the Markdown box locally in the appropriate docs/plan.md files. Then commit your changes and push the branch to origin.`

- [x] **Task 1.2: Implement HuggingFace Dataset Ingestion**
  - **Description:** Implement the `datasets` wrapper to download and format industry benchmarks (e.g., RVL-CDIP, FUNSD) locally.
  - **Estimated Time:** 2 hours
  - **Dependencies:** Task 1.1
  - **Related Requirements:** [SRS-BENCH-001](../docs/srs.md)
  - **Related Tests:** [`dataset_ingestion_SRS-BENCH-001.feature`](../apps/backend/tests/features/dataset_ingestion_SRS-BENCH-001.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task 1.2. Then begin development within apps/backend/, integrating the HuggingFace `datasets` library per ADR 007. Invoke the @feature-writer skill for BDD testing. Upon completion, generate apps/backend/docs/tasks/Task-1.2-Walkthrough.md natively in the repository referencing the SRS, delete any scratchpads, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`

## Phase 2: Execution & Metric Engines (Backend)

- [x] **Task 2.1: Ollama Batch Execution Harness**
  - **Description:** Write the core iteration logic to pass formatted dataset items to the local Ollama API via REST HTTP calls. Include error handling for unpulled models or daemon crashes.
  - **Estimated Time:** 3 hours
  - **Dependencies:** Task 1.2
  - **Related Requirements:** [SRS-BENCH-002](../docs/srs.md), TC-001
  - **Related Tests:** [`batch_execution_SRS-BENCH-002.feature`](../apps/backend/tests/features/batch_execution_SRS-BENCH-002.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task 2.1. Then begin development within apps/backend/ focusing on local-first processing via the Ollama REST API (ADR 005). Invoke the @feature-writer skill for BDD scenarios. Upon completion, generate apps/backend/docs/tasks/Task-2.1-Walkthrough.md with SRS mappings, delete internal tracking files, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`

- [x] **Task 2.2: Metric Collection & Accuracy Validation**
  - **Description:** Implement telemetry tracking (latency, tokens/sec, VRAM) during inference and compare the final output to the ground-truth label to calculate an accuracy score. Route this data to the SQLite persistence layer.
  - **Estimated Time:** 3 hours
  - **Dependencies:** Task 2.1
  - **Related Requirements:** [SRS-BENCH-003](../docs/srs.md)
  - **Related Tests:** [`metric_collection_SRS-BENCH-003.feature`](../apps/backend/tests/features/metric_collection_SRS-BENCH-003.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task 2.2. Then begin development within apps/backend/. Calculate the required performance and accuracy metrics. Invoke the @feature-writer skill for BDD testing. Upon completion, generate apps/backend/docs/tasks/Task-2.2-Walkthrough.md referencing the SRS, delete any scratchpads, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`

- [x] **Task 2.3: Backend Orchestration API**
  - **Description:** Create a REST/WebSocket API (e.g., FastAPI) to expose the execution harness to the frontend. It must accept configuration commands (Model, Dataset), trigger runs, and stream the embedded Ollama daemon's stdout/stderr logs.
  - **Estimated Time:** 3 hours
  - **Dependencies:** Task 2.2
  - **Related Requirements:** F-006, F-007
  - **Related Tests:** [`orchestration_api_SRS-BENCH-006.feature`](../apps/backend/tests/features/orchestration_api_SRS-BENCH-006.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task 2.3. Develop a lightweight API in apps/backend/ to orchestrate runs based on UI input and stream daemon logs. Generate the BDD tests and Walkthrough upon completion.`

## Phase 3: Presentation & Reporting (Frontend)

- [x] **Task 3.1: Interactive Control Dashboard**
  - **Description:** Create an interactive UI to configure benchmark runs (select Ollama, model, HF dataset), trigger execution via the Orchestration API, stream live daemon logs, and view historical metrics from SQLite.
  - **Estimated Time:** 6 hours
  - **Dependencies:** Task 2.3
  - **Related Requirements:** [SRS-BENCH-005](../docs/srs.md), F-006, F-007
  - **Related Tests:** [`control_dashboard_SRS-BENCH-005.feature`](../apps/frontend/tests/features/control_dashboard_SRS-BENCH-005.feature)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task 3.1. Then begin development within apps/frontend/. Build the configuration form, the log viewer, and the historical metrics charts. Utilize Playwright with strict DOM assertions to test the UI mounting natively against production builds. Invoke the @feature-writer skill for BDD testing. Upon completion, generate apps/frontend/docs/tasks/Task-3.1-Walkthrough.md referencing the SRS, delete any scratchpads, check off the Markdown box locally in the appropriate docs/plan.md files, commit your changes, and push the branch to origin.`

## Phase 4: Verification & Handoff

- [x] **Task 4.1: Documentation, Dockerization & Setup Sync**
  - **Description:** Update the root `README.md` and Docker setup based on the final configuration of the testing environments.
  - **Estimated Time:** 1 hour
  - **Dependencies:** Phase 3 Complete
  - **Related Requirements:** NFR-003, NFR-004
  - **Related Tests:** N/A
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch. Then read the project's Architecture Decision Records (ADRs) and the finalized tech stack to populate or update the 'Setup Development Environment' (including 'Run the Application' and 'Run tests') and 'Setup Production Environment' (including 'Deploy to Production' and 'Monitor and Update') sections of the README.md file. Ensure installation instructions are platform-agnostic (e.g., don't assume macOS/Homebrew) or explicitly accommodate multiple operating systems as required by the ADRs. However, if the project requires Dockerization, ensure the final Phase of the implementation plan includes a task to populate or update the \`Dockerfile\` based on the finalized tech stack and ADRs as well as include a "How to Dockerize" section in the README.md file that includes a basic overview of how Docker works and its main components. Make sure to check off the task as complete in the appropriate docs/plan.md once finished. Then commit your changes and push the branch to origin.`

- [ ] **Task 4.2: Final Architecture Synthesis**
  - **Description:** Finalize the full architecture rendering using the Architecture Writer skill.
  - **Estimated Time:** 1 hour
  - **Dependencies:** Task 4.1
  - **Related Requirements:** NFR-001
  - **Related Tests:** N/A
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch. Then invoke the @architecture-writer skill. Read its instructions entirely, then execute all steps to synthesize the @docs/prd.md, @docs/srs.md, all srs.md files in apps/[Module Name]/docs/ and ADRs in the @docs/architecture/ folder and an in-depth scan of the codebase reality into a comprehensive @docs/architecture.md file featuring ISO 42010 viewpoints and Mermaid diagrams. Make sure to check off the task as complete in the appropriate @docs/plan.md once finished. Then commit your changes and push the branch to origin.`

## Summary Timeline
- **Total Estimated Time:** 16 hours
- **Critical Path:** SQLite Config -> HuggingFace Ingestion -> Ollama Execution -> Metrics Validation -> UI Pager -> Architecture Handoff
