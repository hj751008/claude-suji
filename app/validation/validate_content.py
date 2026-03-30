from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTENT_ROOT = ROOT / "app" / "content"
REQUIRED_CONTENT_FILES = (
    "skills.json",
    "prerequisites.json",
    "recommendation-examples.json",
    "error-patterns.json",
    "activity-recommendations.json",
    "lesson-steps.json",
    "evaluator-rubrics.json",
    "observation-form-mappings.json",
)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def discover_content_dirs() -> list[Path]:
    content_dirs: list[Path] = []
    for path in sorted(CONTENT_ROOT.iterdir()):
        if not path.is_dir():
            continue
        if path.name == "templates":
            continue
        if all((path / filename).exists() for filename in REQUIRED_CONTENT_FILES):
            content_dirs.append(path)
    return content_dirs


def require_source_docs(record: dict, label: str, errors: list[str]) -> None:
    source_docs = record.get("sourceDocs")
    if not isinstance(source_docs, list) or not source_docs:
        add_error(errors, f"{label} is missing non-empty sourceDocs.")


def reject_threshold_like_fields(record: dict, label: str, errors: list[str]) -> None:
    banned_keys = {
        "threshold",
        "thresholds",
        "score",
        "scores",
        "cutoff",
        "cutoffs",
        "minimumEvidence",
        "retryRule",
        "overrideRule",
    }
    overlap = banned_keys.intersection(record.keys())
    if overlap:
        names = ", ".join(sorted(overlap))
        add_error(errors, f"{label} contains threshold-like fields that are not approved: {names}.")


def validate_skills(skills: list[dict], errors: list[str]) -> set[str]:
    seen: set[str] = set()
    skill_ids: set[str] = set()

    for record in skills:
        skill_id = record.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            add_error(errors, "Skill record is missing a valid id.")
            continue
        if skill_id in seen:
            add_error(errors, f"Duplicate skill id found: {skill_id}.")
        seen.add(skill_id)
        skill_ids.add(skill_id)

        require_source_docs(record, f"Skill {skill_id}", errors)
        reject_threshold_like_fields(record, f"Skill {skill_id}", errors)

        parent_skill_id = record.get("parentSkillId")
        if parent_skill_id is not None and not isinstance(parent_skill_id, str):
            add_error(errors, f"Skill {skill_id} has an invalid parentSkillId.")

    for record in skills:
        skill_id = record.get("id")
        parent_skill_id = record.get("parentSkillId")
        if parent_skill_id and parent_skill_id not in skill_ids:
            add_error(errors, f"Skill {skill_id} references unknown parentSkillId {parent_skill_id}.")

    return skill_ids


def validate_prerequisites(prerequisites: list[dict], skill_ids: set[str], errors: list[str]) -> None:
    for index, record in enumerate(prerequisites, start=1):
        label = f"Prerequisite record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        prereq_id = record.get("prerequisiteSkillId")
        target_id = record.get("targetSkillId")
        relationship = record.get("relationship")
        approval_status = record.get("approvalStatus")

        if prereq_id not in skill_ids:
            add_error(errors, f"{label} references unknown prerequisiteSkillId {prereq_id}.")
        if target_id not in skill_ids:
            add_error(errors, f"{label} references unknown targetSkillId {target_id}.")
        if relationship not in {"REQUIRED", "HELPFUL", "UNDECIDED"}:
            add_error(errors, f"{label} has unsupported relationship {relationship}.")
        if approval_status not in {"approved", "provisional", "draft-from-docs", "UNDECIDED"}:
            add_error(errors, f"{label} is missing a safe approvalStatus.")


def validate_recommendations(recommendations: list[dict], skill_ids: set[str], errors: list[str]) -> None:
    for index, record in enumerate(recommendations, start=1):
        label = f"Recommendation record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        target_id = record.get("recommend")
        confidence = record.get("confidence")
        needs_review = record.get("needsReview")

        if target_id not in skill_ids:
            add_error(errors, f"{label} recommends unknown skill id {target_id}.")
        if confidence not in {"limited", "moderate", "high", "UNDECIDED"}:
            add_error(errors, f"{label} has unsupported confidence value {confidence}.")
        if not isinstance(needs_review, bool):
            add_error(errors, f"{label} must include a boolean needsReview flag.")


def validate_error_patterns(error_patterns: list[dict], skill_ids: set[str], errors: list[str]) -> None:
    seen: set[str] = set()

    for index, record in enumerate(error_patterns, start=1):
        label = f"Error pattern record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        pattern_id = record.get("id")
        skill_id = record.get("skillId")

        if not isinstance(pattern_id, str) or not pattern_id:
            add_error(errors, f"{label} is missing a valid id.")
        elif pattern_id in seen:
            add_error(errors, f"Duplicate error pattern id found: {pattern_id}.")
        else:
            seen.add(pattern_id)

        if skill_id not in skill_ids:
            add_error(errors, f"{label} references unknown skillId {skill_id}.")


def validate_activity_recommendations(activities: list[dict], skill_ids: set[str], errors: list[str]) -> None:
    seen: set[str] = set()

    for index, record in enumerate(activities, start=1):
        label = f"Activity recommendation record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        activity_id = record.get("activityId")
        skill_id = record.get("skillId")
        activity_type = record.get("activityType")

        if not isinstance(activity_id, str) or not activity_id:
            add_error(errors, f"{label} is missing a valid activityId.")
        elif activity_id in seen:
            add_error(errors, f"Duplicate activityId found: {activity_id}.")
        else:
            seen.add(activity_id)

        if skill_id not in skill_ids:
            add_error(errors, f"{label} references unknown skillId {skill_id}.")
        if activity_type not in {"dialogue-flow", "worked-bridge"}:
            add_error(errors, f"{label} has unsupported activityType {activity_type}.")


def validate_lesson_steps(lesson_steps: list[dict], activity_ids: set[str], errors: list[str]) -> None:
    seen: set[str] = set()

    for index, record in enumerate(lesson_steps, start=1):
        label = f"Lesson step record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        lesson_step_id = record.get("lessonStepId")
        activity_id = record.get("activityId")

        if not isinstance(lesson_step_id, str) or not lesson_step_id:
            add_error(errors, f"{label} is missing a valid lessonStepId.")
        elif lesson_step_id in seen:
            add_error(errors, f"Duplicate lessonStepId found: {lesson_step_id}.")
        else:
            seen.add(lesson_step_id)

        if activity_id not in activity_ids:
            add_error(errors, f"{label} references unknown activityId {activity_id}.")


def validate_evaluator_rubrics(rubrics: list[dict], lesson_step_ids: set[str], errors: list[str]) -> None:
    seen: set[str] = set()

    for index, record in enumerate(rubrics, start=1):
        label = f"Evaluator rubric record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        lesson_step_id = record.get("lessonStepId")
        required_signals = record.get("requiredSignals")
        signal_text_hints = record.get("signalTextHints")

        if lesson_step_id not in lesson_step_ids:
            add_error(errors, f"{label} references unknown lessonStepId {lesson_step_id}.")
        elif lesson_step_id in seen:
            add_error(errors, f"Duplicate evaluator rubric lessonStepId found: {lesson_step_id}.")
        else:
            seen.add(lesson_step_id)

        if not isinstance(required_signals, list) or not required_signals:
            add_error(errors, f"{label} must include a non-empty requiredSignals list.")
            continue

        if signal_text_hints is None:
            continue
        if not isinstance(signal_text_hints, dict):
            add_error(errors, f"{label} signalTextHints must be an object when provided.")
            continue

        for signal_name, hints in signal_text_hints.items():
            if signal_name not in required_signals:
                add_error(errors, f"{label} signalTextHints references unknown required signal {signal_name}.")
                continue
            if not isinstance(hints, list) or not hints:
                add_error(errors, f"{label} signalTextHints for {signal_name} must be a non-empty list.")
                continue
            if not all(isinstance(hint, str) and hint.strip() for hint in hints):
                add_error(errors, f"{label} signalTextHints for {signal_name} must contain only non-empty strings.")


def validate_observation_form_mappings(mappings: list[dict], lesson_step_ids: set[str], errors: list[str]) -> None:
    seen: set[str] = set()

    for index, record in enumerate(mappings, start=1):
        label = f"Observation form mapping record #{index}"
        require_source_docs(record, label, errors)
        reject_threshold_like_fields(record, label, errors)

        lesson_step_id = record.get("lessonStepId")
        fields = record.get("fields")

        if lesson_step_id not in lesson_step_ids:
            add_error(errors, f"{label} references unknown lessonStepId {lesson_step_id}.")
        elif lesson_step_id in seen:
            add_error(errors, f"Duplicate observation form mapping lessonStepId found: {lesson_step_id}.")
        else:
            seen.add(lesson_step_id)

        if not isinstance(fields, list) or not fields:
            add_error(errors, f"{label} must include a non-empty fields list.")


def main() -> int:
    errors: list[str] = []
    content_dirs = discover_content_dirs()
    if not content_dirs:
        add_error(errors, f"No content packs with the required schema were found under {CONTENT_ROOT}.")

    total_counts = {
        "skills": 0,
        "prerequisites": 0,
        "recommendations": 0,
        "error_patterns": 0,
        "activities": 0,
        "lesson_steps": 0,
        "evaluator_rubrics": 0,
        "observation_form_mappings": 0,
    }

    for content_dir in content_dirs:
        pack_errors: list[str] = []
        pack_label = f"[{content_dir.name}]"

        skills = load_json(content_dir / "skills.json")
        prerequisites = load_json(content_dir / "prerequisites.json")
        recommendations = load_json(content_dir / "recommendation-examples.json")
        error_patterns = load_json(content_dir / "error-patterns.json")
        activities = load_json(content_dir / "activity-recommendations.json")
        lesson_steps = load_json(content_dir / "lesson-steps.json")
        evaluator_rubrics = load_json(content_dir / "evaluator-rubrics.json")
        observation_form_mappings = load_json(content_dir / "observation-form-mappings.json")

        skill_ids = validate_skills(skills, pack_errors)
        validate_prerequisites(prerequisites, skill_ids, pack_errors)
        validate_recommendations(recommendations, skill_ids, pack_errors)
        validate_error_patterns(error_patterns, skill_ids, pack_errors)
        validate_activity_recommendations(activities, skill_ids, pack_errors)
        activity_ids = {record["activityId"] for record in activities if isinstance(record.get("activityId"), str)}
        validate_lesson_steps(lesson_steps, activity_ids, pack_errors)
        lesson_step_ids = {record["lessonStepId"] for record in lesson_steps if isinstance(record.get("lessonStepId"), str)}
        validate_evaluator_rubrics(evaluator_rubrics, lesson_step_ids, pack_errors)
        validate_observation_form_mappings(observation_form_mappings, lesson_step_ids, pack_errors)

        total_counts["skills"] += len(skills)
        total_counts["prerequisites"] += len(prerequisites)
        total_counts["recommendations"] += len(recommendations)
        total_counts["error_patterns"] += len(error_patterns)
        total_counts["activities"] += len(activities)
        total_counts["lesson_steps"] += len(lesson_steps)
        total_counts["evaluator_rubrics"] += len(evaluator_rubrics)
        total_counts["observation_form_mappings"] += len(observation_form_mappings)

        for message in pack_errors:
            add_error(errors, f"{pack_label} {message}")

    if errors:
        print("Validation failed:")
        for message in errors:
            print(f"- {message}")
        return 1

    print("Validation passed.")
    print(f"Content packs: {len(content_dirs)}")
    print(f"Skills: {total_counts['skills']}")
    print(f"Prerequisite links: {total_counts['prerequisites']}")
    print(f"Recommendation examples: {total_counts['recommendations']}")
    print(f"Error patterns: {total_counts['error_patterns']}")
    print(f"Activity recommendations: {total_counts['activities']}")
    print(f"Lesson steps: {total_counts['lesson_steps']}")
    print(f"Evaluator rubrics: {total_counts['evaluator_rubrics']}")
    print(f"Observation form mappings: {total_counts['observation_form_mappings']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
