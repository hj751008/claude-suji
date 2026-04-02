# Unit 2 Source Evidence: Teaching Records (2026-04-02)

## Status

- This note narrows the current Unit 2 approval scope to operator-facing
  teaching records tied to already source-backed skills:
  - activity recommendations
  - lesson steps
  - evaluator rubrics
  - observation-form mappings
  - error patterns
  - recommendation examples
- This note is strong enough to support `provisional` app-facing status for the
  Unit 2 teaching records listed above.
- This note does not approve new prerequisite links, final mastery thresholds,
  or replay-ready transcript fixtures.

## Source Basis

- `docs/mastery-rules.md`
- `docs/unit2-source-evidence-core-concepts-2026-04-02.md`
- `docs/unit2-source-evidence-signed-change-2026-04-02.md`
- `docs/unit2-source-evidence-multiplicative-structure-2026-04-02.md`
- `docs/unit2-draft-learning-design-2026-03-30.md`

## Extracted Rationale

### Activities and lesson steps stay inside the approved skill boundaries

- `ACT-U2-S1-SORT-BY-TYPE` and `STEP-U2-S1-CATEGORY-SORT` stay on source-backed
  category language around zero, integers, and rational numbers.
- `ACT-U2-S2-NUMBER-LINE-BRIDGE` and `STEP-U2-S2-NUMBER-LINE-ORDER` stay on
  source-backed left-right comparison, midpoint, and negative-order reasoning.
- `ACT-U2-S3-ABSOLUTE-VALUE-DISTANCE` and
  `STEP-U2-S3-ABSOLUTE-VALUE-DISTANCE` stay on source-backed distance language
  for absolute value.
- `ACT-U2-S4-SIGNED-CHANGE-BRIDGE` and `STEP-U2-S4-SIGNED-CHANGE` stay on
  source-backed number-line movement, contextual signed change, and sign
  consistency.
- `ACT-U2-S5-SIGN-FIRST-EXPRESSION` and
  `STEP-U2-S5-SIGN-FIRST-EXPRESSION` stay on source-backed sign-first,
  reciprocal, power, and multiplicative structure handling.

### Rubrics and observation fields measure the same source-backed signals

- The evaluator rubrics and observation-form mappings do not introduce new
  mastery criteria. They operationalize the same behaviors already recorded in
  the Unit 2 worked examples:
  - category separation and set membership
  - left-right comparison on the number line
  - absolute value as distance
  - directed signed change
  - sign-first multiplicative structure
- Because those signals remain conservative and skill-local, they can move to
  `provisional` without changing thresholds or pass counts.

### Error patterns and recommendation examples stay conservative

- The Unit 2 error patterns mirror the same misunderstandings surfaced in the
  source-backed skill notes and draft learning design.
- The recommendation examples route the learner back to the same source-backed
  skill clusters and do not claim final mastery.
- Their current `limited` and `needsReview` framing remains conservative enough
  for `provisional` status.

## What This Slice Approves

- `app/content/unit2-scaffold/activity-recommendations.json`
- `app/content/unit2-scaffold/lesson-steps.json`
- `app/content/unit2-scaffold/evaluator-rubrics.json`
- `app/content/unit2-scaffold/observation-form-mappings.json`
- `app/content/unit2-scaffold/error-patterns.json`
- `app/content/unit2-scaffold/recommendation-examples.json`

## What This Slice Does Not Approve

- `app/content/unit2-scaffold/prerequisites.json` promotion beyond
  `draft-from-docs`
- new Unit 2 prerequisite chains inferred from pacing convenience alone
- replay-ready transcript fixtures or normalized session-history datasets
- final mastery thresholds or pass counts

## Next Slice

1. Decide whether Unit 2 prerequisite links can move beyond `draft-from-docs`
   with enough evidence.
2. If replay-ready transcript fixtures are needed, convert them from review
   examples into validator-backed evidence files separately.
