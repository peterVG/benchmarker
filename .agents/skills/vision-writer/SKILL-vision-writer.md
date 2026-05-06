---
name: Product Vision Architect
description: Guides the user through a structured discovery process to populate the product-vision-template.md
allowed-tools:
  - google_search
  - code_interpreter
references:
  - docs/templates/product-vision-template.md
---

# Product Vision Architect Skill

## Purpose
This skill facilitates a collaborative, Socratic dialogue to help the user define and refine their product strategy. It transforms abstract ideas into a concrete, validated `docs/product-vision.md` file based on the official template.

## When to Use This Skill
- When the user invokes `/product-vision`
- During the initial "Discovery" phase of a new project or feature
- When a product idea lacks market validation, technical stack clarity, or defined "moats"

## Workflow

### Step 1: Initial Context Gathering
The agent reads the existing `product-vision-template.md` to understand the required fields. It then asks the user for a high-level summary of the idea to establish a baseline.

### Step 2: Socratic Deep-Dive (Section by Section)
The agent does NOT present a wall of text. It engages in **Progressive Discovery**:
1. **Inquiry:** Focuses on 1-2 related sections (e.g., "Product Vision" and "Target Users").
2. **Challenge:** Uses Socratic reasoning to test assumptions. 
   - *Example:* "You mentioned the target is the Dutch public sector; how does this reconcile with the decentralized Arweave storage given current GDPR sovereignty trends?"
3. **Refinement:** Suggests "Gains" and "Pains" based on the user's professional context.

### Step 3: Market & Technical Grounding
- **Verification:** Uses `Google Search` to find "Key Competitors" or verify "Standards, Laws, and Regulations" (e.g., latest e-ARK or ERC-3643 updates).
- **Reference Downloads & Uploads:** Offer to download for the user any specific "Standards, Laws, Regulations" OR "Technical and Domain References" documents that they mention, and store them directly into the `docs/references/` folder. Also instruct the user to manually upload any private files to this folder.
- **KB Refinement Prompt:** Explicitly prompt the user to ask whether any of the raw reference resources now in `docs/references/` should be further refined to create a synthesized `.agents/kb/` file.
- **Feasibility:** Uses `code_interpreter` for "Cost Structure" estimates (e.g., Arweave storage fees or infrastructure overhead).

### Step 4: Drafting & Iteration
The agent maintains a working draft. After each section is "settled," it provides a summary and asks if the user wants to move to the next block of the template.

### Step 5: Final Output
Once all sections are complete, the agent generates `docs/product-vision.md`.

### Step 6: Trigger KB Refinement
If the user previously indicated they want any raw reference resources in `docs/references/` to be further refined into `.agents/kb/` files, explicitly invoke the **Knowledge Base Synthesizer** skill (`.agents/skills/kb-synthesizer/SKILL-kb-synthesizer.md`) to process those specific documents.

## Socratic Prompting Guidelines
- **Ask "Why":** If a user suggests a feature, ask what "Pain" it specifically eliminates.
- **Assumptive Probing:** "If we assume [Constraint X] is true, how does that change our 'Unfair Advantage'?"
- **The "Moat" Check:** Push back on generic advantages. If the user says "easy to use," challenge them to define why it's "difficult to copy."
- **Architectural Completeness:** When discussing the Technical Stack, explicitly ask the user what Datastore (database) and Hosting/Deployment environment they envision if they do not provide one.

## Integration with AI Agent Workflow

USER: /product-vision I want to build a NextCloud plugin for Arweave archiving.
AGENT: [Activates Product Vision Architect]
AGENT: [Searches Dutch public sector NextCloud usage to ground the conversation]
AGENT: "I see you're targeting the Dutch public sector. Would this primarily serve as a 'dark archive' for compliance, or a functional extension for daily users? This will help us define the 'Product Vision' and 'Core Features'."
...
AGENT: [Finalizes all sections]
AGENT: [Creates docs/vision.md]

## Success Criteria
- ✅ **Completness:** Every placeholder in the template is replaced with specific, high-fidelity content.
- ✅ **Internal Consistency:** The "Value Proposition" directly addresses the "Pains" in the Customer Profile.
- ✅ **Technical Realism:** The "Technical Stack" is compatible with the "Key Constraints."
- ✅ **Strategic Depth:** The "Unfair Advantage" identifies a genuine barrier to entry.
- ✅ **Documentation:** A fully populated `docs/product-vision.md` is generated.