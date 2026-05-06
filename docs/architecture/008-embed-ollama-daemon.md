# Architecture Decision Record - Benchmarker
008-embed-ollama-daemon.md

1. **Title:** Embed Ollama Daemon within the Project
2. **Status:** Accepted (Supersedes ADR 005)
3. **Context / Requirement Reference:** F-002 Batch Model Execution Harness and TC-001 Local Execution Only require a reliable, local engine to execute AI inference. We initially assumed an external system-level Ollama installation (ADR 005), but this violates the Zero-Friction Setup principle if users must manually install and manage the daemon and model cache locations.
4. **Decision:** We will embed the Ollama daemon directly within the project and manage its lifecycle programmatically. Additionally, we will configure the daemon to store downloaded models locally within the project at `models/[model-name-version]/`.
5. **Rationale:** Embedding the daemon and caching models locally ensures that the project is completely self-contained. It prevents conflicts with global Ollama installations and makes the benchmarking environment fully reproducible and portable across machines without requiring complex system-level configurations.
6. **Assumptions:** The host machine supports running the Ollama binary natively, and sufficient disk space is available within the project directory for the models.
7. **Alternatives Considered:** 
   - Relying on a system-wide Ollama installation (ADR 005 - rejected to improve zero-friction setup).
   - Using Docker for Ollama (rejected as it adds Docker as a dependency for local execution).
8. **Consequences / Implications:** The project will need to handle downloading the appropriate Ollama binary for the host OS and managing its process lifecycle (start/stop) during benchmark runs. The `models/` directory must be added to `.gitignore` to prevent committing large weights to version control.
9. **Related Decisions / Notes:** Supersedes `005-use-ollama-for-execution.md`. Integrates directly with the `batch_execution_SRS-BENCH-002.feature` tests.
