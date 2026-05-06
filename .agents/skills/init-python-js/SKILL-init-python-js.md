---
description: Initialize a new Python/Javascript project with best practice root directory structure
---

# Python/Javascript Project Initialization

This skill guides the AI agent to initialize a new Python/Javascript project with the optimal directory structure, separating the frontend and backend, orchestrated by Docker.

## Step 1: Scaffold the Root Directory Structure

When scaffolding a new project, you MUST create the following directory structure at the root, while keeping all the files and folders that are currently also in the root directory.

```text
project-root/
├── docker-compose.yml 
├── .env 
├── apps/ 
│   ├── README.md
│   ├── frontend/            
│   │   ├── package.json     
│   │   ├── public/          
│   │   ├── src/             
│   │   │   ├── main.js      
│   │   │   ├── components/  
│   │   │   └── api/         
│   │   ├── tests/           
│   │   │   ├── unit/        
│   │   │   ├── ui/          
│   │   │   ├── e2e/         
│   │   │   ├── features/    
│   │   │   ├── performance/ 
│   │   │   └── allure-results/
│   │   └── Dockerfile       
│   │
│   └── backend/             
│       ├── requirements.txt 
│       ├── pytest.ini
│       ├── Dockerfile       
│       ├── app/             
│       │   ├── main.py      
│       │   ├── core/        
│       │   ├── modules/     
│       │   │   ├── users/   
│       │   │   │   ├── routers.py
│       │   │   │   ├── models.py
│       │   │   │   └── schemas.py
│       │   │   └── module-1/
│       │   │       ├── routers.py
│       │   │       ├── models.py
│       │   │       └── schemas.py
│       │   └── tasks/  
│       └── tests/
│           ├── unit/
│           ├── integration/
│           ├── ui/
│           ├── features/
│           ├── performance/
│           └── allure-results/
```

Use appropriate commands (e.g. `npx create-react-app`, `npx create-next-app` for frontend; `pip install` or direct directory creation for backend) to generate these structures STRICTLY within the `apps/` subdirectory (under `apps/frontend/` and `apps/backend/`). **DO NOT generate workspace manifests or applications inside the repository root.**

## Step 2 Populate the apps/README.md file to explain directory structure

Create and populate a `README.md` file at the root of the `apps/` directory (i.e., `apps/README.md`) to explain the recursive directory structure. You can use the following text as a template, adjusting for the specific stack used:

For a Python/Javascript project, the best practice is a Monorepo approach that strictly separates the backend API (Python) from the frontend client application (Javascript/TypeScript).

The Standard Monorepo Pattern: In a dedicated monorepo, the apps/ folder is typically used to house all independent, deployable applications in the project, regardless of whether they are client-side or server-side. eg, apps/frontend (a React frontend) and apps/backend (an Express/FastAPI backend) sitting side-by-side.

Unified Workspace Management: By treating the Python API as just another "app" within the workspace, modern monorepo tools can orchestrate tasks, cache builds, and run pipelines across both the frontend and backend uniformly without needing custom directory targeting.

Co-locating Backend Logic: Putting the entire Python backend (both the web API and background workers like Celery) into a single apps/backend/ directory follows the best practice of co-locating web and worker nodes. Housing these together creates a synergy that allows them to seamlessly share components. We use a domain-driven `modules/` architecture to organize features logically instead of flat `models` and `routers` folders.

Global Orchestration: A `docker-compose.yml` file sits one directory higher in the global project root. This file is responsible for orchestrating the entire suite of applications within this `apps/` directory (e.g., spinning up the frontend, backend, and any required databases simultaneously) to ensure a single-command, zero-friction local development environment.

```text
project-root/
├── docker-compose.yml       # Orchestrates the full stack (Frontend, Backend, DB, Workers) 
├── .env                     # Secure storage for environment variables (DB credentials, API keys) 
├── apps/                    # Core applications (Monorepo approach) 
│   ├── README.md            # Explains the monorepo directory structures
│   ├── frontend/            # JavaScript/TypeScript Client (e.g., React, Svelte, Vanilla JS) 
│   │   ├── package.json     # Node dependencies 
│   │   ├── public/          # Static web assets 
│   │   ├── src/             # Main frontend source code
│   │   │   ├── main.js      # Main JavaScript entry point 
│   │   │   ├── components/  # Reusable UI elements 
│   │   │   └── api/         # API client layer to fetch data from the Python backend 
│   │   ├── tests/           # Dedicated Frontend Test suites
│   │   │   ├── unit/        # Unit tests (e.g., Vitest, Jest)
│   │   │   ├── ui/          # Component tests (e.g., Testing Library, Storybook)
│   │   │   ├── e2e/         # End-to-end user tests (e.g., Playwright, Cypress)
│   │   │   ├── features/    # BDD scenarios (e.g., Cucumber.js)
│   │   │   ├── performance/ # Lighthouse or localized UI load tests
│   │   │   └── allure-results/ # Standardized test reporting output
│   │   └── Dockerfile       # Frontend container configuration 
│   │
│   └── backend/             # Python API (e.g., FastAPI, Django, Flask) 
│       ├── requirements.txt # Python dependencies 
│       ├── pytest.ini       # Pytest configuration
│       ├── Dockerfile       # Backend container configuration 
│       ├── app/             # Main Python source code 
│       │   ├── main.py      # Entry point for the server 
│       │   ├── core/        # Core configuration (e.g., database.py, security)
│       │   ├── modules/     # Domain-driven feature modules 
│       │   │   ├── users/   # e.g., A specific feature module
│       │   │   │   ├── routers.py 
│       │   │   │   ├── models.py
│       │   │   │   └── schemas.py
│       │   │   └── module-1/ # e.g., Additional feature modules
│       │   │       ├── routers.py 
│       │   │       ├── models.py
│       │   │       └── schemas.py
│       │   └── tasks/       # Background workers (e.g., Celery tasks) 
│       └── tests/           # Consolidated testing infrastructure
│           ├── unit/        
│           ├── integration/ 
│           ├── ui/          
│           ├── features/    
│           ├── performance/ 
│           └── allure-results/
```

When writing or configuring code for this stack, you must adhere to the following principles:

**Complete Separation**: The frontend and backend run on different ports during development (e.g., Frontend Client on 5173, FastAPI on 8000) and are completely isolated. The frontend doesn't need to know the backend is written in Python; it simply makes standard HTTP requests (GET, POST, PUT, DELETE) and receives JSON in return.
**The Backend (Python)**: For maintainability, the backend uses a Strict Domain-Driven architecture. It organizes feature-specific code into domain-driven `modules/` (e.g., `modules/users/routers.py`) and background workers into `tasks/`. All app-wide global resources and configurations stay safely tucked in the `core/` directory, while generic health checks live directly in `main.py`.
**Python Virtual Environments**: Because the project relies on isolated workspaces, all Python execution (e.g., `pip install`, `pytest`, `uvicorn`) MUST strictly utilize a localized virtual environment (`.venv`). When generating READMEs, executing tasks, or running bash scripts, you MUST explicitly activate the environment (`source .venv/bin/activate`) to prevent system-wide OS PEP-668 conflicts.
**The Frontend (JavaScript)**: Client-side code is framework-flexible, grouped into a `src/` directory containing view `components/` and an `api/` layer specifically responsible for handling all communication with the backend.
**Docker Integration**: Utilizing a `docker-compose.yml` file at the root, along with individual `Dockerfile`s in the backend and frontend folders, standardizes the development environment across the team and minimizes "it works on my machine" issues.
**Isolated Testing & Linting**: All global cache directories (`.pytest_cache`, `.eslintcache`) and reporting suites MUST strictly run and output within their local workspace directory (e.g. `apps/backend/tests/`) instead of the shared global repository root.
**Testing Taxonomy**: Both apps share a comprehensive and symmetrical testing architecture supporting `unit/`, BDD `features/`, UI `performance/`, and local `allure-results/` test reporting. They only differ where execution environments demand it: The backend uses `integration/` tests to quickly verify raw HTTP interactions with databases, whereas the frontend uses `e2e/` (End-to-End) tests via tools like Playwright or Cypress to physically invoke Chromium and simulate real visual user browser sessions.
**Centralized Logging / Observability**: All applications must route their logs as unbuffered event streams exclusively to `stdout`. The repository relies on a centralized observability stack (Promtail, Loki, Redpanda, Prometheus, Grafana) orchestrated via `docker-compose` to capture and index these logs, strictly forbidding local file logging.

## Step 3: Configure Testing Frameworks

The main test execution environments are driven by `pytest` for the backend, and various JavaScript runners (like Vitest, Cypress, or Playwright) for the frontend.

## Tools and Frameworks

### 1. Backend Testing Frameworks
- **pytest & pytest-vcr**: Extensively used for writing unit and backend integration tests inside `apps/backend/tests/`. Uses `.pytest_cache`.
- **behave**: Used for writing tests in domain-specific language (Gherkin syntax). Definitions reside under `apps/backend/tests/features`.
- **locust**: Used to simulate user loads and measure system limitations under stress. Resides under `apps/backend/tests/performance`.

### 2. Frontend Testing Frameworks
- **vitest / jest**: Core testing framework for asserting standalone functions in `apps/frontend/tests/unit`.
- **testing-library / storybook**: Designed specifically for rendering and assessing component behavior in `apps/frontend/tests/ui`.
- **playwright / cypress**: End-to-end framework and UI performance auditing tool utilized in `apps/frontend/tests/e2e` and `apps/frontend/tests/performance`.
- **cucumber.js**: BDD framework executing Gherkin feature files for frontend UI flows in `apps/frontend/tests/features`.

### 3. Global Test Reporting: `allure`
- **Purpose**: Generates interactive and highly detailed test execution reports globally.
- **Integration**: Plugs cleanly into both Python and JavaScript ecosystems (`allure-pytest`, `allure-behave`, `allure-playwright`, `allure-cyopress`).
- **Configuration**: Results from both environments MUST explicitly output ONLY to their localized folders (`apps/backend/tests/allure-results` and `apps/frontend/tests/allure-results`) strictly avoiding the global root. Furthermore, backend testing suites (e.g. `pytest.ini`) MUST explicitly configure the `--clean-alluredir` flag, and frontend environments MUST run a custom `pretest` execution hook (e.g. `rm -rf tests/allure-results`) to automatically purge historical JSON payloads before initiating new test cycles.

### 4. Code Formatting and Linting (Python Backend): `ruff`
- **Purpose**: Ensures code quality and standard style before testing.
- **Configuration**: Defined in `pyproject.toml` (located inside `apps/backend/`) targeting modern Python features.

### 5. Code Formatting and Linting (Javascript Frontend): `eslint` & `prettier`
- **Purpose**: Enforces code quality and formatting consistency for the Javascript/TypeScript codebase.
- **Configuration**: Defined in the frontend `package.json` and config files within `apps/frontend/`.

## Best Practices
- Run code formatting and linting via `ruff` (backend) AND `eslint`/`prettier` (frontend) explicitly **within their respective application workspaces (`cd apps/frontend/`, etc.)** prior to running tests.
- Execute unit and integration tests via `pytest` by running the command locally within `apps/backend/` sequentially after activating the python virtual environment (`source .venv/bin/activate`).
- After a test run, compile `allure` results using the Allure CLI against the isolated `apps/backend/tests/allure-results` folder.

## Step 4: Configure Documentation Generation

Clear documentation is critical for maintaining the separation of concerns in a monorepo. Configure the following documentation frameworks:

1. **Backend (Python):** Use `pdoc` to automatically extract docstrings (which MUST follow Google or NumPy style) and generate API documentation. Add `pdoc` to your backend `requirements.txt`.
2. **Frontend (Javascript):** Use `JSDoc` for inline comments and function signatures. You MUST explicitly run `npm install --save-dev jsdoc` inside `apps/frontend/`, create a base `jsdoc.json` configuration file isolating parsing to the `src/` directory, and strictly wire a `"docs": "jsdoc -c jsdoc.json"` command into the frontend `package.json` scripts block!

## Step 5: Generate Inline Documentation Rule

Create a @.agents/rules/docs-enforce.md file that contains the following verbatim content:

---
description: Ensure all code is comprehensively documented using the standard inline documentation formats for this stack.
---

# Inline Documentation Enforcement

**Purpose:** This rule dictates how an AI agent MUST document the codebase to satisfy the Inline Documentation Mandate in `AGENTS.md`.

## Active Enforcement

Before declaring any coding task "complete" or writing tests, the agent MUST verify that the following components include verbose inline documentation that clearly explains their function and intended usage:

1.  **ALL** Classes
2.  **ALL** Functions / Methods
3.  **ALL** Modules
4.  **ALL** Complex or non-obvious code blocks

### Python (Backend) Standards
The agent MUST use standard Python docstrings (using `"""`) adhering strictly to either the **Google** or **NumPy** docstring format.
These docstrings MUST be parseable by `pdoc` to generate the final developer documentation site.

### Javascript/TypeScript (Frontend) Standards
The agent MUST use standard `JSDoc` syntax (using `/** ... */`) for all frontend logic, hooks, utility functions, and complex React/Vue components.

*Failure to document code according to these standards violates the core AGENTS.md manifesto.*

## Step 6: Generate linting rule

Create a @.agents/rules/lint-enforce.md file that contains the following verbatim content:  

---
description: Ensure all code is strictly linted and formatted before pushing or testing.
---

# Linting and Formatting Enforcement

**Purpose:** This file instructs the AI agent on exactly how to lint and format the codebase to satisfy the Test-Driven Development (TDD) linting mandate in `AGENTS.md`.

## Active Tools

Based on the accepted Architecture Decision Records (`docs/architecture/004-coding-style-and-linting.md`), this project uses:

- **Ruff** for Python analysis and fast, PEP8-compliant code formatting (Backend).
- **ESLint** for static code analysis (Frontend).
- **Prettier** for opinionated code formatting (Frontend).

## Execution Requirements

Before running any tests, committing code, or completing an execution task, you MUST execute the following CLI commands to ensure the codebase complies with the configured standards. Note that commands MUST be executed inside the correct workspace boundary.

### 1. Format the Frontend Codebase
```bash
cd apps/frontend/
npx prettier --write .
```

### 2. Lint the Frontend (and auto-fix)
```bash
cd apps/frontend/
npx eslint . --fix
```

### 3. Lint and Format the Python Backend (and auto-fix)
```bash
cd apps/backend/
ruff check . --fix
ruff format .
```

## Agent Resolution Mandate

If the `eslint` or `ruff check` commands return a non-zero exit code (indicating unresolved linting errors or warnings configured as errors), the agent **MUST NOT** proceed to testing or committing.

The agent MUST:

1. Review the specific CLI output of the linting errors.
2. Formulate a plan to fix the code logic causing the violations.
3. Apply the fixes.
4. Rerun `npx eslint .` or `ruff check .` to verify all errors are resolved.

Only when Ruff, Prettier, and ESLint all exit cleanly (code 0) is the codebase considered valid for testing or PR submission.

## Step 7: Generate Architecture Decision Records (ADRs)

Use the @.agents/rules/adr-formatting.md rule to write ADRs to the @docs/architecture/ directory. Be sure to include separate ADRs specifically for the choice of:
1) test runners and reporting frameworks.
2) Inline code docs generators.
3) Coding style standards and linting tooling.
4) The centralized observability stack (Loki, Redpanda, Promtail, Prometheus, Grafana).

## Step 8: Configure Global `.gitignore`

The root directory already contains a `.gitignore` file. You MUST strictly append the following lines to it to ensure proper exclusion of test artifacts, dependency caches, and selective tracking for test directories across the monorepo:

```text
# Test reports & artifacts
**/artifacts/
**/playwright-report/
**/allure-results/
**/coverage/

# Dependency directories
node_modules/
**/node_modules/
__pycache__/
*.pyc

# Scratch files and transient tests
**/test-card.js
**/screenshot.spec.js

# Allow selective tracking in tests/
**/tests/*
!**/tests/features/
!**/tests/support/
!**/tests/unit/
!**/tests/ui/
!**/tests/e2e/
!**/tests/integration/
!**/tests/performance/
!**/tests/README.md
```

## Step 9: Update Documentation

1. **Insert** platform-agnostic Python/Node installation instructions into the top of the `README.md` file (e.g., referencing official guides or version managers like `asdf`, `mise`, `pyenv`, `nvm`, etc.) to ensure a zero-friction setup for new developers. **CRITICAL: You MUST NOT delete or overwrite any existing content in the `README.md` file when adding this section.**
2. **Update** the `## Run tests` section (or append one if it doesn't exist) in the `README.md` in the project's root directory with instructions on how to execute each respective test suites, including which directories to run them from, where to find their raw results and how to get an overview of all test results in a tool like Allure. You MUST also explicitly instruct the user to run `npx playwright install` within their frontend setup routines so they download the necessary end-to-end testing browsers. **CRITICAL: You MUST NOT delete or overwrite any existing unrelated content in the `README.md` file when updating this section.**
3. **Update** the `## View logs` section (located under `# Setup Development Environment`) in the root `README.md` with explicit instructions on how to install/spin up the centralized logging tools (Loki, Redpanda, Promtail, Prometheus, Grafana) via `docker-compose`, and how to access the Grafana UI locally.
