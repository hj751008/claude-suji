from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from project_docs import update_next_steps, update_project_context


ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate conservative unit-pack draft JSON from source-backed docs.")
    parser.add_argument("--content-dir", required=True, help="Target content directory, e.g. app/content/unit2-scaffold")
    parser.add_argument("--source-note", required=True, help="Source note markdown path")
    parser.add_argument("--subskills-doc", required=True, help="Subskills markdown path")
    parser.add_argument("--learning-design-doc", required=True, help="Learning design markdown path")
    parser.add_argument("--transcript-doc", help="Optional transcript examples markdown path")
    parser.add_argument("--dry-run", action="store_true", help="Print a generation summary without writing files.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing JSON files.")
    parser.add_argument("--update-project-docs", action="store_true", help="Update PROJECT_CONTEXT.md and NEXT_STEPS.md with auto-managed unit status.")
    parser.add_argument("--project-context-path", default="PROJECT_CONTEXT.md", help="Override PROJECT_CONTEXT.md path for testing.")
    parser.add_argument("--next-steps-path", default="NEXT_STEPS.md", help="Override NEXT_STEPS.md path for testing.")
    return parser.parse_args()


def resolve_repo_path(path_str: str) -> Path:
    path = Path(path_str)
    return path if path.is_absolute() else ROOT / path


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def extract_h2_section(lines: list[str], heading: str) -> list[str]:
    target = f"## {heading}"
    start = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        raise ValueError(f"Could not find section {target!r}.")

    section: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        section.append(line)
    return section


def extract_h3_blocks(section_lines: list[str]) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_body: list[str] = []

    for line in section_lines:
        if line.startswith("### "):
            if current_heading is not None:
                blocks.append((current_heading, current_body))
            current_heading = line[len("### ") :].strip()
            current_body = []
        else:
            if current_heading is not None:
                current_body.append(line)

    if current_heading is not None:
        blocks.append((current_heading, current_body))
    return blocks


def extract_quoted_id(heading: str) -> str:
    match = re.search(r"`([^`]+)`", heading)
    if not match:
        raise ValueError(f"Expected backticked id in heading: {heading}")
    return match.group(1)


def heading_suffix_after_colon(heading: str) -> str:
    parts = heading.split(":", 1)
    return parts[1].strip() if len(parts) == 2 else ""


def find_inline_value(lines: list[str], prefix: str) -> str | None:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip().strip("`")
    return None


def find_nested_bullets(lines: list[str], label_prefix: str) -> list[str]:
    results: list[str] = []
    capture = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(label_prefix):
            capture = True
            continue
        if capture:
            if stripped.startswith("- ") or stripped.startswith("* "):
                results.append(stripped[2:].strip().strip("`"))
                continue
            if not stripped:
                continue
            if stripped.startswith("### ") or stripped.startswith("## "):
                break
            if stripped.startswith("- ") is False and stripped.startswith("* ") is False and not line.startswith("  "):
                break
    return results


def flatten_sentence(value: str) -> str:
    return " ".join(value.split()).strip().rstrip(".")


def sentence_case_label(value: str) -> str:
    words = value.replace("-", "_").split("_")
    cleaned = [word for word in words if word]
    if not cleaned:
        return "Signal"
    label = " ".join(cleaned)
    return label[:1].upper() + label[1:]


def slugify(value: str) -> str:
    lowered = value.lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-") or "item"


def parse_subskills(subskills_lines: list[str]) -> list[dict]:
    section = None
    for heading in ("Draft Unit 2 Skill Set", "Draft Skill Set", "Draft Unit Skill Set"):
        try:
            section = extract_h2_section(subskills_lines, heading)
            break
        except ValueError:
            continue
    if section is None:
        raise ValueError("Could not find a supported draft skill-set section.")
    records: list[dict] = []
    for heading, body in extract_h3_blocks(section):
        skill_id = extract_quoted_id(heading)
        title = find_inline_value(body, "- Title:")
        support_points = find_nested_bullets(body, "- Why this is supported:")
        if title is None:
            raise ValueError(f"Missing title for {skill_id}.")
        support_text = support_points[0] if support_points else "source-backed unit skill"
        summary = f"Draft {skill_id} skill extracted from {flatten_sentence(support_text)}."
        records.append(
            {
                "id": skill_id,
                "status": "draft-from-docs",
                "title": title,
                "summary": summary,
            }
        )
    return records


def parse_recommendations(learning_lines: list[str]) -> list[dict]:
    section = extract_h2_section(learning_lines, "Draft Recommendation Situations")
    records: list[dict] = []
    for heading, body in extract_h3_blocks(section):
        skill_id = extract_quoted_id(heading)
        when_line = next((line.strip()[2:].strip() for line in body if line.strip().startswith("- Recommend when ")), None)
        if when_line is None:
            when_line = next((line.strip()[2:].strip() for line in body if line.strip().startswith("- ")), None)
        operator_focus = find_nested_bullets(body, "- Operator focus:")
        records.append(
            {
                "when": when_line,
                "recommend": skill_id,
                "confidence": "limited",
                "needsReview": True,
                "operatorNote": operator_focus[0] if operator_focus else "Keep the discussion grounded in the documented concept.",
            }
        )
    return records


def parse_error_patterns(learning_lines: list[str]) -> list[dict]:
    section = extract_h2_section(learning_lines, "Draft Learner Error Patterns")
    records: list[dict] = []
    for heading, body in extract_h3_blocks(section):
        skill_id = extract_quoted_id(heading)
        summary_suffix = heading_suffix_after_colon(heading) or "draft pattern"
        bullets = [line.strip()[2:].strip() for line in body if line.strip().startswith("- ")]
        records.append(
            {
                "id": f"{skill_id.lower()}-{slugify(summary_suffix)}",
                "skillId": skill_id,
                "status": "draft-from-docs",
                "summary": flatten_sentence(summary_suffix[:1].upper() + summary_suffix[1:]) + ".",
                "watchFor": bullets[:2],
                "operatorNote": bullets[0] if bullets else "Return to the documented concept before moving on.",
            }
        )
    return records


def parse_activities(learning_lines: list[str]) -> list[dict]:
    activity_section = extract_h2_section(learning_lines, "Draft Activity Recommendations")
    lesson_section = extract_h2_section(learning_lines, "Draft Lesson Steps")
    activity_ids_by_skill: dict[str, str] = {}
    for heading, body in extract_h3_blocks(lesson_section):
        lesson_step_id = extract_quoted_id(heading)
        activity_id = find_inline_value(body, "- Activity link:")
        skill_match = re.search(r"(U\d+-S[\w]+)", lesson_step_id)
        if activity_id and skill_match:
            activity_ids_by_skill[skill_match.group(1)] = activity_id

    records: list[dict] = []
    for heading, body in extract_h3_blocks(activity_section):
        skill_id = extract_quoted_id(heading)
        title = heading_suffix_after_colon(heading)
        activity_type = find_inline_value(body, "- Activity type:")
        goals = find_nested_bullets(body, "- Goal:")
        records.append(
            {
                "activityId": activity_ids_by_skill.get(skill_id, f"ACT-{skill_id}-{slugify(title).upper()}"),
                "skillId": skill_id,
                "status": "draft-from-docs",
                "activityType": activity_type or "dialogue-flow",
                "title": title,
                "goal": goals[0] if goals else "Replace with a source-backed goal.",
            }
        )
    return records


def parse_transcripts(transcript_lines: list[str] | None) -> dict[str, dict]:
    if not transcript_lines:
        return {}
    section = extract_h2_section(transcript_lines, "Transcript Drafts")
    records: dict[str, dict] = {}
    for heading, body in extract_h3_blocks(section):
        lesson_step_id = find_inline_value(body, "- Lesson step:")
        tutor_lines = find_nested_bullets(body, "- Tutor:")
        learner_lines = find_nested_bullets(body, "- Learner:")
        if lesson_step_id:
            records[lesson_step_id] = {
                "transcriptId": extract_quoted_id(heading),
                "tutor": tutor_lines[0] if tutor_lines else None,
                "learner": learner_lines[0] if learner_lines else None,
            }
    return records


def parse_lesson_steps(learning_lines: list[str], transcripts: dict[str, dict]) -> list[dict]:
    section = extract_h2_section(learning_lines, "Draft Lesson Steps")
    records: list[dict] = []
    for heading, body in extract_h3_blocks(section):
        lesson_step_id = extract_quoted_id(heading)
        transcript = transcripts.get(lesson_step_id, {})
        activity_id = find_inline_value(body, "- Activity link:")
        tutor_moves = find_nested_bullets(body, "- Tutor move:")
        stopping = find_nested_bullets(body, "- Good stopping point:")
        transcript_tutor = transcript.get("tutor")
        transcript_learner = transcript.get("learner")
        records.append(
            {
                "lessonStepId": lesson_step_id,
                "activityId": activity_id,
                "status": "draft-from-docs",
                "openingLine": transcript_tutor or (tutor_moves[0] if tutor_moves else "Replace with a source-backed opening line."),
                "firstTutorQuestion": transcript_tutor or "Replace with the first tutor question.",
                "smallHint": transcript_learner or "Replace with a source-backed small hint.",
                "goodStoppingPoint": stopping[0] if stopping else "Replace with a source-backed stopping point.",
                "watchFor": [],
                "exampleTutorMove": transcript_tutor or (tutor_moves[0] if tutor_moves else "Replace with a source-backed tutor move."),
                "exampleLearnerResponse": transcript_learner or "Replace with a source-backed learner response.",
            }
        )
    return records


def parse_evaluator_rubrics(learning_lines: list[str]) -> list[dict]:
    section = extract_h2_section(learning_lines, "Draft Evaluator Signals")
    records: list[dict] = []
    for heading, body in extract_h3_blocks(section):
        lesson_step_id = extract_quoted_id(heading)
        required_signals = [item.strip("`") for item in find_nested_bullets(body, "- Required signals:")]
        records.append(
            {
                "lessonStepId": lesson_step_id,
                "status": "draft-from-docs",
                "requiredSignals": required_signals,
            }
        )
    return records


def parse_observation_focus(learning_lines: list[str], rubrics: list[dict]) -> list[dict]:
    rubric_map = {record["lessonStepId"]: record["requiredSignals"] for record in rubrics}
    section = extract_h2_section(learning_lines, "Draft Observation-Form Focus")
    records: list[dict] = []
    for heading, body in extract_h3_blocks(section):
        lesson_step_id = extract_quoted_id(heading)
        bullets = [line.strip()[2:].strip() for line in body if line.strip().startswith("- ")]
        focus = bullets[0] if bullets else f"Capture what the learner said during {lesson_step_id}."
        focus_sentence = flatten_sentence(focus)
        lower_prefix = "capture whether the learner "
        learner_prompt = f"Write what the learner said during {lesson_step_id}."
        tutor_prompt = focus_sentence[:1].upper() + focus_sentence[1:] + "."
        if focus_sentence.lower().startswith(lower_prefix):
            suffix = focus_sentence[len(lower_prefix) :]
            learner_prompt = f"Write how the learner {suffix}."
            tutor_prompt = f"Note whether the learner {suffix}."

        fields = []
        for signal_name in rubric_map.get(lesson_step_id, []):
            label = sentence_case_label(signal_name)
            fields.append(
                {
                    "fieldId": signal_name,
                    "signalOnTrue": signal_name,
                    "label": label,
                    "prompt": f"Did the learner show evidence for {label.lower()}?",
                    "trueMeans": f"The learner showed evidence for {label.lower()}.",
                }
            )

        records.append(
            {
                "lessonStepId": lesson_step_id,
                "status": "draft-from-docs",
                "learnerResponsePrompt": learner_prompt,
                "tutorNotePrompt": tutor_prompt,
                "fields": fields,
            }
        )
    return records


def attach_source_docs(records: list[dict], source_docs: list[str]) -> list[dict]:
    for record in records:
        record["sourceDocs"] = source_docs
    return records


def attach_error_watchers(lesson_steps: list[dict], error_patterns: list[dict]) -> None:
    watch_map = {record["skillId"]: record.get("watchFor", []) for record in error_patterns}
    for record in lesson_steps:
        lesson_step_id = record.get("lessonStepId", "")
        match = re.search(r"(U\d+-S[\w]+)", lesson_step_id)
        if match:
            record["watchFor"] = watch_map.get(match.group(1), [])


def write_json(path: Path, payload: list[dict], force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Re-run with --force to overwrite.")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    content_dir = resolve_repo_path(args.content_dir)
    source_note_path = resolve_repo_path(args.source_note)
    subskills_path = resolve_repo_path(args.subskills_doc)
    learning_design_path = resolve_repo_path(args.learning_design_doc)
    transcript_path = resolve_repo_path(args.transcript_doc) if args.transcript_doc else None
    project_context_path = resolve_repo_path(args.project_context_path)
    next_steps_path = resolve_repo_path(args.next_steps_path)

    slug = content_dir.name
    source_lines = load_lines(source_note_path)
    unit_id = find_inline_value(source_lines, "- Working unit id:")
    topic_ko = find_inline_value(source_lines, "- Korean topic label:")
    topic_en = find_inline_value(source_lines, "- English working label:")
    if unit_id is None or topic_ko is None or topic_en is None:
        raise ValueError("Source note must include working unit id, Korean topic label, and English working label bullets.")

    subskills_lines = load_lines(subskills_path)
    learning_lines = load_lines(learning_design_path)
    transcript_lines = load_lines(transcript_path) if transcript_path else None

    skills = attach_source_docs(parse_subskills(subskills_lines), [args.source_note, args.subskills_doc])
    recommendations = attach_source_docs(parse_recommendations(learning_lines), [args.subskills_doc, args.learning_design_doc])
    error_patterns = attach_source_docs(parse_error_patterns(learning_lines), [args.source_note, args.learning_design_doc])
    activities = attach_source_docs(parse_activities(learning_lines), [args.subskills_doc, args.learning_design_doc])
    transcripts = parse_transcripts(transcript_lines)
    lesson_steps = attach_source_docs(parse_lesson_steps(learning_lines, transcripts), [args.subskills_doc, args.learning_design_doc])
    attach_error_watchers(lesson_steps, error_patterns)
    rubrics = attach_source_docs(parse_evaluator_rubrics(learning_lines), [args.learning_design_doc])
    observation = attach_source_docs(parse_observation_focus(learning_lines, rubrics), [args.learning_design_doc])

    outputs = {
        "skills.json": skills,
        "recommendation-examples.json": recommendations,
        "error-patterns.json": error_patterns,
        "activity-recommendations.json": activities,
        "lesson-steps.json": lesson_steps,
        "evaluator-rubrics.json": rubrics,
        "observation-form-mappings.json": observation,
    }

    if args.dry_run:
        summary = {
            "contentDir": str(content_dir.relative_to(ROOT)),
            "generatedCounts": {name: len(records) for name, records in outputs.items()},
            "projectDocsUpdate": args.update_project_docs,
            "sampleIds": {
                "skills": [record["id"] for record in skills[:3]],
                "lessonSteps": [record["lessonStepId"] for record in lesson_steps[:3]],
                "requiredSignals": rubrics[0]["requiredSignals"] if rubrics else [],
            },
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    content_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for file_name, payload in outputs.items():
        output_path = content_dir / file_name
        write_json(output_path, payload, args.force)
        written.append(str(output_path.relative_to(ROOT)))
    if args.update_project_docs:
        update_project_context(project_context_path, unit_id, slug, topic_ko, topic_en, "draft-records-generated")
        update_next_steps(next_steps_path, unit_id, slug, "draft-records-generated")
        written.append(str(project_context_path.relative_to(ROOT)))
        written.append(str(next_steps_path.relative_to(ROOT)))

    print(json.dumps({"written": written}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
