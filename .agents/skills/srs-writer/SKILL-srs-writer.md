---
name: SRS Writer
description: Creates Software Requirements Specification from PRD using technical references
allowed-tools:
  - google_search
  - code_interpreter
references:
---

# SRS Generator Skill

## Purpose

This skill generates a Software Requirements Specification (SRS) from a Product Requirements Document (PRD), using technical references to ensure accuracy and up-to-date specifications.

## When to Use This Skill

- When asked to "Generate an SRS"
- When translating PRD business requirements into technical specifications
- When the user references this skill explicitly

## Progressive Disclosure

This skill demonstrates **progressive disclosure** by:
1. **Loading references only when activated** - Saves tokens when working on other tasks
2. **Using google_search** - Verifies current library versions (e.g., latest Arweave.js)
3. **Using code_interpreter** - Validates technical calculations (e.g., storage costs)

## Workflow

### Step 1: Read the PRD
```
AGENT: [Reads @docs/prd.md]
AGENT: [Identifies core features and business requirements]
```

### Step 2: Load Technical References
```
AGENT: [Loads @docs/kb/rfc-2119.md and @docs/kb/iso-29148.md for standards definitions]
AGENT: [Loads relevant reference files from the @docs/references/ folder]
AGENT: [Now has deep technical grounding]
```

### Step 3: Verify Current Versions
```
AGENT: [Uses google_search to ensure SRS uses the most current versions of software libraries and references]
```

### Step 4: Validate Constraints
```
AGENT: [Checks @docs/prd.md for budget, technical and other constraints]
AGENT: [Verifies that technical approach meets all constraints from PRD]
```

### Step 5: Generate SRS
```
AGENT: [Creates docs/srs.md]
AGENT: [Maps all PRD requirements to the SRS using a dedicated **Source** section at the end of each requirement block. Format: `- [[source ID]](../prd.md) [source name]`]
AGENT: [**CRITICAL**: Do not omit Non-Functional Requirements (NFRs) or Technical Constraints (TCs). Every single item in the PRD—including architecture rules, performance limits, and framework restrictions—MUST be mapped 1:1 to an explicit SRS requirement block to guarantee 100% forward traceability.]
AGENT: [Ensures forward-traceability by defining an expected **Tests** section mapping to all target Gherkin, integration, performance, ui, and unit test files. Format MUST respect the monorepo bounds defined in `.agents/rules/workspace-boundaries.md` by dynamically mapping to the active technology stack's idiomatic isolated testing vocabulary (e.g. `- [[filename]](../apps/backend/tests/features/[filename])` for Python/JS tracking, or `- [[filename]](../apps/my_app_web/test/features/[filename])` for BEAM/Elixir tracking)]
AGENT: [If an SRS requirement cannot be validated via a standard BDD feature file (e.g., overarching NFRs or Technical Constraints), the **Tests** block MUST define alternative automated verification strategies locally. Examples include: CI/CD configuration files, static code analysis tools, locus testing bounds, or explicit UI assertions.]
AGENT: [Ensures SRS strictly complies with ISO/IEC/IEEE 29148 (Unambiguous, Complete, Verifiable, Consistent, Traceable)]
AGENT: [Uses "MUST" or "MUST NOT" for mandatory requirements and "SHOULD" or "SHOULD NOT" for optional requirements per RFC 2119]
AGENT: [Includes accurate library versions and technical constraints]
```

### Step 6: Verify Traceability
```
AGENT: [Cross-references every F-XXX, NFR-XXX, and TC-XXX identifier listed in the PRD against the newly generated SRS document.]
AGENT: [If any PRD identifier is missing from the SRS, the agent MUST halt, append the missing requirements, and regenerate the mapping before completing the task.]
AGENT: [Conclude the task by appending a Summary Traceability Matrix or checklist ensuring 100% PRD coverage.]
```

## Example Output

**From PRD:**
```markdown
## Feature: File Upload
Users should be able to upload datasets up to 500MB for permanent storage.
Budget: $100/month for storage costs.
```

**Generated SRS:**
```markdown
# SRS-UPLOAD-001: File Upload Service

## Functional Requirements

### SRS-UPLOAD-001.1: File Size Support
The system MUST support file uploads up to 500MB.

**Technical Implementation:**
- Use Arweave.js v1.14.4 (verified via google_search)
- Chunk files larger than 100MB per Arweave transaction limits
- Transaction format per references/arweave/transaction-format.md

**Source**
- `[prd.md](../prd.md)` F-001 File Upload

**Tests**
- [`large_file_upload_SRS-UPLOAD-001.feature`](../tests/features/large_file_upload_SRS-UPLOAD-001.feature)

### SRS-UPLOAD-001.2: Permanent Storage
Files MUST be stored permanently on Arweave.

**Cost Validation:**
- Executed scripts/validation/calculate_storage_fees.py
- Estimated cost: $0.005/MB = $2.50 per 500MB file
- 40 files/month = $100/month ✅ Within budget

**Source**
- `[prd.md](../prd.md)` F-001 File Upload

**Tests**
- [`large_file_upload_SRS-UPLOAD-001.feature`](../tests/features/large_file_upload_SRS-UPLOAD-001.feature)

### SRS-UPLOAD-001.3: Chunking Strategy
Files larger than 100MB MUST be chunked.

**Technical Specification:**
- Chunk size: 100MB (per Arweave transaction limits)
- Use AO message passing for chunk coordination (per references/ao/message-passing.md)
- Implement resumable uploads per SRS-PERF-003

**Source**
- `[prd.md](../prd.md)` F-001 File Upload

**Tests**
- [`large_file_upload_SRS-UPLOAD-001.feature`](../tests/features/large_file_upload_SRS-UPLOAD-001.feature)
```

## Benefits of Progressive Disclosure

### Without Progressive Disclosure
```
AGENT: [Loads ALL references upfront: 50 pages of Arweave docs]
AGENT: [Loads ALL references upfront: 30 pages of AO specs]
AGENT: [Loads ALL references upfront: OAuth, JWT, etc.]
AGENT: [Context window: 80% full before even starting]
AGENT: [Hallucinates library versions because context is full]
```

### With Progressive Disclosure
```
AGENT: [Loads ONLY Arweave and AO references - 10 pages]
AGENT: [Context window: 20% full]
AGENT: [Uses google_search for current versions]
AGENT: [Accurate SRS with verified technical specs]
```

## Integration with AI Agent Workflow

```
USER: @AGENTS.md Generate a baseline SRS in /docs based on @docs/prd.md and the manifesto principles in the AGENTS.md file. Use the "Gherkin Writer" skill to generate Gherkin scenarios for each unique requirement in @docs/srs.md and @docs/prd.md
AGENT: [Activates SRS Generator skill]
AGENT: [Reads AGENTS.md for AI Agent principles]
AGENT: [Reads docs/prd.md for business, functional and non-functional requirements and constraints]
AGENT: [Loads @docs/references for technical specifications and context]
AGENT: [Uses google_search to verify current library versions]
AGENT: [Creates docs/srs.md with accurate technical specifications]
AGENT: [Activates Gherkin Writer skill]
AGENT: [Creates Gherkin .feature files in the tests/features folder for each unique requirement in docs/srs.md and docs/prd.md]
```

## Success Criteria

A well-generated SRS should:
- ✅ Strictly comply with ISO/IEC/IEEE 29148: Unambiguous, Complete, Verifiable, Consistent, and Traceable requirements
- ✅ Strictly comply with RFC 2119: "MUST" or "MUST NOT" for mandatory requirements and "SHOULD" or "SHOULD NOT" for optional requirements
- ✅ Map 100% of PRD items (Features, Non-Functional Requirements, and Technical Constraints) mathematically to numbered SRS technical requirements
- ✅ Use current, verified library versions (not hallucinated)
- ✅ Include technical constraints from prd.md and reference documents
- ✅ Validate costs/performance with executable scripts
- ✅ Follow Antigravity principles from AGENTS.md
- ✅ Guarantee full forward-traceability without data loss from the primary PRD
