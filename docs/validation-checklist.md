# Validation Checklist

## Purpose
Define the minimum review checklist before changing mastery, prerequisite, or recommendation logic in sujimathAI. This document exists to keep validation honest and consistent.

## Scope
Use this checklist for:
- mastery rule changes
- prerequisite map changes
- recommendation rule changes

This checklist does not assume automated validation exists unless a repo file explicitly proves it.

## Required Checks Before Logic Changes
- Confirm which source-of-truth document is affected.
- Confirm the change is described in plain language.
- Confirm no undecided rule is being treated as approved.
- Manual check: review affected examples, learner flow assumptions, and related docs.
- Automated check: `UNDECIDED / NOT YET DEFINED IN REPO`

## Document Update Checks
- Update the matching source-of-truth document in the same change.
- If thresholds, relationships, or recommendation rules changed, record that change explicitly.
- If a rule remains unsettled, leave it marked as `UNDECIDED`.

## Evidence Checks
- Confirm the change includes evidence or a documented rationale.
- Confirm the evidence source is named.
- Manual check: verify evidence is strong enough for the claimed rule change.
- If evidence is incomplete, report that directly.

## Release-Readiness Checks
- Confirm the change summary states what changed and why.
- Confirm known risks, missing checks, or manual follow-up items are listed.
- Manual check: reviewer can trace the change from logic update to source-of-truth doc.
- Release gate automation: `UNDECIDED / NOT YET DEFINED IN REPO`
