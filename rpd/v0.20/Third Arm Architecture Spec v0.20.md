# Third Arm Architecture Spec v0.20

**Stage:** 1
**Based on:** v0.19 Architecture Spec
**Date:** 2026-04-06

---

## Architecture change in v0.20

No structural architecture refactor. The change is a runtime policy clarification:
`POST /session/start` now enforces `READY` as an explicit precondition.

---

## Session start precondition

### Runtime rule

`POST /session/start` is accepted only when `StateMachine.state == READY`.

The router does not:
- auto-home from `IDLE`
- trigger implicit transitions to reach `READY`
- guess operator intent from current state

If the current state is anything other than `READY`, the endpoint returns `409 Conflict`.

### 409 contract

```json
{
  "detail": {
    "message": "Session start requires arm state 'ready'; call POST /arm/home first",
    "current_state": "idle"
  }
}
```

The same response shape is also used when a second session start is rejected while another session is already active.

### Relationship to `/arm/home`

`POST /arm/home` remains the explicit way to move the arm from `IDLE` to `READY`.
The Stage 1 smoke path already uses this ordering, so the policy change tightens the contract without changing the intended operator workflow.

---

## Implementation touchpoints

- `src/third_arm/api/routers/session.py`
  - `READY` check only
  - structured `409` detail with `message` + `current_state`
- `tests/integration/test_full_flow.py`
  - happy path from `READY`
  - reject from `IDLE`
- `tests/integration/test_catalog_validation.py`
  - catalog `404` tests now home first so they continue testing catalogue validation rather than state precondition
- `docs/api/openapi.yaml`
  - `409` response for `/session/start` documents the structured conflict schema

---

## Frozen constraints (unchanged)

- Slot model: frozen
- Bundle layout: frozen
- `pytest -m smoke` merge gate: enforced via CI
- `docs/api/openapi.yaml`: authoritative checked-in Stage 1 contract
