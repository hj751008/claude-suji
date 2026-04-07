# Unit 1 Deliverable Definition (2026-04-04)

## Purpose

- This document defines the most realistic near-term product deliverable for the current repository.
- The recommended deliverable is not "all current units."
- The recommended deliverable is a focused `Unit 1` tutor-flow package that can be shown, replayed, validated, and extended conservatively.

## PM Decision

- Treat `Unit 1` as the first deliverable package.
- Treat `Unit 2` and `Unit 3` as later add-on unit packs, not part of the first product claim.
- Use the current runtime, operator UI, transcript replay, and harness structure as the shared contract that later units must satisfy before they are added.

## Why Unit 1 First

- `Unit 1` is the strongest validated slice in the repository.
- `Unit 1` is documented as `runtime-complete`.
- `Unit 1` has transcript-backed regression coverage, operator UI support, and some real pilot-log comparison.
- `Unit 2` and `Unit 3` are useful and runtime-loaded, but their current status is still more conservative:
  - more `provisional` content and policy language
  - weaker or narrower pilot evidence
  - more explanation cost if presented as part of a first external-facing result

## Deliverable Statement

- The first deliverable is:
  - a local, operator-facing `Unit 1` tutoring workflow for prime factorization
  - with replayable transcript evidence
  - with blocker-first recommendation and session handoff
  - with a browser QA surface for inspection and pilot logging
- The first deliverable is not:
  - a broad classroom-ready product
  - a finalized mastery-scoring product
  - a full multi-unit curriculum release

## Historical Proof-First Done Definition (Non-Authoritative)

- This section is kept as a historical proof-first milestone note.
- Per [authority-map.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\authority-map.md), it is not the active execution contract for `Unit 1`.
- The active contract remains the tutor-flow package and recommended demo flow defined above.

- `Unit 1` is considered done as the first public result only when all of the following are true:
  - the live demo landing, `/unit1`, and `/unit1/proof` are stable in production
  - the `Unit 1` claim is explained honestly on the proof page
  - `Unit 1` browser QA and route-level review are complete for the current public surface
  - `Unit 1` can be shown as the first public result without depending on `Unit 2` or `Unit 3`
  - other units do not appear on the current public surface as part of the first claim
- This done definition is intentionally narrower than "Unit 1 is fully finished forever."
- It means the first public `Unit 1` package is stable enough to show while later units continue behind that front layer.

## Target User For The First Deliverable

- Primary user: internal operator, reviewer, or pilot tutor
- Secondary user: project stakeholder who needs to see one concrete working tutoring loop
- Not yet targeted as a polished student self-serve product

## In-Scope Capabilities

- Load or infer `Unit 1` content through the shared runtime
- Start a learning session from a learner record
- Prepare an observation form from the current lesson step
- Run one learning turn and produce the next action
- Replay transcript fixtures as regression evidence
- Inspect recommendation handoff and blocker-first reopen behavior
- Use the local operator UI for transcript replay, session inspection, one-turn submission, and raw pilot-log export

## Unit 1 Content Scope

- Topic: prime factorization
- Current skill family:
  - `U1-S1` to `U1-S4`
  - `U1-S5A` to `U1-S5D`
- Current evidence posture:
  - runtime-complete for transcript-backed regression coverage
  - pilot-validated at provisional house-format level
  - not broadly field-validated

## Out Of Scope For The First Deliverable

- Broad production or classroom validation
- Numeric mastery cutoff finalization
- Broad reassessment or override policy finalization
- Full student-facing UI polish
- Unit 2 and Unit 3 inclusion in the first product claim
- Automatic claim that all future units are ready once runtime-loaded

## Acceptance Criteria

- `python app/cli.py validate-content` passes
- `python -m app.harness.run_harness` passes
- Unit 1 transcript replay remains available for success and conservative paths
- Unit 1 session handoff remains inspectable through CLI and operator UI
- Operator UI can still:
  - replay transcripts
  - start a session
  - refresh the observation form
  - submit one turn
  - export pilot-log data
- Documentation stays conservative about field confidence and scoring certainty
- The public demo keeps the first claim centered on `Unit 1` only
- The proof page states confirmed facts, current limits, and the later-unit expansion gate separately

## Recommended Demo Flow

- Start from a Unit 1 learner record or Unit 1 transcript preset
- Replay a completed transcript that triggers blocker-first follow-up planning
- Open the next session from the recommendation output
- Show the first blocker step and refresh the observation form
- Submit one turn and show how the runtime decides whether to continue or review the next recommendation

## Packaging Recommendation

- Present the first result as `Unit 1 Tutor Flow Demo`, not as the full Suji Math AI product
- Keep `Unit 2` and `Unit 3` visible in the repository as expansion work, but do not center the first demonstration on them
- Treat the operator UI as the current demo surface unless a separate learner-facing UI is later approved

## Expansion Gate For Adding Another Unit

- A later unit may be attached to the first deliverable only when all of the following are true:
  - app-facing content is source-backed and reviewable
  - `python app/cli.py validate-content` passes
  - `python -m app.harness.run_harness` passes
  - transcript replay exists for the relevant success and conservative paths
  - recommendation and handoff behavior are verified for the shared runtime flow
  - prerequisite claims are explicitly documented and conservative
  - mastery thresholds or cutoffs are not silently broadened

## Historical Sequencing Note (Non-Authoritative)

- This section records the sequencing assumption that was in effect when the proof-first package was treated as the current milestone.
- It does not override the active tutor-flow execution contract above.

- Build the next presentation layer, demo checklist, and packaging docs around `Unit 1` only.
- Continue developing `Unit 2` and `Unit 3` behind that stable front layer when the work does not change the current `Unit 1` result.
- Attach later units to the deliverable only after they satisfy the shared validation gate above.

## Historical Unit 1 Closeout Checklist (Non-Authoritative)

- This checklist is retained as a historical status record.
- It must not be used as the final authority for whether `Unit 1` is visibly delivered.

- Status key:
  - `PASS` means the item is already satisfied in the current repo state.
  - `FAIL` means the item still needs work before `Unit 1` can be treated as closed for the current milestone.

1. `live demo landing, unit1, proof are production-stable`
- Status: `PASS`
- Evidence: the separate demo repo is deployed on Vercel production, and live QA on `/`, `/unit1`, and `/unit1/proof` completed successfully on `2026-04-05`.

2. `Unit 1 claim is explained honestly on the proof page`
- Status: `PASS`
- Evidence: the proof page separates confirmed facts, current limits, and the next validation gate without broadening the product claim.

3. `Unit 1-related QA and browser checks are finished`
- Status: `PASS`
- Evidence: production and local browser checks were run for desktop and mobile views, and the live production pages loaded cleanly.

4. `Unit 1 can be shown as the first public result`
- Status: `PASS`
- Evidence: the homepage, Unit 1 page, and proof page now present a coherent first deliverable story with direct navigation between flow and proof.

5. `No other Unit appears on the public surface yet`
- Status: `PASS`
- Evidence: the public demo only exposes the Unit 1 landing, Unit 1 overview, and Unit 1 proof routes.

## Historical Closeout Verdict (Non-Authoritative)

- This verdict reflects the earlier proof-first milestone framing.
- It is not the controlling verdict for the current visible MVP question.

- `Unit 1` is closed for the current milestone as a first public deliverable.
- `Unit 2` and `Unit 3` remain in the repository as expansion work behind the same conservative validation gate.
- Later work should keep the public demo claim centered on `Unit 1` until a new milestone explicitly expands it.
