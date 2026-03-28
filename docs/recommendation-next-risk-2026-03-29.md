# Recommendation Next Risk (2026-03-29)

## Why This Is Next

Unit 1 transcript, handoff, and pilot validation are now strong enough to stop
reopening Unit 1 by default. The next major risk is not transcript realism. It
is recommendation ranking and generalization beyond the current minimal
blocker-first rule set.

## Confirmed Current State

### 1. What the docs approve

- `docs/recommendation-rules.md` approves only a minimal ordering rule:
  1. `REQUIRED` blockers first
  2. `HELPFUL` blockers next
  3. unblocked target skills after blocker-driven sequences
  4. ties by stable skill-id ordering
- The same document leaves the following as `UNDECIDED`:
  - ranking weights
  - numeric scoring formulas
  - tie-break logic beyond stable skill-id ordering
  - higher-confidence recommendation ranking

### 2. What the runtime does

- `app/runtime/diagnostics.py` currently:
  - builds one recommendation per target skill
  - prepends blocker activities ahead of target-skill activities
  - keeps `targetSkillId` on the original skill
  - sets `recommendedNextSkillIds = blocker + target`
  - sorts recommendations by:
    - has `REQUIRED` blocker
    - else has any blocker
    - else no blocker
    - then `targetSkillId`
- `app/runtime/session_planner.py` then chooses `latestRecommendations[0]`
  without any extra ranking layer.

### 3. What is already acceptable

- This behavior is acceptable for the current Unit 1 milestone because:
  - it matches the approved minimal blocker-first rule
  - it keeps confidence conservative
  - it avoids hidden scoring

## Why This Is Still a Risk

### 1. Ranking is still narrow

- Once future units or more skills exist, stable skill-id ordering will become a
  weak tie-break.
- The current runtime has no richer policy for:
  - recency
  - repeated struggle intensity
  - cross-skill urgency
  - same-skill repetition fatigue

### 2. The current planner is first-item only

- `plan_next_session()` simply takes the first recommendation.
- This is safe now, but it means future ranking changes will directly affect the
  entire session flow.

### 3. Unit 1 evidence already exposed the UX pressure point

- During Unit 1 review, `S5` completion often surfaced the same `targetSkillId`
  while reopening from a blocker-first step.
- That behavior is currently explainable and document-approved, but it shows how
  recommendation wording and ranking can become confusing before the policy is
  broadened.

## Recommended Next Work

1. Write an approved recommendation-ranking extension for the current app loop.
   - Keep it rule-based.
   - Do not introduce hidden weights.
   - State exact tie-break order.
   - Current draft: `docs/recommendation-ranking-extension-draft-2026-03-29.md`

2. Add explicit harness cases for ranking ties.
   - same blocker class, different skills
   - repeated evidence on one skill vs single evidence on another
   - no-blocker recommendations with multiple candidates

3. Decide whether the planner should keep using only the first recommendation
   or expose a narrow multi-option review surface.

## Recommended Decision Boundary

- If the next work is still inside Unit 1 only:
  - extend recommendation ranking tests first
- If the next work is a new unit:
  - create the new unit pack first
  - then revisit ranking once multiple units or broader skill sets exist

## Practical Recommendation

Because the repository does not yet contain a Unit 2 pack, the most grounded
next task is:

- `recommendation ranking/generalization scoping and harness expansion`

This moves the project forward without reopening Unit 1 policy or inventing a
new unit before content exists.
