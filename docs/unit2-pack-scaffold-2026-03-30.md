# Unit 2 Pack Scaffold (2026-03-30)

## Status

- This is a scaffold only.
- It now approves the next unit topic label `정수와 유리수` because that topic
  is supported by explicit source titles.
- It now also approves first-pass Unit 2 draft records for examples, learner
  difficulties, activities, lesson steps, evaluator signals, and
  observation-form fields.
- It still does not approve a Unit 2 curriculum mapping, prerequisite graph, or
  runtime activation.

## Why This Exists

- Unit 1 is currently the only runtime-loaded unit pack.
- The repository now needs a clear place to gather the next unit's app-facing
  content files.
- Current repo docs do not yet provide enough extracted Unit 2 source material
  to fill a real pack safely.

## Current Decision

- Create `app/content/unit2-scaffold/` with the same file shape as Unit 1.
- Record the next unit topic as `정수와 유리수` only because that topic is
  explicitly supported by checked source titles.
- Keep only unsupported files empty instead of inventing prerequisites or
  runtime behavior.
- Do not wire the scaffold into runtime loaders or validators yet.

## Confirmed Source Basis

- `C:\MathFile\중1\중1_ 미래엔 중단원마무리_1_2_정수와_유리수.pdf`
- `C:\MathFile\중1\[수준별 문제은행_발전] Ⅰ-2. 정수와 유리수.pdf`

These sources now support the topic label, draft subskills, and first-pass
teaching records captured in `docs/unit2-draft-learning-design-2026-03-30.md`.

## What Is Still Missing

- Unit 2 runtime loading
- Unit 2 harness cases
- replay-ready Unit 2 transcript fixtures

## Current Runtime Decision

- Keep Unit 2 scaffold-only for now.
- Reason:
  - prerequisite links and draft transcript examples now exist, but the unit is
    still missing runtime registration and harness cases that exercise the new
    Unit 2 records
- Validator coverage now reaches the scaffold files, but runnable evidence is
  still missing.
- Only move to runtime activation when loader changes and runnable evidence are
  added in the same change.

## Allowed Next Steps

1. Add Unit 2 source extraction docs to `docs/`.
2. Replace the remaining empty scaffold files with doc-backed Unit 2 records.
3. Only after the content is grounded, extend runtime loading and validation
   beyond Unit 1.

## Not Approved By This Scaffold

- curriculum codes
- textbook alignment claims
- numeric mastery thresholds
- scoring cutoffs
- cross-unit prerequisite jumps
- runtime activation of Unit 2
