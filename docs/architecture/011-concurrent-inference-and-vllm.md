# Architecture Decision Record - Benchmarker
011-concurrent-inference-and-vllm.md

1. **Title:** Support Concurrent Inference and Pluggable vLLM Runner
2. **Status:** Accepted
3. **Context / Requirement Reference:** The original system was limited to serial benchmarking due to SQLite file locks and single-threaded batch orchestrators. To support actual load testing and benchmarking model performance under concurrent requests (e.g., measuring continuous batching efficiency), the system needs to process multiple prompts simultaneously.
4. **Decision:** 
   - We will refactor the `Execution Controller` to use a thread pool to dispatch concurrent asynchronous inference requests based on a UI-provided `concurrency` setting.
   - We will introduce a new `vLLMRunner` that programmatically spawns a local vLLM Python process to serve as an alternative to Ollama.
   - We will enable Write-Ahead Logging (WAL) in SQLite and stream metric results to the Database individually, ensuring these writes are pushed to the WebUI for real-time reporting.
5. **Rationale:** This approach allows us to genuinely test parallel inference throughput while strictly adhering to our scale-to-zero, minimal dependency architecture (SQLite). By keeping the writes decoupled and using WAL mode combined with connection timeouts, we mitigate write contention and avoid `database is locked` errors without needing a heavy database like PostgreSQL.
6. **Assumptions:** 
   - The host machine has sufficient RAM/VRAM to handle multiple concurrent generations.
   - vLLM can be invoked locally via a Python subprocess just like the Ollama binary.
7. **Alternatives Considered:** 
   - Migrating to PostgreSQL or InfluxDB for concurrent writes (Rejected due to NFR-003 Minimal Dependencies).
   - Only supporting Ollama for concurrency (Rejected because vLLM is an industry standard for continuous batching).
8. **Consequences / Implications:** 
   - Increased backend complexity to manage thread pools and WebSockets.
   - The UI must now handle real-time streaming updates instead of just a final batch report.
9. **Related Decisions / Notes:** 
   - Supplements `009-pluggable-ai-runner-architecture.md`
   - Modifies implementation details of `006-use-sqlite-for-datastore.md`
