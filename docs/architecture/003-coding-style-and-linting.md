# Architecture Decision Record - Benchmarker
003-coding-style-and-linting.md

1. **Title:** Use Ruff, ESLint, and Prettier for Coding Style and Linting
2. **Status:** Accepted
3. **Context / Requirement Reference:** The Linting Mandate requires all code to be linted and formatted before tests run or code merges.
4. **Decision:** We will use Ruff for the Python backend. We will use ESLint and Prettier for the JavaScript frontend.
5. **Rationale:** Ruff consolidates Flake8, Black, Isort, and others into a single ultra-fast Rust-based tool. ESLint combined with Prettier provides the industry standard for JS analysis and formatting.
6. **Assumptions:** Pre-commit hooks or CI/CD pipelines will enforce these tools.
7. **Alternatives Considered:** 
   - Python: Using separate `black`, `isort`, and `flake8` pipelines (slower and more complex to maintain).
   - JS: StandardJS (less flexible than ESLint + Prettier).
8. **Consequences / Implications:** Agents and humans must run these tools locally in their respective directories before pushing.
9. **Related Decisions / Notes:** See `lint-enforce.md` rule.
