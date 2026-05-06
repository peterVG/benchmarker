# Applications

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
