# Open Questions

- Should Stage 1 continue allowing `POST /session/start` from `IDLE`, or should explicit homing to `READY` become mandatory before session start?
- ~~Should checked-in `docs/api/openapi.yaml` remain hand-maintained, or should runtime FastAPI schemas become the authoritative contract source?~~ **Resolved (2026-04-06):** hand-maintained. FastAPI `/docs` available for interactive use. Decision in DECISIONS_LOG.md.
- ~~For the next artifact-detail slice, should `GET /artifacts/{session_id}` expose only manifest/file metadata, or also include a summarized trace view?~~ **Resolved (v0.18):** returns manifest metadata + file inventory + trace event count only. No content download, no MCAP decoding.
