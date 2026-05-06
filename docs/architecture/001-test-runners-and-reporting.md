# Architecture Decision Record - Benchmarker
001-test-runners-and-reporting.md

1. **Title:** Use Pytest, Vitest, Playwright, and Allure for Testing and Reporting
2. **Status:** Accepted
3. **Context / Requirement Reference:** The Test-Driven Development mandate requires comprehensive testing and reporting across the Python backend and JavaScript frontend.
4. **Decision:** We will use Pytest (with pytest-vcr) for Python backend testing. We will use Vitest and Playwright for JavaScript frontend unit and e2e testing. We will use Allure to generate standardized, cross-platform test reports.
5. **Rationale:** Pytest is the industry standard for Python, offering extensive plugins. Vitest is extremely fast for Vanilla JS/Vite setups. Playwright offers modern e2e capabilities. Allure acts as a unified reporting bridge for both ecosystems.
6. **Assumptions:** Developers will have Java installed to run the Allure CLI, and Node.js for Playwright.
7. **Alternatives Considered:** 
   - Backend: `unittest` (too verbose, fewer fixtures).
   - Frontend: `Jest` (slower with Vite than Vitest), `Cypress` (heavier than Playwright for simple apps).
8. **Consequences / Implications:** We must ensure Allure output directories (`tests/allure-results/`) are strictly isolated and purged before each run to avoid merging old data.
9. **Related Decisions / Notes:** Relates to the strict artifact isolation mandate.
