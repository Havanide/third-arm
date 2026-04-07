# Third Arm — Architecture Spec v0.22

**Date:** 2026-04-07
**Stage:** 1 (mock hardware, desktop-first)

No arm-motion runtime changes in v0.22. This document adds bench bring-up environment
assumptions, configuration reference, and the E-stop gap documentation. It also makes the
bench config profile executable through the existing settings layer.

See `rpd/v0.21/Third Arm Architecture Spec v0.21.md` for the full Stage 1 software architecture.

---

## Bench Bring-Up Environment Assumptions

The Stage 1 bench environment must meet these requirements before bring-up begins:

| Component | Requirement |
|-----------|-------------|
| Host machine | Python 3.10+, git; port 8080 accessible on LAN |
| Arm unit | Powered and mechanically secured; comms not connected (Stage 1 mock) |
| E-stop button | Wired to arm power rail; in operator reach |
| Tray fixture | slot_A (150,50,120mm) and slot_B (150,0,120mm) marked; handover zone (300,0,200mm) clear |
| Sessions storage | `/data/third-arm/sessions` writable; persists across service restarts |

---

## Configuration Files (Stage 1)

| File | Purpose | Key delta |
|------|---------|-----------|
| `configs/app/default.yaml` | Base defaults | — |
| `configs/app/stage1_desktop.yaml` | Dev laptop | `host: 127.0.0.1`, `mock: true` |
| `configs/app/stage1_bench.yaml` | Bench host | `host: 0.0.0.0`, `mock: true` |
| `configs/slots/stage1_slots.yaml` | Slot catalogue | slot_A, slot_B enabled; slot_C disabled |
| `configs/slots/stage1_objects.yaml` | Object catalogue | water bottle, mug enabled; tablet disabled |
| `configs/calibration/placeholder.yaml` | Calibration | placeholder for Stage 1.5 |

**Safety invariant:** `hardware.mock: true` must be set in any Stage 1 config. The bring-up
checklist verifies `mock_mode: true` from `GET /status` before any handover operations.

`configs/app/stage1_bench.yaml` is loaded via `THIRD_ARM_CONFIG=configs/app/stage1_bench.yaml`
or `THIRD_ARM_CONFIG_PROFILE=stage1_bench`. `scripts/dev.sh` reads the resolved runtime settings
and starts uvicorn with the matching host/port/log-level/reload values.

---

## E-Stop Gap (Stage 1)

The state machine includes a `SAFE_STOP` state and a `TASK_ABORTED` state, but Stage 1 does
not expose a REST trigger to reach them:

| | Stage 1 | Stage 1.5 |
|-|---------|-----------|
| Software E-stop | Kill service (SIGTERM / Ctrl+C) | `POST /arm/estop` → `SAFE_STOP` state |
| Physical E-stop | Button cuts arm power rail | Same; also triggers software SAFE_STOP via OS signal |
| `home_complete` | Auto-triggered after `home_cmd` (mock) | Gated on physical sensor callback |

**Stage 1.5 design question (open):** should `estop` be a top-level trigger valid from all
states, or routed through existing `StateMachine.trigger()` semantics? See `OPEN_QUESTIONS.md`.

---

## Runtime Components (unchanged from v0.21)

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

## API Endpoints (Stage 1, frozen)

No changes from v0.21. See `docs/api/openapi.yaml` for the authoritative contract.

---

## Task Lifecycle State Sequence (unchanged from v0.21)

| Trigger | From | To |
|---------|------|-----|
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

Stage 1: `home_complete` auto-triggered (mock). Stage 1.5: gated on physical sensor.
