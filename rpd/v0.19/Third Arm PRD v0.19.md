# Third Arm PRD v0.19

**Stage:** 1
**Based on:** v0.18 PRD
**Date:** 2026-04-06

---

## Stage 1 Product Scope (unchanged from v0.18)

Stage 1 remains: desktop-first, operator-triggered, mock hardware.

### Operator REST API — confirmed endpoints (all documented in openapi.yaml)

| Method | Path | Status |
|--------|------|--------|
| GET | `/health` | complete |
| GET | `/status` | complete |
| POST | `/arm/home` | complete |
| POST | `/session/start` | complete |
| POST | `/session/stop` | complete |
| POST | `/handover/request` | complete |
| GET | `/artifacts` | complete |
| GET | `/artifacts/{session_id}` | complete (v0.18) |

### API documentation (v0.19)

`docs/api/openapi.yaml` now accurately reflects all Stage 1 endpoints, request bodies,
response schemas, known 4xx responses, and FastAPI validation errors. Hand-maintained per
decision in DECISIONS_LOG.md. Runtime-generated `/docs` remains available for exploration,
but the checked-in YAML is the authoritative reviewed contract.

---

## Acceptance criteria (cumulative, Stage 1) — unchanged

1. Full operator flow executes end-to-end via REST
2. Bundle produced with `manifest.json`, `session_trace.ndjson`, `telemetry.mcap`
3. `manifest.closed_at` set after session stop
4. Trace events ordered: `session_started` first, `session_stopped` last
5. `GET /artifacts` lists all closed sessions
6. `GET /artifacts/{session_id}` returns bundle metadata with degraded response for broken bundles
7. `pytest -m smoke` passes as merge gate (CI-enforced)
8. `docs/api/openapi.yaml` matches the implemented Stage 1 API surface
