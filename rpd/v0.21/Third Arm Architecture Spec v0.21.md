# Third Arm — Architecture Spec v0.21

**Date:** 2026-04-06
**Stage:** 1 (mock hardware, desktop-first)

---

## Runtime Components

```
FastAPI app (create_app)
├── Lifespan: StateMachine, MockArmDriver, SessionService, HandoverService, BundleWriter
├── Routers
│   ├── health.py     GET /health
│   ├── status.py     GET /status
│   ├── arm.py        POST /arm/home
│   ├── session.py    POST /session/start, POST /session/stop
│   ├── handover.py   POST /handover/request
│   └── artifacts.py  GET /artifacts, GET /artifacts/{session_id}
└── Dependency injection via app.state + Depends
```

---

## State Machine (frozen)

States: BOOT → SELF_CHECK → IDLE → HOMING → READY → TASK_ARMING → ACQUIRE →
        LIFT → PRESENT → TRANSFER_WAIT → RELEASE → RETRACT → TASK_COMPLETE → HOMING → READY

### Task lifecycle state sequence (per handover)

| Trigger | From | To |
|---------|------|----|
| `session_start` | READY | TASK_ARMING |
| `task_arm` | TASK_ARMING | ACQUIRE |
| `lift_cmd` | ACQUIRE | LIFT |
| `present_cmd` | LIFT | PRESENT |
| `transfer_complete` | PRESENT | TRANSFER_WAIT |
| `release_cmd` | TRANSFER_WAIT | RELEASE |
| `retract_cmd` | RELEASE | RETRACT |
| `task_done` | RETRACT | TASK_COMPLETE |
| `home_cmd` | TASK_COMPLETE | HOMING |
| `home_complete` | HOMING | READY |

Stage 1: `home_complete` is auto-triggered after `home_cmd` (mock).
Stage 1.5+: `home_complete` gated on physical sensor confirmation from driver.

---

## Trace Event Schema (frozen)

All events written to `session_trace.ndjson` as newline-delimited JSON.
Common fields: `event`, `handover_id` (where applicable), `session_id`.

### Per-session event sequence

```
session_started          { session_id, operator_id, object_id, slot_id, started_at }
handover_requested       { handover_id, session_id, object_id, slot_id }
task_lifecycle_entered   { handover_id, session_id, arm_state: "task_arming" }
handover_driver_started  { handover_id, session_id }
handover_completed       { handover_id, session_id }
task_lifecycle_completed { handover_id, session_id, arm_state: "ready" }
session_stopped          { session_id, stopped_at }
```

---

## Bundle Layout (frozen)

```
sessions/
└── session_<ts>_<id>/
    ├── manifest.json          { session_id, schema_version, created_at, closed_at, operator_id, ... }
    ├── session_trace.ndjson   newline-delimited JSON trace events
    └── telemetry.mcap         placeholder (Stage 1); real MCAP in Stage 1.5+
```

---

## API Endpoints (Stage 1, frozen)

| Method | Path | Description | Key responses |
|--------|------|-------------|---------------|
| GET | /health | Liveness | 200 `{ok, ts, message}` |
| GET | /status | Arm state + session | 200 `{ts, arm_state, session_id, uptime_s, mock_mode}` |
| POST | /arm/home | Home the arm | 202 `{accepted, new_state}` / 409 |
| POST | /session/start | Open session (READY required) | 200 `{session_id, started_at, operator_id}` / 409 `{detail: {message, current_state}}` |
| POST | /session/stop | Close session | 200 `{session_id, stopped_at, status}` / 404 |
| POST | /handover/request | Execute handover (task lifecycle) | 202 `{handover_id, object_id, slot_id, completed_at, status}` / 409 |
| GET | /artifacts | List session bundles | 200 `{bundles: [...], count}` |
| GET | /artifacts/{session_id} | Inspect bundle (degraded-safe) | 200 `ArtifactDetailResponse` / 404 |

---

## Security Boundaries (Stage 1)

- `GET /artifacts/{session_id}`: `session_id` validated against `^[A-Za-z0-9][A-Za-z0-9._-]*$`; resolved path checked to remain within `sessions_dir`; 404 on any unsafe value
- No authentication in Stage 1 (local desktop deployment only)
