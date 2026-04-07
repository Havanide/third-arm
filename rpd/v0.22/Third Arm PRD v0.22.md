# Third Arm — PRD v0.22

**Date:** 2026-04-07
**Stage:** 1 (mock hardware, desktop-first)

---

## Product Goal

A desktop robotic arm system that delivers objects to a user on demand via an intent-driven
handover sequence, orchestrated through a REST API by a human operator in Stage 1.

---

## Stage 1 — Software Complete, Hardware Bring-Up Gate Open

Stage 1 software is frozen as of v0.21. The bench bring-up pack (v0.22) defines the criteria
for the hardware milestone:

> **Stage 1 hardware milestone:** All 12 acceptance criteria in `STAGE1_BENCH_ACCEPTANCE.md`
> pass on the physical bench. This is the gate before Stage 1.5 real-driver integration begins.

### Stage 1 Bench Bring-Up Acceptance Criteria (summary)

| # | Criterion | Pass condition |
|---|-----------|----------------|
| 1 | System powers safely | `GET /health` → `{ok: true}`; no errors |
| 2 | Mock mode confirmed | `mock_mode: true` |
| 3 | Arm reaches READY | `arm_state: "ready"` after home |
| 4 | Session opens from READY | HTTP 200 with `session_id` |
| 5 | Handover cycle completes | HTTP 202; `status: complete` |
| 6 | Arm auto-returns to READY | `arm_state: "ready"` after handover |
| 7 | Session closes cleanly | HTTP 200; `status: stopped` |
| 8 | Bundle artifacts recorded | All 3 files present; trace count ≥ 6 |
| 9 | Smoke gate passes on bench | `pytest -m smoke -v` → 1 passed |
| 10 | Graceful stop mid-session | HTTP 200; bundle not corrupted |
| 11 | IDLE guard enforced | HTTP 409 when arm not homed |
| 12 | No unexpected 5xx | Zero unhandled exceptions |

---

## Stage 1.5 — Next Milestone (preview)

**Trigger:** Stage 1 bench bring-up PASS verdict recorded.

**New capabilities:**
- Real arm driver wired (physical arm moves during handover)
- Camera-gated grasp confirmation before `transfer_complete`
- `home_complete` gated on physical home sensor (not auto-triggered)
- `POST /arm/estop` endpoint (routes to `SAFE_STOP` state)
- `telemetry.mcap` populated from real arm telemetry

**What does NOT change:**
- REST API contract (frozen in Stage 1)
- State machine states (new `estop` trigger only)
- Bundle format (frozen in Stage 1)
- Operator flow (same sequence; behavior gated by real hardware)

---

## Out of Scope (Stage 1 and 1.5)

- IMU / sEMG intent detection (Stage 2+)
- Autonomous handover triggering (Stage 3+)
- Multi-operator or multi-session concurrency
