# References Directory

This directory contains **technical documentation, whitepapers, and specifications** that the AI agent can reference when needed.

## Purpose

The `references/` directory implements **Progressive Disclosure** - the agent only loads these documents when a skill explicitly requires deep technical grounding, saving context window tokens.

## What Goes Here

### Technical Specifications
- Protocol documentation (e.g., Arweave protocol specs)
- API references (e.g., AO Process API)
- RFC documents
- Industry standards

### Whitepapers
- Academic papers relevant to your domain
- Technical architecture documents
- Research papers

### Third-Party Documentation
- Library documentation
- Framework guides
- Platform specifications

## Example Structure

```
references/
├── arweave/
│   ├── arweave-yellow-paper.pdf
│   ├── transaction-format.md
│   └── fee-calculation.md
├── ao/
│   ├── ao-process-spec.md
│   └── message-passing.md
└── standards/
    ├── oauth2-rfc6749.md
    └── jwt-rfc7519.md
```

## How Skills Use References

Skills specify when to load references using the `references` field in their YAML frontmatter:

```yaml
---
name: Architecture Generator
description: Creates system architecture based on technical specs
allowed-tools:
  - google_search
references:
  - docs/references/arweave/arweave-yellow-paper.pdf
  - .agents/kb/ao/ao-process-spec.md
---
```

**Progressive Disclosure in Action:**
- ✅ Agent only loads these files when the skill is activated
- ✅ Saves tokens when working on unrelated tasks
- ✅ Ensures accurate, up-to-date technical information

## vs. Knowledge Base (`.agents/kb`)

| Directory | Purpose | When Loaded |
|-----------|---------|-------------|
| `docs/references/` | Deep technical specs, loaded by skills | Only when skill is activated |
| `.agents/kb/` | Domain knowledge, loaded by user | When explicitly referenced with `@.agents/kb/file.md` |

**Rule of thumb:**
- Use `docs/references/` for **source material** that skills need automatically
- Use `.agents/kb/` for **domain knowledge** you want to reference manually

## Example: SRS Generation with References

```yaml
---
name: SRS Generator
description: Creates Software Requirements Specification
allowed-tools:
  - google_search
references:
  - docs/references/arweave/transaction-format.md
  - .agents/kb/ao/message-passing.md
---

# SRS Generator Skill

When generating an SRS for file upload:
1. Read the PRD for business requirements
2. Load docs/references/arweave/transaction-format.md for technical constraints
3. Use google_search to verify current library versions
4. Generate SRS with accurate technical specifications
```

## Best Practices

### 1. Keep Files Focused
One topic per file. Don't create massive reference documents.

**Good:**
- `arweave-transaction-format.md`
- `arweave-fee-calculation.md`

**Bad:**
- `arweave-everything.md`

### 2. Use Standard Formats
- Markdown (`.md`) for text documentation
- PDF for official whitepapers
- JSON/YAML for structured data

### 3. Include Metadata
Add a header to each reference file:

```markdown
# Arweave Transaction Format

**Source:** https://docs.arweave.org/developers/server/http-api
**Version:** 2.7
**Last Updated:** 2024-01-15
**Relevant To:** File upload, data storage

[Content...]
```

### 4. Version Control
Keep references up to date. When a spec changes:
1. Update the reference file
2. Update the "Last Updated" date
3. Commit with a clear message

## Progressive Disclosure Benefits

For Gemini's large context window:
- **Token Efficiency:** Don't load 50-page specs unless needed
- **Accuracy:** Agent uses current, verified information
- **Focus:** Agent only sees relevant technical details for the current task

## Example Workflow

```
USER: Generate an SRS for file upload using Arweave

AGENT: [Activates SRS Generator skill]
AGENT: [Skill specifies docs/references/arweave/transaction-format.md]
AGENT: [Loads ONLY that reference file]
AGENT: [Uses google_search to verify current Arweave.js version]
AGENT: [Generates SRS with accurate technical constraints]
```

Without progressive disclosure, the agent would load ALL references upfront, wasting tokens on irrelevant specs.
