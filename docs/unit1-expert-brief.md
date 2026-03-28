# Unit 1 Expert Brief

## Purpose

This brief is for project experts reviewing whether Unit 1 tutor-flow
validation can be treated as complete enough to close the current round.

## Decision Request

Please answer these questions:

1. Can Unit 1 tutor-flow validation be considered complete enough for the
current repo milestone, even though no raw real operator logs are checked into
the repository?
2. Are the current transcript fixtures representative enough of intended
operator logging format to use as regression examples until real logs are
available?
3. What is the minimum additional evidence required for stronger sign-off?

## Verified Facts

- Current Unit 1 transcript coverage includes successful and failure-path
  samples for `U1-S2`, `U1-S3`, `U1-S4`, and `U1-S5A` through `U1-S5D`.
  Source: [app/OPERATOR_GUIDE.md](../app/OPERATOR_GUIDE.md)
- Recommendation behavior is recorded as observed runtime output, not policy.
  Source: [docs/unit1-recommendation-observed-behavior.md](./unit1-recommendation-observed-behavior.md)
- Handoff coverage is verified for completed transfer transcripts through:
  `plan_next_session`, `resume_or_plan_session`, `start_learning_session`,
  `prepare_observation_form`, blocker-first `U1-S3` reopen, and blocker-first
  session completion reorder.
  Source: [docs/unit1-recommendation-observed-behavior.md](./unit1-recommendation-observed-behavior.md)
- Accumulation behavior is verified for repeated-target `U1-S5A` paths,
  including `sessions[]`, `evidenceEvents[]`, `latestSkillSummaries`, and
  `latestRecommendations`.
  Source: [docs/unit1-recommendation-observed-behavior.md](./unit1-recommendation-observed-behavior.md)
- A local browser UI now exists for operator QA over the same runtime paths:
  transcript replay, recommendation handoff inspection, start-session, and
  one-turn observation submission.
  Source: [app/OPERATOR_GUIDE.md](../app/OPERATOR_GUIDE.md)
- Recommendation policy currently keeps the target skill conservative and
  prepends blocker activities ahead of it, rather than replacing the target
  skill.
  Source: [docs/recommendation-rules.md](./recommendation-rules.md)
- `U1-S3 -> U1-S5` is documented as `HELPFUL`, not `REQUIRED`.
  Source: [docs/prerequisite-map.md](./prerequisite-map.md)

## Current Gap

- The repository contains an observation-log template for recording Suji's real
  response after a short tutoring session, but not actual raw operator logs.
  Source: [docs/observation-log-template.md](./observation-log-template.md)
- The repository contains session plans and tutor dialogue-flow docs, but those
  are design artifacts, not real tutoring transcripts.
  Source:
  [docs/suji-mini-session-prime-factorization-01.md](./suji-mini-session-prime-factorization-01.md),
  [docs/suji-tutor-dialogue-flow-prime-factorization.md](./suji-tutor-dialogue-flow-prime-factorization.md)
- The checked-in session log is a repo development log, not learner-session
  evidence.
  Source: [docs/SESSION_LOG.md](./SESSION_LOG.md)

## Working Recommendation

- Do not call Unit 1 tutor-flow validation fully complete in the strong sense
  yet.
- It is reasonable to call it:
  - runtime-complete for transcript-backed regression coverage
  - not yet field-validated against real operator logs
- Stronger sign-off should require at least:
  1. one or two raw real operator logs
  2. a comparison showing where the current fixtures match or diverge from
     those logs
  3. a short decision on whether the current fixture style is acceptable as the
     provisional house format
