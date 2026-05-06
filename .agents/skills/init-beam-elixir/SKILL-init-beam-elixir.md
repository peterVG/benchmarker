---
description: Initialize a new BEAM/Elixir project with best practice root directory structure
---

# BEAM/Elixir Project Initialization

This skill guides the AI agent to initialize a new BEAM/Elixir project with the optimal directory structure dictated by the OTP (Open Telecom Platform) framework.

## Step 1: Scaffold the Root Directory Structure

When scaffolding a new project, you MUST create the following directory structure at the root, while keeping all the files and folders that are currently also in the root directory:

**Proposed Resolution for Workspace Boundaries:**
When reviewing `.agents/rules/workspace-boundaries.md`, you may detect a contradiction regarding the placement of the `mix.exs` file. You MUST treat this project as a Polyglot Monorepo structure where each application inside `apps/` is fully independent (i.e., running `mix phx.new my_app` inside `apps/` instead of an umbrella project). This complies with the strict "No Language Tooling at Root" rule and is consistent with the directory structure shown below.

```text
project-root/
├── .github/
│   └── workflows/    # GitHub Actions for Multi-Arch releases
├── ansible/          # Ansible playbooks (GPU provisioning, observability, deployments)
├── terraform/        # Terraform configurations (local virtualization, Cloud VMs)
├── .coderabbit.yaml  # CodeRabbit AI PR Reviewer configurations
├── docker-compose.yml
├── .env
├── prd.md            # Global Product Requirements Document
├── apps/
│   └── my_app/
│       ├── config/
│       ├── include/
│       ├── lib/
│       ├── priv/
│       ├── test/
│       │   ├── unit/
│       │   ├── integration/
│       │   ├── ui/
│       │   ├── features/
│       │   ├── performance/
│       │   └── allure-results/
│       ├── mix.exs
│       ├── mix.lock
│       └── srs.md    # Local Software Requirements Specification linked to PRD
└── README.md
```

Use appropriate Mix commands (`mix phx.new` or `mix new`) and ensure the generation targets a subdirectory within `apps/` (e.g. `apps/my_app/`), rather than the repository root. **CRITICAL: When scaffolding any new service or web module within the `/apps` directory, you MUST explicitly hardcode a unique HTTP port for its development server (e.g. `config/dev.exs`) by scanning the repository's existing applications and incrementing exactly +1 to ensure no two workspaces ever clash on the same port locally.** 

## Step 2: Enforce Documentation Traceability & Sync

Every BEAM/Elixir project MUST adhere rigidly to a Monorepo Requirements Engineering methodology. The AI agent MUST enforce the following rules when creating or updating requirements:

1. **Global Source of Truth:** The root `prd.md` serves as the global orchestrator of the project's vision.
2. **Localized Specs:** Each application in `apps/` MUST maintain its own `srs.md` containing requirements strictly bounded to that specific application/node.
3. **Traceability Metadata:** Every `srs.md` MUST include a YAML frontmatter block at the top that explicitly links to the root PRD. For example:
   ```yaml
   ---
   title: "MyApp Software Requirements Specification"
   parent: "../../prd.md"
   ---
   ```
4. **Line-by-Line Traceability:** Every requirement definition in an `srs.md` MUST explicitly link back to its parent requirement in the root `prd.md` using relative markdown links (e.g., `[PRD Req 1.2](../../prd.md#req-1.2)`).
5. **Active Sync Enforcement:** The agent MUST strictly adhere to the `.agents/rules/sync-logic.md` rule. If an architecture change happens in one app's `srs.md`, the agent is mathematically required to trace upward and update the root `prd.md` or laterally update other apps' `srs.md` if the change breaches an API boundary.

## Step 3: Enforce Distributed Methods & Orchestration

Every BEAM/Elixir project MUST adhere to the following advanced orchestration and distributed architectural patterns:
1. **Architecture Agnostic:** Code MUST be fully portable between ARM64 (Mac) and x86_64 (e.g., GX10 Blackwell) without source code changes. 
2. **Multi-Arch Releases:** You must configure `.github/workflows/` with GitHub Actions pipelines that build distinct Elixir Releases for both ARM64 and x86_64 target architectures.
3. **Environment Parity (`runtime.exs`):** The system MUST use `config/runtime.exs` to dynamically detect available hardware. For example, if a Blackwell GPU (or CUDA driver) is found, it must initialize the `EXLA` backend for high-speed tasks (NX/Bumblebee), otherwise it falls back to CPU/Metal-based processing for safe local testing.
4. **Functional Isolation:** In production, the system must support deployment as independent nodes (e.g., one node runs Web UI, another strictly runs OCR engines).
5. **Cluster & Discovery:** Nodes MUST form a cluster securely using `ERL_AFLAGS="-setcookie arkly_secret_cookie"`. Nodes must automatically discover each other using `libcluster` (via Gossip or DNSSRV).
6. **Distributed Job Processing**: Use Oban "Engines" to designate which nodes can run specific queues, preventing under-resourced nodes from being overloaded. Use Erlang PartitionSupervisor to restrict concurrent processing tasks to match GPU core availability (preventing VRAM exhaustion).

## Step 4: Enforce Technical Stack

You MUST ensure the application uses and configures the following technical dependencies logically into `mix.exs` and node infrastructure:

* **Job & Node Orchestration:** `oban` and `oban_web` (persistent job processing, workflows via Postgres). `broadway` for multi-stage pipelines. `libcluster` (node discovery), `horde` (Distributed Supervisor/Registry so nodes don't need hardcoded IPs), and `Distributed Erlang` / RPC (prefer RPC or Process Aliases over REST/JSON between nodes).
* **AI & Compute Compute:** `nx`, `exla` (CUDA 12.x support), `bumblebee` (HuggingFace Transformers/Vision inside BEAM), `tesseract-elixir` (AI OCR precursor).
* **Data & Storage:** `ecto`, Postgres, `pgvector`, Apache Age (knowledge graph), and `elasticsearch-elixir`. `ex_aws_s3` for storage alongside Phoenix `allow_upload/3`. Phoenix PubSub for live processing updates.
* **Observability (Centralized Stack):**
  - `opentelemetry`: Distribute tracing layer to correlate cross-node actions via Trace IDs.
  - `logger_json`: Write unbuffered JSON objects to stdout. MUST configure to include `node()` metadata for Grafana filtering.
  - `prom_ex` & Prometheus: Auto-capture BEAM metrics (CPU, Oban depth, processes).
  - Promtail (sidecar scraping stdout to Redpanda buffer), Loki (Log aggregator), Grafana.
* **Infrastructure Management:** Terraform (orchestrates local Proxmox VMs, Docker via Orbstack, or Cloud resources) and Ansible (automates GPU/CUDA 12.x provisioning, Promtail/OTel sidecars, and building/pushing Elixir Releases across the cluster).

## Step 5: Populate the apps/README.md file

Create and populate the `apps/README.md` file to explain the application directory structure. Use the following verbatim text:

The best practice for structuring a BEAM project—whether written in Erlang or Elixir—is strictly dictated by the OTP (Open Telecom Platform) framework. Because the BEAM ecosystem expects code to be bundled as self-contained OTP applications, following standard directory layouts ensures compatibility with community build tools, releases, and hot code swapping mechanisms.

While Elixir modernizes some of the naming conventions (like using lib/ instead of src/), the underlying architecture remains identical. This is the standard, best-practice directory layout for a modern BEAM/Elixir project:

```text
project-root/
├── .coderabbit.yaml         # CodeRabbit AI PR Reviewer configurations
├── docker-compose.yml       # Orchestrates the observability stack and databases
├── .env                     # Secure storage for environment variables (DB credentials, API keys)
├── apps/
│   └── my_app/
│       ├── config/       # Application configuration files (e.g., test.exs, dev.exs)
│       ├── include/      # Public header files (.hrl) required by other applications
│       ├── lib/          # Main Elixir source code (or src/ for Erlang .erl files)
│       ├── priv/         # Non-BEAM specific files (executables, static assets)
│       ├── test/         # Consolidated testing infrastructure
│       │   ├── unit/        
│       │   ├── integration/ 
│       │   ├── ui/          
│       │   ├── features/    
│       │   ├── performance/ 
│       │   └── allure-results/
│       ├── mix.exs       # Elixir project configuration and dependencies list
│       └── mix.lock      # Locked versions of dependencies
└── README.md     # Explains this directory structure
```

When writing or configuring code for this stack, you must adhere to the following principles:

**`apps/my_app/`:** In this monorepo structure, backend and frontend Phoenix code is grouped as a standalone OTP application nestled inside `apps/`. It maintains its own `config/`, `lib/`, `deps/`, `test/`, and `mix.exs` completely independent of the global project root.
**`lib/`**: Contains all main source code logic and context boundaries.
**Infrastructure Orchestration**: A `docker-compose.yml` file sits one directory higher in the global project root. Unlike containerized frontend/backend setups, BEAM apps natively run via their local Mix environments. This compose file is specifically responsible for orchestrating the centralized logging stack and local databases without containerizing the Elixir application itself.
**Testing Taxonomy**: Both apps share a comprehensive testing architecture supporting `unit/`, `integration/`, `ui/`, BDD `features/`, `performance/`, and standardized `allure-results/` test reporting. Elixir projects route Ecto test databases specifically to their application root rather than system-wide.
**Isolated Testing & Linting**: All global cache directories and reporting suites MUST strictly run and output within their local workspace directory (e.g. `apps/my_app/test/`) instead of the shared global repository root.
**Centralized Logging / Observability**: All applications must route logs as unbuffered event streams exclusively to `stdout`. The ecosystem relies on a centralized observability stack (Promtail, Loki, Redpanda, Prometheus, Grafana) orchestrated via `docker-compose` to capture and index these logs, strictly forbidding local file logging.

## Step 6: Configure Testing Frameworks

### 1. BDD Feature-Driven Development Standard
To maintain BDD functionality, we use the Elixir-native `Wallaby.Feature` macro atop ExUnit. **Crucially, traditional Gherkin parser libraries (like WhiteBread or Cabbage) are deprecated and fundamentally broken on modern Elixir (v1.15+).** Instead of `.feature` text files, BEAM architects must write native Elixir scenarios in `test/features/` to maintain ecosystem compatibility while generating rich Allure test reports.

### 2. Test Artifact Isolation and Reporting
To guarantee clean project roots, all test-generated artifacts MUST be strictly collapsed into the idiomatic Elixir `test/` directory.

- **Databases:** Ecto test databases must be routed to `test/spotbrowse_test.db` in `config/test.exs` rather than the application root.
- **Test Reports:** Structured test reports (like Allure via `junit_formatter`) must output directly to `test/allure-results/` and compile to `test/allure-report/`.
- **UI Snapshots:** Wallaby failure screenshots must be directed to `test/wallaby_screenshots/`.
- **Do not use plural custom directories:** Custom directories like `tests/` break native `mix test` conventions. The singular `test/` folder should exclusively contain both source logic and ephemeral test artifacts (safely `.gitignore`'d).

### 3. Allure Test Reporting Integration
To properly configure Allure in a BEAM project, adhere to the following native setup:

1. **Leverage the Native Formatter:** We explicitly avoid third-party libraries like `junit_formatter` or `allure_test_formatter`. Instead, Arkrim utilizes a dedicated internal application called `elixir_feature_tests`.
2. **Add Formatter to dependencies:** Add `{:elixir_feature_tests, path: "../elixir_feature_tests", only: :test}` to your application's `mix.exs` file to gain access to the BDD Step macros and the correct JSON serializers.
3. **Configure ExUnit formatter:** Update your `test/test_helper.exs` to include `ExUnit.start(formatters: [ExUnit.CLIFormatter, ElixirFeatureTests.AllureFormatter])`.
4. **Allure CLI:** Ensure that `allure-commandline` is accessible. To view the generated HTML report locally, run `allure serve test/allure-results`. The custom GenServer natively writes the JSON payloads to a `test/allure-results/` directory relative to where the `mix test` command was invoked. You MUST configure a mix alias or test execution hook (e.g. `rm -rf test/allure-results`) to automatically purge historical JSON payloads before initiating new test cycles.

### 4. PhoenixTest and Playwright Integration
To support robust End-to-End (E2E) and integration testing, configure both PhoenixTest and Playwright:

1. **PhoenixTest Setup:** 
   - Add `{:phoenix_test, "~> 0.3.0", only: :test, runtime: false}` to your `mix.exs` dependencies.
   - Configure it to seamlessly traverse LiveView and static pages within ExUnit tests without overhead.
2. **Playwright Setup (for JS/Browser E2E):**
   - Alternatively or additionally to Wallaby, if Playwright is preferred for deep browser automation interacting with LiveView:
   - Run `npm init playwright@latest` inside your `apps/my_app_web/assets/` (or equivalent) directory.
   - Configure playwright to target the Phoenix test server port and ensure tests are output to `test/playwright-results/` to respect the artifact isolation rule.

### 5. QA, Linting, and Security Analysis Standards
To ensure code quality, predictable retries, and strict type safety, configure the following QA tools in your `mix.exs` dependencies. Instruct the agent to use the latest stable versions compatible with the stack:

1. **Formatting:** Use the built-in `mix format` to enforce standard Elixir code style across the project.
2. **Credo** (`{:credo, "> 0.0.0", only: [:dev, :test], runtime: false}`): Focuses on code consistency and "teaching" idiomatic Elixir. It catches high-level design smells that bytecode analysis might ignore. Fast and should be run frequently (`mix credo --strict`).
3. **Dialyzer/Dialyxir** (`{:dialyxir, "> 0.0.0", only: [:dev, :test], runtime: false}`): Uses "Success Typing" to catch type errors. Ensures the data boundaries and type checks are right.
4. **Litmus** (`{:litmus, "> 0.0.0", only: [:dev, :test], runtime: false}`): Performs "purity analysis" by checking if functions have side effects that aren't explicitly declared. Vital for predictable retries (idempotency in Oban), bytecode verification across OS environments, and statically identifying potential "uncaught" exceptions.
5. **Boundary** (`{:boundary, "> 0.0.0", runtime: false}`): Enforces a "pluggable" design by preventing one module from calling internal functions of another module without a proper public API. Requires defining boundaries in the `mix.exs` for each app. Fast and should be run frequently.
6. **Sobelow** (`{:sobelow, "> 0.0.0", only: [:dev, :test], runtime: false}`): Essential for Phoenix LiveView frontends to identify security vulnerabilities (like XSS or insecure uploads) where pure bytecode analysis falls short.

## Step 7: Configure Documentation Generation

Elixir has robust built-in standards for documentation. You must configure the project to use these native tools:

1. **Inline Documentation:** Use `@moduledoc` and `@doc` attributes to document all public modules and functions.
2. **Developer Documentation:** Add `{:ex_doc, "~> 0.31", only: :dev, runtime: false}` to your `mix.exs` dependencies to generate HTML/Epub documentation using `mix docs`.

## Step 8: Generate Inline Documentation Rule

Create a @.agents/rules/docs-enforce.md file that contains the following verbatim content:

---
description: Ensure all code is comprehensively documented using Elixir's native documentation attributes.
---

# Inline Documentation Enforcement

**Purpose:** This rule dictates how an AI agent MUST document the codebase to satisfy the Inline Documentation Mandate in `AGENTS.md`.

## Active Enforcement

Before declaring any coding task "complete" or writing tests, the agent MUST verify that the following components include verbose inline documentation that clearly explains their function and intended usage:

1.  **ALL** Modules (using `@moduledoc`)
2.  **ALL** Public Functions and Macros (using `@doc`)
3.  **ALL** Complex or non-obvious private functions / code blocks (using inline `#` comments)

### Elixir (Backend) Standards
The agent MUST use standard Elixir documentation attributes. These attributes expect Markdown strings and MUST be placed immediately before the module/function definition.
These attributes MUST be parseable by `ex_doc` to generate the final developer documentation site.

### Javascript/CSS (Frontend) Standards
For custom frontend scripts in `assets/`, the agent MUST use standard `JSDoc` syntax (using `/** ... */`) for all functions and logic blocks.

*Failure to document code according to these standards violates the core AGENTS.md manifesto.*

## Step 9: Generate QA and Linting Rule

Create a @.agents/rules/qa-enforce.md file that contains the following verbatim content:

---
description: Ensure all code is cleanly formatted, passes purity analysis, typings, and security checks before testing or committing.
---

# Parallel QA Execution and Linting Enforcement

**Purpose:** This rule dictates the exact QA pipeline and CLI commands that an AI agent MUST execute to validate both the Elixir backend codebase (purity, typing, styles, boundary isolation, security) and Javascript frontend assets.

## Active Enforcement

Before executing any test suite, or before declaring a coding task "complete", the agent MUST successfully execute the QA checks in the following parallel execution strategy (or enforce them sequentially, ensuring all pass):

### 1. Enforce Backend Formatting (Elixir & HEEx)
```bash
mix format --check-formatted
```
*If this fails:* Auto-fix the issues with `mix format`.

### 2. Style and Security Checks (Credo & Sobelow)
* **Credo:** Checks code style and idiomatic design smells.
```bash
mix credo --strict
```
* **Sobelow:** Checks for web security vulnerabilities (XSS, insecure uploads, etc.).
```bash
mix sobelow
```
*If these fail:* Read the output, modify the offending code to align with style/security standards.

### 3. Type Safety Validation (Dialyzer)
* **Dialyzer:** Builds/checks the PLT (Persistent Lookup Table) to ensure type safety.
```bash
mix dialyzer
```
*If this fails:* Proactively fix type mismatches or incorrect `@spec` definitions.

### 4. Bytecode Purity Analysis (Litmus)
* **Litmus:** Performs bytecode purity analysis and exception path tracing. Run each time *after* compiling to ensure functions intended to be idempotent remain pure and side-effect free.
```bash
mix compile && mix litmus
```
*If this fails:* Refactor logic to isolate side-effects explicitly and ensure core retryable paths remain pure.

### 5. Encapsulation Verification (Boundary)
* **Boundary:** Verifies no cross-app encapsulation leaks exist.
```bash
mix compile && mix boundary
```
*If this fails:* Expose the required private function via a public API or correct the unauthorized cross-module call.

### 6. Format and Lint Frontend Assets
Navigate to the Phoenix assets directory (e.g., `apps/my_app_web/assets/`) and run the Javascript/CSS formatters and linters:
```bash
npx prettier --write .
npx eslint . --fix
```

## Agent Resolution Mandate and Strict Testing

If any QA analyzers, linters, or formatters return a non-zero exit code, the agent **MUST NOT** proceed to testing or committing.

The agent MUST:
1. Review the specific CLI output of the failing QA tools.
2. Formulate a plan to fix the code logic causing the violations.
3. Apply the fixes.
4. Rerun all failing checks until everything resolves cleanly.

**Testing Strictness:** The agent MUST run `mix test` ONLY IF all the above QA checks pass successfully.

## Step 10: Generate Architecture Decision Records (ADRs)

Use the `@.agents/rules/adr-formatting.md` rule to write ADRs to the `@docs/architecture/` directory. Be sure to include separate ADRs specifically for the choice of:
1) Test runners and reporting frameworks.
2) Inline code docs generators.
3) Parallel QA execution tools, coding style standards, and static typing tooling (including Credo, Dialyzer, and Sobelow).
4) Bytecode purity analysis (Litmus) and boundary enforcement (Boundary) to guarantee idempotent retries and architectural encapsulation.
5) The centralized observability stack (Loki, Redpanda, Promtail, Prometheus, Grafana).
6) Use of Horde for distributed registries, Oban Engines for node-specific job routing, and Erlang PartitionSupervisor for GPU execution limitation.
7) Advanced provisioning choices including Terraform for VMs/VPCs and Ansible for GPU/CUDA provisioning and release deploy mechanics.
8) The architecture-agnostic Environment Detection fallback strategies in `runtime.exs` and RPC vs JSON REST decision.

## Step 11: Configure Global `.gitignore`

The root directory already contains a `.gitignore` file. You MUST strictly append the following lines to it to ensure proper exclusion of test artifacts, dependency caches, and selective tracking for test directories across the monorepo:

```text
# Test reports & artifacts
**/artifacts/
**/coverage/
**/playwright-report/
**/allure-results/
test/wallaby_screenshots/

# Dependency directories
**/deps/
**/_build/
**/ebin/
**/doc/
*.beam

# Scratch files and transient tests
**/test-card.js
**/screenshot.spec.js

# Allow selective tracking in test/
**/test/*
!**/test/features/
!**/test/support/
!**/test/README.md
```

## Step 12: Configure Observability Configurations

When initializing the observability stack, you MUST ensure that the raw configuration files required by the containers are present on the host and mapped correctly:

1. **Create `config/loki/local-config.yaml`**: Give Loki a basic local storage config (e.g. `auth_enabled: false` and filesystem chunks directories).
2. **Create `config/promtail/docker-config.yaml`**: Configure Promtail to scrape `/var/log` (or local file paths) and push them to the Loki client URL (`http://loki:3100/loki/api/v1/push`).
3. **Create `config/prometheus/prometheus.yml`**: Configure Prometheus to scrape `localhost:9090`, `loki:3100`, and `redpanda:9644`.
4. **Volume Mount Configurations**: Update the `docker-compose.yml` file to volume mount these local host files into the respective containers (e.g., `./config/loki/local-config.yaml:/etc/loki/local-config.yaml:ro`).

## Step 13: Update Documentation

1. **Insert** platform-agnostic Elixir/Erlang installation instructions into the top of the `README.md` file (e.g., referencing official guides or version managers like `asdf`, `mise`, etc.) to ensure a zero-friction setup for new developers. **CRITICAL: You MUST NOT delete or overwrite any existing content in the `README.md` file when adding this section.**
2. **Update** the `## Run tests` section (or append one if it doesn't exist) in the `README.md` in the project's root directory with instructions on how to execute each respective test suites, including which directories to run them from, where to find their raw results and how to get an overview of all test results in a tool like Allure. You MUST also explicitly instruct the user to run `npx playwright install` within their frontend setup routines so they download the necessary end-to-end testing browsers. **CRITICAL: You MUST NOT delete or overwrite any existing unrelated content in the `README.md` file when updating this section.**
3. **Update** the `## View logs` section (located under `# Setup Development Environment`) in the root `README.md` with explicit instructions on how to install/spin up the centralized logging tools (Loki, Redpanda, Promtail, Prometheus, Grafana) via `docker-compose`, and how to access the Grafana UI locally.
