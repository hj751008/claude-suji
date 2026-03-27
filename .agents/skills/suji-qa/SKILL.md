---
name: suji-qa
description: Run sujimathAI QA checks for learner/session flows, content validation, and harness coverage. Use when validating new behavior, session orchestration changes, recommendation logic, evaluator changes, or before landing app logic updates.
---

# suji-qa

Use this skill to validate behavior in `sujimathAI` before calling work done.

## Check
- Start with the smallest reproducible CLI or harness command that exercises the changed path.
- Prefer existing checks first: `python app/cli.py validate-content` and `python app/cli.py run-harness`.
- When session or learner-record behavior changed, run the exact CLI flow that a user or tool would execute.
- Report what was run, what passed, and what was not verified.
- If a change affects math or progression behavior, note whether the result is still provisional or document-backed.

## Guardrails
- Do not claim QA coverage that was not actually run.
- If a browser check would add confidence, say so explicitly instead of implying it happened.
