# TDD Enforcement Rule

**Rule ID:** TDD-ENFORCE  
**Priority:** CRITICAL  
**Applies To:** All implementation tasks

---

## Rule Statement

Before writing ANY implementation code, the agent MUST:

1. **Create test files first** (unit tests or functional tests).
2. **Write failing tests** that define expected behavior.
3. **Run tests** to verify they fail (proving they test something).
4. **Implement code** to make tests pass.
5. **Verify success** by showing passing tests in the required Walkthrough artifact.

**Action on Violation:** STOP immediately. Delete implementation code. Create tests first.

---

## Test Types Required

- **Unit Tests (`tests/unit/`):** Required for all business logic, utilities, data transformations.
- **Functional Tests (`tests/features/`):** Required for all user-facing features (Gherkin/BDD).
- **Integration Tests (`tests/integration/`):** Required for API endpoints, database operations, external services.
- **UI Tests (`tests/ui/`):** Required for frontend rendering/interactions (matching the UI Test Mandate).
- **Performance Tests (`tests/performance/`):** Required for production-intended applications.

---

## Walkthrough Artifact Requirements

When implementation is complete, the `Task-[Task ID]-Walkthrough.md` artifact MUST include:

1. **Test Execution Output:** Raw CLI output showing tests passing.
2. **Coverage Report:** Output demonstrating that code coverage meets the project threshold.
3. **SRS Traceability:** A mapping of which specific SRS requirements or PRD features were covered by the executed tests.

---

## Exceptions

This rule does NOT apply to:

1. **Exploratory prototyping** (Explicitly marked as "spike" or "prototype").
2. **Documentation updates** (README, comments, etc.).
3. **Configuration changes** (YAML, JSON config files).
4. **Refactoring existing tested code** (If tests already exist and pass).

*For these cases, the agent must explicitly state: "TDD-ENFORCE: Not applicable - [reason]"*

---

**This rule is ALWAYS ACTIVE and CANNOT be disabled without explicit user approval.**
