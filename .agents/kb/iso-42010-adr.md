# ISO/IEC/IEEE 42010: Systems and software engineering — Architecture description

**Purpose:** This document defines the exact structure and required information for all Architecture Decision Records (ADRs) generated in this project. It ensures compliance with international standards for architecture descriptions.

## Required Information Items for ADRs

Any AI Agent creating an Architecture Decision Record (ADR) in the `/docs/architecture/` directory MUST include the following 9 specific information items in the Markdown file. 

The format MUST begin with a top-level header `# Architecture Decision Record - [Project Name]`, followed by the filename, and then the following 9 sections as Markdown headers (e.g., `## Context`, `## Decision`):

### 1. Title
A concise, human-readable name describing the core architectural decision being made.

### 2. Status
The current state of the decision. Valid values are:
*   `Proposed` (Under review)
*   `Accepted` (Approved and in effect)
*   `Deprecated` (Will be phased out)
*   `Superseded` (Replaced by a newer ADR; MUST link to the new ADR)

### 3. Context / Requirement Reference
The technical problem, force, constraint, or specific requirement necessitating the decision. What is the background? Why must we make a choice?

### 4. Decision
The specific architectural choice being made. What is the solution?

### 5. Rationale
The explanation and justification for *why* this specific decision was chosen over others. Why is this the best path forward given the context?

### 6. Assumptions
Any underlying assumptions made while arriving at this decision. What beliefs about the system, users, or technology are we relying on?

### 7. Alternatives Considered
A list of other options that were evaluated and the explicit reasons why each alternative was rejected. This prevents future teams (or agents) from re-evaluating the same dead ends.

### 8. Consequences / Implications
What happens because of this decision? What becomes easier? What becomes harder? What are the immediate trade-offs or technical debt incurred?

### 9. Related Decisions / Notes
References to other related ADRs, outstanding issues, implementation notes, or PRs. If none exist, state "None at this time."
