# Unit 2 Transcript Examples (2026-03-30)

## Status

- These are draft transcript examples for operator review.
- They are not replay-ready runtime fixtures because Unit 2 is still not
  runtime-loaded.
- They exist to make the new lesson steps easier to review before loader,
  validator, and harness work begins.

## Source Basis

- `docs/unit2-draft-learning-design-2026-03-30.md`
- `app/content/unit2-scaffold/lesson-steps.json`
- `app/content/unit2-scaffold/evaluator-rubrics.json`
- `app/content/unit2-scaffold/observation-form-mappings.json`

## Transcript Drafts

### `u2-s1-category-sort-ko-draft`

- Lesson step: `STEP-U2-S1-CATEGORY-SORT`
- Tutor:
  - `0은 왜 양수나 음수 대신 따로 봐야 하는지 말해 볼래?`
- Learner:
  - `0은 정수이지만 양수도 음수도 아니고, 정수는 유리수에도 들어가.`
- Operator note:
  - learner separated zero correctly and connected integers to rational numbers
- Observation-form style evidence:
  - learner response:
    - `0은 정수이지만 양수도 음수도 아니고, 정수는 유리수에도 들어가.`
  - expected field focus:
    - `classifies_zero_separately`
    - `states_integer_subset_of_rational`

### `u2-s2-number-line-order-ko-draft`

- Lesson step: `STEP-U2-S2-NUMBER-LINE-ORDER`
- Tutor:
  - `-7과 -3 중에서 수직선에서 더 왼쪽에 있는 수는 어느 쪽일까?`
- Learner:
  - `-7이 더 왼쪽이라서 더 작아. 절댓값이 더 크다고 큰 수는 아니야.`
- Operator note:
  - learner used left-right position and avoided absolute-value reversal
- Observation-form style evidence:
  - learner response:
    - `-7이 더 왼쪽이라서 더 작아. 절댓값이 더 크다고 큰 수는 아니야.`
  - expected field focus:
    - `orders_by_left_right_position`
    - `explains_negative_order_without_abs_reversal`

### `u2-s3-absolute-value-distance-ko-draft`

- Lesson step: `STEP-U2-S3-ABSOLUTE-VALUE-DISTANCE`
- Tutor:
  - `-4에서 0까지의 거리가 얼마인지 먼저 말해 볼래?`
- Learner:
  - `거리는 4니까 절댓값도 4야. -4가 아니야.`
- Operator note:
  - learner used distance language before notation and removed the negative sign
- Observation-form style evidence:
  - learner response:
    - `거리는 4니까 절댓값도 4야. -4가 아니야.`
  - expected field focus:
    - `defines_absolute_value_as_distance`
    - `removes_negative_sign_from_absolute_value`

### `u2-s4-signed-change-ko-draft`

- Lesson step: `STEP-U2-S4-SIGNED-CHANGE`
- Tutor:
  - `3에서 -5를 더하면 수직선에서 어느 방향으로 움직인다고 볼 수 있을까?`
- Learner:
  - `왼쪽으로 5만큼 가니까 결과는 -2가 돼.`
- Operator note:
  - learner translated the sign into movement and kept the final sign consistent
- Observation-form style evidence:
  - learner response:
    - `왼쪽으로 5만큼 가니까 결과는 -2가 돼.`
  - expected field focus:
    - `tracks_direction_of_signed_change`
    - `keeps_result_sign_consistent`

### `u2-s5-sign-first-expression-ko-draft`

- Lesson step: `STEP-U2-S5-SIGN-FIRST-EXPRESSION`
- Tutor:
  - `계산하기 전에 전체 식의 부호부터 어떻게 될지 말해 볼래?`
- Learner:
  - `먼저 전체 부호는 음수야. 그리고 역수 구조는 그대로 두고 계산해야 해.`
- Operator note:
  - learner named the sign first and preserved the structure instead of flattening the expression
- Observation-form style evidence:
  - learner response:
    - `먼저 전체 부호는 음수야. 그리고 역수 구조는 그대로 두고 계산해야 해.`
  - expected field focus:
    - `predicts_overall_sign_first`
    - `keeps_power_or_reciprocal_structure`

## Current Use

- Use these examples as review artifacts, not as executable runtime fixtures.
- If Unit 2 becomes runtime-loaded later, convert these into the same evidence
  shape used by Unit 1 transcript fixtures.
