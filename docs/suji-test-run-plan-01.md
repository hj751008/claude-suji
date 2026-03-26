# Suji Test Run Plan 01

## Purpose
This document defines one small real test run for Suji so the current Unit 1 tutoring design can be checked in practice.

This is not a full lesson plan. It is a short test run to confirm whether the current flow is usable for Suji.

## What We Are Testing
- whether Suji can find a first starting point more easily with the `S2` webtoon-style entry
- whether Suji can make one simple verification judgment with the `S4` plain-style check
- whether this format split reduces overload instead of increasing it

## Session Basis
- `docs/suji-mini-session-prime-factorization-01.md`
- `docs/suji-worked-bridge-prime-factorization-entry-webtoon.md`
- `docs/suji-worked-bridge-prime-factorization-verification.md`

## Test Run Length
- about 10-15 minutes

## Test Flow

### 1. Start With S2 Entry
- Use the webtoon-style entry bridge for `24`
- Main question:
  - "가장 먼저 나눠 볼 쉬운 수는 뭐니?"
- What to watch:
  - does Suji freeze immediately
  - does the even-number clue help her start
  - does she say `2` with her own reason

### 2. Do One Short Continue Step
- Stay narrow
- Ask only whether `12` in `2 x 12` can still be broken
- Main question:
  - "지금 남은 수들 중에서 아직 소수가 아닌 것은 뭐니?"
- What to watch:
  - does Suji think the work is already finished
  - can she point to the unfinished part without pressure

### 3. Move To S4 Verification
- Use the plain verification bridge with `2 x 6` vs `2 x 2 x 3`
- Main question:
  - "곱이 맞는 것 말고, 먼저 각 인수가 소수인지 볼까?"
- What to watch:
  - does Suji focus only on the product
  - can she reject `2 x 6` because `6` is not prime

## What Counts As A Good Test Result
- Suji starts `24` by choosing `2` for a reason
- Suji notices that `12` is still not prime in `2 x 12`
- Suji rejects `2 x 6` as a final prime factorization for the right reason

The test run is still useful even if only the first one or two happen.

## Where To Stop
- stop after one stable success in the entry step if Suji is already tired
- stop after the verification step if Suji has made one correct checking judgment
- do not add application problems, divisor count, or square-making in this run

## Immediate Observation Notes To Record After The Session
- where Suji first froze
- which first question helped most
- whether webtoon style reduced hesitation
- whether plain style made the checking step clearer
- what felt too fast, too vague, or too heavy

## Default Interpretation Rule
- If Suji starts more easily in `S2`, keep webtoon only for entry moments.
- If Suji handles `S4` better in plain form, keep verification and procedure steps plain.
- If either step still causes strong freezing, reduce the step size before adding more content.
