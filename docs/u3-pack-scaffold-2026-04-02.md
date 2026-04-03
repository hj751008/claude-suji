# U3 Pack Scaffold (2026-04-02)

## Status

- This is a scaffold only.
- It records `문자의 사용과 식` as the working next-unit topic.
- It is supported by explicit source titles that currently use the broader name
  `문자의 사용과 식의 계산`.
- It does not approve runtime activation.

## Why This Exists

- Keep new unit creation consistent with the current content-pack schema.
- Avoid redoing the same folder and doc setup by hand.

## Current Decision

- Create `app/content/unit3-scaffold/` with the standard pack file shape.
- Use `문자의 사용과 식` as the conservative working topic label for this scaffold.
- Fill source notes before app-facing records.
- Keep unsupported files empty instead of inventing content.

## Confirmed Source Basis

- `C:\MathFile\중1\중1_ 미래엔 중단원마무리_2_1_문자의_사용과_식의_계산.pdf`
- `C:\MathFile\중1\[수준별 문제은행_발전] Ⅱ-1. 문자의 사용과 식의 계산.pdf`

These source titles are enough to support the Unit 3 working topic label and
the existence of a conservative scaffold, but not enough yet to approve filled
runtime-facing records.

## What Is Still Missing

- source-backed skills
- source-backed subskill boundaries between early variable use and later
  expression calculation
- prerequisite links
- teaching records
- transcript examples
- runtime registration
- validator and harness coverage

## Allowed Next Steps

1. Fill `docs/u3-source-note-2026-04-02.md` with source-backed extraction notes.
2. Draft `docs/u3-subskills-unit3-scaffold-2026-04-02.md` from the confirmed
   PDFs.
3. Only after the docs are grounded, generate draft JSON records for the Unit 3
   scaffold.

## Not Approved By This Scaffold

- curriculum codes
- textbook alignment claims beyond the explicit source titles
- final internal unit split for later expression-calculation content
- mastery thresholds
- scoring cutoffs
- cross-unit prerequisite jumps
- runtime activation of Unit 3
