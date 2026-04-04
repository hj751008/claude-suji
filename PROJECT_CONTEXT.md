# Project Context

## Project Purpose
Build a Korean middle school math learning AI with strong math accuracy, honest validation, and curriculum-grounded behavior.

## Current Structure
- `app/`: application code
- `docs/`: project docs and session records
- `.agents/skills/`: repository-local agent workflows

## Source of Truth
- Repository docs in `docs/`
- Explicit curriculum/reference materials checked into the project
- Approved thresholds and rules documented in the repo

## Current App State
- `app/` now includes a schema-first Unit 1 runtime with content validation, learner summary, prerequisite-aware recommendations, session payload generation, session runner logic, and learner-record persistence
- The current CLI operator loop reaches `start-learning-session -> run-learning-turn`, so a tutor can open or resume a session, submit an observation, and immediately see the next step or next recommendation
- The runtime is still intentionally conservative: mastery thresholds, pass labels, and scoring cutoffs remain provisional or undecided unless approved in `docs/`
- The current runnable flow reaches `learner_record -> activeSession -> observation submission -> learner summary/recommendation refresh`, and the runtime now includes Unit 1, Unit 2 `정수와 유리수`, and Unit 3 `문자의 사용과 식`
- `app/content/unit2-scaffold/` and `app/content/unit3-scaffold/` are now runtime-loaded with source-backed `provisional` skills, teaching records, and conservative prerequisite links
- Replay-ready Unit 3 transcript fixtures now include approved notes-only completion paths for `U3-S2`, `U3-S4`, and `U3-S5`, while broader mastery thresholds and prerequisite expansion remain intentionally undecided

## Next Priorities
1. Keep Unit 3 `문자의 사용과 식` evidence-backed and conservative now that notes-only completion is approved for `U3-S2`, `U3-S4`, and `U3-S5`
2. Keep extending Unit 2 `정수와 유리수` from source-backed `provisional` records into stronger prerequisite, transcript-evidence, and harness-backed coverage
3. Expand failure-path validation for malformed learner/session state, not just happy-path harness cases

## Auto-Managed Unit Pipeline
<!-- AUTO-MANAGED-UNIT-PIPELINE START -->
<!-- UNIT:U2 START -->
### U2 `정수와 유리수`
- Slug: `unit2-scaffold`
- English label: `Integers and Rational Numbers`
- Auto-managed stage: `runtime-gate-passed`
<!-- UNIT:U2 END -->

<!-- UNIT:U3 START -->
### U3 `문자의 사용과 식`
- Slug: `unit3-scaffold`
- English label: `Using Variables and Expressions`
- Auto-managed stage: `runtime-gate-passed`
<!-- UNIT:U3 END -->
<!-- AUTO-MANAGED-UNIT-PIPELINE END -->
