# Third Arm Procurement Estimate v0.16

This note mirrors the spreadsheet version and exists so procurement logic stays in the repo history.

## Buying rule
- **Mandatory now**: anything that blocks Stage 1 bench bring-up.
- **Buy soon**: parts that are not blockers for the first handover loop, but are worth reserving early to avoid rework.
- **Defer**: anything that drags Stage 2/3 complexity back into Stage 1.

## Core rule for substitutions
A part can be swapped only if it preserves:
- desktop-first Stage 1;
- operator-triggered control;
- camera-ready geometry;
- edge-first REST + WebSocket control plane;
- 24V rail and hardwired safety path;
- replay-capable logging.

## Engineering recommendation
For Stage 1, do **not** buy wearable mount hardware, body batteries, or sEMG kits before the bench loop is stable. That is where budgets get diluted and progress slows down.
