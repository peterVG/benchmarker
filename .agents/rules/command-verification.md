---
description: Ensure all terminal commands, build steps, and execution scripts documented for humans are actually functional.
---

# Strict Command Verification

Guarantee that any CLI commands, build steps, or execution scripts documented for humans are actually functional and tested against current dependencies.

1. **Test Before Documenting:** Before validating or documenting ANY terminal command, build step, or execution script in a `README.md` or `walkthrough.md`, you MUST first execute that exact command locally using your CLI execution tools to verify it succeeds without errors against the currently installed dependency versions.
2. **Handle Failures:** If the local verification command fails, you MUST NOT document the broken command. Instead, you must either troubleshoot and correct the command syntax, or modify the project configurations/dependencies until the command executes successfully.
3. **Dependency and Registry Validation:** Before proposing any third-party dependency, npm library, Python package, or Docker Registry image in a Design Document, ADR, or `docker-compose.yml`, you MUST actively verify its current existence, optimal versioning, and canonical nomenclature. Run dynamic validations (e.g., `npm info <package>`, terminal package searches, or `search_web` for container registries) to ensure the technology is explicitly not deprecated or relocated before you document it.
