# Third Arm — Procurement Note v0.22

**Date:** 2026-04-07
**Stage:** 1 (mock hardware)

No BOM changes in v0.22. Stage 1 bring-up uses `MockArmDriver` — all state transitions
are simulated in software. No new hardware is required for Stage 1 bench bring-up.

See `rpd/v0.16/Third Arm Procurement Note v0.16.md` for the current Bill of Materials.

---

## Stage 1 Bench Bring-Up — Required Items

All of these should already be on hand or available in the lab:

| Item | Requirement | Source |
|------|-------------|--------|
| Host machine | Python 3.10+; LAN port 8080 | In house |
| Bench fixture / mount | Rigid arm mount | Existing (v0.17 assembly) |
| Tray fixture | slot_A and slot_B positions | Existing |
| Water bottle 500ml | Demo object for slot_A | In house |
| Ceramic mug | Demo object for slot_B | In house |
| E-stop button | Wired to arm power rail | Existing wiring |

No new procurement required for Stage 1 bring-up.

---

## Stage 1.5 — Procurement Prerequisites

The following items must be procured and on hand before Stage 1.5 bring-up begins:

| Item | Purpose | Notes |
|------|---------|-------|
| Camera module | Vision-gated grasp confirmation | Field of view must cover handover zone (300,0,200mm) |
| Home sensor | Gate `home_complete` on physical confirmation | Must be compatible with arm mount and driver interface |
| Real arm driver interface | Host → arm comms (USB/serial/CAN) | Spec TBD in Stage 1.5 planning |
| E-stop signal cable | Wire button to OS/driver kill signal | In addition to existing power rail cut |

Stage 1.5 procurement details will be specified in the Stage 1.5 architecture planning slice
(RPD v0.23+).
