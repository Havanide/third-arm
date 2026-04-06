# Third Arm PRD v0.20

**Stage:** 1
**Based on:** v0.19 PRD
**Date:** 2026-04-06

---

## Stage 1 Product Scope (updated)

Stage 1 remains: desktop-first, operator-triggered, mock hardware.

### Operator REST API — confirmed flow

The operator setup flow is now explicitly:

`POST /arm/home -> POST /session/start -> POST /handover/request -> POST /session/stop -> GET /artifacts`

`POST /session/start` is no longer accepted from `IDLE`.
Operators must first home the arm to `READY`.

### Session start policy (v0.20)

- `POST /session/start` succeeds only when the current arm state is `READY`
- If the state is not `READY`, the endpoint returns `409 Conflict`
- The error response includes:
  - a human-readable `message`
  - `current_state`
- No implicit home or auto-transition occurs inside `/session/start`

---

## Acceptance criteria (cumulative, Stage 1)

1. Full operator flow executes end-to-end via REST
2. The operator homes the arm before starting a session
3. `POST /session/start` rejects non-`READY` states with explicit `409`
4. Bundle produced with `manifest.json`, `session_trace.ndjson`, `telemetry.mcap`
5. `manifest.closed_at` set after session stop
6. `GET /artifacts/{session_id}` returns bundle metadata with degraded response for broken bundles
7. `pytest -m smoke` passes as merge gate (CI-enforced)
8. `docs/api/openapi.yaml` matches the implemented Stage 1 API surface
