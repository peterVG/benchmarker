# Architecture Decision Record - Benchmarker
010-native-bare-metal-deployment.md

1. **Title:** Use Native Bare-Metal Deployment for Application Runtime
2. **Status:** Accepted
3. **Context / Requirement Reference:** The deployment architecture must guarantee 100% native hardware acceleration for the embedded AI daemon (Ollama) across diverse host platforms, including Apple Silicon (Mac M5 Unified Memory) and Nvidia hardware (Blackwell GPUs). Standard containerization (Docker) on macOS does not currently support passing the Metal GPU into a Linux container, which forces the embedded AI daemon to run on the CPU during inference, violating performance requirements.
4. **Decision:** We will deploy the frontend and backend applications natively (bare-metal) on the production host, bypassing Docker for the core application runtime. The backend will be managed natively using process managers (e.g., `PM2` or `systemd`), while the frontend assets will be built and served via a lightweight static web server on the host. The observability stack (Loki, Grafana, Redpanda) will remain containerized.
5. **Rationale:** Executing the FastAPI backend and its embedded Ollama daemon natively is the only robust way to ensure immediate, zero-friction access to the host's native GPU drivers (CUDA or Metal) without introducing platform-specific container complexity or degrading performance on Macs.
6. **Assumptions:** The host machine will have the required runtime dependencies (Python >=3.12, Node.js >=20) pre-installed or managed via version managers (`mise`, `asdf`, etc.).
7. **Alternatives Considered:** 
   - **Dockerizing the Backend:** Rejected due to the inability to access the Metal GPU on macOS hosts from within a Docker Linux container.
   - **OS-Specific Docker Deployments:** (i.e. Native on Mac, Docker on Linux) - Rejected because it fragments the deployment documentation and adds unnecessary complexity for users attempting a standard deployment.
8. **Consequences / Implications:** Deployment requires developers/operators to configure the host environment manually with Python and Node.js rather than pulling a single Docker image. 
9. **Related Decisions / Notes:** Integrates directly with ADR `008-embed-ollama-daemon.md`. The observability infrastructure specified in ADR `004-centralized-observability.md` remains in Docker via `docker-compose.yml`.
