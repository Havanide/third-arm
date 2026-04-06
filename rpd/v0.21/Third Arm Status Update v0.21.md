# Third Arm — Status Update v0.21

**Date:** 2026-04-06
**Stage:** 1 (mock hardware, desktop-first)
**Branch:** feat/stage1-pre-bringup-hardening

---

## Milestone: Stage 1 Runtime Boundary Finalized

Stage 1 runtime is complete and hardened for hardware bring-up. All operator-visible behavior
is locked: session lifecycle, task lifecycle state machine, trace event schema, and bundle
artifact format are frozen.

---

## What Changed in v0.21

### HandoverService — task lifecycle binding

`POST /handover/request` is now the explicit task lifecycle entry point. The full state sequence
is bound in code:

```
READY → session_start → TASK_ARMING
      → task_arm      → ACQUIRE
      → lift_cmd      → LIFT
      → present_cmd   → PRESENT
      → transfer_complete → TRANSFER_WAIT
      → release_cmd   → RELEASE
      → retract_cmd   → RETRACT
      → task_done     → TASK_COMPLETE
      → home_cmd      → HOMING
      → home_complete → READY
```

Each state transition is driven in sequence. The arm auto-returns to READY after each handover
(Stage 1 mock). Stage 1.5 will gate `home_complete` on physical sensor confirmation.

### Trace events — task lifecycle

Five trace events are emitted per handover (in order):

| # | Event | Trigger |
|---|-------|---------|
| 1 | `handover_requested` | Before state machine entry |
| 2 | `task_lifecycle_entered` | After READY → TASK_ARMING |
| 3 | `handover_driver_started` | After `task_arm` trigger |
| 4 | `handover_completed` | After `task_done` (TASK_COMPLETE) |
| 5 | `task_lifecycle_completed` | After return to READY |

### Session boundary — resolved open question

`POST /session/start` is confirmed as a pure bundle gate (no state machine transition).
`POST /handover/request` is the task lifecycle entry. Decision recorded in DECISIONS_LOG.md.

### Integration tests

- Smoke test asserts post-handover `arm_state == "ready"` via `GET /status`
- Smoke test asserts all 5 lifecycle trace events present and in correct order
- New test `test_handover_rejects_non_ready_active_session` forces the shared state machine
  into `TASK_ARMING` after session open and expects `409` from `POST /handover/request`

---

## Stage 1 — All Acceptance Criteria Met

| Criterion | Status |
|-----------|--------|
| Operator flow: home → session → handover → stop → artifacts | ✅ |
| Bundle artifacts: manifest.json, session_trace.ndjson, telemetry.mcap | ✅ |
| Session READY precondition enforced | ✅ |
| Task lifecycle state machine fully bound | ✅ |
| Trace events: full lifecycle sequence per handover | ✅ |
| Arm auto-returns to READY after handover | ✅ |
| Smoke gate: mandatory CI merge gate | ✅ |
| OpenAPI spec: hand-maintained, fully synced | ✅ |
| Path traversal protection on artifact inspection | ✅ |

---

## Next

Stage 1.5: camera integration and vision-gated grasp confirmation.
Gate `home_complete` on physical arm driver confirmation.
