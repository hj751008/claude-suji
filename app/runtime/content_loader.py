from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
UNIT1_DIR = APP_ROOT / "content" / "unit1-prime-factorization"
UNIT2_DIR = APP_ROOT / "content" / "unit2-scaffold"


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@dataclass(frozen=True)
class UnitContent:
    skills: list[dict]
    prerequisites: list[dict]
    recommendation_examples: list[dict]
    error_patterns: list[dict]
    activity_recommendations: list[dict]
    lesson_steps: list[dict]
    evaluator_rubrics: list[dict]
    observation_form_mappings: list[dict]


def normalize_unit_id(unit_id: str) -> str:
    value = unit_id.strip().upper()
    if not re.fullmatch(r"U\d+", value):
        raise ValueError(f"Unsupported unit id {unit_id!r}.")
    return value


def infer_unit_id_from_skill_id(skill_id: str | None) -> str | None:
    if not isinstance(skill_id, str):
        return None
    match = re.match(r"^(U\d+)-", skill_id.strip().upper())
    return None if match is None else match.group(1)


def infer_unit_id_from_lesson_step_id(lesson_step_id: str | None) -> str | None:
    if not isinstance(lesson_step_id, str):
        return None
    match = re.match(r"^STEP-(U\d+)-", lesson_step_id.strip().upper())
    return None if match is None else match.group(1)


def infer_unit_id_from_activity_id(activity_id: str | None) -> str | None:
    if not isinstance(activity_id, str):
        return None
    match = re.match(r"^ACT-(U\d+)-", activity_id.strip().upper())
    return None if match is None else match.group(1)


def _load_content_dir(content_dir: Path) -> UnitContent:
    return UnitContent(
        skills=_load_json(content_dir / "skills.json"),
        prerequisites=_load_json(content_dir / "prerequisites.json"),
        recommendation_examples=_load_json(content_dir / "recommendation-examples.json"),
        error_patterns=_load_json(content_dir / "error-patterns.json"),
        activity_recommendations=_load_json(content_dir / "activity-recommendations.json"),
        lesson_steps=_load_json(content_dir / "lesson-steps.json"),
        evaluator_rubrics=_load_json(content_dir / "evaluator-rubrics.json"),
        observation_form_mappings=_load_json(content_dir / "observation-form-mappings.json"),
    )


def load_content_for_unit(unit_id: str) -> UnitContent:
    normalized = normalize_unit_id(unit_id)
    content_dirs = {
        "U1": UNIT1_DIR,
        "U2": UNIT2_DIR,
    }
    content_dir = content_dirs.get(normalized)
    if content_dir is None:
        raise ValueError(f"No content pack is registered for {normalized}.")
    return _load_content_dir(content_dir)


def load_unit1_content() -> UnitContent:
    return load_content_for_unit("U1")


def load_unit2_content() -> UnitContent:
    return load_content_for_unit("U2")
