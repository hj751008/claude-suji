from __future__ import annotations

import json
from pathlib import Path

from app.runtime.content_loader import load_unit1_content
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
    create_session_state,
    evaluate_current_step,
    observation_form_to_evaluation_input,
    session_history_to_evidence_events,
    submit_observation,
)


HARNESS_ROOT = Path(__file__).resolve().parent


def _load_cases() -> list[dict]:
    with (HARNESS_ROOT / "unit1_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_learner_summary_cases() -> list[dict]:
    with (HARNESS_ROOT / "learner_summary_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_session_runner_cases() -> list[dict]:
    with (HARNESS_ROOT / "session_runner_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_evaluator_cases() -> list[dict]:
    with (HARNESS_ROOT / "evaluator_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_observation_submission_cases() -> list[dict]:
    with (HARNESS_ROOT / "observation_submission_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_session_history_summary_cases() -> list[dict]:
    with (HARNESS_ROOT / "session_history_summary_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_learner_record_cases() -> list[dict]:
    with (HARNESS_ROOT / "learner_record_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_session_planner_cases() -> list[dict]:
    with (HARNESS_ROOT / "session_planner_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_session_orchestrator_cases() -> list[dict]:
    with (HARNESS_ROOT / "session_orchestrator_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_active_session_cases() -> list[dict]:
    with (HARNESS_ROOT / "active_session_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_learner_record_submission_cases() -> list[dict]:
    with (HARNESS_ROOT / "learner_record_submission_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_failure_cases() -> list[dict]:
    with (HARNESS_ROOT / "failure_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_start_learning_session_cases() -> list[dict]:
    with (HARNESS_ROOT / "start_learning_session_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_learning_turn_cases() -> list[dict]:
    with (HARNESS_ROOT / "learning_turn_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_prepare_observation_form_cases() -> list[dict]:
    with (HARNESS_ROOT / "prepare_observation_form_cases.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_transcript_fixture(transcript_file: str, transcript_id: str) -> dict:
    transcript_path = Path(HARNESS_ROOT.parent.parent, transcript_file)
    with transcript_path.open("r", encoding="utf-8") as handle:
        transcripts = json.load(handle)

    if not isinstance(transcripts, list):
        raise ValueError(f"Transcript fixture {transcript_file} must be a JSON array.")

    transcript = next(
        (
            record
            for record in transcripts
            if isinstance(record, dict) and record.get("transcriptId") == transcript_id
        ),
        None,
    )
    if transcript is None:
        raise ValueError(f"Transcript fixture {transcript_file} is missing transcriptId {transcript_id}.")
    return transcript


def _turn_sequence_from_case(case: dict) -> tuple[str, bool, list[dict] | None, dict | None]:
    transcript = None
    learner_file = case.get("learnerFile")
    start_before_turns = bool(case.get("startBeforeTurns"))
    turn_sequence = case.get("turnSequence")

    transcript_file = case.get("transcriptFile")
    transcript_id = case.get("transcriptId")
    if isinstance(transcript_file, str) and isinstance(transcript_id, str):
        transcript = _load_transcript_fixture(transcript_file, transcript_id)
        if learner_file is None:
            learner_file = transcript.get("learnerFile")
        start_before_turns = start_before_turns or bool(transcript.get("startBeforeTurns"))
        if turn_sequence is None:
            turns = transcript.get("turns", [])
            if not isinstance(turns, list) or not turns:
                raise ValueError(f"Transcript {transcript_id} must contain at least one turn.")
            turn_sequence = []
            for index, turn in enumerate(turns):
                if not isinstance(turn, dict):
                    raise ValueError(f"Transcript {transcript_id} turn {index} must be an object.")
                observation_form = turn.get("observationFormInput")
                if not isinstance(observation_form, dict):
                    raise ValueError(
                        f"Transcript {transcript_id} turn {index} is missing observationFormInput."
                    )
                turn_sequence.append(observation_form)

    if not isinstance(learner_file, str) or not learner_file:
        raise ValueError(f"{case['name']}: learnerFile is required.")

    if not isinstance(turn_sequence, list) or not turn_sequence:
        return learner_file, start_before_turns, None, transcript

    return learner_file, start_before_turns, turn_sequence, transcript


def _load_learner_record_from_case(case: dict, content=None) -> dict:
    if "transcriptFile" not in case or "transcriptId" not in case:
        learner_path = Path(HARNESS_ROOT.parent.parent, case["learnerFile"])
        with learner_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    if content is None:
        raise ValueError(f"{case['name']}: transcript-backed case requires content.")

    learner_file, start_before_turns, turn_sequence, _transcript = _turn_sequence_from_case(case)
    learner_path = Path(HARNESS_ROOT.parent.parent, learner_file)
    with learner_path.open("r", encoding="utf-8") as handle:
        learner_record = json.load(handle)

    if start_before_turns:
        started = start_learning_session(learner_record)
        learner_record = started["learnerRecord"]

    if turn_sequence:
        for observation_form in turn_sequence:
            result = run_learning_turn(learner_record, observation_form, content)
            learner_record = result["learnerRecord"]

    return learner_record


def _assert_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    event = case["event"]
    expected = case["expected"]

    validation_errors = validate_evidence_event(event)
    if validation_errors:
        return [f"{case['name']}: invalid evidence input: {'; '.join(validation_errors)}"]

    result = diagnose_event(content, event)
    recommendation_skill_ids = [record["targetSkillId"] for record in result.recommendations]
    activity_ids = [
        activity["activityId"]
        for record in result.recommendations
        for activity in record.get("recommendedActivities", [])
    ]
    lesson_step_ids = [
        step["lessonStepId"]
        for record in result.recommendations
        for step in record.get("sessionPayload", {}).get("steps", [])
    ]

    if result.mastery["skillId"] != expected["masterySkillId"]:
        failures.append(
            f"{case['name']}: expected mastery skill {expected['masterySkillId']}, got {result.mastery['skillId']}."
        )

    if result.mastery["status"] != expected["masteryStatus"]:
        failures.append(
            f"{case['name']}: expected mastery status {expected['masteryStatus']}, got {result.mastery['status']}."
        )

    if recommendation_skill_ids != expected["recommendationSkillIds"]:
        failures.append(
            f"{case['name']}: expected recommendations {expected['recommendationSkillIds']}, got {recommendation_skill_ids}."
        )
    if activity_ids != expected["activityIds"]:
        failures.append(
            f"{case['name']}: expected activity ids {expected['activityIds']}, got {activity_ids}."
        )
    if lesson_step_ids != expected["lessonStepIds"]:
        failures.append(
            f"{case['name']}: expected lesson step ids {expected['lessonStepIds']}, got {lesson_step_ids}."
        )

    return failures


def _assert_learner_summary_case(case: dict, content) -> list[str]:
    failures: list[str] = []

    try:
        result = summarize_learner(content, case["events"])
    except ValueError as exc:
        return [f"{case['name']}: learner summary failed unexpectedly: {exc}"]

    expected = case["expected"]
    actual_skill_ids = [record["skillId"] for record in result.skillSummaries]
    if actual_skill_ids != expected["skillIds"]:
        failures.append(
            f"{case['name']}: expected skill summaries {expected['skillIds']}, got {actual_skill_ids}."
        )

    for record in result.skillSummaries:
        expected_status = expected["statuses"].get(record["skillId"])
        if record["status"] != expected_status:
            failures.append(
                f"{case['name']}: expected {record['skillId']} status {expected_status}, got {record['status']}."
            )

    actual_required_blocked = [
        record["skillId"] for record in result.skillSummaries if record.get("hasRequiredPrerequisiteBlocker")
    ]
    if actual_required_blocked != expected["requiredBlockedSkills"]:
        failures.append(
            f"{case['name']}: expected required prerequisite blockers {expected['requiredBlockedSkills']}, got {actual_required_blocked}."
        )

    actual_helpful_blocked = [
        record["skillId"]
        for record in result.skillSummaries
        if record.get("blockedByPrerequisites") and not record.get("hasRequiredPrerequisiteBlocker")
    ]
    if actual_helpful_blocked != expected["helpfulBlockedSkills"]:
        failures.append(
            f"{case['name']}: expected helpful prerequisite blockers {expected['helpfulBlockedSkills']}, got {actual_helpful_blocked}."
        )

    actual_recommendation_skill_ids = [record["targetSkillId"] for record in result.recommendations]
    if actual_recommendation_skill_ids != expected["recommendationSkillIds"]:
        failures.append(
            f"{case['name']}: expected learner recommendations {expected['recommendationSkillIds']}, got {actual_recommendation_skill_ids}."
        )

    for record in result.recommendations:
        expected_next = expected["recommendedNextSkillIds"].get(record["targetSkillId"])
        actual_next = record.get("recommendedNextSkillIds")
        if actual_next != expected_next:
            failures.append(
                f"{case['name']}: expected next-skill chain {expected_next} for {record['targetSkillId']}, got {actual_next}."
            )
        expected_activity_sequence = expected["recommendedActivitySequenceIds"].get(record["targetSkillId"])
        actual_activity_sequence = [activity["activityId"] for activity in record.get("recommendedActivitySequence", [])]
        if actual_activity_sequence != expected_activity_sequence:
            failures.append(
                f"{case['name']}: expected activity sequence {expected_activity_sequence} for {record['targetSkillId']}, got {actual_activity_sequence}."
            )
        expected_session_steps = expected["sessionLessonStepIds"].get(record["targetSkillId"])
        actual_session_steps = [step["lessonStepId"] for step in record.get("sessionPayload", {}).get("steps", [])]
        if actual_session_steps != expected_session_steps:
            failures.append(
                f"{case['name']}: expected session lesson steps {expected_session_steps} for {record['targetSkillId']}, got {actual_session_steps}."
            )

    return failures


def _assert_session_runner_case(case: dict) -> list[str]:
    failures: list[str] = []
    recommendation_path = Path(HARNESS_ROOT.parent.parent, case["recommendationFile"])
    with recommendation_path.open("r", encoding="utf-8") as handle:
        recommendation = json.load(handle)

    state = create_session_state(recommendation)
    expected_start = case["expectedStart"]
    if state["status"] != expected_start["status"]:
        failures.append(f"{case['name']}: expected start status {expected_start['status']}, got {state['status']}.")
    if state["currentStep"]["lessonStepId"] != expected_start["currentLessonStepId"]:
        failures.append(
            f"{case['name']}: expected current step {expected_start['currentLessonStepId']}, got {state['currentStep']['lessonStepId']}."
        )
    actual_next = state["nextStep"]["lessonStepId"] if state["nextStep"] else None
    if actual_next != expected_start["nextLessonStepId"]:
        failures.append(f"{case['name']}: expected next step {expected_start['nextLessonStepId']}, got {actual_next}.")
    if state["remainingStepIds"] != expected_start["remainingStepIds"]:
        failures.append(
            f"{case['name']}: expected remaining ids {expected_start['remainingStepIds']}, got {state['remainingStepIds']}."
        )

    for advance_case in case["advanceSequence"]:
        state = advance_session_state(state, advance_case["completeStep"])
        expected = advance_case["expected"]
        actual_current = state["currentStep"]["lessonStepId"] if state["currentStep"] else None
        actual_next = state["nextStep"]["lessonStepId"] if state["nextStep"] else None

        if state["status"] != expected["status"]:
            failures.append(f"{case['name']}: expected advanced status {expected['status']}, got {state['status']}.")
        if actual_current != expected["currentLessonStepId"]:
            failures.append(
                f"{case['name']}: expected current step {expected['currentLessonStepId']}, got {actual_current}."
            )
        if actual_next != expected["nextLessonStepId"]:
            failures.append(f"{case['name']}: expected next step {expected['nextLessonStepId']}, got {actual_next}.")
        if state["completedStepIds"] != expected["completedStepIds"]:
            failures.append(
                f"{case['name']}: expected completed steps {expected['completedStepIds']}, got {state['completedStepIds']}."
            )

    return failures


def _assert_evaluator_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    session_path = Path(HARNESS_ROOT.parent.parent, case["sessionFile"])
    with session_path.open("r", encoding="utf-8") as handle:
        session_state = json.load(handle)

    if "observationFormInput" in case:
        evaluation_input = observation_form_to_evaluation_input(
            session_state,
            case["observationFormInput"],
            content.observation_form_mappings,
        )
    else:
        evaluation_input = case["evaluationInput"]

    evaluation_result = evaluate_current_step(session_state, evaluation_input, content.evaluator_rubrics)
    expected_eval = case["expectedEvaluation"]
    if evaluation_result["lessonStepId"] != expected_eval["lessonStepId"]:
        failures.append(
            f"{case['name']}: expected lesson step {expected_eval['lessonStepId']}, got {evaluation_result['lessonStepId']}."
        )
    if evaluation_result["decision"] != expected_eval["decision"]:
        failures.append(
            f"{case['name']}: expected decision {expected_eval['decision']}, got {evaluation_result['decision']}."
        )
    if evaluation_result["canAutoAdvance"] != expected_eval["canAutoAdvance"]:
        failures.append(
            f"{case['name']}: expected canAutoAdvance {expected_eval['canAutoAdvance']}, got {evaluation_result['canAutoAdvance']}."
        )

    applied_state = apply_evaluator_decision(session_state, evaluation_result)
    expected_state = case["expectedAppliedState"]
    actual_current = applied_state["currentStep"]["lessonStepId"] if applied_state["currentStep"] else None
    if applied_state["status"] != expected_state["status"]:
        failures.append(f"{case['name']}: expected applied status {expected_state['status']}, got {applied_state['status']}.")
    if actual_current != expected_state["currentLessonStepId"]:
        failures.append(
            f"{case['name']}: expected current step {expected_state['currentLessonStepId']}, got {actual_current}."
        )
    if applied_state["completedStepIds"] != expected_state["completedStepIds"]:
        failures.append(
            f"{case['name']}: expected completed ids {expected_state['completedStepIds']}, got {applied_state['completedStepIds']}."
        )

    return failures


def _assert_observation_submission_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    session_path = Path(HARNESS_ROOT.parent.parent, case["sessionFile"])
    with session_path.open("r", encoding="utf-8") as handle:
        session_state = json.load(handle)

    updated_state = submit_observation(
        session_state,
        case["observationFormInput"],
        content.evaluator_rubrics,
        content.observation_form_mappings,
    )
    expected = case["expected"]

    actual_current = updated_state["currentStep"]["lessonStepId"] if updated_state["currentStep"] else None
    if updated_state["status"] != expected["status"]:
        failures.append(f"{case['name']}: expected status {expected['status']}, got {updated_state['status']}.")
    if actual_current != expected["currentLessonStepId"]:
        failures.append(
            f"{case['name']}: expected current step {expected['currentLessonStepId']}, got {actual_current}."
        )
    if updated_state["completedStepIds"] != expected["completedStepIds"]:
        failures.append(
            f"{case['name']}: expected completed ids {expected['completedStepIds']}, got {updated_state['completedStepIds']}."
        )
    if len(updated_state.get("history", [])) != expected["historyCount"]:
        failures.append(
            f"{case['name']}: expected history count {expected['historyCount']}, got {len(updated_state.get('history', []))}."
        )
    if updated_state.get("history"):
        record = updated_state["history"][0]
        if record["lessonStepId"] != expected["historyLessonStepId"]:
            failures.append(
                f"{case['name']}: expected history lesson step {expected['historyLessonStepId']}, got {record['lessonStepId']}."
            )
        if record["evaluation"]["decision"] != expected["historyDecision"]:
            failures.append(
                f"{case['name']}: expected history decision {expected['historyDecision']}, got {record['evaluation']['decision']}."
            )

    return failures


def _assert_session_history_summary_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    session_path = Path(HARNESS_ROOT.parent.parent, case["sessionFile"])
    with session_path.open("r", encoding="utf-8") as handle:
        session_state = json.load(handle)

    updated_state = submit_observation(
        session_state,
        case["observationFormInput"],
        content.evaluator_rubrics,
        content.observation_form_mappings,
    )
    events = session_history_to_evidence_events(updated_state)
    result = summarize_learner(content, events)
    expected = case["expected"]

    if len(events) != expected["eventCount"]:
        failures.append(f"{case['name']}: expected event count {expected['eventCount']}, got {len(events)}.")

    actual_event_skill_ids = [event["skillId"] for event in events]
    if actual_event_skill_ids != expected["eventSkillIds"]:
        failures.append(
            f"{case['name']}: expected event skill ids {expected['eventSkillIds']}, got {actual_event_skill_ids}."
        )

    actual_summary_skill_ids = [record["skillId"] for record in result.skillSummaries]
    if actual_summary_skill_ids != expected["summarySkillIds"]:
        failures.append(
            f"{case['name']}: expected summary skill ids {expected['summarySkillIds']}, got {actual_summary_skill_ids}."
        )

    for record in result.skillSummaries:
        expected_status = expected["summaryStatuses"].get(record["skillId"])
        if record["status"] != expected_status:
            failures.append(
                f"{case['name']}: expected {record['skillId']} status {expected_status}, got {record['status']}."
            )

    return failures


def _assert_learner_record_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    learner_path = Path(HARNESS_ROOT.parent.parent, case["learnerFile"])
    with learner_path.open("r", encoding="utf-8") as handle:
        learner_record = json.load(handle)
    session_files = case.get("sessionFiles")
    if not isinstance(session_files, list) or not session_files:
        session_files = [case["sessionFile"]]

    updated_record = learner_record
    for session_file in session_files:
        session_path = Path(HARNESS_ROOT.parent.parent, session_file)
        with session_path.open("r", encoding="utf-8") as handle:
            session_state = json.load(handle)
        updated_record = merge_session_into_learner_record(updated_record, session_state, content)
    expected = case["expected"]

    if len(updated_record.get("sessions", [])) != expected["sessionCount"]:
        failures.append(
            f"{case['name']}: expected session count {expected['sessionCount']}, got {len(updated_record.get('sessions', []))}."
        )
    if len(updated_record.get("evidenceEvents", [])) != expected["evidenceEventCount"]:
        failures.append(
            f"{case['name']}: expected evidence count {expected['evidenceEventCount']}, got {len(updated_record.get('evidenceEvents', []))}."
        )

    actual_skill_ids = [record["skillId"] for record in updated_record.get("latestSkillSummaries", [])]
    if actual_skill_ids != expected["latestSkillIds"]:
        failures.append(
            f"{case['name']}: expected latest skill ids {expected['latestSkillIds']}, got {actual_skill_ids}."
        )

    for record in updated_record.get("latestSkillSummaries", []):
        expected_status = expected["latestStatuses"].get(record["skillId"])
        if record["status"] != expected_status:
            failures.append(
                f"{case['name']}: expected latest status {expected_status} for {record['skillId']}, got {record['status']}."
            )

    actual_recommendation_skill_ids = [record["targetSkillId"] for record in updated_record.get("latestRecommendations", [])]
    if actual_recommendation_skill_ids != expected["recommendationSkillIds"]:
        failures.append(
            f"{case['name']}: expected recommendation skill ids {expected['recommendationSkillIds']}, got {actual_recommendation_skill_ids}."
        )

    expected_session_target_skill_ids = expected.get("sessionTargetSkillIds")
    if expected_session_target_skill_ids is not None:
        actual_session_target_skill_ids = [
            record.get("targetSkillId")
            for record in updated_record.get("sessions", [])
            if isinstance(record, dict)
        ]
        if actual_session_target_skill_ids != expected_session_target_skill_ids:
            failures.append(
                f"{case['name']}: expected session target skill ids {expected_session_target_skill_ids}, got {actual_session_target_skill_ids}."
            )

    expected_next_skill_ids = expected.get("recommendationNextSkillIds", {})
    if expected_next_skill_ids:
        actual_next_skill_ids = {
            record.get("targetSkillId"): record.get("recommendedNextSkillIds", [])
            for record in updated_record.get("latestRecommendations", [])
            if isinstance(record, dict)
        }
        if actual_next_skill_ids != expected_next_skill_ids:
            failures.append(
                f"{case['name']}: expected recommendation next skill ids {expected_next_skill_ids}, got {actual_next_skill_ids}."
            )

    return failures


def _assert_session_planner_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    learner_record = _load_learner_record_from_case(case, content)

    planned = plan_next_session(learner_record)
    expected = case["expected"]

    if planned["plannedFromSkillId"] != expected["plannedFromSkillId"]:
        failures.append(
            f"{case['name']}: expected planned skill {expected['plannedFromSkillId']}, got {planned['plannedFromSkillId']}."
        )
    if planned["recommendedNextSkillIds"] != expected["recommendedNextSkillIds"]:
        failures.append(
            f"{case['name']}: expected next skill ids {expected['recommendedNextSkillIds']}, got {planned['recommendedNextSkillIds']}."
        )
    if planned["sessionPreview"]["firstLessonStepId"] != expected["firstLessonStepId"]:
        failures.append(
            f"{case['name']}: expected first lesson step {expected['firstLessonStepId']}, got {planned['sessionPreview']['firstLessonStepId']}."
        )
    if planned["sessionPreview"]["stepCount"] != expected["stepCount"]:
        failures.append(
            f"{case['name']}: expected step count {expected['stepCount']}, got {planned['sessionPreview']['stepCount']}."
        )

    return failures


def _assert_session_orchestrator_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    learner_record = _load_learner_record_from_case(case, content)

    result = resume_or_plan_session(learner_record)
    expected = case["expected"]

    if result["action"] != expected["action"]:
        failures.append(f"{case['name']}: expected action {expected['action']}, got {result['action']}.")

    if result["action"] == "resume_session":
        preview = result.get("resumePreview", {})
        if preview.get("targetSkillId") != expected["targetSkillId"]:
            failures.append(
                f"{case['name']}: expected resume target skill {expected['targetSkillId']}, got {preview.get('targetSkillId')}."
            )
        if preview.get("currentLessonStepId") != expected["currentLessonStepId"]:
            failures.append(
                f"{case['name']}: expected current lesson step {expected['currentLessonStepId']}, got {preview.get('currentLessonStepId')}."
            )
        if preview.get("remainingStepCount") != expected["remainingStepCount"]:
            failures.append(
                f"{case['name']}: expected remaining step count {expected['remainingStepCount']}, got {preview.get('remainingStepCount')}."
            )
    else:
        planned = result.get("plannedSession", {})
        preview = planned.get("sessionPreview", {})
        if planned.get("plannedFromSkillId") != expected["plannedFromSkillId"]:
            failures.append(
                f"{case['name']}: expected planned skill {expected['plannedFromSkillId']}, got {planned.get('plannedFromSkillId')}."
            )
        expected_next_skill_ids = expected.get("recommendedNextSkillIds")
        if expected_next_skill_ids is not None and planned.get("recommendedNextSkillIds") != expected_next_skill_ids:
            failures.append(
                f"{case['name']}: expected next skill ids {expected_next_skill_ids}, got {planned.get('recommendedNextSkillIds')}."
            )
        if preview.get("firstLessonStepId") != expected["firstLessonStepId"]:
            failures.append(
                f"{case['name']}: expected first lesson step {expected['firstLessonStepId']}, got {preview.get('firstLessonStepId')}."
            )

    return failures


def _assert_active_session_case(case: dict) -> list[str]:
    failures: list[str] = []
    learner_path = Path(HARNESS_ROOT.parent.parent, case["learnerFile"])
    with learner_path.open("r", encoding="utf-8") as handle:
        learner_record = json.load(handle)

    orchestration_result = resume_or_plan_session(learner_record)
    updated_record = store_active_session(learner_record, orchestration_result)
    expected = case["expected"]
    active_session = updated_record.get("activeSession")

    if active_session is None:
        return [f"{case['name']}: expected activeSession to be stored, but it was null."]

    if active_session.get("targetSkillId") != expected["targetSkillId"]:
        failures.append(
            f"{case['name']}: expected active session target skill {expected['targetSkillId']}, got {active_session.get('targetSkillId')}."
        )
    current_step = active_session.get("currentStep") or {}
    if current_step.get("lessonStepId") != expected["currentLessonStepId"]:
        failures.append(
            f"{case['name']}: expected current lesson step {expected['currentLessonStepId']}, got {current_step.get('lessonStepId')}."
        )
    if active_session.get("status") != expected["status"]:
        failures.append(
            f"{case['name']}: expected active session status {expected['status']}, got {active_session.get('status')}."
        )

    return failures


def _assert_learner_record_submission_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    learner_path = Path(HARNESS_ROOT.parent.parent, case["learnerFile"])
    with learner_path.open("r", encoding="utf-8") as handle:
        learner_record = json.load(handle)

    updated_record = submit_observation_to_learner_record(learner_record, case["observationFormInput"], content)
    expected = case["expected"]
    active_session = updated_record.get("activeSession") or {}
    active_current = (active_session.get("currentStep") or {}).get("lessonStepId")

    if active_session.get("targetSkillId") != expected["activeTargetSkillId"]:
        failures.append(
            f"{case['name']}: expected active target skill {expected['activeTargetSkillId']}, got {active_session.get('targetSkillId')}."
        )
    if active_current != expected["activeCurrentLessonStepId"]:
        failures.append(
            f"{case['name']}: expected active current step {expected['activeCurrentLessonStepId']}, got {active_current}."
        )
    if active_session.get("completedStepIds") != expected["activeCompletedStepIds"]:
        failures.append(
            f"{case['name']}: expected active completed ids {expected['activeCompletedStepIds']}, got {active_session.get('completedStepIds')}."
        )

    actual_recommendation_skill_ids = [record["targetSkillId"] for record in updated_record.get("latestRecommendations", [])]
    if actual_recommendation_skill_ids != expected["latestRecommendationSkillIds"]:
        failures.append(
            f"{case['name']}: expected latest recommendation ids {expected['latestRecommendationSkillIds']}, got {actual_recommendation_skill_ids}."
        )
    if len(updated_record.get("evidenceEvents", [])) != expected["evidenceEventCount"]:
        failures.append(
            f"{case['name']}: expected evidence event count {expected['evidenceEventCount']}, got {len(updated_record.get('evidenceEvents', []))}."
        )

    return failures


def _assert_failure_case(case: dict, content) -> list[str]:
    learner_record = None
    if "learnerFile" in case:
        learner_path = Path(HARNESS_ROOT.parent.parent, case["learnerFile"])
        with learner_path.open("r", encoding="utf-8") as handle:
            learner_record = json.load(handle)
    else:
        learner_record = case["learnerRecord"]

    try:
        if case["kind"].startswith("submit_observation_to_learner_record"):
            submit_observation_to_learner_record(learner_record, case["observationFormInput"], content)
        elif case["kind"] == "validate_learner_record":
            errors = validate_learner_record(learner_record)
            if not errors:
                return [f"{case['name']}: expected validation errors but validation passed."]
            combined = "; ".join(errors)
            if case["expectedErrorContains"] not in combined:
                return [
                    f"{case['name']}: expected validation error containing {case['expectedErrorContains']!r}, got {combined!r}."
                ]
            return []
        else:
            return [f"{case['name']}: unsupported failure case kind {case['kind']}."]
    except ValueError as exc:
        if case["expectedErrorContains"] not in str(exc):
            return [
                f"{case['name']}: expected error containing {case['expectedErrorContains']!r}, got {str(exc)!r}."
            ]
        return []

    return [f"{case['name']}: expected ValueError but the call succeeded."]


def _assert_start_learning_session_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    learner_record = _load_learner_record_from_case(case, content)

    result = start_learning_session(learner_record)
    expected = case["expected"]
    guide = result.get("sessionStartGuide", {})
    active_session = result.get("activeSession", {})

    if result.get("action") != expected["action"]:
        failures.append(f"{case['name']}: expected action {expected['action']}, got {result.get('action')}.")
    actual_session_target = guide.get("sessionTargetSkillId", guide.get("targetSkillId"))
    if actual_session_target != expected["targetSkillId"]:
        failures.append(
            f"{case['name']}: expected target skill {expected['targetSkillId']}, got {actual_session_target}."
        )
    if guide.get("currentLessonStepId") != expected["currentLessonStepId"]:
        failures.append(
            f"{case['name']}: expected current step {expected['currentLessonStepId']}, got {guide.get('currentLessonStepId')}."
        )
    if guide.get("firstTutorQuestion") != expected["firstTutorQuestion"]:
        failures.append(
            f"{case['name']}: expected first tutor question {expected['firstTutorQuestion']!r}, got {guide.get('firstTutorQuestion')!r}."
        )
    if guide.get("nextLessonStepId") != expected["nextLessonStepId"]:
        failures.append(
            f"{case['name']}: expected next lesson step {expected['nextLessonStepId']}, got {guide.get('nextLessonStepId')}."
        )
    if guide.get("remainingStepCount") != expected["remainingStepCount"]:
        failures.append(
            f"{case['name']}: expected remaining step count {expected['remainingStepCount']}, got {guide.get('remainingStepCount')}."
        )
    expected_current_skill = expected.get("currentStepSkillId")
    if expected_current_skill is not None and guide.get("currentStepSkillId") != expected_current_skill:
        failures.append(
            f"{case['name']}: expected current step skill {expected_current_skill}, got {guide.get('currentStepSkillId')}."
        )
    if active_session.get("targetSkillId") != expected["targetSkillId"]:
        failures.append(
            f"{case['name']}: expected active target skill {expected['targetSkillId']}, got {active_session.get('targetSkillId')}."
        )
    planned_preview = result.get("plannedSessionPreview", {})
    expected_planned_from = expected.get("plannedFromSkillId")
    if expected_planned_from is not None and planned_preview.get("plannedFromSkillId") != expected_planned_from:
        failures.append(
            f"{case['name']}: expected planned-from skill {expected_planned_from}, got {planned_preview.get('plannedFromSkillId')}."
        )
    expected_next_skill_ids = expected.get("recommendedNextSkillIds")
    if expected_next_skill_ids is not None and planned_preview.get("recommendedNextSkillIds") != expected_next_skill_ids:
        failures.append(
            f"{case['name']}: expected preview next skill ids {expected_next_skill_ids}, got {planned_preview.get('recommendedNextSkillIds')}."
        )

    return failures


def _assert_learning_turn_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    try:
        learner_file, start_before_turns, turn_sequence, _transcript = _turn_sequence_from_case(case)
    except ValueError as exc:
        return [f"{case['name']}: {exc}"]

    learner_path = Path(HARNESS_ROOT.parent.parent, learner_file)
    with learner_path.open("r", encoding="utf-8") as handle:
        learner_record = json.load(handle)

    if start_before_turns:
        started = start_learning_session(learner_record)
        learner_record = started["learnerRecord"]

    result = None
    if isinstance(turn_sequence, list) and turn_sequence:
        for observation_form in turn_sequence:
            result = run_learning_turn(learner_record, observation_form, content)
            learner_record = result["learnerRecord"]
    else:
        result = run_learning_turn(learner_record, case["observationFormInput"], content)
        learner_record = result["learnerRecord"]

    follow_up_turns = case.get("followUpTurnSequence")
    if case.get("restartAfterRecommendation"):
        restarted = start_learning_session(learner_record)
        learner_record = restarted["learnerRecord"]

    if isinstance(follow_up_turns, list) and follow_up_turns:
        for observation_form in follow_up_turns:
            result = run_learning_turn(learner_record, observation_form, content)
            learner_record = result["learnerRecord"]

    assert result is not None

    expected = case["expected"]
    turn_summary = result.get("turnSummary", {})

    if turn_summary.get("decision") != expected["decision"]:
        failures.append(
            f"{case['name']}: expected decision {expected['decision']}, got {turn_summary.get('decision')}."
        )
    if turn_summary.get("nextAction") != expected["nextAction"]:
        failures.append(
            f"{case['name']}: expected next action {expected['nextAction']}, got {turn_summary.get('nextAction')}."
        )
    if turn_summary.get("sessionStatus") != expected["sessionStatus"]:
        failures.append(
            f"{case['name']}: expected session status {expected['sessionStatus']}, got {turn_summary.get('sessionStatus')}."
        )

    if expected["nextAction"] == "continue_active_session":
        next_step_guide = turn_summary.get("nextStepGuide", {})
        if next_step_guide.get("currentLessonStepId") != expected["currentLessonStepId"]:
            failures.append(
                f"{case['name']}: expected next current step {expected['currentLessonStepId']}, got {next_step_guide.get('currentLessonStepId')}."
            )
        if next_step_guide.get("firstTutorQuestion") != expected["firstTutorQuestion"]:
            failures.append(
                f"{case['name']}: expected next first question {expected['firstTutorQuestion']!r}, got {next_step_guide.get('firstTutorQuestion')!r}."
            )
    else:
        next_session = turn_summary.get("nextRecommendedSession", {})
        actual_planned_from = next_session.get("plannedFromSkillId", next_session.get("targetSkillId"))
        if actual_planned_from != expected["targetSkillId"]:
            failures.append(
                f"{case['name']}: expected next recommended target skill {expected['targetSkillId']}, got {actual_planned_from}."
            )
        if next_session.get("firstLessonStepId") != expected["firstLessonStepId"]:
            failures.append(
                f"{case['name']}: expected first lesson step {expected['firstLessonStepId']}, got {next_session.get('firstLessonStepId')}."
            )

    final_session_count = expected.get("finalSessionCount")
    if final_session_count is not None and len(learner_record.get("sessions", [])) != final_session_count:
        failures.append(
            f"{case['name']}: expected final session count {final_session_count}, got {len(learner_record.get('sessions', []))}."
        )

    final_session_target_skill_ids = expected.get("finalSessionTargetSkillIds")
    if final_session_target_skill_ids is not None:
        actual_session_target_skill_ids = [
            record.get("targetSkillId")
            for record in learner_record.get("sessions", [])
            if isinstance(record, dict)
        ]
        if actual_session_target_skill_ids != final_session_target_skill_ids:
            failures.append(
                f"{case['name']}: expected final session target skill ids {final_session_target_skill_ids}, got {actual_session_target_skill_ids}."
            )

    final_evidence_event_count = expected.get("finalEvidenceEventCount")
    if final_evidence_event_count is not None and len(learner_record.get("evidenceEvents", [])) != final_evidence_event_count:
        failures.append(
            f"{case['name']}: expected final evidence event count {final_evidence_event_count}, got {len(learner_record.get('evidenceEvents', []))}."
        )

    final_skill_ids = expected.get("finalSkillIds")
    if final_skill_ids is not None:
        actual_skill_ids = [
            record.get("skillId")
            for record in learner_record.get("latestSkillSummaries", [])
            if isinstance(record, dict)
        ]
        if actual_skill_ids != final_skill_ids:
            failures.append(
                f"{case['name']}: expected final skill ids {final_skill_ids}, got {actual_skill_ids}."
            )

    final_supporting_evidence_counts = expected.get("finalSupportingEvidenceCounts")
    if final_supporting_evidence_counts is not None:
        actual_supporting_evidence_counts = {
            record.get("skillId"): len(record.get("supportingEvidenceIds", []))
            for record in learner_record.get("latestSkillSummaries", [])
            if isinstance(record, dict)
        }
        if actual_supporting_evidence_counts != final_supporting_evidence_counts:
            failures.append(
                f"{case['name']}: expected final supporting evidence counts {final_supporting_evidence_counts}, got {actual_supporting_evidence_counts}."
            )

    final_recommendation_skill_ids = expected.get("finalRecommendationSkillIds")
    if final_recommendation_skill_ids is not None:
        actual_recommendation_skill_ids = [
            record.get("targetSkillId")
            for record in learner_record.get("latestRecommendations", [])
            if isinstance(record, dict)
        ]
        if actual_recommendation_skill_ids != final_recommendation_skill_ids:
            failures.append(
                f"{case['name']}: expected final recommendation skill ids {final_recommendation_skill_ids}, got {actual_recommendation_skill_ids}."
            )

    final_recommendation_next_skill_ids = expected.get("finalRecommendationNextSkillIds")
    if final_recommendation_next_skill_ids is not None:
        actual_recommendation_next_skill_ids = {
            record.get("targetSkillId"): record.get("recommendedNextSkillIds", [])
            for record in learner_record.get("latestRecommendations", [])
            if isinstance(record, dict)
        }
        if actual_recommendation_next_skill_ids != final_recommendation_next_skill_ids:
            failures.append(
                f"{case['name']}: expected final recommendation next skill ids {final_recommendation_next_skill_ids}, got {actual_recommendation_next_skill_ids}."
            )

    return failures


def _assert_prepare_observation_form_case(case: dict, content) -> list[str]:
    failures: list[str] = []
    learner_record = _load_learner_record_from_case(case, content)

    if case.get("startBeforePrepare"):
        started = start_learning_session(learner_record)
        learner_record = started["learnerRecord"]

    prepared = prepare_observation_form_for_learner_record(learner_record, content.observation_form_mappings)
    expected = case["expected"]
    observation_form = prepared.get("observationForm", {})
    template = prepared.get("observationFormTemplate", {})

    if prepared.get("sourceLessonStepId") != expected["lessonStepId"]:
        failures.append(
            f"{case['name']}: expected lesson step {expected['lessonStepId']}, got {prepared.get('sourceLessonStepId')}."
        )
    if list(observation_form.get("fieldValues", {}).keys()) != expected["fieldIds"]:
        failures.append(
            f"{case['name']}: expected field ids {expected['fieldIds']}, got {list(observation_form.get('fieldValues', {}).keys())}."
        )
    if template.get("learnerResponsePrompt") != expected["learnerResponsePrompt"]:
        failures.append(
            f"{case['name']}: expected learner prompt {expected['learnerResponsePrompt']!r}, got {template.get('learnerResponsePrompt')!r}."
        )

    return failures


def main() -> int:
    content = load_unit1_content()
    cases = _load_cases()
    learner_summary_cases = _load_learner_summary_cases()
    session_runner_cases = _load_session_runner_cases()
    evaluator_cases = _load_evaluator_cases()
    observation_submission_cases = _load_observation_submission_cases()
    session_history_summary_cases = _load_session_history_summary_cases()
    learner_record_cases = _load_learner_record_cases()
    session_planner_cases = _load_session_planner_cases()
    session_orchestrator_cases = _load_session_orchestrator_cases()
    active_session_cases = _load_active_session_cases()
    learner_record_submission_cases = _load_learner_record_submission_cases()
    failure_cases = _load_failure_cases()
    start_learning_session_cases = _load_start_learning_session_cases()
    learning_turn_cases = _load_learning_turn_cases()
    prepare_observation_form_cases = _load_prepare_observation_form_cases()

    failures: list[str] = []
    for case in cases:
        failures.extend(_assert_case(case, content))
    for case in learner_summary_cases:
        failures.extend(_assert_learner_summary_case(case, content))
    for case in session_runner_cases:
        failures.extend(_assert_session_runner_case(case))
    for case in evaluator_cases:
        failures.extend(_assert_evaluator_case(case, content))
    for case in observation_submission_cases:
        failures.extend(_assert_observation_submission_case(case, content))
    for case in session_history_summary_cases:
        failures.extend(_assert_session_history_summary_case(case, content))
    for case in learner_record_cases:
        failures.extend(_assert_learner_record_case(case, content))
    for case in session_planner_cases:
        failures.extend(_assert_session_planner_case(case, content))
    for case in session_orchestrator_cases:
        failures.extend(_assert_session_orchestrator_case(case, content))
    for case in active_session_cases:
        failures.extend(_assert_active_session_case(case))
    for case in learner_record_submission_cases:
        failures.extend(_assert_learner_record_submission_case(case, content))
    for case in failure_cases:
        failures.extend(_assert_failure_case(case, content))
    for case in start_learning_session_cases:
        failures.extend(_assert_start_learning_session_case(case, content))
    for case in learning_turn_cases:
        failures.extend(_assert_learning_turn_case(case, content))
    for case in prepare_observation_form_cases:
        failures.extend(_assert_prepare_observation_form_case(case, content))

    if failures:
        print("Harness failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Harness passed.")
    print(f"Single-event cases: {len(cases)}")
    print(f"Learner-summary cases: {len(learner_summary_cases)}")
    print(f"Session-runner cases: {len(session_runner_cases)}")
    print(f"Evaluator cases: {len(evaluator_cases)}")
    print(f"Observation-submission cases: {len(observation_submission_cases)}")
    print(f"Session-history summary cases: {len(session_history_summary_cases)}")
    print(f"Learner-record cases: {len(learner_record_cases)}")
    print(f"Session-planner cases: {len(session_planner_cases)}")
    print(f"Session-orchestrator cases: {len(session_orchestrator_cases)}")
    print(f"Active-session cases: {len(active_session_cases)}")
    print(f"Learner-record submission cases: {len(learner_record_submission_cases)}")
    print(f"Failure cases: {len(failure_cases)}")
    print(f"Start-learning-session cases: {len(start_learning_session_cases)}")
    print(f"Learning-turn cases: {len(learning_turn_cases)}")
    print(f"Prepare-observation-form cases: {len(prepare_observation_form_cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
