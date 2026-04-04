# Next Step

## Goal
Sync `docs/api/openapi.yaml` with the current Stage 1 API surface.

## Scope
- Update `openapi.yaml` to include all current Stage 1 endpoints:
  `GET /health`, `GET /status`, `POST /arm/home`, `POST /session/start`, `POST /session/stop`,
  `POST /handover/request`, `GET /artifacts`, `GET /artifacts/{session_id}`
- Add response schemas for `GET /artifacts/{session_id}` (bundle inspection response)
- Resolve open question: hand-maintained vs auto-generated from FastAPI

## Do not do
- Do not change endpoint behaviour or response contracts
- Do not add new endpoints in this slice
- Do not pull Stage 1.5 vision or MCAP work
- Do not refactor routers

## Done when
- `docs/api/openapi.yaml` matches current implementation
- All existing Stage 1 paths and responses documented
- `CURRENT_STATE.md` and `DECISIONS_LOG.md` updated
