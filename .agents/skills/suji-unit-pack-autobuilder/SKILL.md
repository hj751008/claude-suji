---
name: suji-unit-pack-autobuilder
description: Scaffold a new sujimathAI unit pack and its companion docs inside this repository. Use when starting the next math unit so repeated folder creation, template copying, and draft doc skeleton setup happen quickly without inventing curriculum content.
---

# suji-unit-pack-autobuilder

Use this skill when a new unit needs the same safe starting structure as Unit 2.

## What This Skill Automates

- creates a new `app/content/<slug>/` folder with the standard unit-pack JSON files
- creates companion docs skeletons in `docs/`
- can update `PROJECT_CONTEXT.md` and `NEXT_STEPS.md` through auto-managed markers
- can check whether a unit is truly ready for runtime activation
- keeps the generated content conservative:
  - no invented curriculum mappings
  - no invented mastery thresholds
  - no runtime activation

## Before Running

1. Read `PROJECT_CONTEXT.md` and `NEXT_STEPS.md`.
2. Confirm the new unit has at least:
   - `unit id` such as `U3`
   - content slug such as `unit3-linear-functions`
   - Korean topic label
   - English working label
3. If the source basis is still unknown, generate scaffolds only. Do not fill app-facing content from memory.

## Primary Command

Run:

```powershell
python .agents\skills\suji-unit-pack-autobuilder\scripts\create_unit_pack.py --unit-id U3 --slug unit3-example --topic-ko "예시 단원" --topic-en "Example Unit"
```

Useful flags:

- `--dry-run`
  - preview paths and file names without writing anything
- `--force`
  - overwrite files that already exist
- `--update-project-docs`
  - update `PROJECT_CONTEXT.md` and `NEXT_STEPS.md` through auto-managed blocks instead of hand-editing the same unit status repeatedly

## Second-Stage Draft Generation

After the scaffold docs are filled, run:

```powershell
python .agents\skills\suji-unit-pack-autobuilder\scripts\generate_unit_drafts_from_docs.py --content-dir app\content\unit2-scaffold --source-note docs\unit2-source-note-2026-03-30.md --subskills-doc docs\unit2-subskills-integers-rational-2026-03-30.md --learning-design-doc docs\unit2-draft-learning-design-2026-03-30.md --transcript-doc docs\unit2-transcript-examples-2026-03-30.md --dry-run
```

Use `--force` only when you want the generated draft JSON to overwrite the
existing draft JSON in the target content folder.

If the generation changes project status, add:

```powershell
--update-project-docs
```

## Third-Stage Runtime Activation Gate

Before wiring a unit into runtime, run:

```powershell
python .agents\skills\suji-unit-pack-autobuilder\scripts\check_runtime_activation_gate.py --unit-id U2 --content-dir app\content\unit2-scaffold --pack-scaffold-doc docs\unit2-pack-scaffold-2026-03-30.md --source-note docs\unit2-source-note-2026-03-30.md --subskills-doc docs\unit2-subskills-integers-rational-2026-03-30.md --learning-design-doc docs\unit2-draft-learning-design-2026-03-30.md --transcript-doc docs\unit2-transcript-examples-2026-03-30.md
```

What this gate checks:

- required docs and content files exist
- `python app/cli.py validate-content` passes
- runtime-facing JSON arrays are non-empty
- `activity -> lesson -> rubric -> observation` counts are aligned
- transcript docs cover every lesson step
- replay-ready transcript fixture exists
- runtime loader and CLI are no longer Unit 1-only
- harness has at least one Unit 2 or transcript-fixture reference

If the gate should also update project-state docs, add:

```powershell
--update-project-docs
```

## What The Script Writes

- `app/content/<slug>/`
  - `README.md`
  - `skills.json`
  - `prerequisites.json`
  - `recommendation-examples.json`
  - `error-patterns.json`
  - `activity-recommendations.json`
  - `lesson-steps.json`
  - `evaluator-rubrics.json`
  - `observation-form-mappings.json`
- `docs/`
  - `unit<n>-pack-scaffold-<date>.md`
  - `unit<n>-source-note-<date>.md`
  - `unit<n>-subskills-<slug>-<date>.md`
  - `unit<n>-draft-learning-design-<date>.md`
  - `unit<n>-transcript-examples-<date>.md`

## Guardrails

- Treat generated files as scaffolds, not approved curriculum.
- Keep generated JSON arrays empty until source-backed records exist.
- Do not claim the unit is runtime-ready after scaffold generation.
- Review the auto-managed `PROJECT_CONTEXT.md` and `NEXT_STEPS.md` sections after using `--update-project-docs`, but do not hand-edit inside the generated markers unless you intend to take over that section manually.

## After Running

1. Add source-backed notes in the generated docs.
2. Run the draft generator so `skills/examples/error/activity/lesson/rubric/observation` can be filled from the docs.
3. Run `python app/cli.py validate-content`.
4. Run the runtime activation gate before any loader wiring.
5. Only then decide whether runtime, validator, and harness changes belong in the same follow-up change.
