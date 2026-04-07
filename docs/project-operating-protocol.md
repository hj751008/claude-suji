# Project Operating Protocol

## Purpose

- This document defines how project work must be reviewed, sequenced, and reported.
- It exists to prevent repeated drift between:
  - execution contracts
  - status/closeout notes
  - visible product results
- This protocol is part of the current working base.
- The backup folder is reference material only. It is not the active project base.

## Team Structure

Every meaningful project task must be reviewed through the following team lenses before it is treated as complete.

1. Analysis Team
- Finds structural contradictions, missing assumptions, and priority conflicts.

2. Development Team
- Turns the agreed contract into an implementation plan.
- Checks whether the requested result is actually buildable from the current base.

3. UI Design Team
- Reviews whether the visible surface communicates the right thing clearly and honestly.
- Distinguishes support pages from actual judgment surfaces.
- Owns hierarchy, legibility, and demo-vs-product interpretation risk on the UI side.

4. Frontend Team
- Judges visible product surfaces.
- Decides whether a page is support-only or an actual MVP judgment surface.

5. Backend Team
- Verifies runtime, CLI, harness, operator flow, and implementation reality.

6. DB/Data Team
- Verifies learner record, active session, transcript, observation form, recommendation, and handoff state contracts.
- If no real database is involved, this team still owns the state/data model.

7. Security Team
- Reviews trust boundaries, demo/runtime mismatch, misleading readiness claims, and exposure risks.

8. Maintenance Team
- Owns document authority order, working-tree hygiene, and separation between contract/state/history.

9. Integration Team
- Merges team conclusions into one ordered recovery or execution plan.
- Prevents phase jumping.

## Phase Order

Work must follow these phases in order.

### Phase 1: Analysis

- No implementation.
- No closeout updates.
- No new public claims.
- Required outputs:
  - authority map
  - backup salvage/rewrite map
  - visible MVP contract

### Phase 2: Cleanup

- Clean up authority conflicts in current project docs.
- Demote stale or dangerous status documents.
- Keep the working base in the current repository only.
- No MVP build work yet.

### Phase 3: Build

- Build only after Analysis and Cleanup are locked.
- Use current runtime assets as the implementation base.
- Do not treat support pages as MVP completion.

### Phase 4: Verification

- Verify the actual result.
- Prefer runtime-backed checks, browser checks, and visible output checks over narrative-only proof.

### Phase 5: Closeout

- Update status and next-step docs only after the visible result is reviewed and accepted.

## Hard Rules

1. Do not let status or closeout documents outrank execution contracts.
2. Do not move to the next unit because a document says the current unit is done.
3. Do not treat landing, proof, or route existence as product completion unless the MVP contract explicitly says so.
4. Do not import backup structure into the current working base.
5. Use backup only for reference, comparison, and salvage analysis.
6. Do not skip from Analysis to Build.
7. Do not write `done`, `closeout`, or `next unit` before the visible MVP is reviewed.

## Document Authority Order

Current project documents must be interpreted in this order.

1. Execution contract
- Defines what the result must actually be.

2. Current state
- Records what is true in the repository now.

3. Active sequencing
- Records what should happen next, derived from contract plus current state.

4. Status / checklist / closeout
- Records milestone checks only after verification.

5. History / handoff / planning / reference
- Records context, not authority.

## Reporting Format

Every project report must use this order.

1. `확인됨`
2. `추론`
3. `미확인`
4. `에러`
5. `다음 진행`

Rules:
- `확인됨` must only contain facts supported by the repo, checks, or visible outputs.
- `추론` must explain interpretation, tradeoffs, and team synthesis.
- `미확인` must list what is still unknown.
- `에러` must list contradictions, blockers, or process failures plainly.
- `다음 진행` must follow the current phase order and must not skip gates.

## Backup Policy

- `C:\Users\tcikh\OneDrive\문서\codex\sujimathAI_backup` is reference-only.
- It may be used to:
  - compare old and current document roles
  - salvage durable principles
  - identify previously failed structures
- It may not be used as:
  - the active project base
  - a direct replacement structure
  - proof that current work is complete

## Visible MVP Rule

- A unit is not treated as visibly delivered until there is a reviewer-judgable surface that shows the agreed MVP contract.
- Support-only routes do not count as delivery by themselves.
- Closeout documents must follow visible review, not replace it.
