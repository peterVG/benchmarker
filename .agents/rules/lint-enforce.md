---
description: Ensure all code is strictly linted and formatted before pushing or testing.
---

# Linting and Formatting Enforcement

**Purpose:** This file instructs the AI agent on exactly how to lint and format the codebase to satisfy the Test-Driven Development (TDD) linting mandate in `AGENTS.md`.

## Active Tools

Based on the accepted Architecture Decision Records (`docs/architecture/004-coding-style-and-linting.md`), this project uses:

- **Ruff** for Python analysis and fast, PEP8-compliant code formatting (Backend).
- **ESLint** for static code analysis (Frontend).
- **Prettier** for opinionated code formatting (Frontend).

## Execution Requirements

Before running any tests, committing code, or completing an execution task, you MUST execute the following CLI commands to ensure the codebase complies with the configured standards. Note that commands MUST be executed inside the correct workspace boundary.

### 1. Format the Frontend Codebase
```bash
cd apps/frontend/
npx prettier --write .
```

### 2. Lint the Frontend (and auto-fix)
```bash
cd apps/frontend/
npx eslint . --fix
```

### 3. Lint and Format the Python Backend (and auto-fix)
```bash
cd apps/backend/
ruff check . --fix
ruff format .
```

## Agent Resolution Mandate

If the `eslint` or `ruff check` commands return a non-zero exit code (indicating unresolved linting errors or warnings configured as errors), the agent **MUST NOT** proceed to testing or committing.

The agent MUST:

1. Review the specific CLI output of the linting errors.
2. Formulate a plan to fix the code logic causing the violations.
3. Apply the fixes.
4. Rerun `npx eslint .` or `ruff check .` to verify all errors are resolved.

Only when Ruff, Prettier, and ESLint all exit cleanly (code 0) is the codebase considered valid for testing or PR submission.
