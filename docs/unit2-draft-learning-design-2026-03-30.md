# Unit 2 Draft Learning Design (2026-03-30)

## Status

- This document translates the current Unit 2 source extraction into initial
  app-facing recommendation examples, learner error patterns, and activity
  recommendations.
- It stays at a draft level.
- It now defines first-pass lesson steps, evaluator signals, and
  observation-form fields for the current five draft skills.
- It still does not approve prerequisites, runtime activation, or mastery
  thresholds.

## Source Basis

- `docs/unit2-source-note-2026-03-30.md`
- `docs/unit2-subskills-integers-rational-2026-03-30.md`
- `C:\MathFile\중1\중1_ 미래엔 중단원마무리_1_2_정수와_유리수.pdf`
- `C:\MathFile\중1\[수준별 문제은행_발전] Ⅰ-2. 정수와 유리수.pdf`

## Draft Recommendation Situations

### `U2-S1`

- Recommend when the learner mixes up negative integers, zero, and rational
  numbers during classification tasks.
- Operator focus:
  - keep the discussion on category definitions instead of memorized labels

### `U2-S2`

- Recommend when the learner can read numbers but reverses order on the number
  line, especially with negatives or fractions.
- Operator focus:
  - tie every comparison back to left-right position, midpoint, or interval

### `U2-S3`

- Recommend when the learner treats absolute value as a signed number instead of
  a distance.
- Operator focus:
  - keep returning to “distance from zero” or “distance between points”

### `U2-S4`

- Recommend when the learner can read a signed expression but cannot track
  direction or sign through addition and subtraction.
- Operator focus:
  - slow down the direction change before computing the final value

### `U2-S5`

- Recommend when the learner can start a multiplicative expression but loses the
  sign, power meaning, or reciprocal relationship.
- Operator focus:
  - separate sign reasoning from magnitude reasoning before calculation

## Draft Learner Error Patterns

### `U2-S1`: category confusion

- Learner says zero is positive or negative.
- Learner treats every fraction as “not a number on the line” or forgets that
  integers are included in rational numbers.

### `U2-S2`: order reversal on negatives

- Learner compares negative numbers by absolute value only and reverses the
  order.
- Learner can locate endpoints but not the midpoint or a value between two
  fractions.

### `U2-S3`: absolute value keeps the sign

- Learner writes the absolute value of a negative number as still negative.
- Learner forgets that the smallest absolute value belongs to zero.

### `U2-S4`: signed addition and subtraction drift

- Learner treats `+(-a)` and `-(+a)` mechanically without connecting them to
  movement or change.
- Learner can copy the symbols but cannot translate a condition like “add 5 is
  positive, add 3 is negative.”

### `U2-S5`: sign-first structure loss

- Learner computes magnitudes first but loses sign through multiplication,
  division, powers, or reciprocals.
- Learner knows a rule in isolation but cannot hold it through a multi-step
  expression.

## Draft Activity Recommendations

### `U2-S1`: Sort by sign and set membership

- Activity type: `dialogue-flow`
- Goal:
  - distinguish positive integers, negative integers, zero, integers, and
    rational numbers without label-memorizing shortcuts

### `U2-S2`: Compare and place on the number line

- Activity type: `worked-bridge`
- Goal:
  - compare signed numbers and fractions by position, midpoint, and interval
    instead of by surface appearance

### `U2-S3`: Reframe absolute value as distance

- Activity type: `dialogue-flow`
- Goal:
  - make absolute value a distance idea, not a sign-copying rule

### `U2-S4`: Rewrite signed addition as directed change

- Activity type: `worked-bridge`
- Goal:
  - move between expression form, number-line movement, and inequality
    constraints in signed addition and subtraction

### `U2-S5`: Track sign before calculating

- Activity type: `dialogue-flow`
- Goal:
  - separate sign reasoning, power meaning, reciprocal meaning, and magnitude
    calculation in multiplicative expressions

## Draft Lesson Steps

### `STEP-U2-S1-CATEGORY-SORT`

- Activity link: `ACT-U2-S1-SORT-BY-TYPE`
- Tutor move:
  - make the learner classify zero separately, then connect integers to the
    rational-number set
- Good stopping point:
  - learner says zero is neither positive nor negative and explains why
    integers still belong to rational numbers

### `STEP-U2-S2-NUMBER-LINE-ORDER`

- Activity link: `ACT-U2-S2-NUMBER-LINE-BRIDGE`
- Tutor move:
  - compare by left-right position first, then use that position to explain
    negative-order cases and simple fraction placement
- Good stopping point:
  - learner explains order using number-line position instead of absolute-value
    shortcuts

### `STEP-U2-S3-ABSOLUTE-VALUE-DISTANCE`

- Activity link: `ACT-U2-S3-ABSOLUTE-VALUE-DISTANCE`
- Tutor move:
  - ask for distance first, then connect that distance to absolute-value
    notation
- Good stopping point:
  - learner explains that absolute value is distance and gives a non-negative
    result correctly

### `STEP-U2-S4-SIGNED-CHANGE`

- Activity link: `ACT-U2-S4-SIGNED-CHANGE-BRIDGE`
- Tutor move:
  - translate a signed add/subtract step into left-right movement before
    computing
- Good stopping point:
  - learner keeps movement direction and result sign consistent

### `STEP-U2-S5-SIGN-FIRST-EXPRESSION`

- Activity link: `ACT-U2-S5-SIGN-FIRST-EXPRESSION`
- Tutor move:
  - hold sign reasoning first, then preserve reciprocal or power structure
    through a short expression
- Good stopping point:
  - learner predicts sign before magnitude and does not collapse the expression
    structure

## Draft Evaluator Signals

### `STEP-U2-S1-CATEGORY-SORT`

- Required signals:
  - `classifies_zero_separately`
  - `states_integer_subset_of_rational`

### `STEP-U2-S2-NUMBER-LINE-ORDER`

- Required signals:
  - `orders_by_left_right_position`
  - `explains_negative_order_without_abs_reversal`

### `STEP-U2-S3-ABSOLUTE-VALUE-DISTANCE`

- Required signals:
  - `defines_absolute_value_as_distance`
  - `removes_negative_sign_from_absolute_value`

### `STEP-U2-S4-SIGNED-CHANGE`

- Required signals:
  - `tracks_direction_of_signed_change`
  - `keeps_result_sign_consistent`

### `STEP-U2-S5-SIGN-FIRST-EXPRESSION`

- Required signals:
  - `predicts_overall_sign_first`
  - `keeps_power_or_reciprocal_structure`

## Draft Observation-Form Focus

### `STEP-U2-S1-CATEGORY-SORT`

- Capture whether the learner separated zero correctly and explained how
  integers fit inside rational numbers.

### `STEP-U2-S2-NUMBER-LINE-ORDER`

- Capture whether the learner used left-right number-line language and handled
  negatives without absolute-value reversal.

### `STEP-U2-S3-ABSOLUTE-VALUE-DISTANCE`

- Capture whether the learner explained distance first and avoided a negative
  absolute-value answer.

### `STEP-U2-S4-SIGNED-CHANGE`

- Capture whether the learner translated the sign into movement and kept the
  final sign consistent.

### `STEP-U2-S5-SIGN-FIRST-EXPRESSION`

- Capture whether the learner named the overall sign first and kept reciprocal
  or power structure intact.
