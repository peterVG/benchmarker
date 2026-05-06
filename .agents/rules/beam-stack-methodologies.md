# Technology Stack
## Frontend & Real-time UX
Specific components that handle how the user interacts with the system.
* **Phoenix allow_upload/3**: A specific function within Phoenix LiveView that handles the complexities of file uploads (like progress bars and temporary storage) natively. It integrates with ex_aws_s3 to stream files directly to cloud S3 buckets.
* **Websockets**: The underlying protocol that powers Phoenix PubSub and LiveView. It maintains an open "pipe" between the server and the browser, allowing the BEAM to push real-time progress bars or AI processing updates to the user without them needing to refresh the page.
* **AI Chatbot**: Instead of using Open WebUI in production, which introduces additional integration overhead. There are advantages to building an AI Chatbot interface natively using Phoenix LiveView.
    * **Deep Integration:** With Phoenix, the chatbot isn't a separate "silo." It can interact directly with Oban jobs  , query the Postgres/PgVector database, and trigger system events natively.
    * **Customization:** Open WebUI is a Python/Svelte-based container. Customizing its look and feel to match the system theme is much harder than just styling a LiveView component.
    * **Reduced Overhead:** Phoenix PubSub and Websockets are already in the stack. These are the exact tools needed to build a high-performance, streaming chat interface.
    * **Phoenix LiveView Streams:** Efficiently manages the AI chat history in the browser. It only sends updates over the wire, not the whole conversation, keeping it snappy even after 1,000 messages.
    * **Phoenix Hooks (JS Interop)**: Used for "Scroll to Bottom" logic. When a new token streams in from the AI, a tiny JS Hook ensures the container stays pinned to the latest text.
    * **Async Operations (handle_async)**: Prevents the UI from "freezing" while the AI is thinking. The user can still click other buttons or navigate the app while the chatbot generates a response in the background.
* **Phoenix Test**: A library designed to simplify the testing of Phoenix LiveView and static pages. It allows the user to simulate clicks and form fills in tests without the overhead of a full browser driver.

## Background Processing & Data Pipelines
This section handles the "heavy lifting"—asynchronous tasks and high-throughput data streams.
* **Oban & Oban Web:** The gold standard for job processing. Because it is backed by Postgres, jobs are never lost even if the BEAM nodes restart. Oban Web provides a real-time dashboard to pause, resume, and inspect job failures.
* **Broadway:** Purpose-built for high-volume data. It excels at consuming from sources like Amazon SQS or RabbitMQ, offering native batching (e.g., "wait for 100 messages before processing") and back-pressure to prevent the system from being overwhelmed.
* **Phoenix PubSub:** Provides real-time communication between nodes. It is used to broadcast "processing complete" messages or progress updates to users' browsers instantly via WebSockets.

## External tooling
External tools and libraries that provide functionality and features to the system.
* **Tesseract (tesseract-elixir):** While the stack uses modern AI via Bumblebee, Tesseract serves as a reliable, "old school" fallback for Optical Character Recognition. It is particularly useful for high-speed, low-power text extraction from clean documents where a full GPU-powered Transformer model would be overkill and a waste of tokens.

## Machine Learning & High-Performance Computing
Leveraging the BEAM for numerical stability and GPU-accelerated tasks.
* **Nx / EXLA:** The "Numerical Elixir" foundation. It allows Elixir to perform matrix math at speeds comparable to Python's NumPy by compiling code for the Blackwell GPU via CUDA 12.x.
* **Bumblebee:** The bridge to AI. It provides pre-trained models (like GPT or ResNet) from Hugging Face, allowing you to run image recognition or text generation natively within your Elixir app without needing a separate Python service.
* **Erlang PartitionSupervisor:** A specialized supervisor used to prevent "VRAM Overload." By partitioning workers to match the number of GPU cores, it ensures the system never tries to run more parallel AI tasks than the hardware can physically handle.

## Storage & Data Persistence
The "Source of Truth" layer, combining relational, vector, and graph data.
* **Postgres & Ecto:** Ecto is the toolkit for database interaction, providing a secure DSL for queries. Postgres serves as the primary data store.
* **PgVector:** Adds "AI memory" to Postgres, allowing the storage and searching of mathematical embeddings (vector data) for semantic search.
* **Apache Age:** A graph database extension for Postgres. It allows you to query complex relationships (like social networks or knowledge graphs) using the Cypher query language alongside standard SQL.
* **ElasticSearch (elasticsearch-elixir):** Used for lightning-fast full-text searching across large datasets where standard SQL indexing is insufficient.
* **Ex_aws_s3:** The interface for "unstructured" data. It handles the storage of large files (images, PDFs) in S3-compatible buckets.

## Distribution & Cluster Management
These tools handle the "Mesh" logic, allowing multiple Elixir nodes to act as a single, cohesive unit.
* **Distributed Erlang & RPC:** The foundation of the stack. It allows nodes to communicate natively. Remote Procedure Calls (RPC) allow one node to execute functions on another as if they were local, while Process Aliases provide stable identifiers for processes that might move between nodes.
* **Libcluster:** Automates the "handshake" between nodes. In dynamic environments (like Docker or AWS), it uses Gossip (UDP) or DNS (SRV) to find new nodes and join them to the cluster automatically.
* **Horde & Horde.Registry:** A distributed, supervisor-managed "phone book." It ensures that if a specific process (like a user session or a worker) dies because a server crashed, it is automatically restarted on a healthy node. The Registry allows any node to find that process without knowing its IP address.

## Observability & Telemetry
The "Flight Recorder" of the system, providing deep insights into distributed behavior.
* **OpenTelemetry (OTel):** The "glue" for distributed tracing. It assigns a Trace ID to a request, so if a file upload fails, you can see exactly which node it was on and what the CPU state was at that microsecond.
* **Prometheus & PromEx:** Prometheus collects the "heartbeat" (metrics) of the servers. PromEx is a specialized Elixir plugin that creates instant Grafana dashboards for BEAM-specific stats like "Process Count" or "Ets Table Memory."
* **The Logging Pipeline (Promtail → Redpanda → Loki):**
    * **LoggerJSON:** Forces Elixir to speak in machine-readable JSON.
    * **Promtail:** Scrapes these logs and ships them.
    * **Redpanda:** A high-speed "buffer." If your logging server (Loki) struggles, Redpanda holds the logs so no data is lost.
    * **Loki:** The searchable archive of all logs across all nodes.
* **Grafana:** The single "window" where all the metrics from Prometheus and logs from Loki are visualized in one place.

## Quality Assurance & Static Analysis
Ensuring code correctness, security, and architectural integrity before deployment.
* **Litmus:** Analyzes BEAM Bytecode to ensure "Purity." It guarantees that functions are idempotent (safe to retry), which is critical for Oban jobs that might be restarted after a crash.
* **Dialyzer & Credo:** Dialyzer catches type mismatches (e.g., passing a string where a number is expected), while Credo acts as a "code mentor," enforcing idiomatic Elixir style.
* **Boundary:** Prevents "Spaghetti Code" in large projects by enforcing strict lines between different modules; it stops an "Ordering" module from reaching into a "Billing" module's private functions.
* **Sobelow:** A security scanner specifically for Phoenix. It detects common web vulnerabilities like SQL injection or Cross-Site Scripting (XSS).

## Testing Frameworks
* **ExUnit:** The native Elixir unit testing framework.
* **Wallaby & Playwright:** Browser automation tools. Wallaby integrates deeply with ExUnit for concurrent browser testing, while Playwright provides a modern, robust engine for end-to-end (E2E) scenarios.
* **Allure:** Generates beautiful, visual test reports that show exactly where a feature failed, often including screenshots of the failed browser state.

## Documentation & Standardization
These tools ensure the codebase remains maintainable as the team or project grows.
* **mix format:** The project's "enforcer." It automatically reformats code to follow the standard Elixir style guide. This eliminates "nitpicky" arguments in code reviews about where a comma should go or how to indent a block.
* **mix docs:** Uses the @moduledoc and @doc attributes within your code to generate a professional, searchable HTML website of your project's documentation (similar to the official HexDocs).

## Infrastructure & Deployment
Tools used to provision the "metal" and manage the lifecycle of the code.
* **Terraform:** Defines the "Hardware as Code." It creates the VPCs, DigitalOcean Droplets, or AWS instances. It ensures your Local Virtualization (via Orbstack or Docker) matches your production environment exactly.
* **Ansible:** The "System Administrator." Once Terraform creates a server, Ansible enters to install CUDA 12.x, the NVIDIA Container Toolkit, and the OpenTelemetry Collector. It also handles Release Deployment, pushing the compiled Elixir binary to the servers and restarting services.
* **Tableplus:** A GUI for developers to visually inspect and debug the Postgres and Apache Age databases.

# Development Methodology
1. **Monorepo Development:** All code lives in a single GitHub repository. Developers run the entire stack locally or deploy to their production environment.
2. **Module Architecture:** Each module should be its own app in the Arkrim monorepo (eg. arkrim-engine, arkrim-upload)
3. **Shared Support Apps:** Each module can rely on shared support apps such as:
    - web nodes that runs Phoenix LiveView and handles the UI, uploads, search, etc.
    - worker nodes that run the Oban job queues for processing and orchestration
    - AI/GPU Nodes that live exclusively on the production AI processing nodes. They host the Nx/EXLA runtime and heavy models.
    - index nodes: dedicated to managing Elasticsearch and PgVector connections.
4. **Architecture Agnostic:** The code is written to be portable between ARM64 (Mac) and x86_64 (GX10). The same Git repository must deploy to both ARM64 and x86_64 without code changes.
5. **Environment Detection:** The system must use runtime.exs to detect available hardware. If a Blackwell GPU is found (GX10), it must initialize EXLA for acceleration; otherwise, it falls back to CPU/Metal (Apple M5 by default).

# Deployment Methodology
1. **Multi-Arch Releases:** GitHub Actions builds distinct Elixir Releases for different target architectures.
2. **Functional Isolation:** In production, the system is deployed as independent module nodes. 
3. **Node Discovery:** Nodes must find each other automatically using libcluster via Gossip or DNS.
4. **Environmental Parity (The .env and runtime.exs)**
    * use Elixir's config/runtime.exs to detect the environment.
    * On Mac: The system detects the lack of a CUDA driver and falls back to CPU-based processing for testing the pipeline logic.
    * On NVIDIA machines: The system detects the Blackwell GPU and initializes the EXLA backend for high-speed tasks like OCR and Embedding.

## Deployment Orchestration
1. **Multi-Arch Releases:** GitHub Actions builds distinct Elixir Releases for different target architectures.
2. **Functional Isolation:** In production, the system is deployed as independent nodes. One node might only run the Web UI, while another runs only the OCR engine.
3. **Cluster Formation:** Set up a unique ERL_AFLAGS="-setcookie arkrim_secret_cookie" across all machines.
4. **Node Discovery:** Nodes must find each other automatically using libcluster via Gossip or DNS.
5. **Distributed Job Processing:** Use Oban's "Engines" to designate which nodes can run which queues to ensure there is no overload on under-resourced nodes.
