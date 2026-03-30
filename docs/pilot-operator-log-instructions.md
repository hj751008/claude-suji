# Pilot Operator Log Instructions

## Purpose

Use the local operator UI to capture one or two real pilot runs as raw JSON
logs before calling Unit 1 field validation complete.

## Precondition

Run the local UI:

```bash
python app/cli.py serve-operator-ui
```

Open `http://127.0.0.1:8765`.

## Minimal Pilot Flow

1. In the left sidebar, choose one quick preset:
   - `Pilot A` for `S2-S4 bridge and verification flow`
   - `Pilot B` for `S5 transfer with blocker-first reopen`
   - `Pilot C` for `S5C gcd/lcm transfer with blocker-first reopen`
2. Click `Replay transcript`.
3. Click `Start from current learner state`.
4. Run at least one real operator turn in Step 3.
5. Add or edit the short `Pilot note`:
   - who tested
   - what felt natural or awkward
   - where the operator hesitated
   - whether the logging format felt realistic
6. Click `Save raw log`.

## Output Location

Saved logs are written to:

`output/operator-logs/`

Each saved file contains:

- transcript or learner starting point
- action history from the local operator UI
- latest replay, handoff, prepared form, and turn result payloads
- current learner record snapshot
- pilot note

## Minimum Evidence Target

For stronger Unit 1 sign-off, try to collect at least:

1. one `S2-S4` style run
2. one `S5A-S5D` transfer run
3. if possible, one non-`S5A` live turn such as `Pilot C`

## What To Review After Saving

Compare each raw log against:

- `app/domain/evidence/unit1-tutor-transcripts.example.json`
- `docs/unit1-real-log-comparison-template.md`

The goal is not to prove the runtime correct again.
The goal is to decide whether the current fixture style really matches how an
operator naturally records a live session.
