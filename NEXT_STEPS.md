# Next Steps

## Current Focus

1. Keep turning `app/content/unit2-scaffold/` into a stronger Unit 2 pack for
   `정수와 유리수` now that skills, teaching records, and conservative
   prerequisites are source-backed `provisional`.
2. Keep Unit 1 stable while expanding failure-path validation around malformed
   learner state and session state.
3. Revisit broader recommendation generalization only after the next unit has
   real content or the planner surface needs to widen.

## Immediate Actions

1. Review whether Unit 2 transcript examples should be converted into
   replay-ready evidence fixtures.
2. Add stronger Unit 2 harness or learner-state coverage once the next
   evidence-fixture slice is chosen.
3. Revisit prerequisite links only if new source-backed evidence justifies
   changes beyond the current conservative subset.

## Auto-Managed Unit Actions
<!-- AUTO-MANAGED-UNIT-ACTIONS START -->
<!-- UNIT:U2 START -->
### U2 `unit2-scaffold`
1. Current stage: `runtime-gate-passed`.
2. Review transcript-evidence and harness follow-up work for Unit 2.
3. Run `python app/cli.py validate-content` after the next meaningful content change.
<!-- UNIT:U2 END -->

<!-- UNIT:U3 START -->
### U3 `unit3-scaffold`
1. Current stage: `source-backed-provisional`.
2. Source-backed provisional records exist. Decide whether runtime wiring, transcript fixtures, and harness coverage should be added next.
3. Run `python app/cli.py validate-content` after the next meaningful content change.
<!-- UNIT:U3 END -->
<!-- AUTO-MANAGED-UNIT-ACTIONS END -->
