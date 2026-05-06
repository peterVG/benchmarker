---
name: Implementation Plan Writer
description: Generates an interactive, traceable implementation plan based on PRD, SRS, and Gherkin files
allowed-tools:
  - code_interpreter
---

# Implementation Plan Writer Skill

## Purpose

This skill enables the agent to translate Product Requirements Document (PRD), Software Requirements Specification (SRS), and any relevant formal test specifications (e.g., Gherkin `.feature` files or equivalent stack-specific test mandates) into a cohesive, step-by-step implementation plan.

## When to Use This Skill

- When asked to "Generate an implementation plan" using `prd.md` and `srs.md`
- When breaking down agreed-upon requirements into actionable developer tasks
- When the user references this skill explicitly

## Core Principles

### 1. Interactive Checkboxes

Every task MUST be formatted as an interactive Markdown checkbox so that progress can be tracked directly within the document.

**Format:**

```markdown
- [ ] **Task 1.1: Project Setup & Configuration**
  - **Description:** Initialize the Python virtual environment...
```

### 2. Module-Specific Task Prefixes

When generating implementation plans that are NOT in the global root `docs/plan.md` (e.g., module-specific plans like `apps/[Module Name]/docs/plan.md`), you MUST prefix all Task numbers with the capitalized initials of the module name.
For example:
- **arkrim_engine** task 1.1 = `Task AE-1.1`
- **arkrim_upload** task 3.5 = `Task AU-3.5`

Global root tasks should remain standard without a prefix (e.g., `Task 1.1`).

### 3. Strict Traceability

Every task MUST explicitly link back to its originating requirements (PRD/SRS).

**Format:**

```markdown
- [ ] **Task 2.5: API Error Handling**
  - **Description:** Implement robust error catching...
  - **Estimated Time:** 1 hour
  - **Dependencies:** Task 2.3
  - **Related Requirements:** [SRS-SEC-001](../srs.md#srs-sec-001-local-sovereignty--transparency), [NFR-002](../prd.md#nfr-002-api-transparency)
  - **Related Tests:** [`local_sovereignty_SRS-SEC-001_test.exs`](../../test/features/local_sovereignty_SRS-SEC-001_test.exs)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task [Task ID]. Then begin development, executing all commands strictly within the isolated apps/[Module Name]/ directory (if applicable). Upon completion, YOU MUST perfectly construct the apps/[Module Name]/docs/tasks/Task-[Task ID]-Walkthrough.md file linking explicit SRS mappings (including BOTH the ID and full human-readable title text) in heading position 2 exclusively, and delete the Plan.md and ToDos.md files to preserve zero tracking cruft natively. Then check off the Markdown box locally in the appropriate docs/plan.md, commit your changes, and push the branch to origin.`
```

_If a task is purely structural (e.g., setting up a repository) and has no specific tests, mark Related Tests as `N/A`._

### 4. Development Prompts

Every task MUST include an actionable prompt for the agent to begin development. This prompt MUST NOT hardcode language-specific paths (like `/src` or `/tests`) unless a PRD and SRS explicitly dictate the finalized monorepo/folder architecture. Instead, instruct the agent to propose code and write tests in the "appropriate directories within the repository, adhering rigorously to the established Architecture Decision Records (ADRs)."
Crucially, if the project employs a monorepo or Umbrella architecture (Python/JS or BEAM/Elixir), **the prompt MUST explicitly instruct the executing agent to run all framework tooling, tests, and configurations strictly isolated within the specific module's subdirectory** (e.g., `apps/frontend/` or `apps/arkrim_engine/`).
For tasks that involve building user interfaces, the prompt MUST explicitly instruct the agent to write UI tests using the UI testing framework specified in the project's Architecture Decision Records (ADRs). The plan MUST mandate that these UI tests contain strict DOM assertions to explicitly catch hydration mismatches and SSR crashes, and that the agent ensures tests are run against built production artifacts.
For tasks that involve external dependencies (APIs, databases, filesystems), the prompt MUST explicitly instruct the agent to write Integration tests using the Integration framework specified in the ADRs.
The implementation plan MUST include a dedicated task in the Verification phase to write and execute Performance/Load tests (e.g., Locust) using the framework specified in the ADRs.
For all functional implementation tasks (e.g., business logic, UI features), the prompt MUST explicitly instruct the executing agent to **invoke the `@feature-writer` skill to translate SRS requirements into executable BDD feature tests.**
Additionally, the Agent Prompt for all testing tasks MUST explicitly instruct the developer to output test results using the Test Reporting framework (e.g., Allure) specified in the ADRs, AND to copy the raw CLI output of the test runs into a permanent `apps/[Module Name]/docs/tasks/Task-[Task ID]-Walkthrough.md` file. **Crucially, the prompt MUST mandate that this file is saved directly into the project's `apps/[Module Name]/docs/tasks/` folder and NEVER in an internal agent scratchpad.**
Crucially, the prompt MUST also explicitly instruct the agent to check off the `- [ ]` markdown box locally inside the appropriate `docs/plan.md` the moment the task is confirmed complete, commit its changes, and push its feature branch to `origin`.

### 5. Phased, Dependency-Aware Approach

Tasks MUST be logically grouped into Phases (e.g., Phase 1: Foundation, Phase 2: Core Logic). No task should be scheduled before its dependencies are complete. Usually, Database and Data Layer tasks precede UI tasks.

### 6. Holistic UI Planning

When defining the Implementation Plan, the agent MUST NOT silo highly coupled UI mechanics (e.g., Canvas rendering and the Avatar that controls it) into separate sequential tasks. If the interaction model of a later requirement (e.g., Avatar Steering) supersedes or fundamentally alters the interaction model of an earlier requirement (e.g., Canvas Panning), they MUST be combined into a single holistic UI/UX task to prevent building throwaway interaction code. Abide by `.agents/rules/holistic-ui.md`.

## Template Structure

```markdown
# Implementation Plan: [Project Name]

This document outlines the step-by-step implementation plan...

## Phase 1: [Phase Name]

- [ ] **Task 1.1: [Task Name]**
  - **Description:** [Actionable details]
  - **Estimated Time:** [Estimated developer hours]
  - **Dependencies:** [Previous tasks, e.g., Task 1.1 or None]
  - **Related Requirements:** [[SRS/PRD mapping]](../srs.md)
  - **Related Tests:** [[Path to formal test specification file or N/A]](../../test/)
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task [Task ID]. Then begin development (ensuring all tool commands are run inside apps/[Module Name]/ if applicable)... Additionally, invoke the @feature-writer skill to translate SRS requirements into executable BDD feature tests. Upon completion, YOU MUST generate apps/[Module Name]/docs/tasks/Task-[Task ID]-Walkthrough.md directly in the project repository with clear SRS mapping (including BOTH the ID and full human-readable title text) in the secondary section, and strictly delete the internal tracking Plan/ToDos documents before checking off the Markdown box locally in the appropriate docs/plan.md. Then commit your changes and push the branch to origin.`

## Summary Timeline

- **Total Estimated Time:** [Sum of hours]
- **Critical Path:** [High-level flow, e.g., Database Setup -> API -> UI]
```

## Anti-Patterns to Avoid

### ❌ Don't: Output simple bulleted lists without checkboxes

```markdown
# BAD

- Task 1: Setup database
```

### ❌ Don't: Omit the Traceability Links

```markdown
# BAD

- [ ] **Task 1:** Setup database
  - **Description:** Create schema.
  - **Estimated Time:** 2 hours
```

### ✅ Do: Include full traceability and checkboxes

```markdown
# GOOD

- [ ] **Task 1.2: [Module Name] SQLite Database Schema Setup**
  - **Description:** Write an automated initialization script for the application database...
  - **Estimated Time:** 2 hours
  - **Dependencies:** Task 1.1
  - **Related Requirements:** SRS-DATA-001, TC-002
  - **Related Tests:** `test/features/database_persistence_SRS-DATA-001_test.exs`
  - **Agent Prompt:** `@AGENTS.md Begin by creating a new feature branch for Task [Task ID]. Then begin development within apps/[Module Name]/. Additionally, invoke the @feature-writer skill to translate SRS requirements into executable BDD feature tests. Upon completion, YOU MUST generate apps/[Module Name]/docs/tasks/Task-[Task ID]-Walkthrough.md directly in the project repository with the native SRS cross-references (including BOTH the ID and full human-readable title text) anchored at heading slot 2 exclusively. Then delete the transient Plan.md and ToDos.md files completely. If this task introduces new dependencies or changes run commands, you MUST update the root README.md Setup instructions. After completion, check off the Markdown box locally in the appropriate docs/plan.md. Then commit your changes and push the branch to origin.`
```

## Workflow: PRD/SRS/ADRs → Plan

### Step 1: Read all Context

Scan the @prd.md, @srs.md documents and the ADR files in the @docs/architecture directory.

### Step 2: Group by Phase

Identify foundational requirements (infrastructure, DB) vs core logic vs UI.

### Step 3: Write Tasks with Checkboxes

Draft the plan using the interactive `- [ ]` markdown syntax.

### Step 4: Generate Output to Workspace

> **CRITICAL ARTIFACT ISOLATION OVERRIDE:** You MUST save the generated checklists directly into the project's permanent file structure depending on the plan's scope, and NEVER as an `implementation_plan.md` artifact hidden in your internal system/brain directory.
> 
> When architecting a system or fulfilling a holistic PRD mandate across a monorepo, you MUST generate the plans in this specific sequential order:
> 1. **Global Project Plan:** First, generate the high-level project roadmap and save it to `docs/plan.md` in the repository root.
> 2. **Module-Specific Plans:** Then, generate customized, highly-detailed implementation plans for each specific application/module and save them directly to `apps/[Module Name]/docs/plan.md`.

### Step 5: Map Tests and Requirements

Carefully trace each task to its matching @srs.md block.

### Step 6: Gather Dependencies

Review the final plan, SRS, and ADRs to identify all necessary third-party libraries and frameworks. Generate or update a fresh dependency file appropriate for the stack (e.g., `requirements.txt` for Python, `package.json` for JS).

### Step 7: Documentation, Dockerization & Handoff

Ensure the final Phase of the implementation plan includes a task to populate or update the main `README.md` sections (Development Environment, Viewing Developer Documentation, Production Environment, etc.) based on the finalized tech stack and any Architecture Decision Records (ADRs).
For this final task, you MUST use the following exact Agent Prompt:
`@AGENTS.md Begin by creating a new feature branch. Then read the project's Architecture Decision Records (ADRs) and the finalized tech stack to populate or update the 'Setup Development Environment' (including 'Run the Application' and 'Run tests') and 'Setup Production Environment' (including 'Deploy to Production' and 'Monitor and Update') sections of the README.md file. Ensure installation instructions are platform-agnostic (e.g., don't assume macOS/Homebrew) or explicitly accommodate multiple operating systems as required by the ADRs. However, if the project requires Dockerization, ensure the final Phase of the implementation plan includes a task to populate or update the `Dockerfile` based on the finalized tech stack and ADRs as well as include a "How to Dockerize" section in the README.md file that includes a basic overview of how Docker works and its main components.`
Make sure to check off the task as complete in the appropriate docs/plan.md once finished. Then commit your changes and push the branch to origin.`

### Step 8: Architecture Synthesis

Ensure the _absolute final task_ of the implementation plan invokes the Architecture Writer skill to map the completed system.
For this final task, you MUST use the following exact Agent Prompt:
`@AGENTS.md Begin by creating a new feature branch. Then invoke the @architecture-writer skill. Read its instructions entirely, then execute all steps to synthesize the @docs/prd.md, @docs/srs.md, all srs.md files in apps/[Module Name]/docs/ and ADRs in the @docs/architecture/ folder and an in-depth scan of the codebase reality into a comprehensive @docs/architecture.md file featuring ISO 42010 viewpoints and Mermaid diagrams. Make sure to check off the task as complete in the appropriate @docs/plan.md once finished. Then commit your changes and push the branch to origin.`
