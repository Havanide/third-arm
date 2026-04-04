# Current State

## Current stage
Stage 1

## Current active slice
Stage 1 smoke path established as mandatory merge gate

## Confirmed implemented
- Operator flow works through REST: `POST /arm/home -> POST /session/start -> POST /handover/request -> POST /session/stop -> GET /artifacts`
- `BundleWriter` is wired into `SessionService` and `HandoverService`
- Session bundles contain `manifest.json`, `session_trace.ndjson`, and placeholder `telemetry.mcap`
- `POST /handover/request` requires an active session
- Session start/stop rollback behavior is covered by targeted tests
- Replay reader and artifact listing work against the runtime-produced bundle layout
- Stage 1 smoke path marked with `@pytest.mark.smoke`; runs as dedicated CI gate before full suite

## Confirmed frozen
- API freeze: yes
- slot model: yes
- state machine: yes
- logging/replay contract: yes

## In progress
- none

## Next planned slice
- Add single-bundle artifact inspection via `GET /artifacts/{session_id}`

## Blockers
- none
