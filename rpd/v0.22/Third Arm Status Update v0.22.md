# Third Arm — Status Update v0.22

**Date:** 2026-04-07
**Stage:** 1 (mock hardware, desktop-first)
**Branch:** feat/stage1-bench-bringup

---

## Milestone: Stage 1 Bench Bring-Up Pack Shipped

Stage 1 software is fully frozen and validated. The repository now contains everything needed
to run the first physical bench bring-up: environment guide, operator checklist, acceptance
criteria, and bench-specific configuration.

**No runtime code was changed in this slice.** All 39 tests continue to pass.

---

## What Changed in v0.22

### `docs/bringup/` — new directory

Three documents created to support the first physical bench session:

**STAGE1_BENCH_BRINGUP.md** — Full bring-up guide:
- Objective and scope
- Required hardware (host machine, arm unit, E-stop, tray fixture, objects)
- Slot positions referenced from `stage1_slots.yaml`
- Wiring and power assumptions
- Software setup steps
- Safe power-on sequence with mock_mode safety gate
- Initial API verification sequence
- Manual operator flow (curl commands)
- Stop criteria, abort criteria, E-stop procedure (Stage 1: SIGTERM)
- Quick-reference `bench_quickcheck.sh` script

**STAGE1_BENCH_CHECKLIST.md** — Step-by-step operator checklist:
- 10 sections (A–J): pre-power, power on, service health, actuator check, guard check,
  graceful stop check, full operator flow, artifact verification, E-stop test, smoke gate
- Sign-off table (date, operator, bench host, git SHA, verdict)

**STAGE1_BENCH_ACCEPTANCE.md** — Acceptance criteria:
- 12 numbered pass/fail criteria
- Expected trace event sequence (7 events per session)
- FAIL criteria (abort conditions)
- Known gaps table (non-blocking for Stage 1): E-stop REST endpoint, home_complete gate,
  camera grasp confirmation, telemetry.mcap placeholder

### `configs/app/stage1_bench.yaml` — new config

Bench-specific app config:
- `server.host: "0.0.0.0"` (LAN-accessible; stage1_desktop.yaml uses 127.0.0.1)
- `hardware.mock: true` — safety invariant; must remain true for all Stage 1 bring-up
- `logging.sessions_dir: "/data/third-arm/sessions"` — persistent path on bench host
- All other settings identical to `stage1_desktop.yaml`

### Status docs updated

- `DECISIONS_LOG.md` — new entry: Stage 1 bench bring-up uses MockArmDriver throughout
- `CURRENT_STATE.md` — active slice updated to "Stage 1 bench bring-up pack"; shipped items listed
- `NEXT_STEP.md` — expanded Stage 1.5 prerequisites and scope (estop endpoint, real driver, camera)
- `OPEN_QUESTIONS.md` — new open question: `/arm/estop` REST endpoint design for Stage 1.5

---

## Stage 1 Software Baseline — Fully Frozen

All software acceptance criteria met (from v0.21):

| Criterion | Status |
|-----------|--------|
| Operator flow: home → session → handover → stop → artifacts | ✅ |
| Bundle artifacts: manifest.json, session_trace.ndjson, telemetry.mcap | ✅ |
| Session READY precondition enforced | ✅ |
| Task lifecycle state machine fully bound | ✅ |
| Trace events: full lifecycle sequence per handover (5 events) | ✅ |
| Arm auto-returns to READY after handover | ✅ |
| Smoke gate: mandatory CI merge gate | ✅ |
| OpenAPI spec: hand-maintained, fully synced | ✅ |
| Path traversal protection on artifact inspection | ✅ |

---

## Next

Stage 1.5: real arm driver integration, camera bring-up, and vision-gated grasp confirmation.
Prerequisites: Stage 1 bench bring-up PASS verdict, real driver interface, camera module,
home sensor wired and confirmed.
