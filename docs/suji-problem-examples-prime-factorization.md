# Suji Problem Examples: Prime Factorization

## Purpose
This document gives short, practical problem examples for Suji's Unit 1 `소인수분해` flow.

It is aligned with:
- `docs/suji-subskills-prime-factorization.md`
- `docs/suji-error-patterns-prime-factorization.md`
- `docs/suji-tutor-dialogue-flow-prime-factorization.md`

It is tailored to Suji's current difficulty profile:
- weak starting point
- weak mixed-concept handling
- unstable procedure
- weak application confidence

This document does not define curriculum codes, numeric mastery thresholds, or scoring cutoffs.

## Examples

### Example 1
- Stage:
  - `S1 Quick Diagnosis`
- Target subskill:
  - tell whether a number is prime, composite, or neither
- Problem prompt:
  - "다음 수를 소수, 합성수, 어느 것도 아님으로 나누어 보자: `1, 2, 9, 11`"
- What this problem diagnoses or trains:
  - checks `1` handling and whether Suji uses divisor-based classification
- Likely mistake to watch for:
  - calls `1` a prime number or labels all odd numbers prime
- Which tutor dialogue flow it connects to:
  - `S1 Concept Check: prime, composite, or neither`

### Example 2
- Stage:
  - `S1 Quick Diagnosis`
- Target subskill:
  - separate prime/composite/divisor/multiple language
- Problem prompt:
  - "다음 말 중 옳지 않은 것을 고르자: `1은 소수이다`, `소수는 약수가 2개이다`, `9는 합성수이다`"
- What this problem diagnoses or trains:
  - checks whether Suji can read concept language before starting procedure work
- Likely mistake to watch for:
  - chooses by word familiarity instead of checking the definition
- Which tutor dialogue flow it connects to:
  - `S1 Vocabulary Repair: factor, prime factor, divisor, multiple`

### Example 3
- Stage:
  - `S2 Basic Entry`
- Target subskill:
  - list all prime factors without stopping too early
- Problem prompt:
  - "`18`의 소인수를 모두 찾아 보자."
- What this problem diagnoses or trains:
  - checks whether Suji can continue beyond the first factor split
- Likely mistake to watch for:
  - stops at `2 x 9` or gives only part of the prime factors
- Which tutor dialogue flow it connects to:
  - `S2 Continuation Flow: keep splitting until all factors are prime`

### Example 4
- Stage:
  - `S2 Basic Entry`
- Target subskill:
  - find a divisor pair for a given number
- Problem prompt:
  - "`24`를 소인수분해하기 전, 먼저 어떤 수로 나누고 싶은지 말해 보자."
- What this problem diagnoses or trains:
  - trains Suji to start from an accessible first step instead of freezing
- Likely mistake to watch for:
  - cannot choose a starting split or picks one without reason
- Which tutor dialogue flow it connects to:
  - `S2 Entry Flow: starting with a divisor pair`

### Example 5
- Stage:
  - `S2 Basic Entry`
- Target subskill:
  - notice when a listed factor is still composite
- Problem prompt:
  - "다음 중 소인수분해가 끝난 것을 모두 고르자: `2 x 6`, `2 x 2 x 3`, `3 x 4`"
- What this problem diagnoses or trains:
  - checks whether Suji can tell prime factorization from ordinary factorization
- Likely mistake to watch for:
  - accepts `2 x 6` or `3 x 4` as finished answers
- Which tutor dialogue flow it connects to:
  - `S2 Continuation Flow: keep splitting until all factors are prime`

### Example 6
- Stage:
  - `S3 Expression Stabilization`
- Target subskill:
  - rewrite the final result using only prime numbers
- Problem prompt:
  - "`36`을 두 가지 방법으로 나눈 뒤, 마지막 답을 한 줄로 다시 써 보자."
- What this problem diagnoses or trains:
  - separates split-work from the final clean expression
- Likely mistake to watch for:
  - copies the branch work directly or leaves a composite factor
- Which tutor dialogue flow it connects to:
  - `S3 Expression Flow: rewrite the final answer cleanly`

### Example 7
- Stage:
  - `S3 Expression Stabilization`
- Target subskill:
  - recognize that different split orders can lead to the same final factorization
- Problem prompt:
  - "다음 두 답이 같은지 비교해 보자: `2 x 2 x 3`, `3 x 2 x 2`"
- What this problem diagnoses or trains:
  - trains Suji to compare factor structure instead of visual order
- Likely mistake to watch for:
  - says the answers are different because the order is different
- Which tutor dialogue flow it connects to:
  - `S3 Comparison Flow: same answer from different split paths`

### Example 8
- Stage:
  - `S3 Expression Stabilization`
- Target subskill:
  - move from split-work to final expression without dropping a factor
- Problem prompt:
  - "`60`의 소인수분해를 마친 뒤, 빠진 인수가 없는지 다시 써 보자."
- What this problem diagnoses or trains:
  - checks whether Suji can rewrite the final answer without omission
- Likely mistake to watch for:
  - drops one factor during final cleanup
- Which tutor dialogue flow it connects to:
  - `S3 Expression Flow: rewrite the final answer cleanly`

### Example 9
- Stage:
  - `S4 Verification Habit`
- Target subskill:
  - compare two candidate answers and decide which is complete
- Problem prompt:
  - "`12`의 소인수분해 답으로 `2 x 6`과 `2 x 2 x 3`이 있다. 어느 쪽이 맞는지 이유와 함께 말해 보자."
- What this problem diagnoses or trains:
  - trains full checking instead of product-only checking
- Likely mistake to watch for:
  - accepts `2 x 6` because it multiplies to `12`
- Which tutor dialogue flow it connects to:
  - `S4 Verification Flow: check if the answer is really complete`

### Example 10
- Stage:
  - `S4 Verification Habit`
- Target subskill:
  - check whether any prime factor is missing
- Problem prompt:
  - "`18 = 2 x 3`이라고 한 답이 왜 부족한지 설명해 보자."
- What this problem diagnoses or trains:
  - makes missing-factor checking explicit
- Likely mistake to watch for:
  - says the answer is almost right, so acceptable
- Which tutor dialogue flow it connects to:
  - `S4 Verification Flow: check if the answer is really complete`

### Example 11
- Stage:
  - `S4 Verification Habit`
- Target subskill:
  - check whether every factor is prime and back-check when needed
- Problem prompt:
  - "다음 순서로 스스로 점검해 보자: 소수만 있는가, 빠진 것은 없는가, 원래 수로 다시 맞는가."
- What this problem diagnoses or trains:
  - builds a reusable self-check routine
- Likely mistake to watch for:
  - checks only one condition and stops
- Which tutor dialogue flow it connects to:
  - `S4 Back-Check Flow: product check without overload`

### Example 12
- Stage:
  - `S5 Transfer Practice`
- Target subskill:
  - use prime factorization to think about divisor count
- Problem prompt:
  - "`24 = 2 x 2 x 2 x 3`을 보고, 약수의 개수를 생각할 때 무엇부터 적으면 좋을지 말해 보자."
- What this problem diagnoses or trains:
  - checks whether Suji can reuse factorization instead of restarting from scratch
- Likely mistake to watch for:
  - starts listing divisors one by one and gets lost
- Which tutor dialogue flow it connects to:
  - `S5 Transfer Flow: divisor-count application`

### Example 13
- Stage:
  - `S5 Transfer Practice`
- Target subskill:
  - use prime factorization to decide what to multiply for a square number
- Problem prompt:
  - "`18`에 어떤 수를 곱하면 제곱수가 되는지 구해 보자."
- What this problem diagnoses or trains:
  - trains Suji to look for the missing factor from prime-factor counts
- Likely mistake to watch for:
  - guesses a multiplier randomly
- Which tutor dialogue flow it connects to:
  - `S5 Transfer Flow: making a square number`

### Example 14
- Stage:
  - `S5 Transfer Practice`
- Target subskill:
  - use factor structure when comparing common divisors or common multiples
- Problem prompt:
  - "`12`와 `18`이 함께 있을 때, 지금 찾는 것이 공약수 쪽인지 공배수 쪽인지 먼저 말해 보자."
- What this problem diagnoses or trains:
  - reduces mixed-concept overload before actual calculation
- Likely mistake to watch for:
  - mixes up GCD and LCM from the start
- Which tutor dialogue flow it connects to:
  - `S5 Transfer Flow: common divisor or common multiple confusion`

## Use Notes
- Start with one small example, not a mixed set.
- If Suji freezes, step back to the previous stage instead of adding more explanation.
- Prefer examples where Suji can explain one reason, not only give one answer.
- Stop after one stable success and move on before confidence drops again.
