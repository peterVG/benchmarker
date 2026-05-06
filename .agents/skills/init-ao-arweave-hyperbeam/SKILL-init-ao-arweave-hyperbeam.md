---
description: Initialize a new AO / Arweave / Hyperbeam project with best practice root directory structure
---

# AO / Arweave / Hyperbeam Project Initialization

This skill guides the AI agent to initialize a new project targeting the Permaweb ecosystem (AO/Arweave/Hyperbeam) with the optimal directory structure, separating the Vanilla JS/TypeScript frontend from the Lua-based AO process backend.

## Step 1: Scaffold the Root Directory Structure

When scaffolding a new project, you MUST create the following directory structure at the root, while keeping all the files and folders that are currently also in the root directory.

```text
project-root/
├── .env                     
├── wallet.json.example      # Template for the Arweave wallet keyfile
├── apps/ 
│   ├── README.md
│   ├── frontend/            
│   │   ├── package.json     
│   │   ├── public/          
│   │   ├── src/             
│   │   │   ├── main.js      
│   │   │   ├── components/  
│   │   │   └── api/         # aoconnect and arweaveWallet API calls
│   │   ├── tests/           
│   │   │   ├── unit/        
│   │   │   ├── ui/          
│   │   │   ├── e2e/         
│   │   │   ├── features/    
│   │   │   ├── performance/ 
│   │   │   └── allure-results/
│   │   └── Dockerfile       # Optional standard web server for local dev 
│   │
│   └── backend/             
│       ├── process.lua      # Main AO process entry point
│       ├── src/             
│       │   ├── handlers.lua # Message handlers
│       │   ├── db.lua       # AOS SQLite module interactions
│       │   └── modules/     # Domain-driven feature modules 
│       │       └── feature-1/
│       │           ├── init.lua
│       │           └── logic.lua
│       └── tests/
│           ├── unit/        # Local Lua unit tests
│           ├── integration/ # aoconnect dryrun tests
│           ├── features/
│           └── allure-results/
```

Use appropriate commands to generate these structures STRICTLY within the `apps/` subdirectory (under `apps/frontend/` and `apps/backend/`). **DO NOT generate workspace manifests or applications inside the repository root.** Note that `wallet.json` must NOT be tracked by version control, provide a `.example` file instead.

## Step 2: Populate the apps/README.md file to explain directory structure

Create and populate a `README.md` file at the root of the `apps/` directory (i.e., `apps/README.md`) to explain the recursive directory structure. You can use the following text as a template:

For an AO/Arweave project, the best practice is a Monorepo approach that strictly separates the backend AO processes (Lua) from the frontend client application (Javascript/TypeScript).

The Standard Monorepo Pattern: In a dedicated monorepo, the apps/ folder is typically used to house all independent, deployable applications in the project. e.g., apps/frontend (a Vanilla JS/React frontend interacting via Wander) and apps/backend (Lua scripts compiled and deployed to the AO network).

Unified Workspace Management: By grouping the Lua processes and JS frontend into `apps/`, local orchestration tools can manage building, testing, and deploying both layers efficiently. 

Co-locating Backend Logic: Putting the entire Lua backend into a single `apps/backend/` directory follows the best practice of co-locating process logic and AOS SQLite state interactions. We use a domain-driven `modules/` architecture to organize features logically instead of giant monolithic Lua scripts. The backend is completely deterministic and operates on the "Everything is a Message" hyper-parallel framework of AO.

Global Orchestration vs Decentralization: Unlike traditional Docker compose environments orchestrating local centralized databases, an AO app's state is holographic and permanently stored on Arweave. The frontend operates essentially statelessly and bridges to the AO network via `aoconnect`.

```text
project-root/
├── .env                     # Secure storage for environment variables
├── wallet.json.example      # Example keyfile template (NEVER COMMIT REAL WALLETS)
├── apps/                    # Core applications (Monorepo approach) 
│   ├── README.md            # Explains the monorepo directory structures
│   ├── frontend/            # JavaScript/TypeScript Client 
│   │   ├── package.json     # Node dependencies (including aoconnect, arweave-js)
│   │   ├── public/          # Static web assets 
│   │   ├── src/             # Main frontend source code
│   │   │   ├── main.js      # Main JavaScript entry point 
│   │   │   ├── components/  # Reusable UI elements 
│   │   │   └── api/         # API layer utilizing aoconnect.message() and dryrun()
│   │   ├── tests/           # Dedicated Frontend Test suites
│   │   │   ├── unit/        # Unit tests (e.g., Vitest, Jest)
│   │   │   ├── ui/          # Component tests 
│   │   │   ├── e2e/         # End-to-end user tests (e.g., Playwright, Cypress)
│   │   │   ├── features/    # BDD scenarios (e.g., Cucumber.js)
│   │   │   ├── performance/ # Lighthouse or localized UI load tests
│   │   │   └── allure-results/ # Standardized test reporting output
│   │   └── Dockerfile       # Local web serving container configuration 
│   │
│   └── backend/             # AO Process Backend (Lua)
│       ├── process.lua      # Entry point for the AO process deployment
│       ├── src/             # Main Lua source code 
│       │   ├── handlers.lua # Handlers mapped to AO inbox messages
│       │   ├── db.lua       # Interactions with the AOS SQLite module
│       │   └── modules/     # Domain-driven feature modules 
│       │       └── users/   # e.g., A specific feature module
│       │           ├── init.lua
│       │           └── logic.lua
│       └── tests/           # Consolidated testing infrastructure
│           ├── unit/        # Local Lua tests (e.g., busted)
│           ├── integration/ # Dryrun AO tests against deployed or local mock endpoints
│           ├── features/    
│           └── allure-results/
```

When writing or configuring code for this stack, you must adhere to the following principles:

**Complete Separation**: The frontend communicates with the backend exclusively through the decentralized AO network via `aoconnect`. The frontend signs HTTP messages via the user's wallet (e.g., Wander/ArConnect) and dispatches them to HyperBEAM-powered MUs.
**The Backend (Lua / AO)**: For maintainability, the backend uses a Strict Domain-Driven architecture. It relies on `Handlers.add` pattern to respond to Arweave messages. It uses the AOS SQLite module for fast, deterministic on-chain data querying inside the WASM container.
**Holographic State**: Data is not stored in a traditional centralized database. All application states are purely mathematically derived from the sequential inputs logged to Arweave. You must utilize `dryrun` for read operations to avoid charging users $AR for computations that don't need permanent state mutations!
**The Frontend (JavaScript)**: Client-side code relies natively on `window.arweaveWallet` and `createDataItemSigner`. It MUST include onboarding constraints: generating checks for `./wallet.json` during local execution and routing users to the AR FAUCET if unfunded.
**Isolated Testing & Linting**: All global cache directories and reporting suites MUST strictly run and output within their local workspace directory (e.g. `apps/backend/tests/`) instead of the shared global repository root.
**Testing Taxonomy**: Both apps share a comprehensive testing architecture supporting `unit/`, BDD `features/`, and `allure-results/` test reporting. 

## Step 3: Configure Testing Frameworks

The main test execution environments are driven by the **WAO (WizardAO) SDK** for high-speed Lua backend testing, and various JavaScript runners for the frontend.

## Tools and Frameworks

### 1. Backend Testing Frameworks
- **WAO (WizardAO) SDK**: Core emulation engine used for lightning-fast, sub-second local simulation of the AO network to prevent pattern hallucinations.
- **Busted**: Native Lua test runner executing BDD-style unit blocks (`describe`/`it`) aggressively mapped against the WAO emulator environment inside `apps/backend/tests/unit/`.
- **npx wao & aoconnect integration**: Scripts utilizing the WAO SDK (an extension of Wander/aoconnect with syntactic sugar) to dryrun messages into local AO testnets inside `apps/backend/tests/integration/`.
- **Rebar3 (Erlang Infrastructure)**: Reserved strictly for compiling and testing custom low-level HyperBEAM devices or Erlang/OTP node extensions (via EUnit/Common Test).

### 2. Frontend Testing Frameworks
- **vitest / jest**: Core testing framework for asserting standalone functions in `apps/frontend/tests/unit`.
- **testing-library / storybook**: Designed specifically for rendering and assessing component behavior in `apps/frontend/tests/ui`.
- **playwright / cypress**: End-to-end framework interacting with the Wander wallet mock or physical browser extensions utilized in `apps/frontend/tests/e2e`.
- **cucumber.js**: Core BDD framework parsing Gherkin `.feature` files for end-to-end flows. It leverages the WAO SDK to inject messages into the emulated backend while manipulating Playwright in the frontend.

### 3. Global Test Reporting: `allure`
- **Purpose**: Generates interactive and highly detailed test execution reports globally.
- **Integration**: Plugs cleanly into JavaScript ecosystems and can parse JUnit XML generated by Lua testing tools.
- **Configuration**: Results from both environments MUST explicitly output ONLY to their localized folders (`apps/backend/tests/allure-results` and `apps/frontend/tests/allure-results`) strictly avoiding the global root. Ensure `--clean-alluredir` concepts apply.

### 4. Code Formatting and Linting (Lua Backend): `luacheck` & `lua-format`
- **Purpose**: Ensures code quality and standard style before deploying to the AO network.
- **Configuration**: Defined via `.luacheckrc` and `.lua-format` inside `apps/backend/`. Note the HyperBEAM Canon strictly advises against deeply nested `case` (or `if/elseif`) waterfalls and relies heavily on pattern matching or clean handler delegation.

### 5. Code Formatting and Linting (Javascript Frontend): `eslint` & `prettier`
- **Purpose**: Enforces code quality and formatting consistency for the Javascript/TypeScript codebase.
- **Configuration**: Defined in the frontend `package.json` and config files within `apps/frontend/`.

## Step 4: Configure Documentation Generation

Clear documentation is critical for maintaining the separation of concerns. Configure the following documentation frameworks:

1. **Backend (Lua):** Use `LDoc` to automatically extract docstrings (which MUST follow standard LDoc formatting `-- @param`, `-- @return`) and generate API documentation.
2. **Frontend (Javascript):** Use `JSDoc` for inline comments and function signatures. Create a base `jsdoc.json` configuration file isolating parsing to the `src/` directory.

## Step 5: Generate Inline Documentation Rule

Create a @.agents/rules/docs-enforce.md file that contains the following verbatim content:

---
description: Ensure all code is comprehensively documented using the standard inline documentation formats for this stack.
---

# Inline Documentation Enforcement

**Purpose:** This rule dictates how an AI agent MUST document the codebase to satisfy the Inline Documentation Mandate in `AGENTS.md`. It also enforces the "HyperBEAM Canon" guidelines.

## Active Enforcement

Before declaring any coding task "complete" or writing tests, the agent MUST verify that the following components include verbose inline documentation that clearly explains their function and intended usage:

1.  **ALL** Modules
2.  **ALL** Functions / Methods / Handlers
3.  **ALL** Complex or non-obvious code blocks

### Lua (Backend) Standards
The agent MUST use standard `LDoc` comments (using `---`) adhering strictly to the LDoc format. 
These docstrings MUST be parseable by `LDoc` to generate the final developer documentation site.

### Javascript/TypeScript (Frontend) Standards
The agent MUST use standard `JSDoc` syntax (using `/** ... */`) for all frontend logic, hooks, utility functions, and complex components.

### The HyperBEAM Canon
1. **Surgical Edits**: Minimize line-of-code changes.
2. **Blend In**: Write code as if you were the original author.
3. **No Waterfalls**: Avoid deeply nested conditional branches. Focus on clean Handler assignments for AO processes.

*Failure to document code according to these standards violates the core AGENTS.md manifesto.*

## Step 6: Generate linting rule

Create a @.agents/rules/lint-enforce.md file that contains the following verbatim content:  

---
description: Ensure all code is strictly linted and formatted before pushing or testing.
---

# Linting and Formatting Enforcement

**Purpose:** This file instructs the AI agent on exactly how to lint and format the codebase to satisfy the Test-Driven Development (TDD) linting mandate.

## Active Tools

- **Luacheck** for static code analysis of Lua files (Backend).
- **lua-format** for code formatting (Backend).
- **ESLint** for static code analysis (Frontend).
- **Prettier** for opinionated code formatting (Frontend).

## Execution Requirements

Before running any tests, committing code, or completing an execution task, you MUST execute the following CLI commands to ensure the codebase complies with the configured standards.

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

### 3. Lint and Format the Lua Backend
```bash
cd apps/backend/
lua-format -i $(find src -name "*.lua") process.lua
luacheck src process.lua
```

## Agent Resolution Mandate

If `eslint` or `luacheck` return a non-zero exit code, the agent **MUST NOT** proceed to testing or committing.

The agent MUST:

1. Review the specific CLI output of the linting errors.
2. Formulate a plan to fix the code logic causing the violations.
3. Apply the fixes.
4. Rerun to verify all errors are resolved.

Only when all tools exit cleanly (code 0) is the codebase considered valid for testing or PR submission.

## Step 7: Generate Architecture Decision Records (ADRs)

Use the @.agents/rules/adr-formatting.md rule to write ADRs to the @docs/architecture/ directory. Be sure to include separate ADRs specifically for the choice of:
1) Lua test runners and JS reporting frameworks.
2) Output to Arweave / AO message dispatch protocols (aoconnect).
3) Utilizing AOS SQLite for in-WASM state rather than decentralized NoSQL.
4) Coding style standards and linting tooling (luacheck / ESLint).

## Step 8: Configure Global `.gitignore`

The root directory already contains a `.gitignore` file. You MUST strictly append the following lines to it to ensure proper exclusion of test artifacts, dependency caches, and critical secret files like wallet keyfiles!

```text
# CRITICAL SECRET - NEVER COMMIT
wallet.json

# Test reports & artifacts
**/artifacts/
**/playwright-report/
**/allure-results/
**/coverage/

# Dependency directories
node_modules/
**/node_modules/

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

1. **Insert** platform-agnostic AO/Arweave toolchain installation instructions into the top of the `README.md` file (e.g., node, npm, lua, luarocks, aos-cli, ArConnect extension, and the **WAO testing framework** via `npx wao`). **CRITICAL: You MUST NOT delete or overwrite any existing content in the `README.md` file when adding this section.**
2. **Update** the `## Run tests` section in the `README.md` in the project's root directory with instructions on how to execute each respective test suites, including which directories to run them from, where to find their raw results and how to get an overview of all test results in a tool like Allure. Make sure to explicitly mandate that the Busted framework outputs standard JUnit XML for Allure ingestion (`busted -o junit > allure-results/busted.xml`) without invoking third-party plugins. You MUST also explicitly instruct the user to run `npx playwright install` within their frontend setup routines so they download the necessary end-to-end testing browsers. **CRITICAL: You MUST NOT delete or overwrite any existing unrelated content in the `README.md` file when updating this section.**
3. **Update** the `## Deploy to Permaweb` section (located under `# Setup Development Environment`) in the root `README.md` with explicit instructions on how developers must generate their `wallet.json` file, fund it with `$AR` / `$AO` from faucets, and use the `aos` console or custom deployment scripts to upload their Lua processes securely to the network. Also explain how the JS frontend should be bundled and uploaded to ARDrive or a trustless gateway mesh.
