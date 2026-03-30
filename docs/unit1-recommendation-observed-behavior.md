# Unit 1 Recommendation Observed Behavior

This document records observed recommendation outputs from the current runtime.

It is not a policy document and does not claim that the current recommendation
behavior is correct. It only records what the code returned when the listed
sample transcripts were replayed.

## Commands Used

```bash
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s2-s3-bilingual-text-only-planned-session --summary-only
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s4-verify-ko-text-only-active-session --summary-only
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s5a-divisor-count-ko-text-only-active-session --summary-only
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s5b-square-number-ko-text-only-active-session --summary-only
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s5c-gcd-lcm-ko-text-only-active-session --summary-only
python app/cli.py replay-transcript --transcript-file app/domain/evidence/unit1-tutor-transcripts.example.json --transcript-id u1-s5d-relevant-part-ko-text-only-active-session --summary-only
```

## Observed Outputs

| Completed transcript | Final submitted step | Next action | Observed next recommended target skill | Observed first lesson step |
| --- | --- | --- | --- | --- |
| `u1-s2-s3-bilingual-text-only-planned-session` | `STEP-U1-S3-REWRITE-CLEANLY` | `review_next_recommendation` | `U1-S2` | `STEP-U1-S1-CONCEPT-CHECK` |
| `u1-s4-verify-ko-text-only-active-session` | `STEP-U1-S4-VERIFY-PRIME-FIRST` | `review_next_recommendation` | `U1-S3` | `STEP-U1-S2-ENTRY-BRIDGE` |
| `u1-s5a-divisor-count-ko-text-only-active-session` | `STEP-U1-S5A-DIVISOR-COUNT-TRANSFER` | `review_next_recommendation` | `U1-S5A` | `STEP-U1-S3-REWRITE-CLEANLY` |
| `u1-s5b-square-number-ko-text-only-active-session` | `STEP-U1-S5B-SQUARE-NUMBER` | `review_next_recommendation` | `U1-S5B` | `STEP-U1-S3-REWRITE-CLEANLY` |
| `u1-s5c-gcd-lcm-ko-text-only-active-session` | `STEP-U1-S5C-GCD-LCM-SORT` | `review_next_recommendation` | `U1-S5C` | `STEP-U1-S3-REWRITE-CLEANLY` |
| `u1-s5d-relevant-part-ko-text-only-active-session` | `STEP-U1-S5D-RELEVANT-PART-EXPLAIN` | `review_next_recommendation` | `U1-S5D` | `STEP-U1-S3-REWRITE-CLEANLY` |

## Narrow Factual Notes

- After the `U1-S2` + `U1-S3` planned session finishes, the runtime recommends a new session whose target skill is `U1-S2`, starting from `STEP-U1-S1-CONCEPT-CHECK`.
- After the `U1-S4` verification sample finishes, the runtime recommends a new session whose target skill is `U1-S3`, starting from `STEP-U1-S2-ENTRY-BRIDGE`.
- After the `U1-S5A`, `U1-S5B`, `U1-S5C`, and `U1-S5D` transfer samples finish, the runtime recommends another session for the same target skill, and the first step observed in each case is `STEP-U1-S3-REWRITE-CLEANLY`.
- This document does not judge whether those loops are desirable. It only records the observed outputs from the current code.

## Verified Handoff Coverage

The current harness now verifies the following recommendation handoff paths:

- completed `U1-S5A` transcript -> `plan_next_session`
- completed `U1-S5A` transcript -> `resume_or_plan_session`
- completed `U1-S5A` transcript -> `start_learning_session`
- completed `U1-S5A` transcript -> `start_learning_session` -> `prepare_observation_form`
- completed `U1-S5A` transcript -> `start_learning_session` -> submit blocker-first `U1-S3` step
- completed `U1-S5A` transcript -> complete blocker-first session -> next recommendation reorders to `U1-S3`
- completed `U1-S5B` transcript -> `plan_next_session`
- completed `U1-S5B` transcript -> `resume_or_plan_session`
- completed `U1-S5B` transcript -> `start_learning_session`
- completed `U1-S5B` transcript -> `start_learning_session` -> `prepare_observation_form`
- completed `U1-S5B` transcript -> `start_learning_session` -> submit blocker-first `U1-S3` step
- completed `U1-S5B` transcript -> complete blocker-first session -> next recommendation reorders to `U1-S3`
- completed `U1-S5C` transcript -> `plan_next_session`
- completed `U1-S5C` transcript -> `resume_or_plan_session`
- completed `U1-S5C` transcript -> `start_learning_session`
- completed `U1-S5C` transcript -> `start_learning_session` -> `prepare_observation_form`
- completed `U1-S5C` transcript -> `start_learning_session` -> submit blocker-first `U1-S3` step
- completed `U1-S5C` transcript -> complete blocker-first session -> next recommendation reorders to `U1-S3`
- completed `U1-S5D` transcript -> `plan_next_session`
- completed `U1-S5D` transcript -> `resume_or_plan_session`
- completed `U1-S5D` transcript -> `start_learning_session`
- completed `U1-S5D` transcript -> `start_learning_session` -> `prepare_observation_form`
- completed `U1-S5D` transcript -> `start_learning_session` -> submit blocker-first `U1-S3` step
- completed `U1-S5D` transcript -> complete blocker-first session -> next recommendation reorders to `U1-S3`

These checks verify the field split below in live code paths:

- `plannedFromSkillId`: recommended session origin
- `recommendedNextSkillIds`: blocker-first next-skill chain
- `firstStepSkillId`: first skill the next session actually opens
- `sessionTargetSkillId`: target skill stored on the opened active session

## Verified Accumulation Notes

- Re-merging the same `session-state-with-history.example.json` snapshot into an empty learner record keeps `sessions[]` at `1` and keeps `evidenceEvents[]` at `1`.
- Completing `U1-S5A`, then reopening blocker-first and completing `U1-S3 -> U1-S5A`, leaves `sessions[]` at `2`.
- In that `U1-S5A` repeated-target path, the two stored sessions share the same `targetSkillId` (`U1-S5A`) but differ in step sequence, so both snapshots are retained.
- In that same path, `latestSkillSummaries` ends with `U1-S3` supported by `1` event and `U1-S5A` supported by `2` events.
- In that same path, `latestRecommendations` ends with `U1-S3 -> [U1-S2, U1-S3]` and `U1-S5A -> [U1-S5A]`.
