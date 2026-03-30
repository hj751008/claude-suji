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
- learner mastery state, including target-skill summary status and target-skill event count, if documented and available
- prerequisite relationship data, including documented blocker relationship type, if documented and available
- curriculum or content alignment data, if documented and available
- documented Unit 1 activity and lesson-step mappings, when a recommendation needs a session payload

The following are not yet approved as recommendation inputs:
- ranking weights: `UNDECIDED`
- numeric scoring formulas: `UNDECIDED`
- recency formulas: `UNDECIDED`

## Rule Categories
- `eligibility`: recommend only skills and activities that already exist in documented Unit 1 content
- `readiness`: if a prerequisite blocker exists, keep the target skill conservative and include the blocker ahead of it
- `priority`: order recommendations by prerequisite blocker strength before considering the direct target skill
- `fallback`: when confidence is limited, keep `needsReview = true` and avoid hidden weights or jumps to broader application work

For the current Unit 1 app loop, the repository approves the following minimal ordering rule:

1. skills blocked by a documented `REQUIRED` prerequisite come first
2. skills blocked by a documented `HELPFUL` prerequisite come next
3. unblocked target skills come after blocker-driven sequences
4. within the same blocker class, target-skill urgency orders by:
   - `developing`
   - `needs_review`
   - `insufficient_evidence`
   - `ready_for_next_step`
5. if blocker class and target urgency are the same:
   - higher `eventCount` comes first for `developing`, `needs_review`, and `insufficient_evidence`
   - lower `eventCount` comes first for `ready_for_next_step`
6. if prior keys are still equal, use stable skill-id ordering instead of hidden ranking weights

For the current Unit 1 app loop, the repository also approves the following sequencing rule:

1. if a blocker exists, prepend blocker activities before target-skill activities
2. if no blocker exists, keep the recommendation on the target skill only
3. session payloads must be built only from documented lesson steps

## Fallback Behavior
If required inputs are missing, incomplete, or unverified:
- do not imply high confidence
- prefer conservative recommendations
- mark the case as needing review or more evidence when appropriate

If a learner shows one positive event on a skill but prerequisite evidence is still missing,
the repository approves keeping that skill in the recommendation while conservatively
prepending the blocker skill when documented prerequisite links require it.

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
- recommendation confidence above `limited`: `UNDECIDED`
- recommendation order beyond the blocker/urgency/event-count rule set above: `UNDECIDED`

## Change Policy
- Any approved recommendation rule change must update this document in the same change.
- Changes should state the affected inputs, rule category, and evidence.
- If logic is still provisional, label it clearly as `UNDECIDED`.
