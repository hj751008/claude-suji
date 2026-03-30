# Unit 1 Real Log Comparison (2026-03-28)

## Purpose

Compare the first two real pilot logs from the local operator UI against the
current Unit 1 transcript fixture style.

## Inputs

- Raw log file:
  - `output/operator-logs/operator-log-u1-s2-s3-bilingual-text-only-planned-session-20260328145133-2026-03-28T14-51-33-864Z.json`
  - `output/operator-logs/operator-log-u1-s5a-divisor-count-ko-text-only-active-session-20260328145219-2026-03-28T14-52-19-192Z.json`
  - `output/operator-logs/operator-log-u1-s5a-divisor-count-ko-text-only-active-session-20260328145811-2026-03-28T14-58-11-460Z.json`
  - `output/operator-logs/operator-log-u1-s5a-divisor-count-ko-text-only-active-session-20260328150405-2026-03-28T15-04-05-942Z.json`
  - `output/operator-logs/operator-log-u1-s5c-gcd-lcm-ko-text-only-active-session-20260328151200-2026-03-28T15-12-00-880Z.json`
- Compared transcript fixture:
  - `app/domain/evidence/unit1-tutor-transcripts.example.json`
- Reviewer:
  - Codex
- Date:
  - 2026-03-28

## Comparison A

### 1. Session Shape

- The real run followed the same high-level flow as the fixture:
  - transcript replay
  - next-session handoff
- The run did not include observation-form turn submission.

### 2. Logging Granularity

- The saved log captured:
  - selected transcript id
  - replay result payload
  - start-learning-session payload
  - prepared observation form payload
- The run did not capture:
  - real operator Step 3 submission
  - short learner quote entered by the operator
  - short tutor note entered by the operator
  - checkbox behavior during a live turn

### 3. Language Style

- The replayed transcript remained bilingual and text-only, which matches the
  fixture.
- The pilot note was still the preset template with no added natural-language
  operator commentary.

### 4. Missing Data

- No live Step 3 operator turn was submitted.
- No natural pilot note content was added.
- This means the run is useful for replay and handoff comparison, but not for
  operator-entry style comparison.

### 5. Useful Match

- `plannedFromSkillId = U1-S2`
- `currentLessonStepId = STEP-U1-S1-CONCEPT-CHECK`
- The replay completed with the same conservative recommendation structure seen
  in the fixture-backed regression cases.

### 6. Mismatch

- The fixture contains example tutor and learner messages for each turn.
- The pilot log did not add new real operator-entered Step 3 content, so there
  is no new evidence yet that the fixture message style matches natural live
  operator notes.

### 7. Decision

- Keep current fixture style as provisional house format.

Reason:

- The pilot confirms that replay and handoff shape are realistic enough to use
  operationally.
- It does not yet confirm that Step 3 turn-entry style is realistic.

## Comparison B

### 1. Session Shape

- The real run followed the same high-level flow as the fixture:
  - transcript replay
  - next-session handoff
- The run did not include observation-form turn submission.

### 2. Logging Granularity

- The saved log captured:
  - selected transcript id
  - replay result payload
  - start-learning-session payload
  - prepared observation form payload
- The run did not capture:
  - live operator turn entry
  - natural tutor note
  - natural learner paraphrase or quote
  - checkbox use in Step 3

### 3. Language Style

- The replayed transcript remained Korean text-only, which matches the fixture.
- The pilot note was still the preset template with no extra operator language.

### 4. Missing Data

- No Step 3 live submission was recorded.
- No pilot-note detail was added.
- This means the run is strong for handoff comparison but weak for comparing
  real operator logging style.

### 5. Useful Match

- `plannedFromSkillId = U1-S5A`
- `recommendedNextSkillIds = [U1-S3, U1-S5A]`
- `currentLessonStepId = STEP-U1-S3-REWRITE-CLEANLY`
- This matches the blocker-first reopen behavior already observed in the
  transcript fixture and harness.

### 6. Mismatch

- The fixture includes one completed transfer turn with learner and tutor text.
- The pilot log stopped before a new live turn was entered, so fixture realism
  for turn-entry style is still unproven.

### 7. Decision

- Keep current fixture style as provisional house format.

Reason:

- The real run supports the fixture's replay and handoff structure.
- It still does not validate the natural shape of live operator Step 3 notes.

## Comparison C

### 1. Session Shape

- The real run followed the full local operator flow:
  - transcript replay
  - next-session handoff
  - observation-form refresh
  - live Step 3 turn submission

### 2. Logging Granularity

- The saved log captured:
  - selected transcript id
  - replay result payload
  - start-learning-session payload
  - prepared observation form payload
  - one live `run-learning-turn` submission
- The live submission contained:
  - learner response text
  - checkbox values
  - no tutor note

### 3. Language Style

- The live learner response was Korean freeform text:
  - `한글도 인식 할 수 있을려나`
- This is a real operator-entered text sample, but it reads like a system check
  rather than a natural math-learning utterance.
- The pilot note remained the preset template with no added natural commentary.

### 4. Missing Data

- The live turn did not include a tutor note.
- The live learner response was not a realistic math-content answer.
- This means the run validates form-capture and evaluation flow, but only
  weakly validates the realism of fixture message style.

### 5. Useful Match

- `plannedFromSkillId = U1-S5A`
- `currentLessonStepId = STEP-U1-S3-REWRITE-CLEANLY`
- The observation form used the expected S3 fields:
  - `uses_only_prime_factors`
  - `keeps_all_factors`
- The submitted turn stayed conservative:
  - `decision = needs_follow_up`
  - `nextAction = continue_active_session`
- This matches the intended cautious tutoring behavior when the operator entry
  is incomplete or not mathematically sufficient.

### 6. Mismatch

- The fixture examples use short math-relevant learner quotes and short tutor
  notes.
- The real live turn used a system-check sentence and left tutor note blank.
- So the fixture format still looks structurally correct, but the current pilot
  does not yet prove that operators naturally write notes in the same style as
  the sample transcript messages.

### 7. Decision

- Keep current fixture style as provisional house format.
- Keep it, but revise examples only if later pilot logs show a consistently
  shorter or noisier operator note style.

Reason:

- The real run confirms that the fixture format is usable through Step 3.
- It does not yet show a strong natural-language match for live educational
  note-taking because the submitted learner text was a test utterance.

## Short Summary

The first two real pilot logs are close enough to the current fixture style for
replay and recommendation handoff. They confirm that the fixture-backed flows
match what an operator actually clicks through in the local UI. They do not yet
validate live Step 3 operator-entry style, because neither pilot included a new
turn submission or natural pilot-note detail. Before final Unit 1 sign-off, at
least one pilot log should include `prepare-observation-form` plus one real
`run-learning-turn` submission.

After the third pilot log, Step 3 submission is now technically validated, but
the content realism is still weak. The current fixture set remains acceptable
for regression and provisional house-format use. Before final Unit 1 sign-off,
at least one additional pilot log should include a mathematically relevant live
learner response and a non-empty tutor note.

## Comparison D

### 1. Session Shape

- The real run followed the full local operator flow:
  - transcript replay
  - next-session handoff
  - observation-form refresh
  - live Step 3 turn submission

### 2. Logging Granularity

- The saved log captured:
  - selected transcript id
  - replay result payload
  - start-learning-session payload
  - prepared observation form payload
  - one live `run-learning-turn` submission
- The live submission contained:
  - math-relevant learner response text
  - checkbox values
  - non-empty tutor note

### 3. Language Style

- The live learner response was a short Korean math explanation:
  - `2 x 2 x 3처럼 소수만 남겨서 다시 써야 해. 2가 하나 더 필요해.`
- The live tutor note was also short and operational:
  - `학습자가 composite factor를 쓰지 말고 누락된 2를 다시 포함해야 한다고 설명함.`
- This is close in style to the current transcript fixture examples:
  - short learner quote
  - short tutor paraphrase
  - conservative checkbox usage

### 4. Missing Data

- The pilot note field still remained the preset template.
- This means the per-turn operator logging style is now validated more strongly
  than the pilot-note commentary style.

### 5. Useful Match

- `plannedFromSkillId = U1-S5A`
- `currentLessonStepId = STEP-U1-S3-REWRITE-CLEANLY`
- The submitted turn used the expected S3 fields:
  - `uses_only_prime_factors = true`
  - `keeps_all_factors = true`
- The submitted turn advanced conservatively and correctly:
  - `decision = completed`
  - `nextAction = continue_active_session`
- This matches the fixture expectation that a short math-relevant utterance plus
  conservative operator signals is enough to move from blocker-first S3 back to
  the original S5A transfer step.

### 6. Mismatch

- The fixture examples are slightly cleaner and more polished than the live
  operator wording.
- The live response and tutor note are shorter and less curated.
- This is a difference in polish, not a format mismatch.

### 7. Decision

- Keep current fixture style as provisional house format.
- Keep the current fixture format itself.
- Minor example-tone adjustment is optional, not required.

Reason:

- The real run now validates both structure and per-turn logging shape.
- The fixture examples are realistic enough for regression use, even if they
  are a bit more polished than live operator text.

## Updated Summary

With the fourth pilot log, the current Unit 1 transcript fixture style is now
supported by real pilot evidence for replay, handoff, observation-form refresh,
and live Step 3 operator entry. The fixture format remains acceptable as the
provisional house format for regression examples. Remaining caution is about
coverage breadth, not basic realism: the strongest live note-style evidence is
currently from the S5A blocker-first reopen path.

## Comparison E

### 1. Session Shape

- The real run followed the full local operator flow:
  - transcript replay
  - next-session handoff
  - observation-form refresh
  - live Step 3 turn submission

### 2. Logging Granularity

- The saved log captured:
  - selected transcript id
  - replay result payload
  - start-learning-session payload
  - prepared observation form payload
  - one live `run-learning-turn` submission
- The live submission contained:
  - math-relevant learner response text
  - checkbox values
  - no tutor note

### 3. Language Style

- The live learner response was a short Korean math explanation:
  - `공배수는 둘 다 담는 쪽이라 먼저 구조를 정하고 계산은 나중에 해야 해.`
- This is close to the fixture style for learner utterances:
  - short
  - concept-first
  - math-relevant
- The tutor-note field remained blank, so tutor-note realism is still stronger
  in `S5A` than in this `S5C` run.

### 4. Missing Data

- No tutor note was entered.
- The pilot note field still remained the preset template.
- This means the run broadens live learner-response evidence more than
  live tutor-note evidence.

### 5. Useful Match

- `plannedFromSkillId = U1-S5C`
- `currentLessonStepId = STEP-U1-S3-REWRITE-CLEANLY`
- The submitted turn used the expected S3 fields:
  - `uses_only_prime_factors = true`
  - `keeps_all_factors = true`
- The submitted turn advanced conservatively and correctly:
  - `decision = completed`
  - `nextAction = continue_active_session`
  - next current step `STEP-U1-S5C-GCD-LCM-SORT`
- This matches the intended blocker-first reopen flow for `U1-S5C`.

### 6. Mismatch

- The fixture examples usually include both learner text and tutor note.
- This live run only validates the learner-text side of that shape.
- So the fixture remains structurally realistic, but tutor-note realism is not
  equally supported across all pilot paths yet.

### 7. Decision

- Keep current fixture style as provisional house format.
- No fixture-format change is needed.

Reason:

- The run adds non-`S5A` live learner-response evidence and confirms the same
  runtime shape on a second transfer branch.
- Remaining weakness is note completeness, not overall format mismatch.
