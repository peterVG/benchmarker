# About this project

Benchmarker is a lightweight, automated benchmarking harness designed to batch-test local AI models (specifically for OCR and text classification) across diverse hardware profiles. 

It replaces manual, non-reproducible testing flows by providing an automated pipeline. According to the [Software Requirements Specification (SRS)](docs/srs.md), the system automatically ingests standard industry datasets like RVL-CDIP and FUNSD via the [HuggingFace datasets library](docs/architecture/007-use-huggingface-datasets.md). The backend orchestrates batch inference exclusively against a **Pluggable AI Runner Architecture** (e.g., Ollama, vLLM, llama.cpp), which dynamically downloads and manages local execution daemons to ensure data privacy and cross-platform compatibility without cloud dependencies.

As tests run, the harness collects detailed system metrics (latency, time to first token, VRAM usage) and calculates OCR/Classification accuracy against ground-truth labels. To comply with scale-to-zero and local-first architectures, all test telemetry is durably persisted into a serverless [SQLite database](docs/architecture/006-use-sqlite-for-datastore.md). Finally, an interactive dashboard orchestrates these runs, streams live execution logs, and presents historical accuracy comparisons. The behavior of the entire system is strictly verified against BDD scenarios defined in the repository's `tests/features/` folders.

# Setup Development Environment

### Prerequisites
The deployment architecture is fully native (bare-metal) to ensure 100% native hardware acceleration for the embedded AI daemon (Ollama) across diverse host platforms (e.g. Apple Silicon M5, Nvidia Blackwell).
We recommend using a version manager like [mise](https://mise.jdx.dev/), [asdf](https://asdf-vm.com/), or [nvm](https://github.com/nvm-sh/nvm)/[pyenv](https://github.com/pyenv/pyenv) to manage your Node and Python versions. 
- Python: >=3.12
- Node.js: >=20

### Initializing the Environment

1. **Backend:** Set up your virtual environment and install the required dependencies:
```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Frontend:** Install the required Javascript dependencies:
```bash
cd apps/frontend
npm install
```

## Run the application

To verify the Pluggable AI Runner architecture and auto-installer logic manually:

1. **Start the Backend:**
Ensure your virtual environment is activated (`source apps/backend/.venv/bin/activate`).
```bash
cd apps/backend
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```
*Note: The `OllamaRunner` will automatically download the correct Ollama binary for your host OS to `apps/backend/bin/` and start the daemon during benchmarking.*

2. **Start the Frontend:**
Open a new terminal session.
```bash
cd apps/frontend
npm run dev
```
Access the interactive dashboard locally at `http://localhost:5173`.

## Run tests

### Backend (Python) BDD Tests
The system uses `behave` for BDD testing rather than standard pytest. Ensure you run it from within the `apps/backend/` directory with your virtual environment activated:
```bash
cd apps/backend
source .venv/bin/activate
behave tests/features/
```
To generate the Allure report:
```bash
allure serve apps/backend/tests/allure-results
```

### Frontend (Javascript) UI Tests
To run frontend e2e tests, run commands from within `apps/frontend/`. First, ensure you install Playwright browsers:
```bash
cd apps/frontend
npx playwright install
```
Then run tests to execute the BDD scenarios against the UI:
```bash
npx bddgen && npx playwright test
```

## View logs

While the application runs natively, the project uses a containerized, centralized observability stack.

### Understanding the Dockerized Observability Stack
If you are new to Docker, here is a basic overview of how it works in this project:
- **Images & Containers:** Docker packages software into standardized units called "containers" using "images". This ensures the software runs exactly the same way regardless of your host OS.
- **Docker Compose:** We use a `docker-compose.yml` file to orchestrate multiple containers simultaneously. 

To spin up the observability containers (Loki, Redpanda, Promtail, Prometheus, and Grafana):
```bash
docker-compose up -d loki redpanda promtail prometheus grafana
```
*(The `-d` flag runs them in detached mode in the background).*

To view logs:
1. Access Grafana locally at http://localhost:3000 (Credentials: `admin`/`admin`).
2. Connect Loki manually under `Connections -> Data sources -> Add Loki at http://loki:3100 -> Save & test`.
3. Use the "Log browser" under the Explore tab to query Loki logs visually.


# Setup Production Environment

## Deploy to Production

In production, Benchmarker is deployed via native processes (Bare-Metal) rather than Docker to ensure the embedded Ollama daemon has unobstructed access to the host's native GPU drivers (CUDA or Metal) without virtualization overhead.

1. **Build the Frontend:**
```bash
cd apps/frontend
npm run build
```
Serve the `apps/frontend/dist` directory using a lightweight static server (e.g. `nginx`, `caddy`, or Python's `http.server`).

2. **Run the Backend:**
We recommend using a process manager like [PM2](https://pm2.keymetrics.io/) or `systemd` to keep the backend API alive. 
```bash
cd apps/backend
source .venv/bin/activate
pip install -r requirements.txt
pm2 start "uvicorn app.api.main:app --host 0.0.0.0 --port 8000" --name "benchmarker-api"
```

## Monitor and Update

**Centralized Logging:**
In production, ensure your process manager routes standard output logs to the host machine's Promtail daemon, which will forward them to Redpanda and Loki.

**Updates:**
To update the system, simply pull the latest changes from Git, rebuild the frontend, install any new backend dependencies, and restart the processes:
```bash
git pull origin main
cd apps/frontend && npm install && npm run build
cd ../backend && source .venv/bin/activate && pip install -r requirements.txt
pm2 restart benchmarker-api
```
---

# About Open Agent Dev

This project has been created using Open Agent Dev, an opionated AI Agent project template focused on docs-as-code development. 

It enforces a strict Branch-Per-Task workflow and Test-Driven Development (TDD). Designed to guide AI dev agents to comply with industry standards and best practices. Tech stack and AI agent neutral.

# Getting Started with Open Agent Dev

## Upload reference documents if you have any
Upload any reference documents to the `/docs/references/` directory. This includes technical specifications, API references, RFC documents, industry standards, academic papers, technical architecture documents, research papers, library documentation, framework guides, platform specifications, etc.

```text
@AGENTS.md read any reference documents in @docs/references/ and use the @.agents/skills/kb-synthesizer skill to generate a knowledge base in @.agents/kb/
```

## Create a Product Vision
Fill out [`docs/templates/product-vision.md`](./docs/templates/product-vision-template.md) as best as possible and save it as [`/docs/product-vision.md`](./docs/product-vision.md)

If you want AI Agent assistance to write the product vision document, you can invoke the bundled skill:
```text
/product-vision I want to build [XYZ]. Refer to the @.agents/kb/ folder for any relevant background information.
```

## Create a Product Requirements Document

```text
@AGENTS.md Generate a prd.md in @docs using the @.agents/skills/prd-writer skill. Base it on @docs/product-vision.md, the @.agents/kb/ folder and the principles in the AGENTS.md file.
```
Review and revise [`/docs/prd.md`](./docs/prd.md) as needed. Check [`/docs/templates/prd-template.md`](./docs/templates/prd-template.md) for additional guidance. Make sure to add any additional requirements that you think are necessary to fully define the product vision.

## Initialize the project

Open Agent Dev currently supports best practices for the Python/Javascript and BEAM/Elixir tech stacks.

```text
@AGENTS.md Initialize the project using the @.agents/skills/SKILL-init-beam-elixir.md skill, the technical stack decisions in @docs/prd.md and the principles in the AGENTS.md file.
```

OR

```text
@AGENTS.md Initialize the project using the @.agents/skills/SKILL-init-python-js.md skill, the technical stack decisions in @docs/prd.md and the principles in the AGENTS.md file.
```

## Create a Software Requirement Specification document and Architecture Decision Records

```text
@AGENTS.md Generate a srs.md in @docs [or @apps/app_123/docs] using the @.agents/skills/srs-writer skill. Base it on @docs/prd.md and the principles in the AGENTS.md file. Use the @.agents/skills/feature-writer skill to generate BDD feature scenarios for each unique requirement in @docs/srs.md and @docs/prd.md. Use the @.agents/rules/adr-formatting.md rule to generate ADR files in the @docs/architecture/ folder based on the technical decisions in @docs/prd.md and @docs/srs.md. Populate the # About this project section of this README.md file with a description of the project based on the @docs/product-vision.md, @docs/prd.md, @docs/srs.md, ADR files and BDD feature files.
```

## Generate an implementation plan to guide development
### The "Global Holistic Execution" Prompt
Use this when you have updated the core PRD or added entirely new modules to a monorepo and need the AI to synthesize everything across the entire project from scratch.
```text
@AGENTS.md Invoke the @plan-writer skill. Delete any existing \plan.md` files across the repository. Then, rigorously analyze the root @docs/prd.md, all `srs.md` configurations in the `apps/` directory, and the @docs/architecture/ records. Synthesize these requirements and generate the global roadmap at `docs/plan.md`, sequentially followed by granular module-specific checklists distributed strictly into each app's respective `apps/[Module Name]/docs/plan.md` location.`
```

### The "Single Module Focus" Prompt
Use this when you've just drilled down into defining a specific app in a monorepo (e.g., you heavily updated apps/app_123/docs/srs.md) and just want to regenerate that specific localized checklist without touching the global roadmap or other apps.

```text
@AGENTS.md Please invoke the @plan-writer skill to generate an implementation plan strictly for the \app_123` module. Read its specific @apps/app_123/docs/srs.md, the global @docs/prd.md, and relevant ADRs, and output the tracking checklist directly into @apps/app_123/docs/plan.md.`
```

## Use the AGENTS.md prompts in your Implementation Plan
Check @docs/plan.md for specific task prompts in your implementation plan.These will guide you through the task list to generate and test your code in compliance with the Open Dev Agent principles and workflow.

## NOTE: Branch-per-task enforcement
A branch-per-task workflow is strictly enforced to ensure all code is reviewed before merging. Direct commits to the `main` branch is blocked by local pre-commit hooks.

If you are a human developer and absolutely must push a hotfix directly to `main`, you can override this safeguard by prefixing your commit command:

```bash
FORCE_MAIN_COMMIT=1 git commit -m "emergency hotfix"
```



