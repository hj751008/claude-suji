# Unit 3 Source Evidence: Teaching Records (2026-04-03)

## Status

- This note narrows the current Unit 3 approval scope to operator-facing
  teaching records tied to already source-backed skills:
  - activity recommendations
  - lesson steps
  - evaluator rubrics
  - observation-form mappings
  - error patterns
  - recommendation examples
- This note is strong enough to support `provisional` app-facing status for the
  Unit 3 teaching records listed above.
- This note does not approve new prerequisite links beyond the current
  conservative subset, final mastery thresholds, or replay-ready transcript
  fixtures.

## Source Basis

- `docs/mastery-rules.md`
- `docs/unit3-source-evidence-skills-2026-04-03.md`
- `docs/u3-draft-learning-design-2026-04-02.md`

## Extracted Rationale

### Activities and lesson steps stay inside the approved skill boundaries

- `ACT-U3-S1-DEFINE-VARIABLE-ROLE` and `STEP-U3-S1-DEFINE-VARIABLE-ROLE` stay
  on naming what a variable represents before writing the relationship.
- `ACT-U3-S2-READ-TERM-STRUCTURE` and `STEP-U3-S2-READ-TERM-STRUCTURE` stay on
  coefficient, constant term, and like-term structure reading.
- `ACT-U3-S3-SUBSTITUTE-WITH-STRUCTURE` and
  `STEP-U3-S3-SUBSTITUTE-WITH-STRUCTURE` stay on substitution while preserving
  sign, grouping, reciprocal, and power meaning.
- `ACT-U3-S4-COMBINE-LIKE-TERMS` and `STEP-U3-S4-COMBINE-LIKE-TERMS` stay on
  removing parentheses safely and combining only like terms.
- `ACT-U3-S5-MODEL-THEN-SIMPLIFY` and `STEP-U3-S5-MODEL-THEN-SIMPLIFY` stay on
  building an expression from a context and then simplifying it conservatively.

### Rubrics and observation fields measure the same source-backed signals

- The evaluator rubrics and observation-form mappings do not introduce new
  mastery criteria.
- They operationalize the same behaviors already recorded in the Unit 3 skill
  notes and learning design:
  - defining variable meaning before writing a relationship
  - reading coefficient, constant term, and like terms by role
  - preserving sign and grouping during substitution
  - distributing or removing parentheses safely
  - building a contextual expression before simplifying it
- Because those signals remain conservative and step-local, they can move to
  `provisional` without changing thresholds or pass counts.

### Error patterns and recommendation examples stay conservative

- The Unit 3 error patterns mirror the same misunderstandings surfaced in the
  source-backed skill note and draft learning design.
- The recommendation examples route the learner back to the same source-backed
  skill clusters and keep the current `limited` plus `needsReview` framing.
- That keeps recommendation behavior conservative while still making the Unit 3
  records usable in the current tutor loop.

## What This Slice Approves

- `app/content/unit3-scaffold/activity-recommendations.json`
- `app/content/unit3-scaffold/lesson-steps.json`
- `app/content/unit3-scaffold/evaluator-rubrics.json`
- `app/content/unit3-scaffold/observation-form-mappings.json`
- `app/content/unit3-scaffold/error-patterns.json`
- `app/content/unit3-scaffold/recommendation-examples.json`

## What This Slice Does Not Approve

- `app/content/unit3-scaffold/prerequisites.json` without a separate
  prerequisite note
- replay-ready transcript fixtures or normalized session-history datasets
- final mastery thresholds or pass counts
- runtime activation

## Next Slice

1. Keep transcript examples as review artifacts until replay-ready evidence is
   explicitly approved.
2. Decide whether the currently conservative Unit 3 prerequisite subset is
   strong enough to move to `provisional`.
