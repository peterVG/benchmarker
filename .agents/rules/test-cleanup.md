# Automated Test Report Cleanup

When configuring test suites that generate report artifacts (e.g., Allure results, Playwright traces, HTML coverage reports), you must ensure that historical test data is automatically cleared before each new test run to prevent "ghost" failures from polluting the reports.

You must implement this cleanup automatically using the native mechanisms of the repository's technology stack:

1. **Node.js (NPM/Yarn)**: Use the `pre` hook lifecycle in `package.json`.
   - Example: Add `"pretest": "rm -rf tests/allure-results"` to run automatically before `"test"`.

2. **Elixir/Erlang (Mix)**: Use Mix task aliases in `mix.exs` to chain shell commands or custom cleanup tasks before the primary `test` task.
   - Example: `defp aliases do [test: ["cmd rm -rf cover/", "test"]] end`

3. **Python (PyTest)**: Use a `Makefile`, `tox` configuration, or a custom `conftest.py` session hook to wipe the coverage or artifact directories before executing the test suite.

4. **Go**: Use a `Makefile` or a wrapper script to clear out `cover.out` or test report directories before invoking `go test`.

**Rule Application:**
Do not expect the user to manually interact with or delete artifact directories. Always configure the project's native build system or test runner to automatically flush these persistence directories upon initiation.
