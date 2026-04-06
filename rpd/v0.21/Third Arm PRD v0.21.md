# Third Arm — PRD v0.21

**Date:** 2026-04-06
**Stage:** 1 (mock hardware, desktop-first)

---

## Product Goal

A desktop robotic arm system that delivers objects to a user on demand via an intent-driven
handover sequence, orchestrated through a REST API by a human operator in Stage 1.

---

## Stage 1 — Complete

All Stage 1 acceptance criteria are met as of v0.21.

### Operator flow (frozen)

```
POST /arm/home
POST /session/start   { operator_id, object_id, slot_id }
POST /handover/request { object_id, slot_id }
POST /session/stop
GET  /artifacts
GET  /artifacts/{session_id}
```

### Session lifecycle (frozen)

- Session requires arm in READY state to open (`POST /session/start` → 409 from IDLE)
- Session holds `session_id`, `started_at`, `operator_id`, `handover_ids`
- Session close writes `closed_at` to `manifest.json`
- Bundle artifacts created at session open; telemetry placeholder written at session close

### Task lifecycle (frozen)

- `POST /handover/request` is the task lifecycle entry (READY → TASK_ARMING)
- Full state machine sequence executed synchronously in Stage 1 mock
- Arm auto-returns to READY after each handover
- Multiple handovers per session supported without re-homing

### Trace event schema (frozen)

Per session:
- `session_started`
- Per handover: `handover_requested`, `task_lifecycle_entered`, `handover_driver_started`, `handover_completed`, `task_lifecycle_completed`
- `session_stopped`

---

## Stage 1.5 — Next

- Camera integration
- Vision-gated grasp confirmation before `transfer_complete`
- `home_complete` gated on physical arm driver confirmation (not auto-triggered)
- Real arm driver integration begins

---

## Out of Scope (Stage 1)

- Real arm hardware
- IMU / sEMG intent detection (Stage 2+)
- Autonomous handover triggering (Stage 3+)
- Multi-operator or multi-session concurrency
