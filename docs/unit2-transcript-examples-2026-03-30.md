# Unit 2 Transcript Examples (2026-03-30)

## Status

- Unit 2 transcript examples are now normalized into replay-ready runtime
  fixtures at
  `app/domain/evidence/unit2-tutor-transcripts.example.json`.
- These fixtures are `provisional` regression examples for the current runtime,
  not claims of final mastery policy or broad classroom validation.
- The current house format stays intentionally conservative:
  - transcript messages are short and text-only
  - `fieldValues` may remain unchecked while text hints drive evaluation
  - each transcript points to a learner fixture that already matches the target
    active-session shape

## Coverage

- `U2-S1`: successful category-sort explanation, plus `uncertain` when zero is
  forced into the positive side
- `U2-S2`: successful number-line ordering, plus `uncertain` when negative
  order is reversed by absolute value
- `U2-S3`: successful absolute-value distance explanation, plus `uncertain`
  when the learner keeps the original negative sign
- `U2-S4`: successful signed-change explanation, plus `uncertain` when the
  learner flips the sign without direction reasoning
- `U2-S5`: successful sign-first structure handling, plus `uncertain` when the
  learner flattens reciprocal or power structure too early

## Source Basis

- `app/content/unit2-scaffold/lesson-steps.json`
- `app/content/unit2-scaffold/evaluator-rubrics.json`
- `app/content/unit2-scaffold/observation-form-mappings.json`
- `docs/unit2-source-evidence-teaching-records-2026-04-02.md`
- `docs/unit2-source-evidence-core-concepts-2026-04-02.md`
- `docs/unit2-source-evidence-signed-change-2026-04-02.md`
- `docs/unit2-source-evidence-multiplicative-structure-2026-04-02.md`

## Current Use

- Use `python app/cli.py list-transcripts --transcript-file app/domain/evidence/unit2-tutor-transcripts.example.json`
  to inspect the current Unit 2 transcript set.
- Use `python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit2-tutor-transcripts.example.json --transcript-id <id>`
  to replay a selected transcript against its learner fixture.
- Treat these fixtures as runtime regression evidence for the current Unit 2
  pack, not as a reason to change thresholds or broader recommendation policy.
