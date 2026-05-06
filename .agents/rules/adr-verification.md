# Architectural Decision Verification

**Purpose:** Eliminate AI context-window decay and architectural hallucinations by mandating deterministic filesystem checks before declaring any technology as unauthorized.

## Search Before Denial
Before an AI agent declares that a specific technology, dependency, testing framework, or architectural pattern is "unauthorized" or "missing from an ADR," the agent MUST explicitly execute a file search tool (e.g. `grep_search`) against the `docs/architecture/` directory to conclusively prove its absence in the written records. 

1. **No Conversational Proxies:** The agent is strictly forbidden from making blanket claims about architectural constraints based purely on probabilistic conversational memory or the absence of the technology in the active system prompt.
2. **Explicit Tech Search:** When tasked with instantiating any third-party framework or dependency, the agent must physically search the ADR logs for formal approval caveats before proceeding or denying the request.
