# ISO/IEC/IEEE 29148: Systems and software engineering — Requirements engineering

**Purpose:** This document defines the success criteria for a well-formed Software Requirements Specification (SRS) in this project. All AI agents MUST ensure that any generated SRS adheres to these five primary characteristics.

## Core Characteristics of a Good SRS

When generating, evaluating, or updating a Requirements Specification, agents must strictly verify the document against the following criteria:

### 1. Unambiguous
Every requirement stated has only one interpretation. 
*   **Agent Instruction:** Avoid subjective verbs or adverbs (e.g., "fast", "user-friendly", "robust"). Use concrete metrics, explicit API endpoints, or exact states.

### 2. Complete
The requirement describes everything the software is supposed to do and nothing it is not supposed to do.
*   **Agent Instruction:** Ensure all edge cases, error handling, and non-functional constraints (security, performance) mapped from the PRD are explicitly defined in the technical specification.

### 3. Verifiable
There must exist a finite, cost-effective process to check that the software meets the requirement.
*   **Agent Instruction:** Every single requirement MUST be written such that a concrete test (e.g., a Gherkin `.feature` scenario) can be written to prove it works. If it cannot be tested, it is not a valid requirement.

### 4. Consistent
No two requirements conflict with one another.
*   **Agent Instruction:** Ensure that terminology used across the document matches the glossary and that technical constraints in one section do not physically contradict constraints in another.

### 5. Traceable
The origin of each requirement must be clear, and there must be a mechanism to link it to subsequent design or test documents.
*   **Agent Instruction:** Every requirement block in the SRS MUST include a `**Source**` section at the end, explicitly linking back to its origin in the PRD (e.g., `- prd.md F-001 Feature Name`).
