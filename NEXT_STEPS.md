# Next Steps

## Current Focus

1. Keep `Unit 1` stable as the first public result now that production routes,
   proof-page claim, share assets, and share metadata are in place.
2. Keep `Unit 2` work in the background only when it does not change the
   current `Unit 1` result or widen the public surface.
3. Keep expanding failure-path validation around malformed learner state and
   session state because that improves the shared engine without changing the
   current `Unit 1` claim.

## Immediate Actions

1. Keep a short regression watch on `/`, `/unit1`, `/unit1/proof`, and
   `/opengraph-image` while avoiding new `Unit 1` scope expansion.
2. Continue low-risk `Unit 2` transcript-evidence, harness, and failure-path
   work behind the stable `Unit 1` front layer.
3. Only revisit `Unit 1` if regression, deploy drift, or share-surface issues
   appear.

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
1. Current stage: `runtime-gate-passed`.
2. Notes-only completion is approved for `U3-S2`, `U3-S4`, and `U3-S5`, while broader prerequisite and cutoff policy stays conservative.
3. Run `python app/cli.py validate-content` after the next meaningful content change.
<!-- UNIT:U3 END -->
<!-- AUTO-MANAGED-UNIT-ACTIONS END -->
