---
description: Ensure that generated documentation does not blindly assume the host OS is macOS or Linux.
---

# Platform-Agnostic Documentation

Ensure that the project does not alienate users on different operating systems by hardcoding platform-specific assumptions (e.g., assuming macOS and Homebrew are the default).

2. **Dynamic Setup Instructions:** When generating installation, testing, or execution instructions for the `README.md` or any documentation, you MUST formulate steps that are agnostic to the host OS, or else explicitly provide instructions for Windows, macOS, and Linux or other OSes as appropriate (e.g Android, iOS, etc)
3. **ADR Dependency:** Installation instructions for tools (like test reporters, databases, or orchestrators) MUST be derived strictly from the finalized tech stack in the Architecture Decision Records (ADRs). Do not default to assuming `brew install` or `apt-get` unless explicitly mandated.
