---
name: Knowledge Base Synthesizer
description: Extracts rules, constraints, and models from raw docs/references into a concise .agents/kb/ Markdown file
allowed-tools:
  - code_interpreter
---

# Knowledge Base (KB) Synthesizer Skill

## Purpose

This skill reads raw, unstructured, or heavy technical documents (e.g., PDFs, whitepapers, legal regulations) residing in the `docs/references/` folder and synthesizes them into high-signal, token-efficient Markdown files stored in the `.agents/kb/` folder. It ensures the agents have immediate, conceptual access to project-relevant rules without wasting context window tokens reading boilerplate.

## When to Use This Skill

- When invoked explicitly by the user (e.g., "Refine the ERC-3643 spec into a KB file").
- Immediately following the execution of the `vision-writer` skill, when the user confirms they want to synthesize newly uploaded/downloaded reference files.

## Workflow

### Step 1: Target Identification
Ask the user which specific file(s) in `docs/references/` they wish to synthesize. Ensure the files exist and can be read by the agent.

### Step 2: Boilerplate Stripping
Read the target reference document. Actively ignore tables of contents, legal preambles, marketing fluff, and non-technical context that does not directly impact the engineering, architecture, or design of the software project.

### Step 3: Extraction & Synthesis
Extract the core actionable information from the reference file:
- **Constraints/Laws:** Hard rules the system must mathematically or legally obey.
- **Data Models:** Specific schemas, required fields, or payload structures.
- **Workflow/Processes:** Mandatory sequences of actions mandated by the standard.
- **Security/Privacy:** Explicit auditing or cryptographic parameters.
Rewrite this extracted information in clear, concise Markdown format (bullet points, clear headings). Do not copy-paste long paragraphs; synthesize the intent.

### Step 4: Traceability & Metadata
Apply a standardized YAML header to the newly generated `.agents/kb/` file so that future agents understand its context and authority. 
Ensure the extracted points maintain explicit footnotes or line-item links back to the original section/page of the source reference document (e.g., `(Source: ERC-3643 Whitepaper, Section 4.2)`).

```markdown
---
kb-title: [Title of the Synthesis]
source-reference: docs/references/[filename]
last-updated: [Current Date]
domain: [e.g., Legal, Architecture, Framework]
---

# [Title]

## Key Constraints
- Constraint 1 (Source: Section X)
- ...
```

### Step 5: Finalization
Save the synthesized Markdown file to the `.agents/kb/` directory using an intuitive filename (e.g., `.agents/kb/erc-3643-compliance-rules.md`). Present the generated file to the user for review.

## Success Criteria
- ✅ High Signal-to-Noise: The resulting KB file contains only actionable technical, legal, or architectural rules; all fluff has been stripped.
- ✅ Traceability: Every rule in the KB file points back to its source in the `docs/references/` file.
- ✅ Format: The file uses the proper YAML metadata header and concise Markdown formatting.
- ✅ Location: The file is saved directly into the `.agents/kb/` directory.
