# Third Arm — Assembly Note v0.22

**Date:** 2026-04-07
**Stage:** 1 (mock hardware)

No mechanical assembly changes in v0.22. This note documents the bench environment layout
required for Stage 1 bring-up.

See `rpd/v0.17/Third Arm Assembly Note v0.17.md` for the current physical arm assembly specification.

---

## Stage 1 Bench Layout

### Arm Mount

- Arm unit rigidly secured to bench fixture before any power is applied
- Mount must prevent motion in X, Y, Z (arm will not move in Stage 1 mock; secured for Stage 1.5)
- Access clearance: ≥ 150 mm on all sides for cable routing and manual reach

### Tray Fixture

Position the tray fixture so that slot centroids match the catalogue positions (from `configs/slots/stage1_slots.yaml`):

| Slot | Position (x, y, z mm) | Status | Object |
|------|----------------------|--------|--------|
| slot_A | 150, 50, 120 | Enabled | Water bottle 500ml |
| slot_B | 150, 0, 120 | Enabled | Ceramic mug |
| slot_C | 150, -50, 120 | Disabled | — (pending calibration) |

Origin: arm base, with X pointing away from operator, Y pointing left, Z pointing up.

### Handover Zone

Centre: x=300, y=0, z=200 mm from arm base.
Clearance radius: 80 mm. Keep this volume unobstructed during bring-up.

### Host Machine

- Positioned outside the handover zone clearance radius
- Connected to LAN; port 8080 accessible from test workstation
- Service terminal visible to operator during bring-up

---

## E-Stop Wiring (Stage 1 Readiness)

| Component | Stage 1 Status |
|-----------|----------------|
| E-stop button | Wired to arm power rail |
| E-stop → software | NOT wired in Stage 1; wired in Stage 1.5 via OS signal or REST |
| Physical button location | Within operator reach from the handover zone |

The button must be tested (arm rail power cut confirmed) during Section I of the bring-up checklist
before the bring-up PASS verdict is recorded.

---

## Power Sequence

1. Host machine ON
2. Service started; `GET /health` → `{ok: true}`; `mock_mode: true` confirmed
3. Arm power rail ON (Stage 1: optional; do it to test E-stop wiring)

Power-off reverse order:
1. `POST /session/stop` (if session active)
2. Kill service (Ctrl+C)
3. Arm power rail OFF
4. Host machine OFF

---

## Stage 1.5 Assembly Prerequisites

Before Stage 1.5 bring-up with real arm motion:
- Camera module mounted on arm or bench; field of view covers handover zone
- Home sensor wired to arm and to host comms interface
- Host → arm comms interface connected (USB/serial/CAN per driver spec)
- E-stop button wired to OS signal or driver kill switch (in addition to power rail)
- Tray position calibrated (slot_C may be enabled after calibration)
