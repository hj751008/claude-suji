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
Current source-of-truth labels are not finalized.

- `Undecided`: mastery level set is not yet approved
- `Undecided`: intermediate states are not yet approved
- `Undecided`: completion/mastered state is not yet approved

When level names are approved, update this section first.

## Pass Criteria Placeholders
The following items are intentionally undecided and must not be assumed in code or content:

- numeric thresholds: `UNDECIDED`
- scoring cutoffs: `UNDECIDED`
- minimum evidence required for pass: `UNDECIDED`
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
- `U1-S1`: learner can identify incorrect statements about primes and composites, including that `1` is not prime and that a prime number has exactly two divisors; pass criteria `UNDECIDED`
- `U1-S2`: learner can find all prime factors of a given number in a multiple-choice item such as 미래엔 중단원마무리 03; pass criteria `UNDECIDED`
- `U1-S3`: learner can rewrite a number into prime factorized form in direct `소인수분해` items such as 미래엔 중단원마무리 04; pass criteria `UNDECIDED`
- `U1-S4`: learner can judge whether a proposed answer really contains all prime factors of the number; pass criteria `UNDECIDED`
- `U1-S5`: learner can use prime-factor information in same-unit follow-up tasks such as divisor-count, common-divisor counting, or making a product into a square number; pass criteria `UNDECIDED`

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
- Unit 1 scoring cutoffs, reassessment rules, and override rules remain `UNDECIDED`.

## Change Policy
- Do not silently change mastery thresholds, pass criteria, or scoring logic.
- Any change to an approved rule must update this document in the same change.
- If a rule is still undecided, mark it clearly as `UNDECIDED` rather than guessing.

## Evidence-Based Updates
- Use documented validation, learner data, or approved policy decisions as evidence.
- Record what changed, why it changed, and what evidence supports it.
- If evidence is weak, incomplete, or pending, state that directly.
