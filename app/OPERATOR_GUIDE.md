# Operator Guide

This is the shortest practical CLI loop for the current Unit 1 tutor runtime.

## 1. Open or Resume a Session

```bash
python app/cli.py start-learning-session --learner app/domain/evidence/learner-record-with-summary.example.json
```

Read the returned `sessionStartGuide`.

- `openingLine`: how to start the turn
- `firstTutorQuestion`: the first question to ask
- `smallHint`: the next small nudge if the learner stalls
- `goodStoppingPoint`: what counts as enough progress for the step
- `watchFor`: common failure patterns to listen for

If the learner already has a resumable session, this command reuses it.
If not, it plans a new session from the latest recommendations and stores it as `activeSession`.

## 2. Record One Learner Turn

```bash
python app/cli.py prepare-observation-form --learner app/domain/evidence/learner-record-with-live-session.example.json
python app/cli.py run-learning-turn --learner app/domain/evidence/learner-record-with-live-session.example.json --input app/domain/evidence/observation-form-step-u1-s2.example.json
```

`prepare-observation-form` returns a strict draft built only from the current
`activeSession.currentStep` and the documented observation-form mapping. It
does not invent fields or prompts. If the mapping is missing, it should fail.

Then fill the returned `observationForm` and pass it to `run-learning-turn`.
Read the returned `turnSummary`.

If the tutor writes a clear learner response but is unsure about the checkboxes,
it is acceptable to leave `fieldValues` conservative and rely on the documented
text cues for a cautious evaluation.

- `decision`: how the evaluator judged the submitted observation
- `sessionStatus`: whether the session is still `in_progress` or now `completed`
- `nextAction`: what the operator should do next

Sample replayable tutor logs live in
`app/domain/evidence/unit1-tutor-transcripts.example.json`. Each transcript keeps
short tutor/learner dialogue snippets together with the exact
`observationFormInput` that the harness replays from
`app/harness/learning_turn_cases.json`.

To replay one sample log directly through the CLI:

```bash
python app/cli.py list-transcripts --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json
python app/cli.py list-transcripts --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --tag transfer
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s5a-divisor-count-ko-text-only-active-session
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s2-s3-bilingual-text-only-planned-session --turn-limit 1 --summary-only
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s5a-divisor-count-ko-text-only-active-session --summary-only
```

This replays each recorded `observationFormInput` through the same
`run-learning-turn` path and returns per-turn summaries plus the final learner
record state. With `--summary-only`, it omits the final learner record and keeps
the output short for quick regression checks. `list-transcripts` can also filter
by `skillId` or `tag`, and `--turn-limit` lets you replay only the first few
turns of a longer sample.

Current Unit 1 transcript coverage:

- `U1-S2`: successful entry move from evenness clue
- `U1-S3`: successful clean rewrite, plus `needs_follow_up` when a repeated factor is dropped
- `U1-S4`: successful prime-first verification, plus `uncertain` when the learner checks only the product
- `U1-S5A`: successful divisor-count reuse of factorization, plus `uncertain` when the learner restarts by listing divisors
- `U1-S5B`: successful square-number missing-factor explanation, plus `uncertain` when the learner guesses a multiplier
- `U1-S5C`: successful GCD/LCM structure sort, plus `uncertain` when the learner calculates before naming the structure
- `U1-S5D`: successful relevant-part explanation, plus `uncertain` when the learner does not identify a useful part

These transcript fixtures are regression examples for the current runtime, not
claims of final mastery policy.

Current Unit 2 transcript coverage:

- `U2-S1`: successful category sorting, plus `uncertain` when zero is treated as positive
- `U2-S2`: successful number-line ordering, plus `uncertain` when negative order is reversed by absolute value
- `U2-S3`: successful absolute-value distance explanation, plus `uncertain` when the learner keeps the negative sign
- `U2-S4`: successful signed-change direction tracking, plus `uncertain` when sign or direction is flipped
- `U2-S5`: successful sign-first expression reading, plus `uncertain` when the learner flattens structure too early

These transcript fixtures are regression examples for the current runtime, not
claims of final mastery policy.

## 3. Follow the Next Action

If `nextAction` is `continue_active_session`:

- stay in the same session
- use `nextStepGuide`
- ask the next `firstTutorQuestion`

If `nextAction` is `review_next_recommendation`:

- the previous session is complete
- review `nextRecommendedSession`
- start a new session when ready

Interpret the recommendation handoff fields as:

- `plannedFromSkillId`: why this next session was recommended
- `recommendedNextSkillIds`: conservative blocker-first skill chain for the next session
- `firstStepSkillId`: the skill of the first step the runtime will actually open
- `sessionTargetSkillId`: the session target stored on the new active session after `start-learning-session`

## 4. Write Back to File When Needed

To persist the updated learner record:

```bash
python app/cli.py start-learning-session --learner <learner-record.json> --write
python app/cli.py prepare-observation-form --learner <learner-record.json> --output <observation-form.json>
python app/cli.py run-learning-turn --learner <learner-record.json> --input <observation-form.json> --write
```

## 5. Optional Local Operator UI

If you want to inspect the same transcript replay and handoff flow in a browser,
run:

```bash
python app/cli.py serve-operator-ui
```

Then open `http://127.0.0.1:8765`.

This local UI does not replace the CLI or harness. It is only a thin
inspection surface over the same runtime paths:

- load one of three quick pilot presets for the first real operator runs
- replay a transcript fixture
- inspect `plannedFromSkillId`, `recommendedNextSkillIds`, `firstStepSkillId`
- start the next session from the current learner state
- prepare and submit one observation form turn without writing files
- export the current operator run as JSON
- save a raw pilot log bundle to `output/operator-logs/`

## Guardrails

- The runtime remains conservative. `completed` means a step rubric was satisfied, not that unit mastery is officially approved.
- `ready_for_next_step` supports the next guided step only. It is not a final mastered label.
- Recommendations and summaries still use `limited` confidence until stronger ranking and threshold rules are approved in `docs/`.
- If a learner response feels mathematically ambiguous, prefer a cautious observation form over forcing auto-completion.
