---
name: PRD Writer
description: Generates a baseline Product Requirements Document (PRD) based on product vision and reference materials.
allowed-tools:
  - google_search
references:
  - docs/templates/prd-template.md
---

# PRD Writer Skill (PRD Generator)

## Purpose

This skill drafts a comprehensive Product Requirements Document (PRD) by interpreting the `docs/product-vision.md` and invoking the **Requirements Extractor** skill to automatically pull constraints and requirements from the files in `docs/references/`.

## When to Use This Skill

- When the user asks to "Generate a baseline PRD" or uses the `/prd-writer` command.

## Workflow

### Step 1: Read the Vision
Read the `docs/product-vision.md` file to understand the overarching business goal, target users, and value proposition. Look for references to specific standards or laws.

### Step 2: Invoke Requirements Extractor
Call the **Requirements Extractor** skill to scan any documents provided in the `docs/references/` folder (such as standards, laws, and regulations). The extractor will return functional and user requirements with strict traceability (source filename and section/page number).

### Step 3: Read Principles
Read the `AGENTS.md` file to ensure the PRD aligns with the stated architectural and project principles (e.g., Scale-to-Zero, Privacy by Design).

### Step 4: Draft the PRD
Draft the `docs/prd.md` document using the structure from `docs/templates/prd-template.md`. 
Ensure that:
- Core features from the product vision are translated into specific functional and user requirements. Add a source citation for each requirement derived from the product-vision.md document.
- The extracted requirements from the `docs/references/` are heavily integrated.
- Every extracted requirement from files in `docs/references/` maintains its traceability citation as provided by the Requirements Extractor.

### Step 5: Update Project Overview
Read the newly finalized `docs/prd.md` and the original `docs/product-vision.md` to synthesize a concise project overview (1-2 paragraphs). Inject this overview directly into the `# About this project` section of the root `README.md` file, replacing the placeholder note.

### Step 6: Final Review
Present the generated `docs/prd.md` and the updated `README.md` to the user for review and refinement.
