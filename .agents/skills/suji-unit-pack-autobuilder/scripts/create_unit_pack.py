from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from project_docs import update_next_steps, update_project_context


ROOT = Path(__file__).resolve().parents[4]
CONTENT_ROOT = ROOT / "app" / "content"
DOCS_ROOT = ROOT / "docs"

JSON_TARGETS = (
    "skills.json",
    "prerequisites.json",
    "recommendation-examples.json",
    "error-patterns.json",
    "activity-recommendations.json",
    "lesson-steps.json",
    "evaluator-rubrics.json",
    "observation-form-mappings.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a new sujimathAI unit pack conservatively.")
    parser.add_argument("--unit-id", required=True, help="Unit id like U3")
    parser.add_argument("--slug", required=True, help="Content folder slug like unit3-linear-functions")
    parser.add_argument("--topic-ko", required=True, help="Korean topic label")
    parser.add_argument("--topic-en", required=True, help="English working label")
    parser.add_argument("--dry-run", action="store_true", help="Show planned files without writing them.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument("--update-project-docs", action="store_true", help="Update PROJECT_CONTEXT.md and NEXT_STEPS.md with auto-managed unit status.")
    parser.add_argument("--project-context-path", default="PROJECT_CONTEXT.md", help="Override PROJECT_CONTEXT.md path for testing.")
    parser.add_argument("--next-steps-path", default="NEXT_STEPS.md", help="Override NEXT_STEPS.md path for testing.")
    return parser.parse_args()


def normalize_unit_id(unit_id: str) -> str:
    value = unit_id.strip().upper()
    if not value.startswith("U") or len(value) < 2:
        raise ValueError("unit id must look like U3.")
    return value


def derive_unit_prefix(unit_id: str) -> str:
    return unit_id.lower().replace("-", "")


def derive_subskills_doc_name(unit_prefix: str, slug: str, today: str) -> str:
    suffix = slug
    if suffix.startswith(f"{unit_prefix}-"):
        suffix = suffix[len(unit_prefix) + 1 :]
    elif suffix.startswith(f"{unit_prefix}_"):
        suffix = suffix[len(unit_prefix) + 1 :]
    return f"{unit_prefix}-subskills-{suffix}-{today}.md"


def resolve_repo_path(path_str: str) -> Path:
    path = Path(path_str)
    return path if path.is_absolute() else ROOT / path


def safe_write(path: Path, content: str, force: bool, written: list[str]) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Re-run with --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    written.append(str(path.relative_to(ROOT)))


def build_readme(unit_id: str, topic_ko: str, topic_en: str, doc_names: dict[str, str]) -> str:
    return f"""# {unit_id} Scaffold

This folder records a conservative starting point for the next unit:

- Unit topic: `{topic_ko}`
- English working label: `{topic_en}`

This folder is intentionally not runtime-loaded until the unit has source-backed
content and runnable validation.

Everything here should remain aligned with:

- `docs/{doc_names['source_note']}`
- `docs/{doc_names['pack_scaffold']}`
- `docs/mastery-rules.md`
- `docs/prerequisite-map.md`
- `docs/recommendation-rules.md`

Guardrails:

- Do not treat this folder as a finished unit pack.
- Keep generated JSON arrays empty until source-backed records exist.
- Do not wire this folder into runtime loaders until validator and harness
  coverage are ready.
"""


def build_source_note(unit_id: str, topic_ko: str, topic_en: str, today: str) -> str:
    return f"""# {unit_id} Source Note ({today})

## Confirmed Topic

- Working unit id: `{unit_id}`
- Korean topic label: `{topic_ko}`
- English working label: `{topic_en}`

## Evidence Basis

- Replace with explicit source file paths or repo docs.

## What This Note Approves

- The next unit pack may use `{topic_ko}` as its working topic label once the
  source basis is filled.

## What This Note Does Not Approve

- curriculum mappings
- mastery thresholds
- runtime activation
- textbook alignment claims beyond explicit source material

## Next Extraction Work

1. Add explicit source files or internal docs.
2. Extract draft subskills from those sources.
3. Fill app-facing content only from the extracted docs.
"""


def build_subskills_doc(unit_id: str, topic_en: str, today: str) -> str:
    return f"""# {unit_id} Subskills: {topic_en} ({today})

## Status

- This is an initial extraction stub for {unit_id}.
- Fill this file only from explicit source material.

## Source Basis

- Replace with explicit source file paths.

## Observed Problem Clusters

- Replace with observed task families from the source material.

## Draft Skill Set

- Add source-backed skill ids and titles here.

## Not Yet Approved

- prerequisite graph
- runtime activation
- mastery thresholds
"""


def build_learning_design_doc(unit_id: str, today: str) -> str:
    return f"""# {unit_id} Draft Learning Design ({today})

## Status

- This document will hold draft examples, error patterns, activities, lesson
  steps, evaluator signals, and observation-form focus.
- Do not add records without source-backed notes.

## Source Basis

- Replace with source-backed docs for this unit.

## Draft Recommendation Situations

- Replace with source-backed recommendation situations.

## Draft Learner Error Patterns

- Replace with source-backed error patterns.

## Draft Activity Recommendations

- Replace with source-backed activity notes.

## Draft Lesson Steps

- Replace with source-backed lesson-step notes.

## Draft Evaluator Signals

- Replace with source-backed required signals.

## Draft Observation-Form Focus

- Replace with source-backed operator capture guidance.
"""


def build_pack_scaffold_doc(unit_id: str, topic_ko: str, today: str) -> str:
    return f"""# {unit_id} Pack Scaffold ({today})

## Status

- This is a scaffold only.
- It records `{topic_ko}` as the working next-unit topic.
- It does not approve runtime activation.

## Why This Exists

- Keep new unit creation consistent with the current content-pack schema.
- Avoid redoing the same folder and doc setup by hand.

## Current Decision

- Create `app/content/` scaffold files first.
- Fill source notes before app-facing records.
- Keep unsupported files empty instead of inventing content.

## What Is Still Missing

- source-backed skills
- prerequisite links
- teaching records
- runtime registration
- validator and harness coverage
"""


def build_transcript_doc(unit_id: str, today: str) -> str:
    return f"""# {unit_id} Transcript Examples ({today})

## Status

- These are draft transcript placeholders for future operator review.
- They are not replay-ready runtime fixtures.

## Source Basis

- Replace with the learning-design doc and content files for this unit.

## Transcript Drafts

- Add transcript examples only after lesson steps and observation-form mappings
  exist.
"""


def main() -> int:
    args = parse_args()
    unit_id = normalize_unit_id(args.unit_id)
    slug = args.slug.strip()
    if not slug:
        raise ValueError("slug must be non-empty.")

    unit_prefix = derive_unit_prefix(unit_id)
    today = date.today().isoformat()
    doc_names = {
        "source_note": f"{unit_prefix}-source-note-{today}.md",
        "pack_scaffold": f"{unit_prefix}-pack-scaffold-{today}.md",
        "subskills": derive_subskills_doc_name(unit_prefix, slug, today),
        "draft_learning_design": f"{unit_prefix}-draft-learning-design-{today}.md",
        "transcript_examples": f"{unit_prefix}-transcript-examples-{today}.md",
    }

    content_dir = CONTENT_ROOT / slug
    planned_paths = [content_dir / "README.md"]
    planned_paths.extend(content_dir / target for target in JSON_TARGETS)
    planned_paths.extend(DOCS_ROOT / name for name in doc_names.values())
    project_context_path = resolve_repo_path(args.project_context_path)
    next_steps_path = resolve_repo_path(args.next_steps_path)
    if args.update_project_docs:
        planned_paths.extend([project_context_path, next_steps_path])

    if args.dry_run:
        print("Dry run:")
        for path in planned_paths:
            print(f"- {path.relative_to(ROOT)}")
        return 0

    written: list[str] = []
    safe_write(
        content_dir / "README.md",
        build_readme(unit_id, args.topic_ko, args.topic_en, doc_names),
        args.force,
        written,
    )
    for target_name in JSON_TARGETS:
        safe_write(content_dir / target_name, "[]\n", args.force, written)
    safe_write(
        DOCS_ROOT / doc_names["source_note"],
        build_source_note(unit_id, args.topic_ko, args.topic_en, today),
        args.force,
        written,
    )
    safe_write(
        DOCS_ROOT / doc_names["pack_scaffold"],
        build_pack_scaffold_doc(unit_id, args.topic_ko, today),
        args.force,
        written,
    )
    safe_write(
        DOCS_ROOT / doc_names["subskills"],
        build_subskills_doc(unit_id, args.topic_en, today),
        args.force,
        written,
    )
    safe_write(
        DOCS_ROOT / doc_names["draft_learning_design"],
        build_learning_design_doc(unit_id, today),
        args.force,
        written,
    )
    safe_write(
        DOCS_ROOT / doc_names["transcript_examples"],
        build_transcript_doc(unit_id, today),
        args.force,
        written,
    )
    if args.update_project_docs:
        update_project_context(project_context_path, unit_id, slug, args.topic_ko, args.topic_en, "scaffold-created")
        update_next_steps(next_steps_path, unit_id, slug, "scaffold-created")
        written.append(str(project_context_path.relative_to(ROOT)))
        written.append(str(next_steps_path.relative_to(ROOT)))

    print(
        json.dumps(
            {
                "unitId": unit_id,
                "slug": slug,
                "topicKo": args.topic_ko,
                "topicEn": args.topic_en,
                "written": written,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
