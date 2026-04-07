# Open Questions

- ~~Should `POST /session/start` also trigger the state-machine `session_start` transition in Stage 1, or remain a pure session/bundle gate until `POST /handover/request`?~~ **Resolved (2026-04-06):** `POST /session/start` is a pure bundle gate. `POST /handover/request` is the task lifecycle entry point (READY→TASK_ARMING). Decision in DECISIONS_LOG.md.
- ~~Should Stage 1 continue allowing `POST /session/start` from `IDLE`, or should explicit homing to `READY` become mandatory before session start?~~ **Resolved (2026-04-06):** `POST /session/start` now requires explicit `READY`; operators must call `POST /arm/home` first.
- ~~Should checked-in `docs/api/openapi.yaml` remain hand-maintained, or should runtime FastAPI schemas become the authoritative contract source?~~ **Resolved (2026-04-06):** hand-maintained. FastAPI `/docs` available for interactive use. Decision in DECISIONS_LOG.md.
- ~~For the next artifact-detail slice, should `GET /artifacts/{session_id}` expose only manifest/file metadata, or also include a summarized trace view?~~ **Resolved (v0.18):** returns manifest metadata + file inventory + trace event count only. No content download, no MCAP decoding.

## Open (Stage 1.5 scope)

- `POST /arm/estop` REST endpoint: Stage 1 has no software E-stop endpoint. `SAFE_STOP` state exists in the state machine but has no REST trigger. Physical E-stop button is wired to arm power rail only. Must be added in Stage 1.5 before real arm motion begins. Design question: should `estop` be a top-level emergency trigger (valid from all states) or routed through existing state-machine `trigger()` semantics?
