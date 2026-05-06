# Architecture Decision Record - Benchmarker
002-inline-code-docs.md

1. **Title:** Use pdoc and JSDoc for Inline Code Documentation
2. **Status:** Accepted
3. **Context / Requirement Reference:** The Inline Documentation Mandate requires verbose code documentation that is parsable by standard generators.
4. **Decision:** We will use `pdoc` to parse Google or NumPy style docstrings for the Python backend. We will use `JSDoc` for the JavaScript frontend.
5. **Rationale:** `pdoc` requires zero configuration for modern Python and automatically documents typing annotations. JSDoc is the universal standard for Vanilla JS.
6. **Assumptions:** Developers will strictly adhere to the enforced formatting styles (Google/NumPy or JSDoc).
7. **Alternatives Considered:** 
   - Backend: `Sphinx` (powerful but requires complex `conf.py` and RST files, violating the "Minimize Dependencies" principle).
   - Frontend: `TypeDoc` (we are using Vanilla JS, not TypeScript, so JSDoc is more appropriate).
8. **Consequences / Implications:** Code reviews must block PRs that lack compliant docstrings.
9. **Related Decisions / Notes:** See `docs-enforce.md` rule.
