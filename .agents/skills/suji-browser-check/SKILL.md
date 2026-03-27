---
name: suji-browser-check
description: Plan or perform limited browser-based checks for sujimathAI when a real UI or web flow needs verification. Use when the task explicitly needs browser interaction, screenshots, form flows, or staging-page validation beyond CLI and harness checks.
---

# suji-browser-check

Use this skill only when CLI and harness checks are not enough.

## Check
- Confirm first whether the behavior can be validated without a browser.
- Use browser checks for real navigation, form interaction, screenshots, layout confirmation, or authenticated page verification.
- Keep the test narrow: one flow, one bug hypothesis, or one acceptance check at a time.
- Capture evidence clearly: what page was visited, what was clicked, and what was observed.

## Guardrails
- Do not substitute browser impressions for math/content validation.
- If login, cookies, or staging access are required, state that dependency before claiming the check is ready.
