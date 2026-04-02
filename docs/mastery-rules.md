# Mastery Rules

## Purpose
Define the source-of-truth rules for mastery decisions in sujimathAI. This document exists to prevent silent rule drift and to make future changes reviewable.

## Scope
This document covers:
- mastery status labels
- pass/fail decision points
- review expectations for mastery rule changes

This document does not yet define recommendation ranking, prerequisite graphs, or curriculum mappings.

## Terminology
- `mastery`: the project's judgment about whether a learner has sufficiently understood a target skill or topic
- `pass criteria`: the documented conditions required to mark a learner as having passed a mastery check
- `threshold`: the explicit cutoff used in a mastery decision
- `evidence`: the data, validation result, or documented rationale used to support a rule

## Mastery Levels
For the current Unit 1 CLI tutor loop, the repository approves the following
app-facing labels:

- `insufficient_evidence`: not enough skill-linked evidence exists for an automated judgment
- `needs_review`: some skill-linked evidence exists, but it is too ambiguous for a stronger automated claim
- `developing`: documented Unit 1 error patterns show the learner still needs support on this skill
- `ready_for_next_step`: documented positive evidence is strong enough to continue to the next guided step or conservative follow-up practice

These labels are approved for the current app loop only. They are not the final
curriculum-level mastery taxonomy.

## Minimum Approved Promotion Rule
The current repository approves one minimal promotion rule for Unit 1:

- a learner may be marked `ready_for_next_step` for a documented skill when at least one
  skill-linked positive evidence event exists, and that event is either:
  - a direct `correct` event tied to the documented skill, or
  - a completed lesson step whose evaluator rubric matched all required signals

This rule authorizes only:

- continuing to the next guided step in the same conservative session flow
- including the skill in a conservative recommendation sequence

This rule does not authorize:

- a final `mastered` label
- unit completion claims
- numeric pass/fail thresholds

The following remain intentionally undecided:

- numeric thresholds: `UNDECIDED`
- scoring cutoffs: `UNDECIDED`
- retry or reassessment rules: `UNDECIDED`
- override or manual review rules: `UNDECIDED`

## Unit 1 Worked Example: Prime Factorization

### Skill Breakdown
- `U1-S1`: identify prime, composite, and basic prime-number properties
- `U1-S2`: find the prime factors of a given natural number
- `U1-S3`: express a number in prime factorized form
- `U1-S4`: check whether a proposed prime-factor result is complete and valid
- `U1-S5`: use prime factorization in follow-up tasks such as divisor-count or square-making questions

### Mastery Evidence Examples
- `U1-S1`: learner can identify incorrect statements about primes and composites, including that `1` is not prime and that a prime number has exactly two divisors; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`
- `U1-S2`: learner can find all prime factors of a given number in a multiple-choice item such as 미래엔 중단원마무리 03; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`
- `U1-S3`: learner can rewrite a number into prime factorized form in direct `소인수분해` items such as 미래엔 중단원마무리 04; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`
- `U1-S4`: learner can judge whether a proposed answer really contains all prime factors of the number; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`
- `U1-S5`: learner can use prime-factor information in same-unit follow-up tasks such as divisor-count, common-divisor counting, or making a product into a square number; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`

### Evidence Notes For Unit 1
- 미래엔 중단원마무리 02 supports `U1-S1` with statements about primes, composites, and divisor properties.
- 미래엔 중단원마무리 03 supports `U1-S2` and `U1-S4` by asking which option contains all prime factors of a number.
- 미래엔 중단원마무리 04 supports `U1-S3` with a direct prime-factorization expression task.
- 미래엔 중단원마무리 05-08 and 발전 문제은행 05-20 support `U1-S5` with divisor-count, common-divisor, square-making, and related applications.

### Notes
- Evidence basis for this worked example is limited to:
  - `C:\MathFile\중1\중1_ 미래엔 중단원마무리_1_1_소인수분해.pdf`
  - `C:\MathFile\중1\[수준별 문제은행_발전] Ⅰ-1. 소인수분해.pdf`
- These are evidence examples, not approved numeric thresholds.
- `ready_for_next_step` is approved as a conservative next-step judgment, not as final mastery.
- Unit 1 scoring cutoffs, reassessment rules, and override rules remain `UNDECIDED`.

## Unit 2 Worked Example: Core Signed-Number Concepts

### Skill Breakdown
- `U2-S1`: identify integers, rational numbers, positives, negatives, and zero
- `U2-S2`: compare and order integers and rational numbers on the number line
- `U2-S3`: use absolute value to reason about distance and size

### Mastery Evidence Examples
- `U2-S1`: learner can separate positive integers, negative integers, zero, integers, and rational numbers in statement-check or category-selection items; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`
- `U2-S2`: learner can compare signed values by number-line position, identify the midpoint between marked values, or read inequality language correctly in a signed-number context; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`
- `U2-S3`: learner can explain or use absolute value as distance from the origin, including ordering numbers by distance or recognizing that zero has the smallest absolute value; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`

### Evidence Notes For Unit 2
- 미래엔 중단원마무리 01-02 support `U2-S1` with positive-integer filtering and integer/rational statement checks.
- 미래엔 중단원마무리 03 and related explanation notes support `U2-S2` with midpoint reasoning on the number line.
- 미래엔 중단원마무리 04-05 support `U2-S2` and `U2-S3` with ordering-by-distance and absolute-value interpretation.
- `docs/unit2-source-evidence-core-concepts-2026-04-02.md` records the narrower source-backed rationale for this first Unit 2 slice.

### Notes
- Evidence basis for this worked example is limited to:
  - `C:\MathFile\중1\중1_ 미래엔 중단원마무리_1_2_정수와_유리수.pdf`
  - `C:\MathFile\중1\[수준별 문제은행_발전] Ⅰ-2. 정수와 유리수.pdf`
- This worked example promotes only the Unit 2 conceptual cluster `U2-S1` to `U2-S3`.
- These are evidence examples, not approved numeric thresholds.
- `ready_for_next_step` is approved as a conservative next-step judgment, not as final mastery.
- Unit 2 scoring cutoffs, reassessment rules, and override rules remain `UNDECIDED`.

## Unit 2 Worked Example: Signed Addition And Subtraction

### Skill Breakdown
- `U2-S4`: add and subtract integers and rational numbers

### Mastery Evidence Examples
- `U2-S4`: learner can translate a signed addition or subtraction step into number-line movement, keep the direction of change consistent, or solve a contextual condition where adding signed quantities changes whether the result is positive or negative; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`

### Evidence Notes For Unit 2
- 발전 문제은행 03 supports `U2-S4` with a contextual condition problem where adding signed quantities changes whether the result is positive or negative.
- 미래엔 중단원마무리 page 2 supports `U2-S4` with a number-line item asking which signed expression the movement diagram represents.
- 미래엔 중단원마무리 page 3 supports `U2-S4` with direct signed-computation checks.
- `docs/unit2-source-evidence-signed-change-2026-04-02.md` records the narrower source-backed rationale for this Unit 2 operation slice.

### Notes
- Evidence basis for this worked example is limited to:
  - `C:\MathFile\중1\중1_ 미래엔 중단원마무리_1_2_정수와_유리수.pdf`
  - `C:\MathFile\중1\[수준별 문제은행_발전] Ⅰ-2. 정수와 유리수.pdf`
- This worked example promotes only `U2-S4`.
- These are evidence examples, not approved numeric thresholds.
- `ready_for_next_step` is approved as a conservative next-step judgment, not as final mastery.
- Unit 2 scoring cutoffs, reassessment rules, and override rules remain `UNDECIDED`.

## Unit 2 Worked Example: Multiplicative Signed Expressions

### Skill Breakdown
- `U2-S5`: multiply, divide, and simplify expressions with integers and rational numbers

### Mastery Evidence Examples
- `U2-S5`: learner can keep sign rules consistent through signed products and quotients, rewrite or evaluate a reciprocal-based quotient-product expression, or compare structured signed expressions that rely on distributive-law or even-power reasoning; one correct skill-linked event may justify `ready_for_next_step`, but final mastery remains `UNDECIDED`

### Evidence Notes For Unit 2
- 미래엔 중단원마무리 page 3 supports `U2-S5` with direct signed multiplication and division result checks.
- 미래엔 중단원마무리 page 3 and answer/explanation page 5 support `U2-S5` with reciprocal-based free-response computation.
- 발전 문제은행 page 3 supports `U2-S5` with an even-power expression item and a reciprocal-of-reciprocal division item.
- 발전 문제은행 page 5 supports `U2-S5` with distributive-law comparison and sign-pattern conditions across multiple numbers.
- `docs/unit2-source-evidence-multiplicative-structure-2026-04-02.md` records the narrower source-backed rationale for this multiplicative slice.

### Notes
- Evidence basis for this worked example is limited to:
  - `C:\MathFile\중1\중1_ 미래엔 중단원마무리_1_2_정수와_유리수.pdf`
  - `C:\MathFile\중1\[수준별 문제은행_발전] Ⅰ-2. 정수와 유리수.pdf`
- This worked example promotes only `U2-S5`.
- These are evidence examples, not approved numeric thresholds.
- `ready_for_next_step` is approved as a conservative next-step judgment, not as final mastery.
- Unit 2 scoring cutoffs, reassessment rules, and override rules remain `UNDECIDED`.

## Change Policy
- Do not silently change mastery thresholds, pass criteria, or scoring logic.
- Any change to an approved rule must update this document in the same change.
- If a rule is still undecided, mark it clearly as `UNDECIDED` rather than guessing.

## Evidence-Based Updates
- Use documented validation, learner data, or approved policy decisions as evidence.
- Record what changed, why it changed, and what evidence supports it.
- If evidence is weak, incomplete, or pending, state that directly.
