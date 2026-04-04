# Prerequisite Map

## Purpose
Define the source-of-truth rules for prerequisite relationships in sujimathAI. This document exists to prevent guessed topic links and to keep progression logic reviewable.

## Scope
This document covers:
- topic-to-topic prerequisite relationships
- allowed relationship labels
- evidence required before adding or changing a link

This document does not yet define mastery thresholds, recommendation ranking, or curriculum mappings.

## Terminology
- `prerequisite`: a skill or topic that should be understood before attempting another one
- `target`: the later skill or topic being supported
- `relationship`: the documented link between a prerequisite and a target
- `evidence`: the source material or approved rationale supporting the link

## Relationship Types
Approved relationship set is not finalized.

- `REQUIRED`: approved label, use only when supported by evidence
- `HELPFUL`: approved label, use only when supported by evidence
- `UNDECIDED`: use when the relationship has not been approved

## Evidence Requirements
- Do not add prerequisite links without explicit evidence.
- Prefer documented curriculum materials, internal learning design docs, or approved teacher/content review.
- If evidence is partial or disputed, mark the link as `UNDECIDED`.

## Placeholder Mapping Table
| Prerequisite | Target | Relationship | Evidence | Status |
| --- | --- | --- | --- | --- |
| `UNDECIDED` | `UNDECIDED` | `UNDECIDED` | `UNDECIDED` | `placeholder` |

## Unit 1 Worked Example: Prime Factorization

### Skill Breakdown
- `U1-S1`: identify prime, composite, and basic prime-number properties
- `U1-S2`: find the prime factors of a given natural number
- `U1-S3`: express a number in prime factorized form
- `U1-S4`: check whether a proposed prime-factor result is complete and valid
- `U1-S5`: use prime factorization in follow-up tasks such as divisor-count or square-making questions

### Conservative Prerequisite Links
| Prerequisite | Target | Relationship | Evidence | Status |
| --- | --- | --- | --- | --- |
| `U1-S1 identify prime/composite` | `U1-S2 find prime factors` | `HELPFUL` | 미래엔 중단원마무리 02 covers prime/composite properties, and 03 asks for all prime factors in the same unit | `provisional` |
| `U1-S2 find prime factors` | `U1-S3 express in prime factorized form` | `HELPFUL` | 미래엔 중단원마무리 03 asks for all prime factors, and 04 moves to direct prime-factorized form | `provisional` |
| `U1-S3 express in prime factorized form` | `U1-S4 validate prime-factor result` | `REQUIRED` | 미래엔 중단원마무리 03 requires checking whether an option contains the complete prime-factor set of a number | `provisional` |
| `U1-S3 express in prime factorized form` | `U1-S5 use prime factorization in follow-up tasks` | `HELPFUL` | 미래엔 중단원마무리 05-08 and 발전 문제은행 05-20 reuse prime-factorization structure for divisor, square, GCD, and LCM applications | `provisional` |

## Unit 2 Worked Example: Integers and Rational Numbers

### Skill Breakdown
- `U2-S1`: identify integers, rational numbers, positives, negatives, and zero
- `U2-S2`: compare and order integers and rational numbers on the number line
- `U2-S3`: use absolute value to reason about distance and size
- `U2-S4`: add and subtract integers and rational numbers
- `U2-S5`: multiply, divide, and simplify expressions with integers and rational numbers

### Conservative Prerequisite Links
| Prerequisite | Target | Relationship | Evidence | Status |
| --- | --- | --- | --- | --- |
| `U2-S1 identify sign/category language` | `U2-S2 compare and order on the number line` | `HELPFUL` | 미래엔 중단원마무리 01-02 establish sign/category language before 03 and later comparison items move into midpoint, ordering, and inequality reading in the same unit cluster | `provisional` |
| `U2-S2 compare and order on the number line` | `U2-S3 use absolute value as distance` | `HELPFUL` | 미래엔 중단원마무리 04-05 and the related explanation notes define absolute value through distance and ordering on the number line | `provisional` |
| `U2-S1 identify sign/category language` | `U2-S4 add and subtract signed numbers` | `HELPFUL` | The Unit 2 signed-change evidence uses positive/negative meaning before directed movement and result-sign reasoning, so stable sign language supports signed addition and subtraction | `provisional` |
| `U2-S2 compare and order on the number line` | `U2-S4 add and subtract signed numbers` | `HELPFUL` | 미래엔 중단원마무리 page 2 translates signed addition and subtraction into number-line movement, so number-line direction reasoning supports the signed-change skill directly | `provisional` |

### Deliberately Unlinked For Now
- `U2-S5` does not yet receive an internal prerequisite link.
- `docs/unit2-source-evidence-prerequisites-2026-04-02.md` records why the current evidence is strong enough for the four links above but still too weak for a `U2-S5` prerequisite chain.

## Unit 3 Worked Example: Variables And Expressions

### Skill Breakdown
- `U3-S1`: use variables to represent quantities and simple relationships
- `U3-S2`: read the structure of algebraic expressions
- `U3-S3`: evaluate algebraic expressions by substitution
- `U3-S4`: simplify linear expressions with variables
- `U3-S5`: model and simplify contextual expressions

### Conservative Prerequisite Links
| Prerequisite | Target | Relationship | Evidence | Status |
| --- | --- | --- | --- | --- |
| `U3-S1 define variable meaning` | `U3-S5 model contextual expressions` | `HELPFUL` | The current Unit 3 extraction defines `U3-S5` as building an expression from a situation, so variable-role clarity directly supports later modeling work | `provisional` |
| `U3-S2 read term structure` | `U3-S4 simplify linear expressions` | `HELPFUL` | The current Unit 3 extraction defines `U3-S4` through parentheses, distribution, and like-term combination, so reading structural roles supports that simplification step directly | `provisional` |

### Deliberately Unlinked For Now
- `U3-S3` does not yet receive an internal prerequisite link.
- `U3-S4 -> U3-S5` is still left unapproved.
- `docs/unit3-source-evidence-prerequisites-2026-04-03.md` records why the current evidence is strong enough for the two links above but still too weak for a broader Unit 3 chain.
- Notes-only completion logs are now accepted for `U3-S2`, `U3-S4`, and
  `U3-S5`, including the blocker-first replay paths for `U3-S4` and `U3-S5`.
- That evidence increase does not justify a broader Unit 3 prerequisite chain.

## Rules For Uncertain Links
- Do not guess prerequisite chains.
- Do not convert an uncertain link into `REQUIRED` or `HELPFUL` without evidence.
- If a link is suspected but not proven, keep it as `UNDECIDED` and note the missing evidence.

## Change Policy
- Any approved prerequisite change must update this document in the same change.
- Changes should state what was added, removed, or reclassified.
- If evidence is incomplete, report that directly instead of implying certainty.
