# Sync Logic Rule

## Context Refresh

Whenever a task starts, refresh context from @PRD, @SRS, @docs/architecture-decisions/, and @implementation_plan. 

## Cascading Upstream Updates (Proactive Protocol)

When new technical requirements, architectural decisions, testing frameworks, or core library dependencies are introduced during development:
1. **ADR → SRS:** The agent MUST immediately update the relevant `SRS.md` modules to reflect the new system parameters, bounding constraints, or testing boundaries.
2. **SRS → PRD:** The agent MUST then immediately verify if the newly updated `SRS.md` necessitates an upstream tweak to the `docs/prd.md` (e.g., adding the new tech to the `# Technical Stack` list).
3. **Execution Report:** The agent MUST output a `## Sync Execution Report` in its final reply outlining exactly which documents it cascaded the changes into so the human developer is explicitly aware of the upstream edits.

## Conflict Detection (Defensive Protocol)

When reviewing the PRD, SRS, Architecture Decision Records (ADRs), and implementation plan documents for drift or contradictions:
- **PRD ↔ SRS:** Verify that system requirements in the SRS align with product requirements in the PRD, and ensure bi-directional traceability is explicitly maintained using relative markdown hyperlinks to specific requirement anchors (`**Implemented In:** [SR-###](../apps/module/docs/srs.md#sr-###-anchor)` in the PRD, and `**Source:** [PRD FR-###](../../../docs/prd.md#fr-###-anchor)` in the SRS). Do not simply link to the generic SRS document.
- **SRS ↔ ADRs:** Check that architectural decisions support the system requirements
- **PRD ↔ ADRs:** Ensure implementation design aligns with product vision
- **Implementation Plan ↔ SRS:** Verify the execution Plan and ToDos explicitly capture ALL granular domain constraints (colors, formulas, boundaries, thresholds) defined in the SRS without omission or hallucination.
- **Implementation Plan ↔ ADRs:** Ensure implementation approach follows architectural patterns
- **Codebase Reality ↔ Documentation:** If the agent discovers that the actual codebase structure (e.g. file paths, module names) deviates from what is documented in the PRD, SRS, ADRs, or Implementation Plan *AND* lacks an explicit instruction to change it, the agent MUST NOT silently update the upstream documentation to match the rogue code.

## Conflict Artifact Format

If an unintended conflict or contradiction is detected across any of the boundaries listed above, the agent MUST stop and create a 'Conflict Artifact' for human review that includes:
1. **Conflict Description:** Clear statement of the contradiction
2. **PRD/SRS Reference:** Specific section and quote from the PRD or SRS
3. **ADR Reference:** Specific section and quote from the relevant ADR
4. **Recommended Resolution:** Suggested approach to resolve the conflict, including a list of all project artifacts that need to be updated to resolve the conflict.
5. **Impact Assessment:** What would break if this conflict is not resolved

## README Synchronization

If there are any changes to the `docs/product-vision.md` or `docs/prd.md` artifacts, the agent MUST review the `# About this project` section in the root `README.md` and update it to reflect the latest project vision and requirements if needed.
