# Recommendation Ranking Extension Draft (2026-03-29)

## Status

- This document is a draft.
- It is not yet the repository source of truth.
- Current approved recommendation behavior remains defined by
  `docs/recommendation-rules.md`.

## Purpose

Propose a narrow ranking extension for the current app loop without introducing:

- hidden weights
- numeric scoring formulas
- confidence inflation

The goal is to replace pure stable skill-id tie-breaking with a slightly more
intentional, still rule-based order.

## Constraints

- Use only learner-state and documented content inputs already present in the
  runtime or clearly derivable from them.
- Do not introduce curriculum jumps or cross-unit behavior.
- Keep `needsReview = true` and `confidence = limited` unless broader policy is
  approved separately.
- Keep blocker-first sequencing unchanged.

## Draft Inputs

### Inputs already effectively present

- target skill id
- target skill summary status
- target skill event count
- documented prerequisite blockers
- blocker relationship type: `REQUIRED`, `HELPFUL`

### Inputs still excluded

- hidden weights
- numeric scoring formulas
- recency formulas
- manual difficulty estimates
- undocumented teacher heuristics

## Draft Exact Ordering Rule

For the current app loop, recommendations would be ordered by the following
tuple, from highest priority to lowest priority:

1. blocker class
2. target urgency class
3. repeated-evidence strength
4. stable skill-id ordering

## Draft Definitions

### 1. Blocker class

Keep the currently approved blocker-first rule:

1. skills blocked by a documented `REQUIRED` prerequisite
2. skills blocked by a documented `HELPFUL` prerequisite
3. unblocked target skills

### 2. Target urgency class

Within the same blocker class, prefer the recommendation whose target skill
summary is less settled:

1. `developing`
2. `needs_review`
3. `insufficient_evidence`
4. `ready_for_next_step`

Reason:

- `developing` and `needs_review` indicate the learner is still actively
  struggling on that target.
- `insufficient_evidence` is weaker than active struggle, but still less settled
  than a target already marked `ready_for_next_step`.
- `ready_for_next_step` should stay available, but should not outrank a target
  that still has clearer unresolved difficulty.

### 3. Repeated-evidence strength

If blocker class and target urgency class are the same:

1. higher `eventCount` first for `developing`, `needs_review`, and
   `insufficient_evidence`
2. lower `eventCount` first for `ready_for_next_step`

Reason:

- For struggle-oriented statuses, repeated evidence means the concern is more
  reliable and should be handled before a single weak signal.
- For `ready_for_next_step`, lower event count avoids over-favoring a skill that
  has already accumulated more positive evidence than another equally eligible
  skill.

## Final Tie-Break

If all prior keys are equal:

1. stable `targetSkillId` ordering

Reason:

- The runtime still needs deterministic output.
- This keeps the last tie-break explicit instead of hidden.

## Worked Examples

### Example A: same blocker class, different urgency

- `U1-S3`: `needs_review`, blocked by `HELPFUL`
- `U1-S5A`: `ready_for_next_step`, blocked by `HELPFUL`

Draft result:

- `U1-S3` before `U1-S5A`

### Example B: same urgency, repeated struggle vs single struggle

- `U1-S4`: `developing`, event count 3
- `U1-S2`: `developing`, event count 1

Draft result:

- `U1-S4` before `U1-S2`

### Example C: same urgency, both positive

- `U1-S5B`: `ready_for_next_step`, event count 1
- `U1-S5C`: `ready_for_next_step`, event count 3

Draft result:

- `U1-S5B` before `U1-S5C`

## Scope Limits

This draft does not yet decide:

- whether recommendation wording should change
- whether `plannedFromSkillId` should ever switch to the blocker skill
- whether the planner should continue choosing only `latestRecommendations[0]`
- whether future units should share the exact same ordering rule

## Recommended Harness Additions If Approved

1. same blocker class, different target urgency
2. same urgency, repeated struggle vs single struggle
3. same urgency, positive skills with different event counts
4. full tie falling back to stable skill-id ordering

## Approval Question

If the repository wants a slightly richer ranking rule now, the smallest safe
approval is:

- keep blocker-first
- add explicit target-status ordering
- add explicit event-count tie-break
- keep stable skill-id as the final fallback

This would improve determinism and explainability without introducing hidden
scoring.
