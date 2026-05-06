# Architecture Decision Record - Benchmarker
009-pluggable-ai-runner-architecture.md

## 1. Title
Pluggable AI Runner Architecture

## 2. Status
Accepted

## 3. Context / Requirement Reference
The Benchmarker application initially hardcoded the Ollama execution harness for all inference tasks (ADR 005 and ADR 008). However, as local AI tooling rapidly evolves, different AI model runners offer different optimizations depending on hardware (e.g., vLLM for high-throughput GPU inference, llama.cpp for CPU/Mac optimization, or ONNX Runtime). 
To satisfy the requirement that the application should "be able to switch AI model runners (e.g. from ollama to vLLM or llama.cpp)" just as easily as it switches datasets, a more flexible execution architecture is required.

## 4. Decision
We will implement an abstract "Pluggable AI Runner" architecture.
The backend will define an `AIRunner` interface with standard methods:
- `install()`: Auto-downloads and provisions the executable binary for the runner.
- `get_version()`: Retrieves the installed runner's version string.
- `start()` / `stop()`: Manages the lifecycle of the embedded daemon.
- `pull_model(model_name)`: Retrieves the model weights.
- `generate(prompt)`: Executes the inference.
- `iter_logs()`: Streams `stdout/stderr` back to the Orchestration API.

Specific runners (e.g., `OllamaRunner`, `VLLMRunner`) will implement this interface. The Orchestration API will instantiate the required runner dynamically based on the user's dashboard selection.

## 5. Rationale
Hardcoding a single execution engine tightly couples the application to that vendor's API and limitations. By abstracting the execution harness into an interface, the core dataset iteration and metrics collection logic remains independent. This drastically improves the tool's longevity, extensibility, and usefulness for cross-hardware testing.

## 6. Assumptions
- All supported AI runners can operate locally without external cloud dependencies.
- All supported runners provide a REST API or local binding capable of retrieving tokens/sec or execution latency metrics natively.
- All supported runners can be distributed as standalone binaries or local Python dependencies that can be automatically installed without requiring root/sudo privileges.

## 7. Alternatives Considered
- **Sticking strictly with Ollama:** Rejected because Ollama does not natively support all experimental architectures or specific batch optimizations that frameworks like vLLM provide.
- **Using LangChain or LlamaIndex wrappers:** Rejected as they often introduce heavy abstraction overhead and dependencies, violating NFR-003. A bespoke lightweight interface is preferred.

## 8. Consequences / Implications
- **Pros:** Highly extensible. Future-proofs the application against the rapidly changing AI landscape.
- **Cons:** Increases initial development complexity. We must now build and test auto-installer logic, lifecycle management, and API clients for multiple different runners instead of just one. Metric normalization is required if different runners report latency differently.

## 9. Related Decisions / Notes
- Modifies **ADR 008** (Embed Ollama Daemon) by generalizing the embedded daemon requirement to *any* AI runner.
- Impacts **Task B-2.2** (Metric Collection) and **Task B-2.3** (Orchestration API), which must now interact with the abstract `AIRunner` interface rather than a concrete `OllamaHarness` class.
