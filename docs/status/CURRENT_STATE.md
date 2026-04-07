# Current State

## Current stage
Stage 1

## Current active slice
`Stage 1 bench bring-up pack`

## Confirmed implemented
- Operator flow works through REST: `POST /arm/home -> POST /session/start -> POST /handover/request -> POST /session/stop -> GET /artifacts`
- `BundleWriter` is wired into `SessionService` and `HandoverService`
- Session bundles contain `manifest.json`, `session_trace.ndjson`, and placeholder `telemetry.mcap`
- `POST /handover/request` requires an active session
- Session start/stop rollback behavior is covered by targeted tests
- Replay reader and artifact listing work against the runtime-produced bundle layout
- Stage 1 smoke path marked with `@pytest.mark.smoke`; runs as dedicated CI gate before full suite
- `GET /artifacts/{session_id}` returns bundle metadata, presence flags, file inventory, and trace event count; 404 for unknown/unsafe ids; degraded response for incomplete or broken bundles inside the sessions root
- `docs/api/openapi.yaml` is updated as the authoritative hand-maintained Stage 1 contract, including request bodies, success responses, known 4xx responses, and FastAPI validation errors
- `POST /session/start` is allowed only from `READY`; direct calls from `IDLE` now return `409` with structured `detail.message` and `detail.current_state`
- `POST /handover/request` is the task lifecycle entry point: triggers full state sequence READY→TASK_ARMING→ACQUIRE→LIFT→PRESENT→TRANSFER_WAIT→RELEASE→RETRACT→TASK_COMPLETE→HOMING→READY
- Trace events emitted per handover: `handover_requested`, `task_lifecycle_entered`, `handover_driver_started`, `handover_completed`, `task_lifecycle_completed`
- Arm auto-returns to READY after each handover (Stage 1 mock); Stage 1.5 will gate on physical home confirmation
- Integration tests verify post-handover arm state (READY), direct non-READY rejection for `POST /handover/request`, and full lifecycle event ordering

## Confirmed frozen
- API freeze: yes
- slot model: yes
- state machine: yes
- logging/replay contract: yes

## In progress
- none

## Shipped — bench bring-up pack (v0.22)
- `docs/bringup/STAGE1_BENCH_BRINGUP.md` — full bring-up guide (power sequence, operator flow, abort criteria, E-stop procedure)
- `docs/bringup/STAGE1_BENCH_CHECKLIST.md` — step-by-step operator checklist (10 sections, A–J)
- `docs/bringup/STAGE1_BENCH_ACCEPTANCE.md` — 12 acceptance criteria with pass/fail/known-gaps table
- `configs/app/stage1_bench.yaml` — bench config profile; now loadable via `THIRD_ARM_CONFIG` or `THIRD_ARM_CONFIG_PROFILE=stage1_bench`
- `scripts/dev.sh` now resolves host/port/log-level/reload from runtime settings, so bench launch instructions match the repo behavior

## Next planned slice
- Stage 1.5: real arm driver integration + camera; wire `ArmDriverABC` implementation, gate `home_complete` on physical sensor, enable camera, add `POST /arm/estop` endpoint

## Blockers
- none
