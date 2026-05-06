---
name: Requirements Extractor
description: Extracts functional and user requirements from technical and domain reference documents.
allowed-tools:
  - code_interpreter
---

# Requirements Extractor Skill

## Purpose

This skill reads files from the `docs/references/` folder (such as standards, laws, regulations, and technical whitepapers) and systematically extracts specific functional, non-functional, and user requirements that the system must adhere to. 

## When to Use This Skill

- When invoked directly by the user to parse reference material.
- When called up by the **PRD Writer** (or PRD Generator) skill to ingest reference documents and integrate them into the Product Requirements Document (PRD).

## Traceability Mandate

**CRITICAL:** Every requirement extracted MUST maintain strict traceability back to its source document. 
When listing an extracted requirement, you must append an exact citation including:
1. The source document filename
2. The specific page number, section number, or heading where the requirement was found.

**Format:**
`[Requirement Description] (Source: [[filename]](../docs/references/[filename]), Section/Page: [X])`

## Workflow

1. **Identify Sources:** Look in the `docs/references/` directory for uploaded files".
2. **Extract Requirements:** Scan the documents to find constraints, rules, user needs, UI preferences, application features, or functional behaviors required by the specific standards/laws. Provide a complete list, do not exclude any.
3. **Format & Trace:** List the requirements clearly with the Traceability Mandate format applied. Sort them my section and page number from the source document.
4. **Return to Caller:** Provide the extracted, traceable requirements back to the user or the caller skill (like the PRD Writer) for integration.
