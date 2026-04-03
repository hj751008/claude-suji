from __future__ import annotations

from pathlib import Path


AUTO_PIPELINE_HEADING = "## Auto-Managed Unit Pipeline"
AUTO_PIPELINE_START = "<!-- AUTO-MANAGED-UNIT-PIPELINE START -->"
AUTO_PIPELINE_END = "<!-- AUTO-MANAGED-UNIT-PIPELINE END -->"

AUTO_ACTIONS_HEADING = "## Auto-Managed Unit Actions"
AUTO_ACTIONS_START = "<!-- AUTO-MANAGED-UNIT-ACTIONS START -->"
AUTO_ACTIONS_END = "<!-- AUTO-MANAGED-UNIT-ACTIONS END -->"


def _normalize_markdown(text: str) -> str:
    normalized = text.replace("\r\n", "\n").strip()
    return normalized + "\n"


def _unit_block(unit_id: str, body: str) -> str:
    return "\n".join(
        [
            f"<!-- UNIT:{unit_id} START -->",
            body.strip(),
            f"<!-- UNIT:{unit_id} END -->",
        ]
    )


def _upsert_unit_block(section_body: str, unit_id: str, block_body: str) -> str:
    start_marker = f"<!-- UNIT:{unit_id} START -->"
    end_marker = f"<!-- UNIT:{unit_id} END -->"
    new_block = _unit_block(unit_id, block_body)

    if start_marker in section_body and end_marker in section_body:
        start = section_body.index(start_marker)
        end = section_body.index(end_marker) + len(end_marker)
        updated = section_body[:start] + new_block + section_body[end:]
        return updated.strip()

    stripped = section_body.strip()
    if not stripped:
        return new_block
    return stripped + "\n\n" + new_block


def _upsert_auto_section(path: Path, heading: str, start_marker: str, end_marker: str, unit_id: str, block_body: str) -> None:
    text = _normalize_markdown(path.read_text(encoding="utf-8")) if path.exists() else ""
    if text and not text.endswith("\n"):
        text += "\n"

    managed_body = _upsert_unit_block(_extract_section_body(text, heading, start_marker, end_marker), unit_id, block_body)
    managed_section = "\n".join([heading, start_marker, managed_body, end_marker]).strip() + "\n"

    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        heading_start = text.rfind(heading, 0, start)
        replace_start = heading_start if heading_start != -1 else start
        replace_end = text.index(end_marker) + len(end_marker)
        if replace_end < len(text) and text[replace_end] == "\n":
            replace_end += 1
        updated_text = text[:replace_start].rstrip() + "\n\n" + managed_section
        if replace_end < len(text):
            updated_text += "\n" + text[replace_end:].lstrip()
    else:
        updated_text = text.rstrip()
        if updated_text:
            updated_text += "\n\n"
        updated_text += managed_section

    path.write_text(_normalize_markdown(updated_text), encoding="utf-8")


def _extract_section_body(text: str, heading: str, start_marker: str, end_marker: str) -> str:
    if start_marker in text and end_marker in text:
        start = text.index(start_marker) + len(start_marker)
        end = text.index(end_marker)
        return text[start:end].strip()
    return ""


def update_project_context(project_context_path: Path, unit_id: str, slug: str, topic_ko: str, topic_en: str, stage: str) -> None:
    block_body = "\n".join(
        [
            f"### {unit_id} `{topic_ko}`",
            f"- Slug: `{slug}`",
            f"- English label: `{topic_en}`",
            f"- Auto-managed stage: `{stage}`",
        ]
    )
    _upsert_auto_section(
        project_context_path,
        AUTO_PIPELINE_HEADING,
        AUTO_PIPELINE_START,
        AUTO_PIPELINE_END,
        unit_id,
        block_body,
    )


def update_next_steps(next_steps_path: Path, unit_id: str, slug: str, stage: str) -> None:
    if stage == "scaffold-created":
        stage_note = "Fill source-backed docs before generating draft JSON."
    elif stage == "draft-records-generated":
        stage_note = "Review generated drafts, then decide on prerequisites/runtime/harness work."
    elif stage == "source-backed-provisional":
        stage_note = "Source-backed provisional records exist. Decide whether runtime wiring, transcript fixtures, and harness coverage should be added next."
    elif stage == "runtime-gate-passed":
        stage_note = "Runtime activation gate passed. Runtime wiring and harness activation can now land in the same reviewed change."
    elif stage == "runtime-gate-blocked":
        stage_note = "Runtime activation gate is still blocked. Resolve the listed loader, transcript-fixture, and harness gaps before wiring the unit into runtime."
    else:
        stage_note = "Review the current unit-pack state before the next automation step."

    block_body = "\n".join(
        [
            f"### {unit_id} `{slug}`",
            f"1. Current stage: `{stage}`.",
            f"2. {stage_note}",
            "3. Run `python app/cli.py validate-content` after the next meaningful content change.",
        ]
    )
    _upsert_auto_section(
        next_steps_path,
        AUTO_ACTIONS_HEADING,
        AUTO_ACTIONS_START,
        AUTO_ACTIONS_END,
        unit_id,
        block_body,
    )
