# Unit 1 Closeout Checklist (2026-04-05)

## Purpose

- This checklist records whether `Unit 1` currently satisfies the agreed first-public-result definition.
- It is scoped to the current `Unit 1` package only.
- It does not approve `Unit 2` or `Unit 3` for the same public claim.

## Done Definition Reference

- The agreed `Unit 1` done definition is:
  - live demo landing, `/unit1`, and `/unit1/proof` are stable in production
  - the `Unit 1` claim is explained honestly on the proof page
  - `Unit 1` browser QA and route-level review are complete for the current public surface
  - `Unit 1` can be shown as the first public result
  - no later unit is part of the current public surface claim

## Current Checklist

### Public Surface Stability

- [x] Production landing `/` is live and reachable
- [x] Production `/unit1` is live and reachable
- [x] Production `/unit1/proof` is live and reachable
- [x] The current production demo stays centered on `Unit 1`
- [x] `Unit 2` and `Unit 3` are not part of the current public route claim

### Honest Product Claim

- [x] The landing page presents `Unit 1` as the first result, not the full product
- [x] The proof page separates confirmed facts from current limits
- [x] The proof page states the later-unit expansion gate explicitly
- [x] The current copy does not claim broad classroom validation
- [x] The current copy does not claim finalized mastery scoring

### Validation And QA

- [x] `python app/cli.py validate-content` passes in the main repo
- [x] `PYTHONPATH=.` + `python app/harness/run_harness.py` passes in the main repo
- [x] Browser QA has been run against the current production demo
- [x] Current production browser QA confirmed `/` and `/unit1/proof` without console errors
- [x] A fresh browser QA confirmation for `/unit1` after the latest deploy is recorded in this checklist

### Unit 1 Demo Readiness

- [x] `Unit 1` can be shown as a first public result
- [x] The public story now closes through `landing -> unit1/proof`
- [x] The current demo reflects a proof-first scope instead of a multi-unit promise
- [x] A curated screenshot or OG/share asset set is finalized for external sharing

## Current Assessment

- `Unit 1` is effectively ready as the first public result for a proof-first demo.
- The main remaining gaps are presentation-closeout tasks, not core runtime credibility gaps.
- The current verification set now includes:
  - `python app/cli.py validate-content` pass on 2026-04-05
  - `PYTHONPATH=.` + `python app/harness/run_harness.py` pass on 2026-04-05
  - production browser confirmation for `/`, `/unit1`, and `/unit1/proof`
- The current curated share set now includes:
  - `home-desktop`
  - `home-mobile`
  - `unit1-desktop`
  - `proof-desktop`
  - live `/opengraph-image` social preview asset
- `qa-snapshots/` remains the broader local capture area, while
  `share-assets/unit1/` is the current share-ready handoff set.
- `Unit 1` no longer has a required presentation-closeout blocker for the current
  milestone.

## Background Work Rule

- Background work on `Unit 2` or `Unit 3` is allowed only when:
  - it does not change the current `Unit 1` public claim
  - it does not widen the current demo surface
  - it does not silently alter shared policy in a way that changes the `Unit 1` result
- Good background work:
  - `Unit 2` transcript fixtures
  - `Unit 2` harness additions
  - failure-path validation
- Not good background work during `Unit 1` closeout:
  - adding later units to the public demo
  - rewriting the public story away from `Unit 1 first`
  - broadening scoring or mastery claims without explicit approval
