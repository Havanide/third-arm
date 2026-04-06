# Third Arm — Assembly Note v0.21

**Date:** 2026-04-06
**Stage:** 1 (mock hardware)

No hardware assembly changes in v0.21. Physical arm and mount configuration is unchanged from v0.17.

See `rpd/v0.17/Third Arm Assembly Note v0.17.md` for the current physical assembly specification.

---

## Bring-Up Sequence (Stage 1 → Stage 1.5)

When transitioning from Stage 1 (mock) to Stage 1.5 (real hardware):

1. Replace `MockArmDriver` with real arm driver implementing `ArmDriverABC`
2. Wire physical home sensor to gate `home_complete` trigger (currently auto-triggered in mock)
3. Wire camera feed to `HandoverService` for grasp confirmation before `transfer_complete`
4. Run smoke gate against real hardware: `pytest -m smoke -v`
5. Verify `session_trace.ndjson` and `telemetry.mcap` populated correctly

The REST API contract, state machine, and bundle format are frozen and do not require changes
for Stage 1.5 hardware integration.
