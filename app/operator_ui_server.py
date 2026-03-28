from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from app.runtime.content_loader import load_unit1_content
from app.runtime.learner_record import prepare_observation_form_for_learner_record, run_learning_turn
from app.runtime.session_orchestrator import start_learning_session


APP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = APP_ROOT.parent
STATIC_ROOT = APP_ROOT / "operator_ui"
DEFAULT_TRANSCRIPT_FILE = APP_ROOT / "domain" / "evidence" / "unit1-tutor-transcripts.example.json"
EVIDENCE_ROOT = APP_ROOT / "domain" / "evidence"
EXPORT_ROOT = REPO_ROOT / "output" / "operator-logs"


def serve_operator_ui(host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), OperatorUiHandler)
    print(f"Operator UI running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nOperator UI stopped.")
    finally:
        server.server_close()


class OperatorUiHandler(BaseHTTPRequestHandler):
    server_version = "SujiOperatorUI/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_static("index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return
        if parsed.path == "/app.js":
            self._serve_static("app.js", "application/javascript; charset=utf-8")
            return
        if parsed.path == "/styles.css":
            self._serve_static("styles.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/api/bootstrap":
            self._handle_bootstrap()
            return

        self._json_response(HTTPStatus.NOT_FOUND, {"error": f"Unknown path: {parsed.path}"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self._read_json_body()
            if parsed.path == "/api/load-learner-record":
                self._handle_load_learner_record(payload)
                return
            if parsed.path == "/api/replay-transcript":
                self._handle_replay_transcript(payload)
                return
            if parsed.path == "/api/start-learning-session":
                self._handle_start_learning_session(payload)
                return
            if parsed.path == "/api/prepare-observation-form":
                self._handle_prepare_observation_form(payload)
                return
            if parsed.path == "/api/run-learning-turn":
                self._handle_run_learning_turn(payload)
                return
            if parsed.path == "/api/save-operator-log":
                self._handle_save_operator_log(payload)
                return
        except ValueError as exc:
            self._json_response(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        self._json_response(HTTPStatus.NOT_FOUND, {"error": f"Unknown path: {parsed.path}"})

    def log_message(self, format: str, *args) -> None:
        return

    def _serve_static(self, name: str, content_type: str) -> None:
        path = STATIC_ROOT / name
        if not path.is_file():
            self._json_response(HTTPStatus.NOT_FOUND, {"error": f"Missing static file: {name}"})
            return

        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            raise ValueError("Missing Content-Length header.")
        raw = self.rfile.read(int(content_length))
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON body: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object.")
        return payload

    def _json_response(self, status: HTTPStatus, payload: dict | list) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_bootstrap(self) -> None:
        learner_files = [
            str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            for path in sorted(EVIDENCE_ROOT.glob("learner-record*.json"))
            if path.is_file()
        ]
        self._json_response(
            HTTPStatus.OK,
            {
                "transcriptFile": str(DEFAULT_TRANSCRIPT_FILE.relative_to(REPO_ROOT)).replace("\\", "/"),
                "transcripts": _list_transcripts(DEFAULT_TRANSCRIPT_FILE),
                "learnerFiles": learner_files,
            },
        )

    def _handle_load_learner_record(self, payload: dict) -> None:
        learner_file = payload.get("learnerFile")
        if not isinstance(learner_file, str) or not learner_file:
            raise ValueError("learnerFile is required.")
        learner_path = _resolve_repo_path(learner_file)
        learner_record = _load_json(learner_path)
        if not isinstance(learner_record, dict):
            raise ValueError("Learner file must contain a JSON object.")
        self._json_response(
            HTTPStatus.OK,
            {
                "learnerFile": str(learner_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "learnerRecord": learner_record,
            },
        )

    def _handle_replay_transcript(self, payload: dict) -> None:
        transcript_file = payload.get("transcriptFile")
        transcript_id = payload.get("transcriptId")
        turn_limit = payload.get("turnLimit")

        if not isinstance(transcript_file, str) or not transcript_file:
            raise ValueError("transcriptFile is required.")
        if not isinstance(transcript_id, str) or not transcript_id:
            raise ValueError("transcriptId is required.")
        if turn_limit is not None and (not isinstance(turn_limit, int) or turn_limit <= 0):
            raise ValueError("turnLimit must be a positive integer when provided.")

        result = _replay_transcript(_resolve_repo_path(transcript_file), transcript_id, turn_limit)
        self._json_response(HTTPStatus.OK, result)

    def _handle_start_learning_session(self, payload: dict) -> None:
        learner_record = payload.get("learnerRecord")
        if not isinstance(learner_record, dict):
            raise ValueError("learnerRecord is required.")

        content = load_unit1_content()
        result = start_learning_session(learner_record)
        result["observationFormTemplate"] = prepare_observation_form_for_learner_record(
            result["learnerRecord"],
            content.observation_form_mappings,
        )["observationFormTemplate"]
        self._json_response(HTTPStatus.OK, result)

    def _handle_prepare_observation_form(self, payload: dict) -> None:
        learner_record = payload.get("learnerRecord")
        if not isinstance(learner_record, dict):
            raise ValueError("learnerRecord is required.")
        content = load_unit1_content()
        result = prepare_observation_form_for_learner_record(learner_record, content.observation_form_mappings)
        self._json_response(HTTPStatus.OK, result)

    def _handle_run_learning_turn(self, payload: dict) -> None:
        learner_record = payload.get("learnerRecord")
        observation_form = payload.get("observationForm")
        if not isinstance(learner_record, dict):
            raise ValueError("learnerRecord is required.")
        if not isinstance(observation_form, dict):
            raise ValueError("observationForm is required.")

        content = load_unit1_content()
        result = run_learning_turn(learner_record, observation_form, content)
        active_session = result["learnerRecord"].get("activeSession")
        if isinstance(active_session, dict):
            prepared = prepare_observation_form_for_learner_record(
                result["learnerRecord"],
                content.observation_form_mappings,
            )
            result["observationFormTemplate"] = prepared["observationFormTemplate"]
            result["observationForm"] = prepared["observationForm"]
        self._json_response(HTTPStatus.OK, result)

    def _handle_save_operator_log(self, payload: dict) -> None:
        bundle = payload.get("bundle")
        filename = payload.get("filename")
        if not isinstance(bundle, dict):
            raise ValueError("bundle is required.")
        if filename is not None and not isinstance(filename, str):
            raise ValueError("filename must be a string when provided.")

        transcript_id = bundle.get("selectedTranscriptId")
        learner_id = None
        learner_record = bundle.get("currentLearnerRecord")
        if isinstance(learner_record, dict):
            learner_id = learner_record.get("learnerId")
        stem = _slugify(filename or transcript_id or learner_id or "operator-log")
        if not stem:
            stem = "operator-log"

        exported_at = bundle.get("exportedAt")
        suffix = _timestamp_slug(exported_at) if isinstance(exported_at, str) else "unknown-time"
        EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
        target = EXPORT_ROOT / f"{stem}-{suffix}.json"
        with target.open("w", encoding="utf-8") as handle:
            json.dump(bundle, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

        self._json_response(
            HTTPStatus.OK,
            {
                "saved": True,
                "path": str(target.relative_to(REPO_ROOT)).replace("\\", "/"),
            },
        )


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _slugify(value: str) -> str:
    allowed = []
    for character in value.lower():
        if character.isalnum():
            allowed.append(character)
        elif character in {"-", "_"}:
            allowed.append(character)
        else:
            allowed.append("-")
    return "".join(allowed).strip("-_")


def _timestamp_slug(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value).strip("-")


def _resolve_repo_path(raw_path: str) -> Path:
    candidate = Path(raw_path)
    path = candidate if candidate.is_absolute() else (REPO_ROOT / candidate)
    resolved = path.resolve()
    if REPO_ROOT not in resolved.parents and resolved != REPO_ROOT:
        raise ValueError("Path must stay inside the repository.")
    if not resolved.exists():
        raise ValueError(f"Path does not exist: {raw_path}")
    return resolved


def _list_transcripts(transcript_path: Path) -> list[dict]:
    transcripts = _load_json(transcript_path)
    if not isinstance(transcripts, list):
        raise ValueError("Transcript fixture must be a JSON array.")

    payload: list[dict] = []
    for record in transcripts:
        if not isinstance(record, dict):
            continue
        turns = record.get("turns", [])
        payload.append(
            {
                "transcriptId": record.get("transcriptId"),
                "name": record.get("name"),
                "skillId": record.get("skillId"),
                "tags": record.get("tags", []),
                "learnerFile": record.get("learnerFile"),
                "turnCount": len(turns) if isinstance(turns, list) else 0,
                "startBeforeTurns": bool(record.get("startBeforeTurns")),
            }
        )
    return payload


def _replay_transcript(transcript_path: Path, transcript_id: str, turn_limit: int | None) -> dict:
    transcripts = _load_json(transcript_path)
    if not isinstance(transcripts, list):
        raise ValueError("Transcript fixture must be a JSON array.")

    transcript = next(
        (
            record
            for record in transcripts
            if isinstance(record, dict) and record.get("transcriptId") == transcript_id
        ),
        None,
    )
    if transcript is None:
        raise ValueError(f"Transcript id {transcript_id!r} was not found.")

    learner_file = transcript.get("learnerFile")
    if not isinstance(learner_file, str) or not learner_file:
        raise ValueError("Transcript is missing learnerFile.")

    learner_path = _resolve_repo_path(learner_file)
    learner_record = _load_json(learner_path)
    if not isinstance(learner_record, dict):
        raise ValueError("Transcript learner file must contain a JSON object.")

    turns = transcript.get("turns", [])
    if not isinstance(turns, list) or not turns:
        raise ValueError("Transcript must contain at least one turn.")
    selected_turns = turns if turn_limit is None else turns[:turn_limit]

    content = load_unit1_content()
    turn_results: list[dict] = []

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

    return {
        "transcriptId": transcript.get("transcriptId"),
        "name": transcript.get("name"),
        "skillId": transcript.get("skillId"),
        "tags": transcript.get("tags", []),
        "learnerFile": str(learner_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "turnCount": len(turns),
        "replayedTurnCount": len(turn_results),
        "turnResults": turn_results,
        "finalLearnerRecord": learner_record,
    }
