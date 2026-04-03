# U3 Draft Learning Design (2026-04-02)

## Status

- This document translates the current Unit 3 source extraction into initial
  app-facing recommendation examples, learner error patterns, and activity
  recommendations.
- It stays at a draft level.
- It now defines first-pass lesson steps, evaluator signals, and
  observation-form focus for the current five draft skills.
- It still does not approve prerequisites, runtime activation, or mastery
  thresholds.

## Source Basis

- `docs/u3-source-note-2026-04-02.md`
- `docs/u3-subskills-unit3-scaffold-2026-04-02.md`
- `C:\MathFile\중1\중1_ 미래엔 중단원마무리_2_1_문자의_사용과_식의_계산.pdf`
- `C:\MathFile\중1\[수준별 문제은행_발전] Ⅱ-1. 문자의 사용과 식의 계산.pdf`

## Draft Recommendation Situations

### `U3-S1`

- Recommend when the learner can describe a situation verbally but cannot
  assign variables or write a matching expression.
- Operator focus:
  - keep the discussion on what each symbol stands for before simplifying

### `U3-S2`

- Recommend when the learner can copy an expression but cannot identify
  coefficient, constant term, number of terms, or like terms.
- Operator focus:
  - make the learner read each term aloud by role, not only by symbol

### `U3-S3`

- Recommend when the learner substitutes values mechanically and loses sign,
  exponent, reciprocal, or grouping structure.
- Operator focus:
  - separate substitution from simplification and check sign first

### `U3-S4`

- Recommend when the learner can start simplification but drops parentheses,
  distributes incorrectly, or combines unlike terms.
- Operator focus:
  - slow down structure changes before collecting terms

### `U3-S5`

- Recommend when the learner can simplify a naked expression but cannot build
  the expression correctly from a context.
- Operator focus:
  - translate the situation into named quantities first, then simplify

## Draft Learner Error Patterns

### `U3-S1`: variable-role confusion

- Learner uses the same variable for different quantities or does not define
  what the variable represents.
- Learner writes a number-only answer where the task still asks for an
  expression.

### `U3-S2`: structure-reading confusion

- Learner confuses coefficient with term count or constant term.
- Learner treats terms of different degree or different variables as like terms.

### `U3-S3`: substitution sign drift

- Learner substitutes correctly but loses a negative sign, reciprocal, or power
  meaning while computing.
- Learner treats `x = 1` style evaluation as if the expression can be reordered
  freely without preserving grouping.

### `U3-S4`: simplification structure loss

- Learner removes parentheses without tracking the outer sign or factor.
- Learner combines unlike terms or changes the coefficient while collecting
  terms.

### `U3-S5`: context-to-expression mismatch

- Learner chooses the right quantities but writes the wrong operation
  relationship.
- Learner can build the first expression but cannot simplify it into a usable
  final form.

## Draft Activity Recommendations

### `U3-S1`: Name the quantity before writing the symbol

- Activity type: `dialogue-flow`
- Goal:
  - translate short situations into variable expressions without losing what
    each symbol stands for

### `U3-S2`: Read each term by role

- Activity type: `dialogue-flow`
- Goal:
  - identify coefficient, constant term, like terms, and linear-expression
    structure by reading terms one by one

### `U3-S3`: Substitute, then compute

- Activity type: `worked-bridge`
- Goal:
  - preserve sign, exponent, reciprocal, and grouping structure after
    substitution

### `U3-S4`: Simplify without breaking structure

- Activity type: `worked-bridge`
- Goal:
  - distribute correctly, remove parentheses safely, and combine only like
    terms

### `U3-S5`: Build the expression from the story

- Activity type: `worked-bridge`
- Goal:
  - model average, concentration, geometry, and counting situations with an
    expression before simplifying

## Draft Lesson Steps

### `STEP-U3-S1-DEFINE-VARIABLE-ROLE`

- Activity link: `ACT-U3-S1-DEFINE-VARIABLE-ROLE`
- Tutor move:
  - ask what each variable stands for before writing the relationship
- Good stopping point:
  - learner names the quantity and writes a matching simple expression

### `STEP-U3-S2-READ-TERM-STRUCTURE`

- Activity link: `ACT-U3-S2-READ-TERM-STRUCTURE`
- Tutor move:
  - read coefficient, variable part, and constant term separately before asking
    whether two terms are alike
- Good stopping point:
  - learner identifies coefficient, constant term, and like terms without
    mixing roles

### `STEP-U3-S3-SUBSTITUTE-WITH-STRUCTURE`

- Activity link: `ACT-U3-S3-SUBSTITUTE-WITH-STRUCTURE`
- Tutor move:
  - substitute first, then hold sign and grouping structure while computing
- Good stopping point:
  - learner evaluates a substituted expression without losing sign or power
    meaning

### `STEP-U3-S4-COMBINE-LIKE-TERMS`

- Activity link: `ACT-U3-S4-COMBINE-LIKE-TERMS`
- Tutor move:
  - remove parentheses carefully, then collect only like terms
- Good stopping point:
  - learner simplifies a linear expression and can explain why unlike terms did
    not combine

### `STEP-U3-S5-MODEL-THEN-SIMPLIFY`

- Activity link: `ACT-U3-S5-MODEL-THEN-SIMPLIFY`
- Tutor move:
  - translate the context into an expression before any arithmetic
- Good stopping point:
  - learner writes a context-matching expression and simplifies it into a clean
    final form

## Draft Evaluator Signals

### `STEP-U3-S1-DEFINE-VARIABLE-ROLE`

- Required signals:
  - `defines_variable_meaning`
  - `writes_matching_expression_from_context`

### `STEP-U3-S2-READ-TERM-STRUCTURE`

- Required signals:
  - `identifies_coefficient_or_constant_correctly`
  - `distinguishes_like_terms_by_structure`

### `STEP-U3-S3-SUBSTITUTE-WITH-STRUCTURE`

- Required signals:
  - `substitutes_values_without_structure_loss`
  - `keeps_sign_or_power_meaning_consistent`

### `STEP-U3-S4-COMBINE-LIKE-TERMS`

- Required signals:
  - `distributes_or_removes_parentheses_correctly`
  - `combines_only_like_terms`

### `STEP-U3-S5-MODEL-THEN-SIMPLIFY`

- Required signals:
  - `builds_expression_from_context_relationship`
  - `simplifies_context_expression_consistently`

## Draft Observation-Form Focus

### `STEP-U3-S1-DEFINE-VARIABLE-ROLE`

- Capture whether the learner named the quantity each variable represents and
  matched that meaning to the expression.

### `STEP-U3-S2-READ-TERM-STRUCTURE`

- Capture whether the learner identified coefficient or constant term correctly
  and kept like-term judgments structural.

### `STEP-U3-S3-SUBSTITUTE-WITH-STRUCTURE`

- Capture whether the learner preserved sign, exponent, reciprocal, and
  grouping structure after substitution.

### `STEP-U3-S4-COMBINE-LIKE-TERMS`

- Capture whether the learner removed parentheses safely and combined only like
  terms.

### `STEP-U3-S5-MODEL-THEN-SIMPLIFY`

- Capture whether the learner built the expression from the situation first and
  only then simplified it.
