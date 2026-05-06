---
name: Feature Writer
description: Translates SRS requirements into executable BDD feature scenarios based on the initialized tech stack
allowed-tools:
  - code_interpreter
---

# Feature Writer Skill

## Purpose

This skill enables the agent to translate Product Requirement Document (PRD) specifications and Software Requirements Specification (SRS) requirements into well-structured BDD scenarios that bridge the gap between requirements and executable tests.

## When to Use This Skill

- When asked to "Draft Gherkin scenarios" using @docs/srs.md and @docs/prd.md
- When translating SRS requirements into behavioral specifications
- When creating `.feature` files for BDD testing
- When the user references this skill explicitly

## Core Principles

### 1. Identify the Tech Stack
Before writing any output, you MUST detect the project's initialized tech stack:
- **BEAM/Elixir Stack:** Identified by the presence of a `mix.exs` file in the root directory.
- **Python/Javascript Stack:** Identified by a polyglot Monorepo structure, typically with a `requirements.txt` or `package.json` setup for the backend/frontend.

### 2. Traceability
Every scenario MUST map back to a specific SRS requirement.

**Format (Standard Gherkin):**
```gherkin
# SRS-REQ-001: User must be able to upload files up to 500MB
Feature: File Upload
  Scenario: Upload large file successfully
    Given I have a 450MB file
    When I upload the file
    Then the upload should complete successfully
```

### 2. Coverage Strategy
For each core feature, write scenarios covering:
- **Happy Path** (1-2 scenarios): Normal, expected usage
- **Edge Cases** (2-3 scenarios): Boundary conditions, limits
- **Error Cases** (1-2 scenarios): What happens when things go wrong
- **User Interactions** (1-2 scenarios): Explicit scenarios for UI elements (e.g., "When the user clicks the 'Ingest' button...", "When the user toggles the sidebar...").

### 3. Declarative Style
Write scenarios that describe **WHAT** happens, not **HOW** it happens.

**Good:**
```gherkin
Given I have an authenticated session
When I upload a file
Then the file should be stored permanently
```

**Bad:**
```gherkin
Given I click the login button and enter credentials
When I navigate to the upload page and select a file from my filesystem
Then the file should be written to the database with a unique ID
```

## Gherkin Template Structure

### Feature File Structure
```gherkin
# [SRS-REQ-XXX]: [Requirement description]
Feature: [Feature Name]
  As a [user type]
  I want to [action]
  So that [business value]

  Background:
    Given [common precondition for all scenarios]
    And [another common precondition]

  # Happy Path
  Scenario: [Normal successful case]
    Given [precondition]
    When [action]
    Then [expected outcome]
    And [additional verification]

  # Edge Case
  Scenario: [Boundary condition]
    Given [edge case setup]
    When [action at boundary]
    Then [expected behavior]

  # Error Case
  Scenario: [Error condition]
    Given [error setup]
    When [action that triggers error]
    Then [error handling behavior]
```

## Step Definitions Best Practices

### Given Steps
Set up the initial state. Use **past tense** or **present perfect**.

```gherkin
Given I am logged in as a researcher
Given I have a 100MB dataset file
Given the system has 500MB of available storage
```

### When Steps
Describe the action. Use **present tense**.

```gherkin
When I upload the file
When I search for "climate data"
When I click the "Share" button
```

### Then Steps
Verify the outcome. Use **should** or **present tense**.

```gherkin
Then the file should be uploaded successfully
Then I should see 5 search results
Then a permanent link should be generated
```

## Anti-Patterns to Avoid

### ❌ Don't: Include Implementation Details
```gherkin
# BAD
When I POST to /api/upload with multipart/form-data
Then the database should insert a row in the files table
```

### ✅ Do: Stay at Business Level
```gherkin
# GOOD
When I upload a file
Then the file should be stored permanently
```

### ❌ Don't: Write UI-Specific Steps
```gherkin
# BAD
When I click the button with id "upload-btn"
Then I should see a div with class "success-message"
```

### ✅ Do: Write Behavior-Focused Steps
```gherkin
# GOOD
When I initiate the upload
Then I should see a success confirmation
```

### ❌ Don't: Test Multiple Behaviors in One Scenario
```gherkin
# BAD
Scenario: Upload and search and share
  When I upload a file
  And I search for the file
  And I share the file
  Then everything should work
```

### ✅ Do: One Scenario Per Behavior
```gherkin
# GOOD
Scenario: Upload file
  When I upload a file
  Then the file should be stored

Scenario: Search for uploaded file
  Given I have uploaded a file
  When I search for the file
  Then I should find it in results
```

## Workflow: SRS → Gherkin

### Step 1: Read the SRS Requirement
```
SRS-SEC-002: The system MUST encrypt all files client-side before upload.
```

### Step 2: Identify Test Scenarios
- Happy Path: File is encrypted before upload
- Edge Case: Large file encryption
- Error Case: Encryption fails

### Step 3: Write Gherkin
```gherkin
# SRS-SEC-002: Client-side encryption before upload
Feature: Client-Side File Encryption
  As a researcher
  I want my files encrypted before leaving my device
  So that my data remains private

  Scenario: File is encrypted before upload
    Given I have a 10MB file
    When I upload the file
    Then the file should be encrypted client-side
    And the encrypted file should be uploaded to storage
    And the original unencrypted file should not leave my device

  Scenario: Large file encryption
    Given I have a 500MB file
    When I upload the file
    Then the file should be encrypted in chunks
    And each chunk should be encrypted before upload

  Scenario: Encryption failure handling
    Given I have a file
    And encryption fails due to insufficient memory
    When I attempt to upload the file
    Then I should see an error message
    And the file should not be uploaded
```

## Example: Complete Feature File

```gherkin
# SRS-UPLOAD-001: Support file uploads up to 500MB with chunking
Feature: Large File Upload
  As a researcher
  I want to upload large datasets
  So that I can permanently archive my research data

  Background:
    Given I am authenticated with my wallet
    And I have sufficient storage credits

  # Happy Path
  Scenario: Upload small file successfully
    Given I have a 5MB file named "data.csv"
    When I upload the file
    Then the upload should complete in under 2 seconds
    And the file should be stored with metadata
    And I should receive a permanent link

  # Happy Path
  Scenario: Upload large file with chunking
    Given I have a 450MB file named "dataset.zip"
    When I upload the file
    Then the file should be split into 5 chunks
    And each chunk should be uploaded separately
    And the upload should complete successfully
    And I should receive a permanent link

  # Edge Case
  Scenario: Upload file at maximum size limit
    Given I have a 500MB file
    When I upload the file
    Then the upload should succeed
    And the file should be chunked appropriately

  # Edge Case
  Scenario: Upload file exceeding size limit
    Given I have a 501MB file
    When I attempt to upload the file
    Then I should see an error message "File exceeds 500MB limit"
    And the upload should not proceed

  # Error Case
  Scenario: Upload fails mid-transfer
    Given I have a 200MB file
    And I start uploading the file
    When the network connection is lost at 50% progress
    Then the upload should pause
    And I should be able to resume the upload
    And the upload should complete from where it left off

  # Source
  # - srs.md SRS-UPLOAD-001: Support file uploads up to 500MB with chunking
  # - prd.md PRD-3.2: Large File Upload
```

## Socratic Questions to Ask

When drafting features, the agent should ask clarifying questions if the SRS is ambiguous:

1. **Performance vs. Security Trade-offs**
   - "The SRS requires client-side encryption (SRS-SEC-002) but the PRD emphasizes speed (PRD-3.2). Should I prioritize encryption strength or upload speed in the scenarios?"

2. **Error Handling Specifics**
   - "The SRS says uploads should be resumable (SRS-UPLOAD-003), but doesn't specify timeout behavior. Should I assume a 30-second timeout or ask for clarification?"

3. **Edge Case Boundaries**
   - "The SRS specifies a 500MB limit. Should I test at exactly 500MB, or also test 499MB and 501MB?"

## Output Format

When asked to draft feature scenarios, the agent MUST adjust its output format and location based on the detected tech stack:

### For the Python/Javascript Stack:
1. **Format:** Use standard Gherkin `.feature` syntax.
2. **Directory:** Create the `.feature` file in `tests/features/` (Plural `tests/`).
3. **Naming Conventions:** Name the file after the feature (e.g., `file_upload.feature`) and append the SRS requirement ID (e.g., `file_upload_SRS-UPLOAD-001.feature`).
4. **Traceability:** Include the SRS header traceability comment at the top, and append a Source block at the bottom mapping the feature to the SRS and PRD origin (e.g. `# Source` \n `# - srs.md SRS-UPLOAD-001...`).

### For the BEAM/Elixir Stack:
1. **Format:** Use the native Elixir `Wallaby.Feature` macros (e.g., `defmodule MyAppWeb.FileUploadFeatureTest do use Wallaby.Feature...`). Pure text `.feature` files are completely banned.
2. **Directory:** Create the `.exs` file strictly in `test/features/` (Singular `test/`).
3. **Naming Conventions:** Name the file following Elixir conventions (e.g., `file_upload_feature_test.exs`) and append the SRS requirement ID (e.g., `file_upload_SRS-UPLOAD-001_feature_test.exs`).
4. **Traceability:** Include `@moduledoc` tags or comments at the top of the module for SRS traceability, and append a comment block at the bottom mapping the feature to the SRS and PRD origin.

## Integration with Antigravity Workflow

```
USER: Using the SRS, write 5 scenarios for file upload.

AGENT: [Activates Feature Writer skill]
AGENT: [Reads @docs/srs.md]
AGENT: [Identifies relevant requirements: SRS-UPLOAD-001, SRS-SEC-002, SRS-PERF-001]
AGENT: [Checks repository for mix.exs] -> (Detects Python/JS Stack)
AGENT: [Creates tests/features/file_upload.feature]
AGENT: [Writes standard Gherkin scenarios]
AGENT: [Asks clarifying question if needed]
```

## Success Criteria

A well-written Gherkin scenario should:
- ✅ Map to a specific SRS requirement
- ✅ Be readable by non-technical stakeholders
- ✅ Focus on behavior, not implementation
- ✅ Cover happy path, edge cases, and errors
- ✅ Use declarative language (WHAT, not HOW)
- ✅ Be executable by a test framework (Cucumber, Behave, etc.)
