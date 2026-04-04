# Third Arm PRD v0.17

## Scope of this version
This version does not change the Stage 1 product scope.
It hardens the acceptance criteria for the already-agreed Stage 1 operator flow.

## Product delta vs v0.16
- Stage 1 now has one explicit end-to-end smoke path as a pre-merge acceptance gate
- The required path remains desktop-first, operator-triggered, and mock-hardware-based
- No new Stage 1.5 / 2 / 3 capabilities are introduced in this slice

## Stage 1 acceptance path
The baseline flow that must remain working before merge:
1. application startup
2. `POST /arm/home`
3. `POST /session/start`
4. `POST /handover/request`
5. `POST /session/stop`
6. `GET /artifacts`

## Required acceptance evidence
- `manifest.json` exists
- `session_trace.ndjson` exists
- `telemetry.mcap` exists
- trace includes `session_started`
- trace includes `handover_completed`
- manifest `closed_at` is set
- bundle is visible via `GET /artifacts`

## What did not change
- No product-scope expansion
- No new hardware requirement
- No new object set
- No Stage 1.5 camera logic
- No Stage 2 intent logic
- No Stage 3 autonomy changes

## Why this matters before hardware bring-up
Before bench hardware work expands, the repo needs one trustworthy software path that proves:
- the app starts
- the operator flow works
- the bundle is written correctly
- replay artifacts are present after the run

This reduces the risk of mixing software regressions with hardware regressions during bring-up.
