---
name: suji-review
description: Review sujimathAI code or docs changes with priority on math correctness, mastery-risk regressions, learner-facing behavior, and missing validation. Use when asked to review a diff, PR, branch, or proposed logic/content change.
---

# suji-review

Use this skill for review passes in `sujimathAI`.

## Review Focus
- Prioritize learner-facing regressions over style comments.
- Check math correctness, curriculum fidelity, and mastery-logic safety first.
- Flag any silent threshold, prerequisite, recommendation, or confidence changes.
- Treat missing harness coverage or missing reproducible checks as review findings when behavior changed.
- Call out where content is still provisional, paraphrased, or not source-of-truth.

## Output
- Lead with findings, ordered by severity.
- Include concrete file references.
- Say explicitly if no findings were found, and mention residual risk or testing gaps.
