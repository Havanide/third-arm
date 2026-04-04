# Third Arm PRD v0.18

**Stage:** 1
**Based on:** v0.17 PRD
**Date:** 2026-04-04

---

## Stage 1 Product Scope (updated)

Stage 1 remains: desktop-first, operator-triggered, mock hardware.

### Operator REST API — confirmed endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| GET | `/status` | Arm state + session info |
| POST | `/arm/home` | Home arm to READY |
| POST | `/session/start` | Begin session, open bundle |
| POST | `/session/stop` | End session, close bundle |
| POST | `/handover/request` | Trigger handover sequence |
| GET | `/artifacts` | List all session bundles |
| **GET** | **`/artifacts/{session_id}`** | **Inspect one bundle (v0.18 addition)** |

### Bundle inspection feature (v0.18)

Operators can now inspect a specific session bundle by `session_id`.

**What it returns:**
- Manifest metadata: `session_id`, `schema_version`, `created_at`, `closed_at`, `is_closed`
- File inventory: for each expected bundle file (`manifest.json`, `session_trace.ndjson`, `telemetry.mcap`) — whether it exists and its size in bytes
- Trace summary: total event count from `session_trace.ndjson`

**What it does NOT do:**
- Does not serve file contents (no download)
- Does not decode MCAP telemetry (Stage 1.5+)
- Does not paginate or filter (future enhancement)

**Error behaviour:**
- 404 if session_id not found or manifest.json missing
- Degraded response (files with `exists: false`) if bundle is incomplete

---

## Acceptance criteria (cumulative, Stage 1)

1. Full operator flow executes end-to-end via REST
2. Bundle is produced with `manifest.json`, `session_trace.ndjson`, `telemetry.mcap`
3. `manifest.closed_at` is set after session stop
4. Trace events are ordered: `session_started` first, `session_stopped` last
5. `GET /artifacts` lists all closed sessions
6. `GET /artifacts/{session_id}` returns bundle metadata and file inventory
7. `pytest -m smoke` passes as merge gate (CI-enforced)
