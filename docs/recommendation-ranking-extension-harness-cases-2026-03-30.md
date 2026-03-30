# Recommendation Ranking Extension Harness Cases (2026-03-30)

## Status

- This note records the tie-case matrix used to evaluate the
  `docs/recommendation-ranking-extension-draft-2026-03-29.md` proposal.
- It does not reopen Unit 1 validation.
- It focuses only on recommendation ranking inside the current Unit 1 app loop.

## Baseline Confirmed Before Draft Cases

- `docs/recommendation-rules.md` approved only blocker-first ordering plus final
  stable `targetSkillId` fallback.
- `app/runtime/diagnostics.py` sorted recommendations by:
  1. `REQUIRED` blocker
  2. any blocker
  3. no blocker
  4. stable `targetSkillId`
- `app/runtime/session_planner.py` still chooses only the first recommendation.

## Draft Tie-Case Matrix

### Case 1: same blocker class, different target urgency

- Inputs:
  - `U1-S5A`: `ready_for_next_step`, event count `1`, blocked by missing
    `U1-S3` evidence (`HELPFUL`)
  - `U1-S5B`: `needs_review`, event count `1`, blocked by missing `U1-S3`
    evidence (`HELPFUL`)
- Current minimal rule would order:
  - `U1-S5A`
  - `U1-S5B`
- Draft rule should order:
  - `U1-S5B`
  - `U1-S5A`

### Case 2: same blocker class, same urgency, repeated struggle vs single struggle

- Inputs:
  - `U1-S5A`: `developing`, event count `1`, blocked by missing `U1-S3`
    evidence (`HELPFUL`)
  - `U1-S5B`: `developing`, event count `2`, blocked by missing `U1-S3`
    evidence (`HELPFUL`)
- Current minimal rule would order:
  - `U1-S5A`
  - `U1-S5B`
- Draft rule should order:
  - `U1-S5B`
  - `U1-S5A`

### Case 3: same blocker class, same urgency, positive evidence count tie-break

- Inputs:
  - `U1-S5A`: `ready_for_next_step`, event count `3`, blocked by missing
    `U1-S3` evidence (`HELPFUL`)
  - `U1-S5B`: `ready_for_next_step`, event count `1`, blocked by missing
    `U1-S3` evidence (`HELPFUL`)
- Current minimal rule would order:
  - `U1-S5A`
  - `U1-S5B`
- Draft rule should order:
  - `U1-S5B`
  - `U1-S5A`

### Case 4: full tie falls back to stable skill-id ordering

- Inputs:
  - `U1-S5A`: `ready_for_next_step`, event count `1`, blocked by missing
    `U1-S3` evidence (`HELPFUL`)
  - `U1-S5B`: `ready_for_next_step`, event count `1`, blocked by missing
    `U1-S3` evidence (`HELPFUL`)
- Current minimal rule would order:
  - `U1-S5A`
  - `U1-S5B`
- Draft rule should also order:
  - `U1-S5A`
  - `U1-S5B`

## Approval Readout

- These cases stay inside already documented Unit 1 skills and prerequisite
  links.
- They use only runtime-visible inputs:
  - blocker relationship class
  - target skill summary status
  - target skill event count
  - stable `targetSkillId`
- They do not require hidden weights, numeric formulas, or curriculum changes.
- The only narrow caveat is that `insufficient_evidence` is not currently an
  observed recommendation-target status in the active Unit 1 runtime, so the
  draft order for that status remains policy-only until a future flow emits it.
