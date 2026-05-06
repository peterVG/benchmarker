# Holistic UI Planning and Implementation

## Context
When implementing user interfaces (UI) and user experiences (UX), requirements are often broken down into sequential tasks. This can lead to implementing a "throwaway" interaction model for early tasks, only to have it completely replaced by a subsequent task (e.g., implementing drag-to-pan in Task A, only to replace it with avatar-steered-panning in Task B).

## Rule
Before beginning development on any frontend or UI task, the agent MUST review subsequent UI tasks in the project plan (`docs/plan.md`) and the relevant Software Requirements Specifications (`docs/srs.md`). 

The agent MUST ensure that the interaction model designed and implemented for the *current* task directly supports the final desired state of the application functionality. 

**Do not build temporary interaction scaffolding or throwaway state management if a subsequent task mandates a different control scheme or architecture.** If the interaction model of a later requirement supersedes or fundamentally alters the interaction model of an earlier requirement, the implementation must be holistic from the start, accommodating the final requirements.
