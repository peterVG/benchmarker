# Architecture Decision Record - Benchmarker
005-use-ollama-for-execution.md

1. **Title:** Use Ollama for Local Model Execution
2. **Status:** Accepted
3. **Context / Requirement Reference:** F-002 Batch Model Execution Harness and TC-001 Local Execution Only require a reliable, local engine to execute AI inference.
4. **Decision:** We will use the Ollama API as the local model execution layer.
5. **Rationale:** Ollama provides a robust, standardized HTTP API (`localhost:11434`) out of the box, abstracting away the complexities of manual weight loading and hardware acceleration optimization (e.g., Apple Metal vs. CUDA). This satisfies NFR-001 Cross-Platform Execution.
6. **Assumptions:** The host machine has Ollama installed and the daemon is running in the background.
7. **Alternatives Considered:** 
   - `llama.cpp` directly (requires more complex Python bindings and compilation steps for different hardware).
   - `LMStudio` (primarily GUI focused, harder to automate programmatically via a headless script).
8. **Consequences / Implications:** The script is dependent on the `ollama` daemon being active. Users must manually install models via `ollama run <model>` before benchmarking.
9. **Related Decisions / Notes:** Integrates directly with the `batch_execution_SRS-BENCH-002.feature` tests.
