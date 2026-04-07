# Stage 1 — Bench Bring-Up Acceptance Criteria

**Version:** v0.22 (2026-04-07)
**Stage:** 1 (mock hardware)
**Reference:** `STAGE1_BENCH_BRINGUP.md` (guide), `STAGE1_BENCH_CHECKLIST.md` (step-by-step)

---

## Minimum Acceptance Criteria (all must pass for PASS verdict)

| # | Criterion | How to verify | Pass condition |
|---|-----------|---------------|----------------|
| 1 | System powers safely | Visual inspection + `GET /health` | `{"ok": true}`; no errors in service log |
| 2 | Mock mode confirmed | `GET /status` | `"mock_mode": true` |
| 3 | Arm reaches READY | `POST /arm/home` → `GET /status` | `"arm_state": "ready"` |
| 4 | Session opens from READY | `POST /session/start` | HTTP 200; `session_id` in response |
| 5 | Handover cycle completes | `POST /handover/request` | HTTP 202; `"status": "complete"` |
| 6 | Arm auto-returns to READY | `GET /status` after handover | `"arm_state": "ready"` |
| 7 | Session closes cleanly | `POST /session/stop` | HTTP 200; `"status": "stopped"` |
| 8 | Bundle artifacts recorded | `GET /artifacts/{session_id}` | `presence.manifest`, `presence.trace`, `presence.telemetry` all `true`; `trace_summary.event_count >= 7` |
| 9 | Smoke gate passes on bench | `pytest -m smoke -v` | 1 passed |
| 10 | Graceful stop mid-session | `POST /session/stop` on active session, then `GET /artifacts/{session_id}` | HTTP 200; `is_closed: true`; `errors: []`; bundle present |
| 11 | IDLE guard enforced | `POST /session/start` without prior home | HTTP 409; `detail.current_state == "idle"` |
| 12 | No unexpected 5xx | Full operator flow (criteria 3–8) | Zero unhandled exceptions; zero 5xx responses |

---

## Trace Event Sequence — Expected per Handover

The bundle's `session_trace.ndjson` must contain these events in this order:

```
1. session_started
2. handover_requested
3. task_lifecycle_entered
4. handover_driver_started
5. handover_completed
6. task_lifecycle_completed
7. session_stopped
```

Minimum event count: **7** (1 per session-level event + 5 per handover + 1 session stop).
Criterion 8 therefore requires `event_count >= 7`.

---

## FAIL Criteria (Bring-Up Must Be Aborted)

Immediately abort bring-up and kill the service if any of these occur:

| Condition | Meaning | Action |
|-----------|---------|--------|
| `mock_mode: false` | Real driver unexpectedly active — safety halt | Kill service, do not proceed |
| Any 5xx response | Service error | Kill service, inspect logs |
| `arm_state` stuck after handover | State machine error | Kill service, inspect logs |
| `mock_mode: true` but stage machine trace missing events | HandoverService regression | File bug, do not re-run |
| Bundle missing after session stop | Storage error | Check sessions dir permissions |
| (Stage 1.5+) Uncontrolled arm motion | Critical safety | E-stop → power off arm rail |

---

## Known Gaps (Non-Blocking for Stage 1)

These are acknowledged limitations in Stage 1. They do not cause a FAIL verdict but must be
addressed in Stage 1.5 before real arm motion begins:

| Gap | Current State | Stage 1.5 Fix |
|-----|--------------|---------------|
| No `/arm/estop` REST endpoint | `SAFE_STOP` state exists in state machine; no REST trigger | Add `POST /arm/estop` endpoint |
| E-stop not wired to software | Physical button cuts power rail only | Wire button to OS/service signal |
| `home_complete` auto-triggered | Mock auto-returns to READY; no sensor gate | Gate on physical home sensor callback |
| No camera grasp confirmation | `transfer_complete` trigger not gated on vision | Wire camera to `HandoverService` |
| `telemetry.mcap` is a placeholder | No real telemetry in Stage 1 | Populate from arm driver in Stage 1.5 |

---

## Bring-Up Verdict Recording

```
Date:         ___________________________
Operator:     ___________________________
Bench host:   ___________________________
Git SHA:      ___________________________
Config file:  configs/app/stage1_bench.yaml

Criteria passed:  ___ / 12
Verdict:          [ ] PASS   [ ] PARTIAL   [ ] FAIL

Notes:
_______________________________________________
_______________________________________________
```
