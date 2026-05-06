---
name: Architecture Writer
description: Reads PRD, SRS, current codebase, and ADRs to synthesize a top-level ISO 42010 System Architecture Document.
allowed-tools:
  - file_system
  - code_interpreter
---

# Architecture Writer Skill

## Purpose

This skill enables the agent to synthesize the project's requirements (PRD/SRS), codebase structure, and Architecture Decision Records (ADRs) into a single, cohesive `docs/architecture.md` file (based on `docs/templates/architecture-template.md`). It provides developers and stakeholders with a high-level "map of the territory," ensuring documentation always reflects reality.

## When to Use This Skill

- Automatically during the final Phase ("Handoff") of any implementation plan (as instructed by `plan-writer`).
- When asked to "Generate an architecture document", "Map the system", or "Document the architecture."
- When significant changes are merged into `main` that substantially alter the tech stack, components, or infrastructure.
- When the user explicitly invokes this skill using `@architecture-writer`.

## Core Principles

### 1. ISO 42010 Viewpoints Conformity

The generated document MUST rigorously organize the architecture into the viewpoints defined by the template (Context, Logical, Data, Physical, Security, Concurrency) to satisfy diverse stakeholder concerns.

### 2. Mandatory Visualizations (Mermaid)

Text alone is insufficient for architecture. The agent MUST generate and render clean, well-structured `mermaid` diagrams for EVERY major section corresponding to a viewpoint.

- **Context Diagram:** Must show the system and its external actors/dependencies.
- **Logical Diagram:** Must show internal module boundaries and message flows.
- **Data Diagram:** Must display an ER Diagram (`erDiagram`) or data pipeline flowchart.
- **Physical/Deployment Diagram:** Must illustrate the infrastructure topology (servers, containers, databases).
- **Sequence Diagram:** Must illustrate complex flows like Authentication or Data Ingestion.

_Note: Ensure Mermaid syntax is valid. NEVER use spaces, hyphens, or special characters in Mermaid node IDs (the programmatic identifiers before the brackets). Always use `CamelCase` or `snake_case` for node IDs (e.g., use `IA_API[Internet Archive]` instead of `IA API[Internet Archive]`)._

### 3. Traceability to ADRs

All technical decisions outlined in the document (frameworks, databases, CI/CD tools) MUST explicitly summarize and link back to the corresponding Architecture Decision Record (`docs/architecture/[ADR].md`). If a tool is used that has no ADR, the agent should highlight this gap.

### 4. Codebase Reflection

The document must reflect _reality_, not just aspirations. Review the actual execution directories (e.g., `app/`, `src/`, or `lib/`), `requirements.txt`/`package.json`, and deployment files (`Dockerfile`, `.github/workflows`) to ensure the listed components genuinely exist in the codebase.

## Workflow: Codebase & ADRs → architecture.md

### Step 1: Read the Blueprint Template

Read the structure provided in `@docs/templates/architecture-template.md`. The output must perfectly mirror this structure.

### Step 2: Read Core Context

Review the latest `@docs/prd.md` and `@docs/srs.md` to understand the stakeholder concerns and system boundaries.

### Step 3: Analyze Codebase Reality

Scan the codebase (`/app`, `/src`, `/lib`, `/tests`, infrastructure files). Identify the actual tech stack, directory structures, database schemas, and external API integrations currently implemented.

### Step 4: Aggregate Architecture Decisions

Read all files matching `docs/architecture/*.md` (excluding templates/directories) to compile the log of accepted ADRs. Extract the core technologies chosen.

### Step 5: Draft the Document & Diagrams

Write the new `docs/architecture.md`. For each ISO 42010 Viewpoint section, meticulously construct the required Mermaid diagram representing the current state of the system based on Steps 2-4. Populate all tables and tech stack summaries.

### Step 6: Verify and Save

Save the output to `docs/architecture.md`. Ensure all links to PRD/SRS/ADRs use correct relative formatting (e.g. `[PRD](./prd.md)` format). DO NOT use absolute paths.

## Success Criteria

- ✅ File successfully created/updated at `docs/architecture.md`.
- ✅ File perfectly follows the ISO 42010 header structure from the template.
- ✅ Contains at least 4 distinct, valid Mermaid diagrams (Context, Logical, Data, Deployment).
- ✅ Explicitly cites the project ADRs in the Technology Decisions Summary table.
- ✅ Strictly reflects the _actual_ codebase state at the time of execution.
