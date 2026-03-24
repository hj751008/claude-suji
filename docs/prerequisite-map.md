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

## Rules For Uncertain Links
- Do not guess prerequisite chains.
- Do not convert an uncertain link into `REQUIRED` or `HELPFUL` without evidence.
- If a link is suspected but not proven, keep it as `UNDECIDED` and note the missing evidence.

## Change Policy
- Any approved prerequisite change must update this document in the same change.
- Changes should state what was added, removed, or reclassified.
- If evidence is incomplete, report that directly instead of implying certainty.
