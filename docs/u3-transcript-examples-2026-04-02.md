# U3 Transcript Examples (2026-04-02)

## Status

- This note maps replay-ready transcript fixtures to each current Unit 3
  lesson step.
- The current replay-ready fixture catalog lives at
  `app/domain/evidence/unit3-tutor-transcripts.example.json`.
- Each step now has:
  - one confirmed completion fixture
  - one uncertain or follow-up fixture

## Source Basis

- `docs/u3-draft-learning-design-2026-04-02.md`
- `docs/unit3-source-evidence-teaching-records-2026-04-03.md`
- `app/content/unit3-scaffold/lesson-steps.json`
- `app/content/unit3-scaffold/observation-form-mappings.json`

## Transcript Targets

### Variable meaning before expression writing

- Lesson step: `STEP-U3-S1-DEFINE-VARIABLE-ROLE`
- Confirmed replay fixture:
  `u3-s1-define-variable-role-ko-text-only-active-session`
- Uncertain replay fixture:
  `u3-s1-define-variable-role-mixed-quantity-ko-uncertain`
- Coverage:
  - learner names what the variable represents before writing the relationship
  - uncertain case keeps mixing quantity meaning with a fixed numeric answer

### Read coefficient, constant term, and like terms

- Lesson step: `STEP-U3-S2-READ-TERM-STRUCTURE`
- Confirmed replay fixture:
  `u3-s2-read-term-structure-ko-text-only-active-session`
- Uncertain replay fixture:
  `u3-s2-read-term-structure-role-swap-ko-uncertain`
- Coverage:
  - learner identifies coefficient and constant term in words
  - uncertain case swaps coefficient and constant roles and over-groups terms

### Substitute while preserving sign and grouping

- Lesson step: `STEP-U3-S3-SUBSTITUTE-WITH-STRUCTURE`
- Confirmed replay fixture:
  `u3-s3-substitute-with-structure-ko-text-only-active-session`
- Uncertain replay fixture:
  `u3-s3-substitute-with-structure-sign-loss-ko-uncertain`
- Coverage:
  - learner rewrites the full substituted expression before computing
  - uncertain case drops the protected negative-sign and power structure

### Remove parentheses and combine only like terms

- Lesson step: `STEP-U3-S4-COMBINE-LIKE-TERMS`
- Confirmed replay fixture:
  `u3-s4-combine-like-terms-ko-text-only-active-session`
- Uncertain replay fixture:
  `u3-s4-combine-like-terms-distribution-slip-ko-uncertain`
- Coverage:
  - learner rewrites the expression one line at a time
  - uncertain case misses part of the distribution and then combines badly
- Current replay note:
  - completion on `U3-S4` currently replans the next session as
    `U3-S2 -> U3-S4` because `U3-S2` is still a helpful blocker-first link

### Build the expression from the story first

- Lesson step: `STEP-U3-S5-MODEL-THEN-SIMPLIFY`
- Confirmed replay fixture:
  `u3-s5-model-then-simplify-ko-text-only-active-session`
- Uncertain replay fixture:
  `u3-s5-model-then-simplify-operation-mismatch-ko-uncertain`
- Coverage:
  - learner names the quantities and relationship before simplifying
  - uncertain case notices quantities but misses the story relationship
- Current replay note:
  - completion on `U3-S5` currently replans the next session as
    `U3-S1 -> U3-S5` because `U3-S1` is still a helpful blocker-first link

## Current Limit

- These fixtures are still one-turn examples, not multi-turn transcripts.
- They are strong enough for current CLI replay and harness coverage, but not
  for broader operator-flow realism claims.
- Additional replay-ready Unit 3 transcript examples can still be added later if
  operator UI QA or session-orchestrator coverage needs stronger evidence.
