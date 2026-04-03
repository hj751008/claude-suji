const state = {
  transcripts: [],
  transcriptFiles: [],
  learnerFiles: [],
  transcriptFile: "",
  selectedTranscriptId: null,
  learnerRecord: null,
  loadedLearnerFile: null,
  lastReplay: null,
  lastStart: null,
  lastPrepared: null,
  lastTurn: null,
  actionHistory: [],
};

const PILOT_PRESETS = {
  "pilot-s2-s4": {
    transcriptId: "u1-s2-s3-bilingual-text-only-planned-session",
    turnLimit: null,
    pilotNote: [
      "Pilot A",
      "Tester: ",
      "Focus: S2-S4 bridge and verification flow",
      "Natural: ",
      "Awkward: ",
      "Operator hesitation: ",
      "Fixture realism: ",
    ].join("\n"),
  },
  "pilot-s5-transfer": {
    transcriptId: "u1-s5a-divisor-count-ko-text-only-active-session",
    turnLimit: null,
    pilotNote: [
      "Pilot B",
      "Tester: ",
      "Focus: S5 transfer with blocker-first reopen",
      "Natural: ",
      "Awkward: ",
      "Operator hesitation: ",
      "Fixture realism: ",
    ].join("\n"),
  },
  "pilot-s5c-transfer": {
    transcriptId: "u1-s5c-gcd-lcm-ko-text-only-active-session",
    turnLimit: null,
    pilotNote: [
      "Pilot C",
      "Tester: ",
      "Focus: S5C gcd/lcm transfer with blocker-first reopen",
      "Natural: ",
      "Awkward: ",
      "Operator hesitation: ",
      "Fixture realism: ",
    ].join("\n"),
  },
  "pilot-u3-s4-blocker": {
    transcriptId: "u3-s4-combine-like-terms-ko-text-only-active-session",
    turnLimit: null,
    pilotNote: [
      "Pilot D",
      "Tester: ",
      "Focus: U3-S4 simplification with blocker-first reopen to U3-S2",
      "Natural: ",
      "Awkward: ",
      "Operator hesitation: ",
      "Fixture realism: ",
    ].join("\n"),
  },
  "pilot-u3-s5-blocker": {
    transcriptId: "u3-s5-model-then-simplify-ko-text-only-active-session",
    turnLimit: null,
    pilotNote: [
      "Pilot E",
      "Tester: ",
      "Focus: U3-S5 contextual modeling with blocker-first reopen to U3-S1",
      "Natural: ",
      "Awkward: ",
      "Operator hesitation: ",
      "Fixture realism: ",
    ].join("\n"),
  },
};

const transcriptList = document.querySelector("#transcript-list");
const learnerFileSelect = document.querySelector("#learner-file-select");
const selectedTranscript = document.querySelector("#selected-transcript");
const replaySummary = document.querySelector("#replay-summary");
const turnResults = document.querySelector("#turn-results");
const handoffSummary = document.querySelector("#handoff-summary");
const handoffJson = document.querySelector("#handoff-json");
const formMeta = document.querySelector("#form-meta");
const observationFormArea = document.querySelector("#observation-form-area");
const turnSummary = document.querySelector("#turn-summary");
const turnJson = document.querySelector("#turn-json");
const logMeta = document.querySelector("#log-meta");
const logJson = document.querySelector("#log-json");
const pilotNoteInput = document.querySelector("#pilot-note");
const turnLimitInput = document.querySelector("#turn-limit");

document.querySelector("#skill-filter").addEventListener("input", renderTranscriptList);
document.querySelector("#tag-filter").addEventListener("input", renderTranscriptList);
document.querySelector("#replay-button").addEventListener("click", replaySelectedTranscript);
document.querySelector("#load-learner-button").addEventListener("click", loadSelectedLearner);
document.querySelector("#start-session-button").addEventListener("click", startFromCurrentLearner);
document.querySelector("#prepare-form-button").addEventListener("click", prepareObservationForm);
document.querySelector("#submit-turn-button").addEventListener("click", submitTurn);
document.querySelector("#export-log-button").addEventListener("click", exportLogBundle);
document.querySelector("#save-log-button").addEventListener("click", saveLogBundle);
pilotNoteInput.addEventListener("input", () => refreshLogPreview());
for (const button of document.querySelectorAll("[data-preset-id]")) {
  button.addEventListener("click", () => applyPilotPreset(button.dataset.presetId));
}

bootstrap().catch((error) => showToast(error.message));

async function bootstrap() {
  const payload = await api("/api/bootstrap");
  state.transcripts = payload.transcripts ?? [];
  state.transcriptFiles = payload.transcriptFiles ?? [];
  state.learnerFiles = payload.learnerFiles ?? [];
  state.transcriptFile = payload.transcriptFile;
  state.selectedTranscriptId = state.transcripts[0]?.transcriptId ?? null;
  renderTranscriptList();
  renderLearnerFiles();
  renderSelectedTranscript();
  refreshLogPreview();
}

function renderLearnerFiles() {
  learnerFileSelect.innerHTML = "";
  for (const learnerFile of state.learnerFiles) {
    const option = document.createElement("option");
    option.value = learnerFile;
    option.textContent = learnerFile;
    learnerFileSelect.append(option);
  }
}

function renderTranscriptList() {
  const skillFilter = document.querySelector("#skill-filter").value.trim().toLowerCase();
  const tagFilter = document.querySelector("#tag-filter").value.trim().toLowerCase();
  transcriptList.innerHTML = "";

  const filtered = state.transcripts.filter((item) => {
    const skillOk = !skillFilter || String(item.skillId ?? "").toLowerCase().includes(skillFilter);
    const tagOk =
      !tagFilter ||
      (Array.isArray(item.tags) &&
        item.tags.some((tag) => String(tag).toLowerCase().includes(tagFilter)));
    return skillOk && tagOk;
  });

  for (const transcript of filtered) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "transcript-item";
    if (transcript.transcriptId === state.selectedTranscriptId) {
      item.classList.add("active");
    }
    item.innerHTML = `
      <strong>${escapeHtml(transcript.name ?? transcript.transcriptId)}</strong>
      <div>${escapeHtml(transcript.transcriptId)}</div>
      <div class="transcript-meta">
        <span>${escapeHtml(transcript.skillId ?? "-")}</span>
        <span>${transcript.turnCount} turns</span>
        <span>${transcript.startBeforeTurns ? "starts session" : "uses active session"}</span>
      </div>
    `;
    item.addEventListener("click", () => {
      state.selectedTranscriptId = transcript.transcriptId;
      renderTranscriptList();
      renderSelectedTranscript();
    });
    transcriptList.append(item);
  }
}

function renderSelectedTranscript() {
  const transcript = state.transcripts.find((item) => item.transcriptId === state.selectedTranscriptId);
  if (!transcript) {
    selectedTranscript.textContent = "No transcript matches the current filter.";
    return;
  }

  selectedTranscript.classList.remove("empty-state");
  selectedTranscript.innerHTML = `
    <h3>${escapeHtml(transcript.name)}</h3>
    <div class="transcript-meta">
      <span>${escapeHtml(transcript.transcriptId)}</span>
      <span>${escapeHtml(transcript.skillId ?? "-")}</span>
      <span>${transcript.turnCount} turns</span>
      <span>${escapeHtml((transcript.tags ?? []).join(", "))}</span>
    </div>
    <p>Source learner: <code>${escapeHtml(transcript.learnerFile ?? "-")}</code></p>
    <p>Fixture file: <code>${escapeHtml(transcript.transcriptFile ?? state.transcriptFile ?? "-")}</code></p>
  `;
}

function applyPilotPreset(presetId) {
  const preset = PILOT_PRESETS[presetId];
  if (!preset) {
    showToast("Unknown preset.");
    return;
  }
  const transcript = state.transcripts.find((item) => item.transcriptId === preset.transcriptId);
  if (!transcript) {
    showToast(`Preset transcript not found: ${preset.transcriptId}`);
    return;
  }

  state.selectedTranscriptId = transcript.transcriptId;
  turnLimitInput.value = preset.turnLimit == null ? "" : String(preset.turnLimit);
  pilotNoteInput.value = preset.pilotNote;
  renderTranscriptList();
  renderSelectedTranscript();
  refreshLogPreview();
  showToast(`Preset loaded: ${transcript.name}`);
}

async function replaySelectedTranscript() {
  const transcript = state.transcripts.find((item) => item.transcriptId === state.selectedTranscriptId);
  if (!transcript) {
    showToast("Select a transcript first.");
    return;
  }

  const turnLimitValue = turnLimitInput.value.trim();
  const turnLimit = turnLimitValue ? Number(turnLimitValue) : null;
  const payload = await api("/api/replay-transcript", {
    transcriptFile: transcript.transcriptFile ?? state.transcriptFile,
    transcriptId: transcript.transcriptId,
    turnLimit,
  });
  state.learnerRecord = payload.finalLearnerRecord;
  state.loadedLearnerFile = payload.learnerFile;
  state.lastReplay = payload;
  state.lastStart = null;
  state.lastPrepared = null;
  state.lastTurn = null;
  state.actionHistory = [];
  recordAction("replay-transcript", {
    transcriptId: payload.transcriptId,
    turnCount: payload.turnCount,
    replayedTurnCount: payload.replayedTurnCount,
    finalAction: payload.turnResults?.at(-1)?.turnSummary?.nextAction ?? null,
  });

  replaySummary.innerHTML = renderMetrics([
    ["Transcript", payload.transcriptId],
    ["Skill", payload.skillId],
    ["Turns replayed", String(payload.replayedTurnCount)],
    ["Learner", payload.learnerFile],
  ]);

  turnResults.innerHTML = "";
  for (const turn of payload.turnResults ?? []) {
    const card = document.createElement("article");
    card.className = "turn-card";
    const summary = turn.turnSummary ?? {};
    const nextBlock =
      summary.nextAction === "continue_active_session"
        ? summary.nextStepGuide?.currentLessonStepId
        : summary.nextRecommendedSession?.firstLessonStepId;
    card.innerHTML = `
      <h3>Turn ${turn.turnIndex}: ${escapeHtml(turn.lessonStepId ?? "-")}</h3>
      <ul>
        <li>decision: ${escapeHtml(summary.decision ?? "-")}</li>
        <li>nextAction: ${escapeHtml(summary.nextAction ?? "-")}</li>
        <li>sessionStatus: ${escapeHtml(summary.sessionStatus ?? "-")}</li>
        <li>next focus: ${escapeHtml(nextBlock ?? "-")}</li>
      </ul>
    `;
    turnResults.append(card);
  }

  handoffSummary.innerHTML = "";
  handoffJson.textContent = "";
  formMeta.innerHTML = "";
  observationFormArea.className = "form-area empty-state";
  observationFormArea.textContent = "Use Step 2 to open the next session or load a learner record.";
  turnSummary.innerHTML = "";
  turnJson.textContent = "";
  refreshLogPreview();
  showToast("Transcript replay finished.");
}

async function loadSelectedLearner() {
  const learnerFile = learnerFileSelect.value;
  if (!learnerFile) {
    showToast("Choose a learner file first.");
    return;
  }
  const payload = await api("/api/load-learner-record", { learnerFile });
  state.learnerRecord = payload.learnerRecord;
  state.loadedLearnerFile = payload.learnerFile;
  state.lastReplay = null;
  state.lastStart = null;
  state.lastPrepared = null;
  state.lastTurn = null;
  state.actionHistory = [];
  recordAction("load-learner-record", {
    learnerFile: payload.learnerFile,
    activeSessionPresent: Boolean(payload.learnerRecord.activeSession),
    sessionCount: (payload.learnerRecord.sessions ?? []).length,
  });
  replaySummary.innerHTML = renderMetrics([
    ["Loaded learner", payload.learnerFile],
    ["Active session", state.learnerRecord.activeSession ? "present" : "none"],
    ["Stored sessions", String((state.learnerRecord.sessions ?? []).length)],
    ["Evidence events", String((state.learnerRecord.evidenceEvents ?? []).length)],
  ]);
  turnResults.innerHTML = "";
  handoffSummary.innerHTML = "";
  handoffJson.textContent = "";
  formMeta.innerHTML = "";
  observationFormArea.className = "form-area empty-state";
  observationFormArea.textContent = "Loaded learner record. Start a session or refresh the observation form.";
  turnSummary.innerHTML = "";
  turnJson.textContent = "";
  refreshLogPreview();
  showToast("Learner record loaded.");
}

async function startFromCurrentLearner() {
  if (!state.learnerRecord) {
    showToast("Replay a transcript or load a learner record first.");
    return;
  }

  const payload = await api("/api/start-learning-session", { learnerRecord: state.learnerRecord });
  state.learnerRecord = payload.learnerRecord;
  state.lastStart = payload;
  state.lastPrepared = {
    observationFormTemplate: payload.observationFormTemplate,
    observationForm: seedObservationForm(payload.observationFormTemplate),
  };
  recordAction("start-learning-session", {
    action: payload.action,
    sessionTargetSkillId: payload.sessionStartGuide?.sessionTargetSkillId ?? null,
    currentStepSkillId: payload.sessionStartGuide?.currentStepSkillId ?? null,
    currentLessonStepId: payload.sessionStartGuide?.currentLessonStepId ?? null,
    plannedFromSkillId: payload.plannedSessionPreview?.plannedFromSkillId ?? null,
    recommendedNextSkillIds: payload.plannedSessionPreview?.recommendedNextSkillIds ?? [],
  });

  const guide = payload.sessionStartGuide ?? {};
  const preview = payload.plannedSessionPreview ?? {};
  handoffSummary.innerHTML = renderMetrics([
    ["sessionTargetSkillId", guide.sessionTargetSkillId],
    ["currentStepSkillId", guide.currentStepSkillId],
    ["currentLessonStepId", guide.currentLessonStepId],
    ["remainingStepCount", String(guide.remainingStepCount ?? 0)],
    ["plannedFromSkillId", preview.plannedFromSkillId ?? "resume_session"],
    [
      "recommendedNextSkillIds",
      Array.isArray(preview.recommendedNextSkillIds)
        ? preview.recommendedNextSkillIds.join(" -> ")
        : "-",
    ],
  ]);
  handoffJson.textContent = JSON.stringify(payload, null, 2);
  renderPreparedForm(payload.observationFormTemplate, seedObservationForm(payload.observationFormTemplate));
  refreshLogPreview();
  showToast("Session handoff loaded.");
}

async function prepareObservationForm() {
  if (!state.learnerRecord) {
    showToast("No learner state available.");
    return;
  }

  const payload = await api("/api/prepare-observation-form", { learnerRecord: state.learnerRecord });
  state.lastPrepared = payload;
  recordAction("prepare-observation-form", {
    lessonStepId: payload.sourceLessonStepId,
    fieldIds: Object.keys(payload.observationForm?.fieldValues ?? {}),
  });
  renderPreparedForm(payload.observationFormTemplate, payload.observationForm);
  refreshLogPreview();
  showToast("Observation form refreshed.");
}

async function submitTurn() {
  if (!state.learnerRecord) {
    showToast("No learner state available.");
    return;
  }

  const observationForm = collectObservationForm();
  const payload = await api("/api/run-learning-turn", {
    learnerRecord: state.learnerRecord,
    observationForm,
  });
  state.learnerRecord = payload.learnerRecord;
  state.lastTurn = payload;
  if (payload.observationFormTemplate && payload.observationForm) {
    state.lastPrepared = {
      sourceLessonStepId: payload.observationFormTemplate.lessonStepId,
      observationFormTemplate: payload.observationFormTemplate,
      observationForm: payload.observationForm,
    };
  }
  recordAction("run-learning-turn", {
    submittedLessonStepId: payload.turnSummary?.submittedLessonStepId ?? observationForm.lessonStepId ?? null,
    decision: payload.turnSummary?.decision ?? null,
    nextAction: payload.turnSummary?.nextAction ?? null,
    sessionStatus: payload.turnSummary?.sessionStatus ?? null,
    inputObservationForm: observationForm,
  });

  const summary = payload.turnSummary ?? {};
  const detail =
    summary.nextAction === "continue_active_session"
      ? summary.nextStepGuide ?? {}
      : summary.nextRecommendedSession ?? {};
  turnSummary.innerHTML = renderMetrics([
    ["decision", summary.decision],
    ["nextAction", summary.nextAction],
    ["sessionStatus", summary.sessionStatus],
    ["current / first step", detail.currentLessonStepId ?? detail.firstLessonStepId ?? "-"],
    ["current / first skill", detail.currentStepSkillId ?? detail.firstStepSkillId ?? "-"],
    [
      "recommendations",
      Array.isArray(summary.latestRecommendationSkillIds)
        ? summary.latestRecommendationSkillIds.join(", ")
        : "-",
    ],
  ]);
  turnJson.textContent = JSON.stringify(payload, null, 2);

  if (payload.observationFormTemplate && payload.observationForm) {
    renderPreparedForm(payload.observationFormTemplate, payload.observationForm);
  } else {
    observationFormArea.className = "form-area empty-state";
    observationFormArea.textContent = "Session completed. Review the recommendation block above.";
  }
  refreshLogPreview();
  showToast("Turn submitted.");
}

function exportLogBundle() {
  const bundle = buildLogBundle();
  downloadJson(bundle, suggestedLogFilename("operator-log"));
  showToast("Operator log exported.");
}

async function saveLogBundle() {
  const bundle = buildLogBundle();
  const payload = await api("/api/save-operator-log", {
    filename: suggestedLogFilename("operator-log"),
    bundle,
  });
  refreshLogPreview(payload.path);
  showToast(`Saved ${payload.path}`);
}

function renderPreparedForm(template, observationForm) {
  if (!template || !observationForm) {
    observationFormArea.className = "form-area empty-state";
    observationFormArea.textContent = "No observation form is available.";
    formMeta.innerHTML = "";
    return;
  }

  formMeta.innerHTML = renderMetrics([
    ["lessonStepId", template.lessonStepId],
    ["Prompt", template.learnerResponsePrompt],
    ["Field count", String((template.fields ?? []).length)],
  ]);

  observationFormArea.className = "form-area";
  observationFormArea.dataset.lessonStepId = observationForm.lessonStepId ?? template.lessonStepId ?? "";
  const fieldsMarkup = (template.fields ?? [])
    .map((field) => {
      const checked = Boolean(observationForm.fieldValues?.[field.fieldId]) ? "checked" : "";
      return `
        <label class="checkbox-row">
          <input type="checkbox" data-field-id="${escapeAttribute(field.fieldId)}" ${checked} />
          <span>${escapeHtml(field.label ?? field.fieldId)}</span>
        </label>
      `;
    })
    .join("");

  observationFormArea.innerHTML = `
    <label class="field">
      <span>Learner response</span>
      <textarea id="learner-response">${escapeHtml(observationForm.learnerResponse ?? "")}</textarea>
    </label>
    <div class="checkbox-grid">${fieldsMarkup}</div>
    <label class="field">
      <span>Tutor note</span>
      <textarea id="tutor-note">${escapeHtml(observationForm.tutorNote ?? "")}</textarea>
    </label>
    <label class="field">
      <span>Timestamp</span>
      <input id="timestamp" type="text" value="${escapeAttribute(observationForm.timestamp ?? nowIso())}" />
    </label>
  `;
}

function collectObservationForm() {
  const fieldValues = {};
  for (const input of observationFormArea.querySelectorAll("[data-field-id]")) {
    fieldValues[input.dataset.fieldId] = input.checked;
  }
  return {
    lessonStepId: observationFormArea.dataset.lessonStepId || null,
    learnerResponse: document.querySelector("#learner-response")?.value ?? "",
    fieldValues,
    tutorNote: document.querySelector("#tutor-note")?.value ?? "",
    timestamp: document.querySelector("#timestamp")?.value ?? nowIso(),
  };
}

function renderMetrics(entries) {
  return entries
    .map(
      ([label, value]) => `
        <div class="metric">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value ?? "-")}</strong>
        </div>
      `,
    )
    .join("");
}

function seedObservationForm(template) {
  const fieldValues = {};
  for (const field of template.fields ?? []) {
    fieldValues[field.fieldId] = false;
  }
  return {
    lessonStepId: template.lessonStepId,
    learnerResponse: "",
    fieldValues,
    tutorNote: "",
    timestamp: nowIso(),
  };
}

function recordAction(kind, detail) {
  state.actionHistory.push({
    actionAt: nowIso(),
    kind,
    detail,
  });
}

function buildLogBundle() {
  return {
    logFormatVersion: "multi-unit-operator-ui-pilot-v1",
    exportedAt: nowIso(),
    selectedTranscriptId: state.selectedTranscriptId,
    transcriptFile: state.transcriptFile,
    transcriptFiles: state.transcriptFiles,
    loadedLearnerFile: state.loadedLearnerFile,
    pilotNote: document.querySelector("#pilot-note")?.value ?? "",
    actionHistory: state.actionHistory,
    latestReplayResult: state.lastReplay,
    latestStartSessionResult: state.lastStart,
    latestPreparedObservationForm: state.lastPrepared,
    latestTurnResult: state.lastTurn,
    currentLearnerRecord: state.learnerRecord,
  };
}

function refreshLogPreview(savedPath = null) {
  const bundle = buildLogBundle();
  logMeta.innerHTML = renderMetrics([
    ["selectedTranscriptId", bundle.selectedTranscriptId ?? "-"],
    ["loadedLearnerFile", bundle.loadedLearnerFile ?? "-"],
    ["action count", String(bundle.actionHistory.length)],
    ["saved path", savedPath ?? "-"],
  ]);
  logJson.textContent = JSON.stringify(bundle, null, 2);
}

function suggestedLogFilename(prefix) {
  const transcriptPart = slugify(state.selectedTranscriptId ?? "manual");
  return `${prefix}-${transcriptPart}-${compactNow()}`;
}

function downloadJson(payload, filename) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${filename}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
}

async function api(url, body) {
  const options = body
    ? {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    : undefined;
  const response = await fetch(url, options);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error ?? `Request failed: ${response.status}`);
  }
  return payload;
}

function showToast(message) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.hidden = false;
  clearTimeout(showToast.timeoutId);
  showToast.timeoutId = setTimeout(() => {
    toast.hidden = true;
  }, 2400);
}

function nowIso() {
  return new Date().toISOString();
}

function compactNow() {
  return nowIso().replaceAll(/[-:.TZ]/g, "").slice(0, 14);
}

function slugify(value) {
  return String(value ?? "")
    .toLowerCase()
    .replaceAll(/[^a-z0-9-_]+/g, "-")
    .replaceAll(/^-+|-+$/g, "");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("'", "&#39;");
}
