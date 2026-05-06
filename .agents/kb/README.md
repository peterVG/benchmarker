# Knowledge Base (`.agents/kb`)

This directory contains **synthesized domain knowledge** optimized for AI agent conceptual understanding and project conventions.

## Purpose

Files in `.agents/kb` are intended to be explicitly referenced by users or automatically applied to impart established patterns, rules, and high-level summaries. They give the AI the conceptual grounding necessary to write consistent code and adhere to project standards.

## vs. References (`docs/references`)

| Directory | Purpose | Use Case | When Loaded |
|-----------|---------|----------|-------------|
| `.agents/kb/` | Synthesized AI knowledge, domain concepts, project conventions. | "How do we do things here?" | Loaded when conceptually relevant or explicitly referenced (e.g., `@.agents/kb/beam-testing.md`). |
| `docs/references/` | Raw technical specifications, whitepapers, third-party docs. | "What are the exact technical details of this protocol/API?" | Loaded via **Progressive Disclosure** only when a specific AI Skill explicitly requests the file. |

**Rule of Thumb:**
- Use **`.agents/kb`** for high-level concepts and project vocabulary you want the AI to learn.
- Use **`docs/references`** for dense specification documents, meant for human readears, that would waste context window tokens unless explicitly required for a highly specific task.

## What Goes Here

- **Best Practices:** e.g., `beam-testing.md`, `python-testing.md`.
- **Project Standards:** e.g., `conventional-commits.md`.
- **Glossary/Concepts:** Definitions of domain-specific terms.

## What Does NOT Go Here

- Full API documentation for third party services (put in `docs/references/`).
- 50-page protocol specifications (put in `docs/references/`).
