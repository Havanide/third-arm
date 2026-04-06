# Next Step

## Goal
Stage 1.5: camera integration and vision-gated grasp confirmation.
Gate `home_complete` on physical arm driver confirmation (not auto-triggered as in Stage 1 mock).

## Scope
- Wire real arm driver (or camera-aware mock) into `HandoverService`
- Add grasp confirmation signal before `transfer_complete` trigger
- Gate `home_complete` on physical home sensor confirmation from driver
- Update `MockArmDriver` to simulate confirmation callbacks with configurable latency
- Update DECISIONS_LOG.md, CURRENT_STATE.md, RPD (v0.22+)

## Do not do
- Do not change Stage 1 session/handover logic already frozen
- Do not pull Stage 2 IMU/sEMG intent work
- Do not break existing smoke gate

## Done when
- Vision-gated grasp confirmation path exercised in tests
- `home_complete` gated on driver callback, not auto-triggered
- Smoke gate still passes
- DECISIONS_LOG.md and CURRENT_STATE.md updated
