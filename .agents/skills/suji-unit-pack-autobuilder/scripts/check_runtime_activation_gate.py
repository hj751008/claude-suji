from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
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
    parser = argparse.ArgumentParser(description="Check whether a unit pack is ready for runtime activation.")
    parser.add_argument("--unit-id", required=True, help="Unit id like U2")
    parser.add_argument("--content-dir", required=True, help="Target content directory, e.g. app/content/unit2-scaffold")
    parser.add_argument("--pack-scaffold-doc", required=True, help="Pack scaffold markdown path")
    parser.add_argument("--source-note", required=True, help="Source note markdown path")
    parser.add_argument("--subskills-doc", required=True, help="Subskills markdown path")
    parser.add_argument("--learning-design-doc", required=True, help="Learning design markdown path")
    parser.add_argument("--transcript-doc", required=True, help="Transcript examples markdown path")
    parser.add_argument(
        "--transcript-fixture",
        help="Replay-ready transcript fixture path. Defaults to app/domain/evidence/<unit>-tutor-transcripts.example.json",
    )
    parser.add_argument("--runtime-loader-path", default="app/runtime/content_loader.py", help="Runtime content loader path")
    parser.add_argument("--cli-path", default="app/cli.py", help="CLI entrypoint path")
    parser.add_argument("--harness-root", default="app/harness", help="Harness root path")
    parser.add_argument("--project-context-path", default="PROJECT_CONTEXT.md", help="Override PROJECT_CONTEXT.md path")
    parser.add_argument("--next-steps-path", default="NEXT_STEPS.md", help="Override NEXT_STEPS.md path")
    parser.add_argument("--update-project-docs", action="store_true", help="Update PROJECT_CONTEXT.md and NEXT_STEPS.md with gate status.")
    return parser.parse_args()


def resolve_repo_path(path_str: str) -> Path:
    path = Path(path_str)
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def find_inline_value(lines: list[str], prefix: str) -> str | None:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip().strip("`")
    return None


def transcript_doc_step_ids(path: Path) -> list[str]:
    step_ids: list[str] = []
    for line in load_lines(path):
        stripped = line.strip()
        prefix = "- Lesson step:"
        if stripped.startswith(prefix) and "`" in stripped:
            start = stripped.find("`") + 1
            end = stripped.find("`", start)
            if end > start:
                step_ids.append(stripped[start:end])
    return step_ids


def run_validate_content() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "app/cli.py", "validate-content"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def scan_for_text(root: Path, needles: list[str]) -> list[str]:
    hits: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if path.suffix.lower() not in {".py", ".json", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lowered = text.lower()
        if any(needle.lower() in lowered for needle in needles):
            hits.append(str(path.relative_to(ROOT)))
    return hits


def main() -> int:
    args = parse_args()
    unit_id = args.unit_id.strip().upper()
    if not unit_id.startswith("U"):
        raise ValueError("unit id must look like U2.")
    unit_number = unit_id[1:]
    if not unit_number:
        raise ValueError("unit id must include a numeric suffix like U2.")

    content_dir = resolve_repo_path(args.content_dir)
    pack_scaffold_doc = resolve_repo_path(args.pack_scaffold_doc)
    source_note = resolve_repo_path(args.source_note)
    subskills_doc = resolve_repo_path(args.subskills_doc)
    learning_design_doc = resolve_repo_path(args.learning_design_doc)
    transcript_doc = resolve_repo_path(args.transcript_doc)
    runtime_loader_path = resolve_repo_path(args.runtime_loader_path)
    cli_path = resolve_repo_path(args.cli_path)
    harness_root = resolve_repo_path(args.harness_root)
    transcript_fixture = resolve_repo_path(
        args.transcript_fixture or f"app/domain/evidence/unit{unit_number}-tutor-transcripts.example.json"
    )
    source_note_lines = load_lines(source_note)
    topic_ko = find_inline_value(source_note_lines, "- Korean topic label:") or unit_id
    topic_en = find_inline_value(source_note_lines, "- English working label:") or unit_id

    required_paths = {
        "contentDir": content_dir,
        "packScaffoldDoc": pack_scaffold_doc,
        "sourceNote": source_note,
        "subskillsDoc": subskills_doc,
        "learningDesignDoc": learning_design_doc,
        "transcriptDoc": transcript_doc,
        "runtimeLoaderPath": runtime_loader_path,
        "cliPath": cli_path,
        "harnessRoot": harness_root,
    }

    blockers: list[str] = []
    checks: dict[str, object] = {}
    for label, path in required_paths.items():
        exists = path.exists()
        checks[label] = {"path": str(path.relative_to(ROOT)), "exists": exists}
        if not exists:
            blockers.append(f"Missing required path: {path.relative_to(ROOT)}")

    for target in JSON_TARGETS:
        target_path = content_dir / target
        if not target_path.exists():
            blockers.append(f"Missing content file: {target_path.relative_to(ROOT)}")

    if blockers:
        summary = {"unitId": unit_id, "gatePassed": False, "checks": checks, "blockers": blockers}
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 1

    payloads = {name: load_json(content_dir / name) for name in JSON_TARGETS}
    counts = {name: len(payload) if isinstance(payload, list) else None for name, payload in payloads.items()}
    checks["recordCounts"] = counts
    for name, count in counts.items():
        if not isinstance(count, int) or count <= 0:
            blockers.append(f"{content_dir.name}/{name} must be a non-empty JSON array before runtime activation.")

    activities = payloads["activity-recommendations.json"]
    lesson_steps = payloads["lesson-steps.json"]
    evaluator_rubrics = payloads["evaluator-rubrics.json"]
    observation_form_mappings = payloads["observation-form-mappings.json"]
    aligned_count = len(activities) == len(lesson_steps) == len(evaluator_rubrics) == len(observation_form_mappings)
    checks["teachingChainCountsAligned"] = {
        "passed": aligned_count,
        "activities": len(activities),
        "lessonSteps": len(lesson_steps),
        "evaluatorRubrics": len(evaluator_rubrics),
        "observationFormMappings": len(observation_form_mappings),
    }
    if not aligned_count:
        blockers.append("Activity/lesson/rubric/observation counts must stay aligned before runtime activation.")

    transcript_step_ids = transcript_doc_step_ids(transcript_doc)
    lesson_step_ids = [record.get("lessonStepId") for record in lesson_steps if isinstance(record, dict)]
    transcript_ready = sorted(transcript_step_ids) == sorted(lesson_step_ids) and len(transcript_step_ids) == len(lesson_step_ids)
    checks["transcriptDocCoverage"] = {
        "passed": transcript_ready,
        "transcriptStepCount": len(transcript_step_ids),
        "lessonStepCount": len(lesson_step_ids),
    }
    if not transcript_ready:
        blockers.append("Transcript examples doc must cover every lessonStepId before runtime activation.")

    validate_ok, validate_output = run_validate_content()
    checks["validateContent"] = {"passed": validate_ok, "output": validate_output}
    if not validate_ok:
        blockers.append("`python app/cli.py validate-content` must pass before runtime activation.")

    fixture_exists = transcript_fixture.exists()
    fixture_count = 0
    if fixture_exists:
        transcript_payload = load_json(transcript_fixture)
        if isinstance(transcript_payload, list):
            fixture_count = len(transcript_payload)
        else:
            blockers.append(f"{transcript_fixture.relative_to(ROOT)} must be a JSON array.")
    checks["transcriptFixture"] = {
        "path": str(transcript_fixture.relative_to(ROOT)),
        "exists": fixture_exists,
        "recordCount": fixture_count,
    }
    if not fixture_exists:
        blockers.append(f"Replay-ready transcript fixture is missing: {transcript_fixture.relative_to(ROOT)}")
    elif fixture_count <= 0:
        blockers.append(f"Replay-ready transcript fixture is empty: {transcript_fixture.relative_to(ROOT)}")

    loader_text = runtime_loader_path.read_text(encoding="utf-8")
    expected_loader_fn = f"load_unit{unit_number}_content"
    loader_registered = expected_loader_fn in loader_text and content_dir.name in loader_text
    checks["runtimeLoaderRegistration"] = {
        "passed": loader_registered,
        "expectedFunction": expected_loader_fn,
        "contentSlug": content_dir.name,
    }
    if not loader_registered:
        blockers.append(
            f"Runtime loader is not ready for {unit_id}: expected {expected_loader_fn} and content slug {content_dir.name} in {runtime_loader_path.relative_to(ROOT)}."
        )

    cli_text = cli_path.read_text(encoding="utf-8")
    cli_ready = expected_loader_fn in cli_text or unit_id.lower() in cli_text.lower()
    checks["cliRegistration"] = {"passed": cli_ready, "path": str(cli_path.relative_to(ROOT))}
    if not cli_ready:
        blockers.append(f"CLI still appears unit-specific and does not reference {unit_id} in {cli_path.relative_to(ROOT)}.")

    harness_hits = scan_for_text(harness_root, [unit_id.lower(), transcript_fixture.name.lower(), expected_loader_fn.lower()])
    checks["harnessCoverage"] = {"passed": bool(harness_hits), "hits": harness_hits}
    if not harness_hits:
        blockers.append(f"Harness does not yet reference {unit_id} or {transcript_fixture.name}.")

    gate_passed = not blockers

    if args.update_project_docs:
        from project_docs import update_next_steps, update_project_context

        project_context_path = resolve_repo_path(args.project_context_path)
        next_steps_path = resolve_repo_path(args.next_steps_path)
        stage = "runtime-gate-passed" if gate_passed else "runtime-gate-blocked"
        update_project_context(project_context_path, unit_id, content_dir.name, topic_ko, topic_en, stage)
        update_next_steps(next_steps_path, unit_id, content_dir.name, stage)
        checks["projectDocsUpdated"] = {
            "projectContextPath": str(project_context_path.relative_to(ROOT)),
            "nextStepsPath": str(next_steps_path.relative_to(ROOT)),
            "stage": stage,
        }

    print(
        json.dumps(
            {
                "unitId": unit_id,
                "gatePassed": gate_passed,
                "checks": checks,
                "blockers": blockers,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
