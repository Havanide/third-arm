# Third Arm — Intent-Driven Handover Service

> **Stage 1 — Desktop-first skeleton**

Modular supernumerary robotic arm that delivers objects on operator request.
The server sits in the **northbound control plane** (REST + WebSocket); it is **not** in the safety-critical hardware loop.

---

## Architecture at a glance

```
Operator UI / CLI
      │  REST  │  WebSocket
      ▼         ▼
  third-arm FastAPI server        ← this repo
      │
      ├─ domain  (state machine, session, handover logic)
      ├─ adapters (mock_arm → hardware → vision → intent)
      └─ logging  (bundle_writer → MCAP + NDJSON traces)
```

### Roadmap stages

| Stage | Focus | Status |
|-------|-------|--------|
| 1 | Operator-triggered, mock hardware, desktop-first | **Current** |
| 1.5 | Camera-on (object detection), real arm driver | Planned |
| 2 | IMU / sEMG intent sensing | Planned |
| 3 | Full autonomous handover loop | Planned |

---

## Quick start

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env as needed (defaults work for Stage 1 mock mode)
```

### 3. Run dev server

```bash
bash scripts/dev.sh
# or
uvicorn third_arm.main:app --reload --host 0.0.0.0 --port 8080
```

### 4. Explore API

- Swagger UI: http://localhost:8080/docs
- ReDoc:       http://localhost:8080/redoc
- OpenAPI JSON: http://localhost:8080/openapi.json

---

## Endpoints (Stage 1 stubs)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| GET | `/status` | Arm state + session info |
| POST | `/session/start` | Begin a new handover session |
| POST | `/session/stop` | End / abort current session |
| POST | `/arm/home` | Command arm to home position |
| POST | `/handover/request` | Trigger object handover |
| GET | `/artifacts` | List session bundles |
| WS | `/ws/stream` | Real-time telemetry stream |

---

## Project layout

```
configs/        Runtime YAML configs (app profiles, slot maps, calibration)
docs/           API specs (OpenAPI, AsyncAPI), architecture diagrams
src/third_arm/  Main Python package
  api/          FastAPI routers, WebSocket, Pydantic schemas
  core/         Settings, IDs, clock, error types
  domain/       State machine, session logic, handover logic
  adapters/     mock_arm | hardware | vision | intent
  logging/      Bundle writer, MCAP traces, replay reader
  storage/      File system helpers
  cli/          Dev runner, bundle export, replay tool
tests/          unit / integration / replay smoke tests
scripts/        dev.sh, format.sh, seed/validate helpers
sessions/       Runtime session bundles (gitignored)
```

---

## Development commands

```bash
bash scripts/format.sh          # ruff format + check
pytest tests/unit/              # unit tests
pytest tests/integration/       # integration tests (starts app)
python scripts/validate_bundle.py sessions/<bundle-dir>
```

---

## Intentionally left as stub (Stage 1)

- Real arm serial/CAN driver (`adapters/hardware/arm_driver.py`)
- GPIO trigger & e-stop (`adapters/hardware/`)
- Camera pipeline (`adapters/vision/`)
- IMU / sEMG processing (`adapters/intent/`)
- MCAP binary writing (placeholder only)
- MQTT transport
- Auth / operator identity
