# Suji Error Patterns: Prime Factorization

## Purpose
This document records short, practical error patterns for Suji's Unit 1 `소인수분해` learning flow.

It is based on [docs/suji-subskills-prime-factorization.md](C:/Users/tcikh/OneDrive/문서/codex/sujimathAI/docs/suji-subskills-prime-factorization.md).

It is tailored to Suji's current difficulty profile:
- weak starting point
- weak mixed-concept handling
- unstable procedure
- weak application confidence

This document does not define curriculum codes, numeric mastery thresholds, or scoring cutoffs.

## S1 Quick Diagnosis

### Subskill: tell whether a number is prime, composite, or neither
- Representative errors:
  - calls `1` a prime number
  - calls any odd number prime
  - labels a number from memory without checking divisors
- Likely confusion:
  - weak concept starting point and weak divisor-based reasoning
- First tutor correction question:
  - "이 수의 약수를 끝까지 써 보면 몇 개니?"
- Sign of improvement:
  - Suji checks divisors before naming the number type

### Subskill: recall that `1` is not prime
- Representative errors:
  - says `1` is prime because it is only divisible by `1`
  - says `1` is composite because it is not prime
- Likely confusion:
  - treats number labels as only two choices and does not use the divisor definition carefully
- First tutor correction question:
  - "`1`의 약수는 몇 개이고, 소수는 약수가 몇 개여야 하지?"
- Sign of improvement:
  - Suji can say that `1` is neither prime nor composite with a reason

### Subskill: recognize that a prime number has exactly two divisors
- Representative errors:
  - says a prime number has one divisor
  - says a prime number has no divisors except itself
  - mixes divisor count with factor count language loosely
- Likely confusion:
  - weak definition recall and unstable math language
- First tutor correction question:
  - "소수의 약수 두 개는 어떤 두 수니?"
- Sign of improvement:
  - Suji states both `1` and the number itself without prompting

### Subskill: separate prime/composite/divisor/multiple language
- Representative errors:
  - calls a divisor a prime number
  - treats common factor language as the same as prime-factor language
  - uses factor and multiple interchangeably
- Likely confusion:
  - weak mixed-concept handling at the vocabulary level
- First tutor correction question:
  - "지금 네가 말한 것은 수의 종류야, 아니면 관계 이름이야?"
- Sign of improvement:
  - Suji uses the right word type before attempting the answer

## S2 Basic Entry

### Subskill: find a divisor pair for a given number
- Representative errors:
  - picks numbers that do not multiply to the target
  - starts with a random split and cannot justify it
  - skips easy small divisors and freezes
- Likely confusion:
  - unstable procedure and low confidence starting the first step
- First tutor correction question:
  - "가장 먼저 나눠 볼 쉬운 수는 뭐니?"
- Sign of improvement:
  - Suji starts with a reasonable divisor pair without long hesitation

### Subskill: keep dividing until the remaining factors are all prime
- Representative errors:
  - stops after one split
  - leaves `4`, `6`, `9`, or `10` as if they were final
- Likely confusion:
  - procedural stopping rule is not stable yet
- First tutor correction question:
  - "지금 남은 수들 중에서 아직 더 쪼갤 수 있는 게 있니?"
- Sign of improvement:
  - Suji continues the split without being told the exact next step

### Subskill: list all prime factors without stopping too early
- Representative errors:
  - lists only one or two prime factors
  - misses a repeated prime factor
  - treats "찾은 것" as "모두 찾은 것"
- Likely confusion:
  - incomplete-result blindness and weak verification habit
- First tutor correction question:
  - "빠진 소인수가 없는지 어디를 다시 보면 좋을까?"
- Sign of improvement:
  - Suji checks completeness before saying she is done

### Subskill: notice when a listed factor is still composite
- Representative errors:
  - writes `2 x 6` or `3 x 12` as the final result
  - accepts a mixed prime-composite list
- Likely confusion:
  - mixes ordinary factorization with prime factorization
- First tutor correction question:
  - "이 답에 소수가 아닌 수가 남아 있니?"
- Sign of improvement:
  - Suji spots a composite leftover and fixes it herself

## S3 Expression Stabilization

### Subskill: rewrite the final result using only prime numbers
- Representative errors:
  - copies the factor tree halfway result
  - rewrites using a composite factor
  - omits one factor during cleanup
- Likely confusion:
  - unstable transition from working process to final expression
- First tutor correction question:
  - "마지막 답 줄에는 무엇만 남아 있어야 하지?"
- Sign of improvement:
  - Suji writes one clean final line using only prime factors

### Subskill: group repeated prime factors clearly
- Representative errors:
  - writes repeated factors inconsistently
  - loses track of how many times a prime appears
  - merges unlike factors carelessly
- Likely confusion:
  - weak organization inside the procedure
- First tutor correction question:
  - "같은 소수끼리 먼저 모아서 세어 볼까?"
- Sign of improvement:
  - Suji can count repeated prime factors reliably

### Subskill: move from split-work to final expression without dropping a factor
- Representative errors:
  - one branch of the split disappears
  - the final answer has fewer factors than the work above
- Likely confusion:
  - attention loss during rewrite and unstable procedural closure
- First tutor correction question:
  - "위에서 나온 소수를 아래 답에 하나씩 모두 옮겼니?"
- Sign of improvement:
  - Suji checks branch-by-branch when rewriting

### Subskill: recognize that different split orders can lead to the same final factorization
- Representative errors:
  - says two students got different answers because they started differently
  - distrusts her own answer when the split path changes
- Likely confusion:
  - overfocus on procedure appearance instead of final factor structure
- First tutor correction question:
  - "두 답에 들어 있는 소수 종류와 개수는 같니?"
- Sign of improvement:
  - Suji compares final prime sets instead of the split order

## S4 Verification Habit

### Subskill: check whether every factor in the answer is prime
- Representative errors:
  - only checks whether the product matches
  - misses a composite factor hiding in the answer
- Likely confusion:
  - verification is too narrow and product-only
- First tutor correction question:
  - "곱하기 전에, 먼저 각 인수가 소수인지 볼까?"
- Sign of improvement:
  - Suji checks primality before checking the product

### Subskill: check whether any prime factor is missing
- Representative errors:
  - accepts `2 x 3` when `2 x 2 x 3` is needed
  - thinks "almost right" means correct
- Likely confusion:
  - weak completeness check and weak confidence in careful checking
- First tutor correction question:
  - "원래 수를 만들려면 같은 소수가 한 번 더 필요한 건 없니?"
- Sign of improvement:
  - Suji can explain why an answer is incomplete, not just say it is wrong

### Subskill: compare two candidate answers and decide which is complete
- Representative errors:
  - chooses the shorter answer because it looks simpler
  - cannot explain why one answer is incomplete
- Likely confusion:
  - surface-level judging instead of structural checking
- First tutor correction question:
  - "두 답을 각각 원래 수와 연결해 보면 어느 쪽이 빠짐이 없니?"
- Sign of improvement:
  - Suji gives a reasoned choice between two similar answers

### Subskill: multiply back or reason back to the original number when needed
- Representative errors:
  - avoids checking because it feels like extra work
  - multiplies back incorrectly and loses confidence
- Likely confusion:
  - low application confidence inside verification
- First tutor correction question:
  - "전부 다 계산하지 않아도, 원래 수와 맞는지 어떤 부분부터 확인할 수 있을까?"
- Sign of improvement:
  - Suji uses a simple back-check without waiting for reassurance

## S5 Transfer Practice

### Subskill: use prime factorization to think about divisor count
- Representative errors:
  - starts listing divisors one by one and gets lost
  - mixes prime factors with divisors themselves
- Likely confusion:
  - weak transfer from factorization to a new task structure
- First tutor correction question:
  - "이 문제에서 필요한 건 소인수 자체니, 약수의 개수니?"
- Sign of improvement:
  - Suji starts from the factorization instead of restarting from scratch

### Subskill: use prime factorization to decide what to multiply for a square number
- Representative errors:
  - multiplies by a random factor
  - adds an already even exponent incorrectly
  - focuses on the final number shape instead of the missing factor
- Likely confusion:
  - weak link between factor counts and square structure
- First tutor correction question:
  - "어떤 소수의 개수가 지금 홀수라서 하나 더 필요하니?"
- Sign of improvement:
  - Suji identifies the missing factor from the prime factorization

### Subskill: use factor structure when comparing common divisors or common multiples
- Representative errors:
  - mixes GCD and LCM ideas
  - looks at only one number's factorization
  - treats any shared factor as the full answer
- Likely confusion:
  - mixed-concept overload in application tasks
- First tutor correction question:
  - "지금 찾는 건 공통으로 들어가는 쪽이니, 모두를 덮는 쪽이니?"
- Sign of improvement:
  - Suji can name whether she is looking for shared structure or covering structure first

### Subskill: explain which part of the factorization matters for the new question
- Representative errors:
  - cannot say why prime factorization helps
  - uses the factorization but not the relevant part
  - waits for the tutor to name the method
- Likely confusion:
  - weak application confidence and weak problem framing
- First tutor correction question:
  - "이 문제에서 소인수분해 결과 중 무엇을 쓰면 바로 도움이 될까?"
- Sign of improvement:
  - Suji can point to the relevant part of the factorization before solving
