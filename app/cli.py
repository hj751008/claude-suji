from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.runtime.content_inference import (
    infer_unit_id_from_event,
    infer_unit_id_from_events,
    infer_unit_id_from_learner_record,
    infer_unit_id_from_session_state,
    infer_unit_id_from_transcript,
)
from app.runtime.content_loader import load_content_for_unit, load_unit1_content, load_unit2_content
from app.runtime.diagnostics import diagnose_event, summarize_learner, validate_evidence_event
from app.runtime.learner_record import (
    merge_session_into_learner_record,
    prepare_observation_form_for_learner_record,
    run_learning_turn,
    store_active_session,
    submit_observation_to_learner_record,
    validate_learner_record,
)
from app.runtime.session_orchestrator import resume_or_plan_session, start_learning_session
from app.runtime.session_planner import plan_next_session
from app.runtime.session_runner import (
    advance_session_state,
    apply_evaluator_decision,
    build_observation_form_template,
    create_session_state,
    evaluate_current_step,
    observation_form_to_evaluation_input,
    session_history_to_evidence_events,
    submit_observation,
)
from app.validation.validate_content import main as validate_content_main


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _dump_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


_CONTENT_CACHE = {
    "U1": load_unit1_content,
    "U2": load_unit2_content,
}


def _load_content(unit_id: str | None):
    if unit_id in _CONTENT_CACHE:
        return _CONTENT_CACHE[unit_id]()
    if isinstance(unit_id, str):
        return load_content_for_unit(unit_id)
    return load_unit1_content()


def _load_content_for_event(event: dict):
    return _load_content(infer_unit_id_from_event(event))


def _load_content_for_events(events: list[dict]):
    return _load_content(infer_unit_id_from_events(events))


def _load_content_for_session_state(session_state: dict):
    return _load_content(infer_unit_id_from_session_state(session_state))


def _load_content_for_learner_record(learner_record: dict):
    return _load_content(infer_unit_id_from_learner_record(learner_record))


def _load_content_for_transcript(transcript: dict, learner_record: dict | None = None):
    return _load_content(infer_unit_id_from_transcript(transcript, learner_record))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal CLI for current content validation and learner diagnosis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-content", help="Validate app content files.")
    validate_learner_record_parser = subparsers.add_parser("validate-learner-record", help="Validate learner record structure and active session consistency.")
    validate_learner_record_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")

    diagnose_parser = subparsers.add_parser("diagnose", help="Diagnose one evidence input JSON file.")
    diagnose_parser.add_argument("--input", required=True, help="Path to the evidence event JSON file.")

    summarize_parser = subparsers.add_parser("summarize-learner", help="Summarize multiple evidence events for one learner.")
    summarize_parser.add_argument("--input", required=True, help="Path to a JSON array of evidence events.")

    start_session_parser = subparsers.add_parser("start-session", help="Create session state from one recommendation JSON object.")
    start_session_parser.add_argument("--input", required=True, help="Path to a recommendation JSON file.")

    advance_session_parser = subparsers.add_parser("advance-session", help="Advance session state by completing the current lesson step.")
    advance_session_parser.add_argument("--input", required=True, help="Path to a session state JSON file.")
    advance_session_parser.add_argument("--complete-step", required=True, help="Lesson step id to mark complete.")

    evaluate_parser = subparsers.add_parser("evaluate-step", help="Evaluate the current session step from learner response input.")
    evaluate_parser.add_argument("--session", required=True, help="Path to a session state JSON file.")
    evaluate_parser.add_argument("--input", required=True, help="Path to a step evaluation input JSON file.")
    evaluate_parser.add_argument("--apply", action="store_true", help="Apply completed decisions and auto-advance the session.")

    evaluate_form_parser = subparsers.add_parser("evaluate-form", help="Evaluate the current session step from an observation form input.")
    evaluate_form_parser.add_argument("--session", required=True, help="Path to a session state JSON file.")
    evaluate_form_parser.add_argument("--input", required=True, help="Path to an observation form JSON file.")
    evaluate_form_parser.add_argument("--apply", action="store_true", help="Apply completed decisions and auto-advance the session.")

    submit_observation_parser = subparsers.add_parser("submit-observation", help="Append an observation record, evaluate it, and update session state.")
    submit_observation_parser.add_argument("--session", required=True, help="Path to a session state JSON file.")
    submit_observation_parser.add_argument("--input", required=True, help="Path to an observation form JSON file.")

    submit_observation_record_parser = subparsers.add_parser(
        "submit-observation-to-learner-record",
        help="Submit an observation against learner_record.activeSession and refresh learner-level state.",
    )
    submit_observation_record_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")
    submit_observation_record_parser.add_argument("--input", required=True, help="Path to an observation form JSON file.")
    submit_observation_record_parser.add_argument("--write", action="store_true", help="Write the updated learner record back to the learner file.")

    run_learning_turn_parser = subparsers.add_parser(
        "run-learning-turn",
        help="Submit an observation to learner_record.activeSession and return an operator-friendly next-step summary.",
    )
    run_learning_turn_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")
    run_learning_turn_parser.add_argument("--input", required=True, help="Path to an observation form JSON file.")
    run_learning_turn_parser.add_argument("--write", action="store_true", help="Write the updated learner record back to the learner file.")

    prepare_observation_form_parser = subparsers.add_parser(
        "prepare-observation-form",
        help="Build a strict observation form draft from the current learner-record step and documented mappings only.",
    )
    prepare_observation_form_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")
    prepare_observation_form_parser.add_argument("--output", help="Optional path to write the observation form draft JSON.")

    session_summary_parser = subparsers.add_parser("summarize-session-history", help="Convert session history to learner evidence and summarize it.")
    session_summary_parser.add_argument("--session", required=True, help="Path to a session state JSON file.")

    update_learner_parser = subparsers.add_parser("update-learner-record", help="Merge a session state into a learner record.")
    update_learner_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")
    update_learner_parser.add_argument("--session", required=True, help="Path to a session state JSON file.")
    update_learner_parser.add_argument("--write", action="store_true", help="Write the updated learner record back to the learner file.")

    plan_session_parser = subparsers.add_parser("plan-next-session", help="Choose the next recommended session from a learner record.")
    plan_session_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")

    resume_or_plan_parser = subparsers.add_parser(
        "resume-or-plan",
        help="Resume an in-progress session when possible, otherwise plan the next session.",
    )
    resume_or_plan_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")

    sync_active_session_parser = subparsers.add_parser(
        "sync-active-session",
        help="Run resume-or-plan and store the resulting live session on the learner record.",
    )
    sync_active_session_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")
    sync_active_session_parser.add_argument("--write", action="store_true", help="Write the updated learner record back to the learner file.")

    start_learning_session_parser = subparsers.add_parser(
        "start-learning-session",
        help="Resume or plan a live session, store it as activeSession, and return the first-step guide.",
    )
    start_learning_session_parser.add_argument("--learner", required=True, help="Path to a learner record JSON file.")
    start_learning_session_parser.add_argument("--write", action="store_true", help="Write the updated learner record back to the learner file.")

    replay_transcript_parser = subparsers.add_parser(
        "replay-transcript",
        help="Replay a sample tutor transcript turn-by-turn against a learner record.",
    )
    replay_transcript_parser.add_argument("--transcript-file", required=True, help="Path to a transcript fixture JSON file.")
    replay_transcript_parser.add_argument("--transcript-id", required=True, help="Transcript id to replay from the fixture.")
    replay_transcript_parser.add_argument("--learner", help="Optional learner record path override.")
    replay_transcript_parser.add_argument(
        "--turn-limit",
        type=int,
        help="Optional maximum number of turns to replay from the start of the transcript.",
    )
    replay_transcript_parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Print transcript replay summaries without the final learner record payload.",
    )
    replay_transcript_parser.add_argument("--write", action="store_true", help="Write the updated learner record back to the learner file.")

    list_transcripts_parser = subparsers.add_parser(
        "list-transcripts",
        help="List available sample tutor transcripts from a fixture file.",
    )
    list_transcripts_parser.add_argument("--transcript-file", required=True, help="Path to a transcript fixture JSON file.")
    list_transcripts_parser.add_argument("--skill-id", help="Optional skill id filter.")
    list_transcripts_parser.add_argument("--tag", help="Optional tag filter.")

    serve_operator_ui_parser = subparsers.add_parser(
        "serve-operator-ui",
        help="Serve a local browser UI for transcript replay and operator handoff inspection.",
    )
    serve_operator_ui_parser.add_argument("--host", default="127.0.0.1", help="Host to bind the local UI server to.")
    serve_operator_ui_parser.add_argument("--port", type=int, default=8765, help="Port for the local UI server.")

    subparsers.add_parser("run-harness", help="Run the first Unit 1 harness.")
    return parser


def run_diagnose(input_path: Path) -> int:
    event = _load_json(input_path)
    errors = validate_evidence_event(event)
    if errors:
        print("Evidence validation failed:")
        for message in errors:
            print(f"- {message}")
        return 1

    content = _load_content_for_event(event)
    result = diagnose_event(content, event)
    payload = {
        "mastery": result.mastery,
        "recommendations": result.recommendations,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_harness() -> int:
    from app.harness.run_harness import main as harness_main

    return harness_main()


def run_validate_learner_record(learner_path: Path) -> int:
    learner_record = _load_json(learner_path)
    errors = validate_learner_record(learner_record)
    if errors:
        print("Learner record validation failed:")
        for message in errors:
            print(f"- {message}")
        return 1

    print("Learner record validation passed.")
    return 0


def run_start_session(input_path: Path) -> int:
    recommendation = _load_json(input_path)
    try:
        session_state = create_session_state(recommendation)
    except ValueError as exc:
        print(f"Session start failed: {exc}")
        return 1

    print(json.dumps(session_state, ensure_ascii=False, indent=2))
    return 0


def run_advance_session(input_path: Path, completed_step: str) -> int:
    session_state = _load_json(input_path)
    try:
        updated_state = advance_session_state(session_state, completed_step)
    except ValueError as exc:
        print(f"Session advance failed: {exc}")
        return 1

    print(json.dumps(updated_state, ensure_ascii=False, indent=2))
    return 0


def run_evaluate_step(session_path: Path, input_path: Path, apply_result: bool) -> int:
    session_state = _load_json(session_path)
    evaluation_input = _load_json(input_path)
    content = _load_content_for_session_state(session_state)
    try:
        evaluation_result = evaluate_current_step(session_state, evaluation_input, content.evaluator_rubrics)
        payload = evaluation_result if not apply_result else apply_evaluator_decision(session_state, evaluation_result)
    except ValueError as exc:
        print(f"Step evaluation failed: {exc}")
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_evaluate_form(session_path: Path, input_path: Path, apply_result: bool) -> int:
    session_state = _load_json(session_path)
    observation_form = _load_json(input_path)
    content = _load_content_for_session_state(session_state)
    try:
        evaluation_input = observation_form_to_evaluation_input(session_state, observation_form, content.observation_form_mappings)
        evaluation_result = evaluate_current_step(session_state, evaluation_input, content.evaluator_rubrics)
        payload = evaluation_result if not apply_result else apply_evaluator_decision(session_state, evaluation_result)
    except ValueError as exc:
        print(f"Observation-form evaluation failed: {exc}")
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_submit_observation(session_path: Path, input_path: Path) -> int:
    session_state = _load_json(session_path)
    observation_form = _load_json(input_path)
    content = _load_content_for_session_state(session_state)
    try:
        updated_state = submit_observation(
            session_state,
            observation_form,
            content.evaluator_rubrics,
            content.observation_form_mappings,
        )
    except ValueError as exc:
        print(f"Observation submission failed: {exc}")
        return 1

    print(json.dumps(updated_state, ensure_ascii=False, indent=2))
    return 0


def run_submit_observation_to_learner_record(learner_path: Path, input_path: Path, write_result: bool) -> int:
    learner_record = _load_json(learner_path)
    observation_form = _load_json(input_path)
    content = _load_content_for_learner_record(learner_record)
    try:
        updated_record = submit_observation_to_learner_record(learner_record, observation_form, content)
    except ValueError as exc:
        print(f"Learner-record observation submission failed: {exc}")
        return 1

    if write_result:
        _dump_json(learner_path, updated_record)

    print(json.dumps(updated_record, ensure_ascii=False, indent=2))
    return 0


def run_learning_turn_command(learner_path: Path, input_path: Path, write_result: bool) -> int:
    learner_record = _load_json(learner_path)
    observation_form = _load_json(input_path)
    content = _load_content_for_learner_record(learner_record)
    try:
        result = run_learning_turn(learner_record, observation_form, content)
        active_session = result["learnerRecord"].get("activeSession")
        if isinstance(active_session, dict):
            result["observationFormTemplate"] = build_observation_form_template(
                active_session,
                content.observation_form_mappings,
            )
    except ValueError as exc:
        print(f"Run-learning-turn failed: {exc}")
        return 1

    if write_result:
        _dump_json(learner_path, result["learnerRecord"])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_prepare_observation_form(learner_path: Path, output_path: Path | None) -> int:
    learner_record = _load_json(learner_path)
    content = _load_content_for_learner_record(learner_record)
    try:
        result = prepare_observation_form_for_learner_record(learner_record, content.observation_form_mappings)
    except ValueError as exc:
        print(f"Prepare-observation-form failed: {exc}")
        return 1

    if output_path is not None:
        _dump_json(output_path, result["observationForm"])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_summarize_session_history(session_path: Path) -> int:
    session_state = _load_json(session_path)
    content = _load_content_for_session_state(session_state)
    try:
        events = session_history_to_evidence_events(session_state)
        result = summarize_learner(content, events)
    except ValueError as exc:
        print(f"Session-history summary failed: {exc}")
        return 1

    payload = {
        "learnerId": result.learnerId,
        "events": events,
        "skillSummaries": result.skillSummaries,
        "recommendations": result.recommendations,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_update_learner_record(learner_path: Path, session_path: Path, write_result: bool) -> int:
    learner_record = _load_json(learner_path)
    session_state = _load_json(session_path)
    content = _load_content_for_session_state(session_state)
    try:
        updated_record = merge_session_into_learner_record(learner_record, session_state, content)
    except ValueError as exc:
        print(f"Learner record update failed: {exc}")
        return 1

    if write_result:
        _dump_json(learner_path, updated_record)

    print(json.dumps(updated_record, ensure_ascii=False, indent=2))
    return 0


def run_plan_next_session(learner_path: Path) -> int:
    learner_record = _load_json(learner_path)
    try:
        planned = plan_next_session(learner_record)
    except ValueError as exc:
        print(f"Next-session planning failed: {exc}")
        return 1

    print(json.dumps(planned, ensure_ascii=False, indent=2))
    return 0


def run_resume_or_plan(learner_path: Path) -> int:
    learner_record = _load_json(learner_path)
    try:
        result = resume_or_plan_session(learner_record)
    except ValueError as exc:
        print(f"Resume-or-plan failed: {exc}")
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_sync_active_session(learner_path: Path, write_result: bool) -> int:
    learner_record = _load_json(learner_path)
    try:
        orchestration_result = resume_or_plan_session(learner_record)
        updated_record = store_active_session(learner_record, orchestration_result)
    except ValueError as exc:
        print(f"Sync-active-session failed: {exc}")
        return 1

    if write_result:
        _dump_json(learner_path, updated_record)

    print(json.dumps(updated_record, ensure_ascii=False, indent=2))
    return 0


def run_start_learning_session(learner_path: Path, write_result: bool) -> int:
    learner_record = _load_json(learner_path)
    content = _load_content_for_learner_record(learner_record)
    try:
        result = start_learning_session(learner_record)
        result["observationFormTemplate"] = build_observation_form_template(
            result["activeSession"],
            content.observation_form_mappings,
        )
    except ValueError as exc:
        print(f"Start-learning-session failed: {exc}")
        return 1

    if write_result:
        _dump_json(learner_path, result["learnerRecord"])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_replay_transcript(
    transcript_path: Path,
    transcript_id: str,
    learner_override_path: Path | None,
    turn_limit: int | None,
    summary_only: bool,
    write_result: bool,
) -> int:
    transcripts = _load_json(transcript_path)
    if not isinstance(transcripts, list):
        print("Replay-transcript failed: transcript fixture must be a JSON array.")
        return 1

    transcript = next(
        (
            record
            for record in transcripts
            if isinstance(record, dict) and record.get("transcriptId") == transcript_id
        ),
        None,
    )
    if transcript is None:
        print(f"Replay-transcript failed: transcriptId {transcript_id!r} was not found.")
        return 1

    learner_file = learner_override_path
    if learner_file is None:
        transcript_learner = transcript.get("learnerFile")
        if not isinstance(transcript_learner, str) or not transcript_learner:
            print("Replay-transcript failed: transcript is missing learnerFile and no --learner override was provided.")
            return 1
        learner_file = Path(transcript_learner)

    learner_path = learner_file
    learner_record = _load_json(learner_path)
    turns = transcript.get("turns", [])
    if not isinstance(turns, list) or not turns:
        print("Replay-transcript failed: transcript must contain at least one turn.")
        return 1
    if turn_limit is not None and turn_limit <= 0:
        print("Replay-transcript failed: --turn-limit must be a positive integer.")
        return 1
    selected_turns = turns if turn_limit is None else turns[:turn_limit]

    content = _load_content_for_transcript(transcript, learner_record)
    turn_results: list[dict] = []

    try:
        if transcript.get("startBeforeTurns"):
            started = start_learning_session(learner_record)
            learner_record = started["learnerRecord"]

        for index, turn in enumerate(selected_turns):
            if not isinstance(turn, dict):
                raise ValueError(f"Transcript turn {index} must be an object.")
            observation_form = turn.get("observationFormInput")
            if not isinstance(observation_form, dict):
                raise ValueError(f"Transcript turn {index} is missing observationFormInput.")

            result = run_learning_turn(learner_record, observation_form, content)
            learner_record = result["learnerRecord"]
            turn_results.append(
                {
                    "turnIndex": turn.get("turnIndex", index + 1),
                    "lessonStepId": turn.get("lessonStepId"),
                    "messages": turn.get("messages", []),
                    "operatorNote": turn.get("operatorNote"),
                    "turnSummary": result.get("turnSummary", {}),
                }
            )
    except ValueError as exc:
        print(f"Replay-transcript failed: {exc}")
        return 1

    if write_result:
        _dump_json(learner_path, learner_record)

    payload = {
        "transcriptId": transcript.get("transcriptId"),
        "name": transcript.get("name"),
        "skillId": transcript.get("skillId"),
        "tags": transcript.get("tags", []),
        "learnerFile": str(learner_path),
        "turnCount": len(turns),
        "replayedTurnCount": len(turn_results),
        "turnResults": turn_results,
    }
    if not summary_only:
        payload["finalLearnerRecord"] = learner_record
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_list_transcripts(transcript_path: Path, skill_id_filter: str | None, tag_filter: str | None) -> int:
    transcripts = _load_json(transcript_path)
    if not isinstance(transcripts, list):
        print("List-transcripts failed: transcript fixture must be a JSON array.")
        return 1

    payload: list[dict] = []
    for record in transcripts:
        if not isinstance(record, dict):
            continue
        skill_id = record.get("skillId")
        tags = record.get("tags", [])
        if skill_id_filter is not None and skill_id != skill_id_filter:
            continue
        if tag_filter is not None:
            if not isinstance(tags, list) or tag_filter not in tags:
                continue
        turns = record.get("turns", [])
        payload.append(
            {
                "transcriptId": record.get("transcriptId"),
                "name": record.get("name"),
                "skillId": skill_id,
                "tags": tags,
                "learnerFile": record.get("learnerFile"),
                "turnCount": len(turns) if isinstance(turns, list) else 0,
                "startBeforeTurns": bool(record.get("startBeforeTurns")),
            }
        )

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_serve_operator_ui(host: str, port: int) -> int:
    from app.operator_ui_server import serve_operator_ui

    try:
        serve_operator_ui(host, port)
    except OSError as exc:
        print(f"Serve-operator-ui failed: {exc}")
        return 1
    return 0


def run_summarize_learner(input_path: Path) -> int:
    events = _load_json(input_path)
    if not isinstance(events, list):
        print("Learner summary input must be a JSON array of evidence events.")
        return 1

    content = _load_content_for_events(events)
    try:
        result = summarize_learner(content, events)
    except ValueError as exc:
        print(f"Learner summary failed: {exc}")
        return 1

    payload = {
        "learnerId": result.learnerId,
        "skillSummaries": result.skillSummaries,
        "recommendations": result.recommendations,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "validate-content":
        return validate_content_main()
    if args.command == "validate-learner-record":
        return run_validate_learner_record(Path(args.learner))
    if args.command == "diagnose":
        return run_diagnose(Path(args.input))
    if args.command == "summarize-learner":
        return run_summarize_learner(Path(args.input))
    if args.command == "start-session":
        return run_start_session(Path(args.input))
    if args.command == "advance-session":
        return run_advance_session(Path(args.input), args.complete_step)
    if args.command == "evaluate-step":
        return run_evaluate_step(Path(args.session), Path(args.input), args.apply)
    if args.command == "evaluate-form":
        return run_evaluate_form(Path(args.session), Path(args.input), args.apply)
    if args.command == "submit-observation":
        return run_submit_observation(Path(args.session), Path(args.input))
    if args.command == "submit-observation-to-learner-record":
        return run_submit_observation_to_learner_record(Path(args.learner), Path(args.input), args.write)
    if args.command == "run-learning-turn":
        return run_learning_turn_command(Path(args.learner), Path(args.input), args.write)
    if args.command == "prepare-observation-form":
        return run_prepare_observation_form(
            Path(args.learner),
            None if args.output is None else Path(args.output),
        )
    if args.command == "summarize-session-history":
        return run_summarize_session_history(Path(args.session))
    if args.command == "update-learner-record":
        return run_update_learner_record(Path(args.learner), Path(args.session), args.write)
    if args.command == "plan-next-session":
        return run_plan_next_session(Path(args.learner))
    if args.command == "resume-or-plan":
        return run_resume_or_plan(Path(args.learner))
    if args.command == "sync-active-session":
        return run_sync_active_session(Path(args.learner), args.write)
    if args.command == "start-learning-session":
        return run_start_learning_session(Path(args.learner), args.write)
    if args.command == "replay-transcript":
        return run_replay_transcript(
            Path(args.transcript_file),
            args.transcript_id,
            None if args.learner is None else Path(args.learner),
            args.turn_limit,
            args.summary_only,
            args.write,
        )
    if args.command == "list-transcripts":
        return run_list_transcripts(Path(args.transcript_file), args.skill_id, args.tag)
    if args.command == "serve-operator-ui":
        return run_serve_operator_ui(args.host, args.port)
    if args.command == "run-harness":
        return run_harness()

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
