---
description: Enforce portable documentation and always use relative links in markdown instead of absolute paths.
---

# Portable Documentation and Linking

All documentation must remain universally portable, readable across any environment, and correctly navigable natively within GitHub.

1. **Strictly Relative Links:** Anytime you generate documenting artifacts, readmes, technical specs, or logs that cross-reference another file in this project, you MUST use standard Markdown relative linking (e.g., `[PRD](../prd.md)` or `[Task 1.1](./tasks/Task-1.1-Plan.md)`).
2. **Prohibited Absolute Paths:** You MUST NEVER write absolute file paths native to your current execution environment (e.g., `file:///Users/...`) into the permanent project repository files. Absolute paths break immediately upon push to a remote repository or clone by another developer.
3. **Verification:** Before saving any markdown file, verify that all file links are relative.
