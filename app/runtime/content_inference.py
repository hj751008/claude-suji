from __future__ import annotations

from app.runtime.content_loader import (
    infer_unit_id_from_activity_id,
    infer_unit_id_from_lesson_step_id,
    infer_unit_id_from_skill_id,
)


def infer_unit_id_from_step(step: dict | None) -> str | None:
    if not isinstance(step, dict):
        return None
    return (
        infer_unit_id_from_skill_id(step.get("skillId"))
        or infer_unit_id_from_lesson_step_id(step.get("lessonStepId"))
        or infer_unit_id_from_activity_id(step.get("activityId"))
    )


def infer_unit_id_from_session_state(session_state: dict | None) -> str | None:
    if not isinstance(session_state, dict):
        return None
    return (
        infer_unit_id_from_step(session_state.get("currentStep"))
        or infer_unit_id_from_step(session_state.get("nextStep"))
        or infer_unit_id_from_skill_id(session_state.get("targetSkillId"))
        or _infer_unit_id_from_steps(session_state.get("steps"))
    )


def infer_unit_id_from_learner_record(learner_record: dict | None) -> str | None:
    if not isinstance(learner_record, dict):
        return None

    active_session = learner_record.get("activeSession")
    inferred = infer_unit_id_from_session_state(active_session)
    if inferred is not None:
        return inferred

    sessions = learner_record.get("sessions", [])
    if isinstance(sessions, list):
        for session in reversed(sessions):
            inferred = infer_unit_id_from_session_state(session)
            if inferred is not None:
                return inferred

    latest_recommendations = learner_record.get("latestRecommendations", [])
    if isinstance(latest_recommendations, list):
        for recommendation in latest_recommendations:
            if not isinstance(recommendation, dict):
                continue
            inferred = infer_unit_id_from_skill_id(recommendation.get("targetSkillId"))
            if inferred is not None:
                return inferred
            payload = recommendation.get("sessionPayload", {})
            if isinstance(payload, dict):
                inferred = _infer_unit_id_from_steps(payload.get("steps"))
                if inferred is not None:
                    return inferred

    latest_skill_summaries = learner_record.get("latestSkillSummaries", [])
    if isinstance(latest_skill_summaries, list):
        for summary in latest_skill_summaries:
            if not isinstance(summary, dict):
                continue
            inferred = infer_unit_id_from_skill_id(summary.get("skillId"))
            if inferred is not None:
                return inferred

    evidence_events = learner_record.get("evidenceEvents", [])
    return infer_unit_id_from_events(evidence_events)


def infer_unit_id_from_event(event: dict | None) -> str | None:
    if not isinstance(event, dict):
        return None
    return (
        infer_unit_id_from_skill_id(event.get("skillId"))
        or infer_unit_id_from_lesson_step_id((event.get("derivedFrom") or {}).get("lessonStepId") if isinstance(event.get("derivedFrom"), dict) else None)
        or infer_unit_id_from_activity_id((event.get("derivedFrom") or {}).get("activityId") if isinstance(event.get("derivedFrom"), dict) else None)
    )


def infer_unit_id_from_events(events: list[dict] | None) -> str | None:
    if not isinstance(events, list):
        return None
    for event in events:
        inferred = infer_unit_id_from_event(event)
        if inferred is not None:
            return inferred
    return None


def infer_unit_id_from_transcript(transcript: dict | None, learner_record: dict | None = None) -> str | None:
    if not isinstance(transcript, dict):
        return infer_unit_id_from_learner_record(learner_record)

    inferred = infer_unit_id_from_skill_id(transcript.get("skillId"))
    if inferred is not None:
        return inferred

    turns = transcript.get("turns", [])
    if isinstance(turns, list):
        for turn in turns:
            if not isinstance(turn, dict):
                continue
            inferred = (
                infer_unit_id_from_lesson_step_id(turn.get("lessonStepId"))
                or infer_unit_id_from_step(turn.get("currentStep"))
            )
            if inferred is not None:
                return inferred

    return infer_unit_id_from_learner_record(learner_record)


def _infer_unit_id_from_steps(steps: list[dict] | None) -> str | None:
    if not isinstance(steps, list):
        return None
    for step in steps:
        inferred = infer_unit_id_from_step(step)
        if inferred is not None:
            return inferred
    return None
