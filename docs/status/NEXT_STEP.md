# Next Step

## Goal
Stage 1.5: real arm driver integration, camera bring-up, and vision-gated grasp confirmation.
This is the first slice where the arm physically moves.

## Prerequisites (before starting Stage 1.5)
1. Stage 1 bench bring-up PASS verdict recorded (all 12 criteria in `STAGE1_BENCH_ACCEPTANCE.md`)
2. Real arm driver interface identified and available (USB/serial/CAN)
3. Camera module physically mounted and accessible
4. Home sensor wired and confirmed functional
5. `POST /arm/estop` endpoint designed and agreed (routes to `SAFE_STOP` state)

## Scope
- Add `POST /arm/estop` REST endpoint → triggers state machine `safe_stop` (new trigger needed) → `SAFE_STOP` state
- Wire `ArmDriverABC` real implementation into `HandoverService` (replace `MockArmDriver`)
- Gate `home_complete` on physical home sensor confirmation callback from driver (not auto-triggered)
- Add grasp confirmation signal before `transfer_complete` trigger (camera-gated)
- Enable camera: `camera.enabled: true` in Stage 1.5 config
- Update `MockArmDriver` to simulate confirmation callbacks with configurable latency (for tests)
- Update `docs/api/openapi.yaml`: add `/arm/estop` endpoint
- Update DECISIONS_LOG.md, CURRENT_STATE.md, RPD (v0.22+)

## Do not do
- Do not change frozen Stage 1 session/handover API contract
- Do not pull Stage 2 IMU/sEMG intent work
- Do not break existing smoke gate (39/39 must still pass with mock driver path)

## Done when
- `POST /arm/estop` available and tested
- `home_complete` gated on driver callback (not auto-triggered)
- Vision-gated grasp confirmation path exercised in tests
- Smoke gate still passes
- Bench bring-up repeated with real driver; PASS verdict recorded
- DECISIONS_LOG.md and CURRENT_STATE.md updated
