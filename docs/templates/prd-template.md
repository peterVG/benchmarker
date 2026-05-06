# Project Requirements Document: [Project Name]

# Executive Summary

# Product Vision
[Project Name] solves the problem of [X] by providing [Y] with [Z].

## Problem Statement


## Target Users

# Functional Requirements

## F-001: [Feature Name]
**Priority:** [Mandatory/Optional]
**User Story:** As a [name of actor type], I want to [action] to create [result]] because [benefit]

### Acceptance Criteria
- eg, User can select files up to 500MB
- eg, User can add metadata fields (title, description, tags)
- eg, Upload progress is visible
- eg, User receives confirmation upon completion

## F-002: [Feature Name]
**Priority:** [Mandatory/Optional]
**User Story:** As a [name of actor type], I want to [action] to create [result]] because [benefit]

### Acceptance Criteria
-
-
-

## Technology Stack
- Frontend: 
- Backend: 
- Storage: 

# Non-Functional Requirements
- quality criteria
- performance criteria
- security criteria
- scalability criteria
- reliability criteria
- maintainability criteria
- usability criteria
- accessibility criteria
- compatibility criteria
- internationalization criteria
- localization criteria

## NFR-001: [Requirement Name]
**Requirement:** [Description]
**Rationale:** [Reason]

# Technical Constraints

## TC-001: Frontend Framework
**Constraint:** Must use React
**Rationale:** Team expertise, component reusability

## TC-002: Storage Solution
**Constraint:** Must use Arweave for permanent storage
**Rationale:** Zero hosting costs, permanent data retention

## Out of Scope (For Now)
- Real-time collaboration
- Version control for files


## Success Criteria
- User can upload 100MB file and retrieve it 10 years later
- Search returns results in under 2 seconds

# Release Criteria

## RC-001: Data Permanence
**Criteria:** User can upload a 100MB file and retrieve it 10 years later
**Verification:** Upload test file, verify transaction on Arweave explorer

## RC-002: Search Performance
**Criteria:** Search returns results in under 2 seconds
**Verification:** Load test with 1000 records, measure p95 latency


## AGENTS.md Principles Integration

The PRD Generator ensures principles defined in AGENTS.md are reflected in product requirements:

### Minimize Dependencies → Feature Simplicity
### Scale-to-Zero → Performance Requirements
### Security by Design → Security Requirements

## PRD Success Criteria

A well-generated PRD should:
- ✅ Map all AGENTS.md sections to appropriate PRD sections
- ✅ Expand high-level features into detailed user stories
- ✅ Include acceptance criteria for each feature
- ✅ Reflect Antigravity principles in requirements
- ✅ Define measurable release criteria
- ✅ Be ready for stakeholder review
- ✅ Serve as input for SRS Generator skill

## Next Steps After PRD Generation

1. **Review PRD** - User reviews and refines generated PRD
2. **Generate SRS** - Use SRS Generator skill: `@PRD.md Generate SRS`
3. **Draft Gherkin** - Use Gherkin Architect skill to create test scenarios
4. **Generate Implementation Plan** - `@PRD.md @SRS.md Generate Implementation Plan`

