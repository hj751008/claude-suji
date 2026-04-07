# Authority Map

## Purpose

- This document defines which project documents are authoritative and in what order.
- It exists to stop status notes, closeout notes, or history notes from overruling execution contracts.
- This map must be read together with [project-operating-protocol.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\project-operating-protocol.md).

## Authority Order

### Level 1: Execution Contract

- Defines what the result must actually be before it can be called delivered.

Primary file:
- [unit1-deliverable-definition-2026-04-04.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\unit1-deliverable-definition-2026-04-04.md)

Authoritative sections in that file:
- `Purpose`
- `PM Decision`
- `Why Unit 1 First`
- `Deliverable Statement`
- `Target User For The First Deliverable`
- `In-Scope Capabilities`
- `Out Of Scope For The First Deliverable`
- `Acceptance Criteria`
- `Recommended Demo Flow`
- `Packaging Recommendation`
- `Expansion Gate For Adding Another Unit`

Not authoritative in that file:
- `Unit 1 Done Definition`
- `Current Recommendation`
- `Unit 1 Closeout Checklist`
- `Closeout Verdict`

Reason:
- Those sections contain status interpretation or sequencing assumptions that must not outrank the core execution contract.

### Level 2: Current State

- Records what is true in the repository right now.

Primary file:
- [PROJECT_CONTEXT.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\PROJECT_CONTEXT.md)

Rules:
- `PROJECT_CONTEXT.md` may describe runtime, repo structure, and current validated scope.
- It may not by itself declare a visible deliverable complete.

### Level 3: Active Sequencing

- Records what should happen next.
- Must be derived from Level 1 plus Level 2 only.

Primary file:
- [NEXT_STEPS.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\NEXT_STEPS.md)

Rules:
- `NEXT_STEPS.md` does not have authority to declare a unit done.
- If `NEXT_STEPS.md` conflicts with the execution contract, the execution contract wins.

### Level 4: Status / Checklist / Closeout

- Records milestone status after verification.
- These files do not define what the deliverable is.

Files:
- [unit1-closeout-checklist-2026-04-05.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\unit1-closeout-checklist-2026-04-05.md)
- [unit1-validation-closeout-2026-03-29.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\unit1-validation-closeout-2026-03-29.md)
- [unit2-validation-closeout-2026-04-02.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\unit2-validation-closeout-2026-04-02.md)

Rules:
- These files are non-authoritative until a visible MVP has been reviewed and accepted.
- These files may summarize checks, but they may not redefine product completion.

### Level 5: History / Handoff / Planning / Reference

- Records context, plans, history, or supporting notes.
- These files are useful, but they do not control execution.

Files include:
- [SESSION_LOG.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\SESSION_LOG.md)
- dated outlines
- demo plans
- source notes
- scaffold notes
- historical handoff-style documents

## Current Conflict Notes

1. `Unit 1 deliverable` versus `Unit 1 closed`
- The execution contract still points to a tutor-flow package.
- Later closeout files and `NEXT_STEPS.md` read as if the visible result is already complete.

2. `Proof/support surface` versus `MVP judgment surface`
- Landing, overview, and proof routes may support the story.
- They do not count as the visible MVP by themselves.

3. `Engineering milestone` versus `visible product milestone`
- Harness, transcript replay, and CLI/operator support are real engineering assets.
- They do not automatically mean the visible Unit 1 MVP is delivered.

## Reading Rule

When two documents disagree, use this order:

1. Execution contract
2. Current state
3. Active sequencing
4. Status / checklist / closeout
5. History / handoff / planning / reference

## Current Enforcement Rule

- Until a visible Unit 1 MVP is reviewed and accepted:
  - no closeout file may be treated as final authority
  - `NEXT_STEPS.md` must not be used to justify moving to later-unit work as the main focus
  - support pages must not be treated as equivalent to the agreed tutoring-loop result
