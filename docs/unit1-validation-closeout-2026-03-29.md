# Unit 1 Validation Closeout (2026-03-29)

## Status

- Unit 1 is `runtime-complete`.
- Unit 1 is `pilot-validated for transcript fixture realism at provisional
  house-format level`.
- Unit 1 is not fully broad field-validated across many operators or many live
  sessions.

## Confirmed Scope

### 1. Content and runtime validation

- `python app/cli.py validate-content` has passed after the Unit 1 transcript,
  rubric, and handoff changes.
- `python -m app.harness.run_harness` has passed after the same changes.
- The harness currently covers:
  - evaluator cases
  - learning-turn cases
  - prepare-observation-form cases
  - session-planner cases
  - session-orchestrator cases
  - start-learning-session cases
  - learner-summary and learner-record accumulation cases

### 2. Transcript-backed regression coverage

- Unit 1 success-path transcript replay exists for:
  - `U1-S2`
  - `U1-S3`
  - `U1-S4`
  - `U1-S5A`
  - `U1-S5B`
  - `U1-S5C`
  - `U1-S5D`
- Unit 1 failure or conservative-path transcript replay exists for:
  - `U1-S3 needs_follow_up`
  - `U1-S4 uncertain`
  - `U1-S5A uncertain`
  - `U1-S5B uncertain`
  - `U1-S5C uncertain`
  - `U1-S5D uncertain`

### 3. Recommendation and handoff validation

- Recommendation policy remains unchanged.
- The runtime still uses `plannedFromSkillId` plus blocker-first step planning.
- The current output split is visible in CLI and the local operator UI:
  - `plannedFromSkillId`
  - `recommendedNextSkillIds`
  - `firstStepSkillId`
  - `sessionTargetSkillId`
  - `currentStepSkillId`
- Blocker-first reopen was verified through transfer cases, including:
  - `U1-S5A`
  - `U1-S5B`
  - `U1-S5C`
  - `U1-S5D`

### 4. Local operator UI validation

- A local operator QA surface exists and is runnable through:
  - `python app/cli.py serve-operator-ui`
- The UI supports:
  - transcript replay
  - start-learning-session handoff inspection
  - observation-form refresh
  - single-turn submission
  - raw pilot-log export and save
- Quick pilot presets exist for:
  - `Pilot A`
  - `Pilot B`

### 5. Real pilot-log comparison

- Real pilot logs were saved to `output/operator-logs/`.
- Replay and handoff shape were confirmed by real pilot runs.
- A later pilot run also confirmed live Step 3 logging with:
  - Korean math-relevant learner response
  - non-empty tutor note
  - conservative checkbox values
- A separate later pilot run confirmed non-`S5A` live Step 3 logging on
  `U1-S5C` with:
  - Korean math-relevant learner response
  - conservative checkbox values
  - the same blocker-first reopen shape
- Comparison result:
  - the current transcript fixture style is realistic enough to keep as the
    provisional house format
  - the examples may still be slightly more polished than natural operator text

## Confirmed Limits

- The current real pilot evidence is still narrow.
- The strongest live tutor-note evidence is still from the `U1-S5A`
  blocker-first reopen path.
- Non-`S5A` live learner-response evidence now exists from `U1-S5C`, but that
  pilot did not include a tutor note.
- Pilot-note freeform commentary is still weak because preset note text was not
  meaningfully edited during the pilot runs.
- This closeout does not claim broad production or classroom validation.

## Decision

- Keep the current Unit 1 transcript fixture format.
- Keep the current recommendation policy.
- Treat Unit 1 validation as closed for the current engineering milestone.
- Keep field-confidence language conservative in docs and discussion.

## Recommended Next Work

1. If desired, add one more live pilot with a non-empty tutor note on a
   non-`S5A` path such as `S2-S4` or `S5C`.
2. Start the next unit or next risk area without reopening Unit 1 policy by
   default.
3. Revisit transcript example tone only if later live logs repeatedly show a
   much shorter or noisier operator style.
