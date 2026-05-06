# RFC 2119: Key words for use in RFCs to Indicate Requirement Levels

**Purpose:** This document defines the exact terminology used across all requirements documentation (PRDs, SRSs, etc.) in this project to ensure unambiguous specifications. All agents MUST strictly adhere to these definitions when reading, updating, or generating requirement documents.

## Definitions

| Term | Definition for AI Agents |
| :--- | :--- |
| **MUST** | The absolute requirement for the system. This word means that the definition is an absolute condition of the specification. If a requirement uses "MUST", it cannot be ignored under any circumstances. |
| **MUST NOT** | The absolute prohibition of a feature. This phrase means that the definition is an absolute prohibition of the specification. |
| **SHOULD** | A highly recommended, but not strictly mandatory, requirement. This word means that there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course. |
| **SHOULD NOT** | A highly discouraged feature or implementation. This phrase means that there may exist valid reasons in particular circumstances when the particular behavior is acceptable or even useful, but the full implications should be understood and the case carefully weighed before implementing any behavior described with this label. |
| **MAY** / **OPTIONAL** | A truly optional item. This word means that an item is truly optional. One implementation may choose to include the item because a particular marketplace requires it or because the implementation enhances the product, for example; another implementation may omit the same item. |

## Guidance for AI Agents

When generating an SRS or evaluating code against a PRD/SRS:
1. Treat every **MUST** or **MUST NOT** as a strict technical constraint that requires a test (Gherkin scenario).
2. Treat **SHOULD** and **SHOULD NOT** as strong recommendations but allow for architectural flexibility if a better path exists (document the deviation in an ADR).
3. Treat **MAY** as an enhancement that can be deprioritized if time or budget is tight.
