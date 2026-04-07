# Repository Guidelines

## Project Scope
`sujimathAI` is a Korean middle school math learning AI project. Treat all code, content, and tooling changes as education-facing work where math correctness and curriculum fidelity matter more than speed.

## Structure
- `app/`: product code, logic, and future test code.
- `docs/`: specs, curriculum notes, and project documentation.
- `.agents/skills/`: repository-local agent workflows such as curriculum checks and mastery review.

## Working Principles
- Make the smallest change that solves the problem. Avoid broad refactors unless clearly required.
- Write a short plan before large changes, data migrations, or rule updates.
- Prioritize mathematical correctness over style or convenience.
- Follow [docs/project-operating-protocol.md](C:\Users\tcikh\OneDrive\문서\codex\sujimathAI\docs\project-operating-protocol.md) for team review, phase order, document authority, and reporting format.
- Do not invent curriculum mappings, standards links, or textbook alignment. Only use mappings backed by project docs or explicit source material.
- Do not silently change mastery thresholds, pass criteria, or scoring cutoffs. If a threshold must change, call it out explicitly.
- Report validation results honestly. If checks were not run, data is incomplete, or confidence is limited, say so directly.

## Development Notes
- Keep logic and content files focused and easy to review.
- Use clear file names such as `linear-functions`, `ratio_review`, or language-native names already established in the repo.
- Search first before editing: `rg "<pattern>" app docs`
- Review local changes with `git status`

## Testing & Review
- Add reproducible checks with new behavior whenever possible.
- Verify math examples, answer keys, mastery logic, and curriculum references before merging.
- PRs should include the purpose of the change, affected math scope, and any validation performed.
