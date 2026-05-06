---
trigger: always_on
description: Ensure all Architecture Decision Records strictly follow the 9-point ISO 42010 structure.
---

# Architecture Decision Records (ADRs) Formatting

**Purpose:** Document the context and justification for all significant architectural, technical, and product decisions.

1. **Record Decisions, Not Conversations:** Synthesize agreed-upon decisions into lightweight markdown files in `docs/architecture/`.
2. **Naming Convention:** Prefix each ADR with a consecutive three-digit number followed by a hyphenated slug describing the decision (e.g., `001-use-sqlite-for-local-storage.md`).
3. **Standard Format:** Each ADR MUST have the header `# Architecture Decision Record - [Project Name]`, followed by a new line with the ADR filename. To comply with the strict ISO 42010 standard for architecture descriptions, every ADR MUST include these 9 specific information items:
    1. **Title:** A concise name describing the decision.
    2. **Status:** The current state of the decision (e.g., Proposed, Accepted, Deprecated, Superseded).
    3. **Context / Requirement Reference:** The technical problem, force, constraint, or specific requirement necessitating the decision.
    4. **Decision:** The specific architectural choice being made.
    5. **Rationale:** The explanation and justification for *why* this decision was chosen.
    6. **Assumptions:** Any underlying assumptions made while arriving at this decision.
    7. **Alternatives Considered:** A list of other options evaluated and the reasons they were rejected.
    8. **Consequences / Implications:** The trade-offs, impacts on the architecture, and what becomes easier or harder.
    9. **Related Decisions / Notes:** References to other related ADRs, outstanding issues, or additional notes.