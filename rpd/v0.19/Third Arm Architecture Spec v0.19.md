# Third Arm Architecture Spec v0.19

**Stage:** 1
**Based on:** v0.18 Architecture Spec
**Date:** 2026-04-06

---

## Architecture is unchanged from v0.18

No code changes in v0.19. This spec documents the API contract as it exists after the openapi.yaml sync.

---

## Stage 1 endpoint inventory (complete)

### GET /health
- Response 200: `{ok: bool, ts: ISO8601, message: str}`
- Liveness probe — always 200 if process alive

### GET /status
- Response 200: `{ts: ISO8601, arm_state: str, session_id: str|null, uptime_s: float, mock_mode: bool}`

### POST /arm/home
- Response 202: `{accepted: bool, new_state: str}`
- Response 409: command rejected in current arm state
- Valid from: IDLE, READY, TASK_COMPLETE, TASK_ABORTED, SAFE_STOP

### POST /session/start
- Request: `{operator_id: str, object_id?: str, slot_id?: str, notes?: str}`
- Response 200: `{session_id: str, started_at: ISO8601, operator_id: str}`
- Response 404: unknown object_id or slot_id
- Response 409: session already active or arm not in valid state

### POST /session/stop
- Response 200: `{session_id: str, stopped_at: ISO8601, status: "stopped"}`
- Response 404: no active session

### POST /handover/request
- Request: `{object_id: str, slot_id: str}` (both required)
- Response 202: `{handover_id: str, object_id: str, slot_id: str, completed_at: ISO8601, status: "complete"}`
- Response 404: unknown object_id or slot_id
- Response 409: no active session or arm not ready

### GET /artifacts
- Response 200: `{bundles: [{session_id, path, size_bytes}], count: int}`

### GET /artifacts/{session_id}
- `session_id` must match `[A-Za-z0-9][A-Za-z0-9._-]*` (no path traversal)
- Response 200 (healthy bundle):
  ```json
  {
    "session_id": "...",
    "schema_version": "1.0",
    "created_at": "...",
    "closed_at": "...",
    "is_closed": true,
    "presence": {"manifest": true, "trace": true, "telemetry": true},
    "files": [
      {"name": "manifest.json", "category": "manifest", "exists": true, "size_bytes": 512},
      {"name": "session_trace.ndjson", "category": "trace", "exists": true, "size_bytes": 1024},
      {"name": "telemetry.mcap", "category": "telemetry", "exists": true, "size_bytes": 0}
    ],
    "trace_summary": {"event_count": 5},
    "errors": []
  }
  ```
- Response 200 (broken bundle): same shape with nullable manifest fields, `exists: false` for missing files, `errors: ["manifest_missing" | "manifest_unreadable" | "trace_unreadable"]`
- Response 404: unknown session_id or unsafe path-like value

---

## Frozen constraints (unchanged)

- API response shapes: frozen
- Slot model: frozen
- State machine transitions: frozen
- Bundle layout: frozen
- `pytest -m smoke` merge gate: enforced via CI
- `docs/api/openapi.yaml`: hand-maintained, authoritative contract reference
