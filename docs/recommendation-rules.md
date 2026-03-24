# Recommendation Rules

## Purpose
Define the source-of-truth rules for recommendation behavior in sujimathAI. This document exists to prevent hidden ranking logic and to keep recommendation changes reviewable.

## Scope
This document covers:
- recommendation inputs
- rule categories used to form recommendations
- fallback behavior when inputs are missing or unclear

This document does not yet define mastery thresholds, prerequisite mappings, or curriculum mappings.

## Recommendation Inputs
Current approved input set is:
- learner mastery state, if documented and available
- prerequisite relationship data, if documented and available
- curriculum or content alignment data, if documented and available

The following are not yet approved as recommendation inputs:
- ranking weights: `UNDECIDED`
- numeric scoring formulas: `UNDECIDED`
- tie-break logic: `UNDECIDED`

## Rule Categories
- `eligibility`: whether an item can be recommended at all
- `readiness`: whether the learner appears prepared for the item
- `priority`: how candidate items are ordered after eligibility checks
- `fallback`: what to do when recommendation confidence is limited

Detailed rule definitions for these categories are `UNDECIDED`.

## Fallback Behavior
If required inputs are missing, incomplete, or unverified:
- do not imply high confidence
- prefer conservative recommendations
- mark the case as needing review or more evidence when appropriate

Exact fallback ordering is `UNDECIDED`.

## Constraints
- Do not use hidden business rules.
- Do not silently change recommendation logic.
- Do not treat undecided rules as approved defaults.

## Rules For Uncertain Cases
- If recommendation inputs conflict, mark the case as uncertain.
- If prerequisite or mastery evidence is missing, do not overstate readiness.
- If ordering logic is not approved, leave it as `UNDECIDED` rather than guessing.

## Unit 1 Worked Example: Prime Factorization

### Skill Breakdown
- `U1-S1`: identify prime, composite, and basic prime-number properties
- `U1-S2`: find the prime factors of a given natural number
- `U1-S3`: express a number in prime factorized form
- `U1-S4`: check whether a proposed prime-factor result is complete and valid
- `U1-S5`: use prime factorization in follow-up tasks such as divisor-count or square-making questions

### Recommendation Examples
- If a learner misses 미래엔 중단원마무리 02 style prime/composite property items, recommend review of `U1-S1` before stronger prime-factorization tasks.
- If a learner can attempt `U1-S3` but misses 미래엔 중단원마무리 03 style checks about whether all prime factors are present, recommend `U1-S4` checking tasks in the same unit.
- If a learner can prime-factorize but struggles on 미래엔 중단원마무리 05-08 or 발전 문제은행 05-20 style application questions, recommend `U1-S5` practice.

### Unit 1 Constraints
- ranking weights: `UNDECIDED`
- numeric scoring formulas: `UNDECIDED`
- tie-break logic: `UNDECIDED`
- recommendation order beyond these examples: `UNDECIDED`

## Change Policy
- Any approved recommendation rule change must update this document in the same change.
- Changes should state the affected inputs, rule category, and evidence.
- If logic is still provisional, label it clearly as `UNDECIDED`.
