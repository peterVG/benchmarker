# AI AGENT Principles

**Purpose:** Define the AI Agent principles guide this project.

**CRITICAL INSTRUCTION:** Before beginning any implementation, scaffolding, or configuration task, you MUST use the list_dir and view_file tools to read the contents of all markdown files in .agents/rules/. You must strictly adhere to these rules over any default framework behaviors.

## Core Principles
1. Don’t assume. Don’t hide confusion. Surface tradeoffs.
2. Minimum code that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria. Loop until verified.

## Test-driven development

**Purpose:** Ensure that all code is well-tested which includes functional feature tests, unit tests integration tests, UI tests, and performance tests.

- **Linting Mandate:** All code MUST be linted and formatted using the tools specified in the project's Architecture Decision Records before tests are run or code is merged. The agent MUST resolve all linting errors automatically.
- **UI Test Mandate:** All frontend feature branches MUST include comprehensive UI tests alongside standard unit tests to ensure UI components render and behave correctly. Crucially, these UI tests MUST execute against built production artifacts (not just dev servers) and MUST include explicit, rigorous DOM assertions that verify components mount without triggering server-side rendering (SSR) or browser hydration errors. Superficial tests that lack strict visual DOM state assertions are strictly forbidden.
- **Integration Test Mandate:** Any backend task that interfaces with an external API, database, or filesystem MUST include integration tests utilizing the framework specified in the project's Architecture Decision Records.
- **Performance Test Mandate:** Any application intended for production deployment MUST include load/performance tests using the framework specified in the project's Architecture Decision Records to simulate expected user concurrency and data volume.
- **Test Reporting Mandate:** All test runs (Unit, UI, Integration, and BDD) MUST generate structured reports using the framework specified in the project's Architecture Decision Records to provide stakeholders with a clear, visual history of test passed/failed states and coverage. The agent MUST include explicit CLI instructions in the project README.md for how developers can execute the complete test suite (including specific commands for BDD feature tests) and how to generate/view the structured test reports.
- **Inline Documentation Mandate:** The AI agent MUST write comprehensive inline documentation for ALL classes, functions, modules, and complex code blocks. This documentation must clearly explain the purpose, arguments, return values, and intended usage of the code. This is a strict requirement for all languages and frameworks, enforced via the specific standards configured in the initializing project template.
- **Walkthrough Documentation:** When executing tests, the agent MUST copy the raw CLI output of the test runs into a permanent `apps/[Module Name]/docs/tasks/Task-[Task ID]-Walkthrough.md` file to provide immediate visual proof of passing tests, in addition to generating the structured test reports.
- **Unit Test Traceability:** When code changes make a unit test obsolete or require modifications to the underlying implementation, the agent MUST explicitly update, refactor, or remove the corresponding unit tests to remain in sync with the source code.
- **Strict Artifact Isolation:** This principle is tactically enforced on all AI agents via the instructions in `[artifact-isolation.md](./.agents/rules/artifact-isolation.md)`.
- **PR Review Mandate:** All proposed Pull Requests MUST be reviewed by an external AI agent (specifically Cubit) acting as a Senior Software Engineer. The agent will analyze code changes, enforce project paradigms, check for logic flaws, and provide change requests before human merge. 
- **Cubic Workflow:** After pushing PRs to Github, wait for Cubit's GitHub review. Ask the agent to "check cubic comments" or "fix cubic issues". Push the fixes and repeat until the pull request is clean.

## Branch-Per-Task

**All development must follow the Git Branch per Task workflow:**

- **Active Enforcement:** The Branch-Per-Task and Execution Documentation requirements are tactically enforced on all AI agents via the instructions in `[task-workflow.md](./.agents/rules/task-workflow.md)`.

## Standalone Production Code

**Purpose:** Ensure that the core application codebase is completely self-contained, deployment-ready, and not permanently entangled with its surrounding project-management or AI-development tooling.

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[src-isolation.md](./.agents/rules/src-isolation.md)`.

## Strict Command Verification

**Purpose:** Guarantee that any CLI commands, build steps, or execution scripts documented for humans are actually functional and tested against current dependencies.

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[command-verification.md](./.agents/rules/command-verification.md)`.

## Pull Request Documentation Updates

**Purpose:** Guarantee that the permanent project documentation stays strictly synchronized with the codebase whenever new features, architecture changes, or schema updates are introduced.

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[pr-documentation-update.md](./.agents/rules/pr-documentation-update.md)`.

## Sync Logic Verification
**Purpose:** Guarantee that upstream documentation (PRD, SRS, ADRs, Implementation Plan) is consistently aligned before writing implementation code, and to require explicit human review for any detected contradictions.

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[sync-logic.md](./.agents/rules/sync-logic.md)`.
- **Search Before Denial:** AI agents MUST explicitly search `docs/architecture/` before denying technology use or claiming an ADR doesn't exist. This is tactically enforced via `[adr-verification.md](./.agents/rules/adr-verification.md)`.

## Portable Documentation (Relative Links)

**Purpose:** Ensure that the project's documentation remains universally portable, readable across any environment, and correctly navigable natively within Git hosting services like Github.

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[links-enforce.md](./.agents/rules/links-enforce.md)`.
- **Strictly Relative Links:** Anytime an AI agent generates documenting artifacts, readmes, technical specs, or logs that cross-reference another file in this project, it MUST use standard Markdown relative linking (e.g., `[PRD](../prd.md)` or `[Task 1.1](./tasks/Task-1.1-Plan.md)`).
- **Prohibited Absolute Paths:** The agent MUST NEVER write absolute file paths native to its current execution environment (e.g., `/Users/johnathondoe/...`) into the permanent project repository files. Absolute paths break immediately upon push to a remote repository or clone by another developer.

## Platform-Agnostic Documentation

**Purpose:** Ensure that the project does not alienate users on different operating systems by hardcoding platform-specific assumptions (e.g., assuming macOS and Homebrew are the default).

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[platform-agnostic.md](./.agents/rules/platform-agnostic.md)`.

## Standards Compliance

**Purpose:** Ensure the project adheres to established industry standards for interoperability, requirements engineering, and documentation.

- **Agent Skills 1.0:** The project template and agent tools comply with the Agent Skills 1.0 specification (including progressive disclosure, multi-tool support, and vendor neutrality). The framework principles are defined in [`.agents/kb/agent-skills-1.0.md`](./.agents/kb/agent-skills-1.0.md).
- **Conventional Commits:** All git commits MUST use the Conventional Commits format (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`). The exact formatting rules are located in [`.agents/kb/conventional-commits.md`](./.agents/kb/conventional-commits.md).
- **ISO/IEC/IEEE 29148:** The Software Requirements Specification (SRS) MUST be Unambiguous, Complete, Verifiable, Consistent, and Traceable. Specific agent instructions for these criteria are defined in [`.agents/kb/iso-29148-srs.md`](./.agents/kb/iso-29148-srs.md).
- **ISO/IEC/IEEE 42010:** Architecture Decision Records (ADRs) MUST include the 9 specific information items required by the ISO 42010 standard for architecture descriptions as defined in [`.agents/kb/iso-42010-adr.md`](./.agents/kb/iso-42010-adr.md).
- **RFC 2119:** All requirements documentation (PRD, SRS) must use explicit RFC 2119 terminology (e.g., MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, OPTIONAL) to define the significance of each requirement. Exact definitions are located in [`.agents/kb/rfc-2119-req-terms.md`](./.agents/kb/rfc-2119-req-terms.md).
- **RFC 3339:** All date and time specifications in projects MUST use the RFC 3339 standard. UTC MUST be used as the default timezone for all logs, databases, and internal timestamps. Exact definitions are located in [`.agents/kb/rfc-3339-date-and-time.md`](./.agents/kb/rfc-3339-date-and-time.md).

## Centralized Logging & Observability

**Purpose:** Ensure that the application treats logs as event streams, writing unbuffered to `stdout` rather than managing logfiles, adhering to modern centralized observability methodologies. This provides the foundation for a modern event streaming and observability stack.

- **Stdout Mandate:** Applications MUST NEVER route or store logs in files themselves. Each running process writes its event stream unbuffered to `stdout`.
- **Observability Stack:** The applications MUST be instrumented and infrastructure-configured to route these stdout streams into a centralized observability stack:
  - **Promtail:** Captures the container `stdout` streams natively.
  - **Redpanda:** Acts as the high-throughput, Kafka-compatible message queue to buffer and distribute log events sequentially without loss.
  - **Loki:** Indexes and stores the log streams for long-term archival.
  - **Prometheus:** Scrapes time-series metrics emitted by the apps and services.
  - **Grafana:** Provides the centralized UI to dashboard, introspect, and correlate the logs and metrics.
- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[logging-enforce.md](./.agents/rules/logging-enforce.md)`.

## Decoupled Execution Timelines

**Purpose:** Guarantee architectural specs can survive aggressive timeline refactoring without requiring massive document rewrites by isolating execution phases from the core requirements.

- **Active Enforcement:** This principle is tactically enforced on all AI agents via the instructions in `[decoupled-execution.md](./.agents/rules/decoupled-execution.md)`.

## Security by Design

**Purpose:** Suggest security requirements and architectural decisions that protect user data.

- [e.g., "Client-side encryption before data leaves the browser"]
- [e.g., "Zero-knowledge architecture - server never sees unencrypted data"]
- [e.g., "User controls their own encryption keys"]

## Privacy by Design

**Purpose:** Suggest privacy requirements and architectural decisions that protect user identification or other information about the user that should remain private.

- [e.g., the application should use W3C Verifiable Credentials]

## Modularity

**Purpose:** Ensure that the application is modular and can be easily extended in the future by divinding functionality into modules. Each module should be self-contained and have a clear interface.

- [e.g., "The application is divided into modules that can be independently developed and tested"]
- [e.g., "The application is divided into modules that can be independently deployed and scaled"]

## Interface-First Design

**Purpose:** Describe how components communicate and how their API or web sockets access enables future extensibility.

- [e.g., "All features exposed via REST API"]
- [e.g., "All features exposed via Web Sockets"]
- [e.g., "Frontend and backend communicate only through documented endpoints"]
- [e.g., "API designed for third-party integrations"]

## Minimize Dependencies

**Purpose:** Ensure the application has minimal dependencies on external services, libraries, and vendor lock-in.

- [e.g., "No external databases - use [your choice] for storage"]
- [e.g., "No authentication service - use [your approach]"]
- [e.g., "Limit npm packages to essential utilities only"]

## Scale-to-Zero

**Purpose:** Ensure the application can scale to zero when idle.

- [e.g., "Static frontend with no server costs"]
- [e.g., "Serverless backend - pay only for actual usage"]
- [e.g., "No always-on databases or services"]

## Local-First

**Purpose:** If applicable, describe how the app works offline, prioritizes local data, and syncs data when back online.

- [e.g., "App functions fully offline, syncs when connected"]
- [e.g., "Local storage is source of truth, cloud is backup"]

## Zero-Friction Setup

**Purpose:** Guarantee that the application is as easy as possible to install and run locally, minimizing "time to first value" for new developers and users.

- **Automated Initialization:** If the application requires a local database, the initialization script MUST automatically check if it exists on startup. If not, it MUST seamlessly create the database, build the required schema/tables, and seed initial data without requiring manual CLI commands from the user.
- **Interactive Auth Prompts:** If the application requires API keys or authentication secrets, the application MUST automatically detect if they are missing on startup and interactively prompt the user for them (or generate a `.env` template automatically) rather than simply crashing with a stack trace.
- **Create Installers:** Whenever possible, create installers for the application that can be used to install the application on a developer and production system. 

## Keep code linear
No deeply nested conditionals and early-exit chains. No hidden jumps. Keep the logic flat at one level as much as possible. Code should read top to bottom like a well-constructed argument — premise, reasoning, conclusion.

##  Bound every loop
Ensure there are maximum caps for polling loops, retry logic, and recursive crawlers. Provide a safe path forward for when the cap is hit.

## Close every resource you open
Every resource you open, you must close. Every connection you borrow, you must return. Resource lifetime must be declared, not assumed — and it must be correct on the error path too, not just the happy one. Don’t acquire what you can’t account for. Follow the code through every exit path and confirm it closes what it opened.

## One function, one job
Each function should do exactly one thing — small enough to be describable in a sentence without the word “and.” Do not generate monolithic functions that do many things at once because you're optimizing for task completion. You should optimize for maintainability. Apply decomposition upfront, not as a refactoring afterthought. No function longer than 60 lines.

## Every exception is caught
Every error must be logged, raised, or explicitly returned. You cannot generate empty catch blocks or unchecked return values.

## Clear separation of side-effect operations
I/O, mutations, and network calls should be named and obvious at the call site. Not hidden inside helpers, not wrapped in abstractions with meaningless names, not multiple layers deep in a chain of decorators. If a function writes to a database, its name and call site should make that clear. Do not bury API calls inside what appear to be utility functions. Ensure you have a clear structural separation between pure computation and side-effectful operations.
