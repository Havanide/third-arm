# Third Arm Status Update v0.20

**Date:** 2026-04-06
**Stage:** 1 (desktop-first, operator-triggered, mock hardware)
**Previous version:** v0.19

---

## What changed in v0.20

### `POST /session/start` now requires `READY`

The state policy ambiguity for session start is now closed.

**Behavior change:**
- `POST /session/start` succeeds only from `READY`
- direct calls from `IDLE` now return `409 Conflict`
- the `409` response includes a human-readable message and `current_state`
- no implicit home is performed inside `/session/start`

### Tests updated

- Stage 1 smoke path remains unchanged and still goes through:
  `POST /arm/home -> POST /session/start`
- Added explicit integration coverage for:
  - success from `READY`
  - `409` rejection from `IDLE`
- Updated catalog validation tests so they still exercise `404` object/slot checks after homing to `READY`

### API docs updated

- `docs/api/openapi.yaml` now documents the structured `409` response for `/session/start`
- The operator flow is explicitly documented as `home -> session/start`

---

## Stage 1 milestone status

- Operator REST flow: complete
- Bundle/replay logging: complete and wired
- E2E smoke gate: complete
- Bundle inspection endpoint: complete
- OpenAPI contract sync: complete
- Session start READY policy: complete (this version)

**Next slice:** Decide whether `POST /session/start` should also trigger the state-machine `session_start` transition during Stage 1.

---

## Files not changed in v0.20

- Procurement: no BOM change
- Assembly: no hardware change
- Stage 1.5/2/3 features: untouched
