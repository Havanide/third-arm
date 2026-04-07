# Stage 1 — Bench Bring-Up Checklist

**Version:** v0.22 (2026-04-07)
**Stage:** 1 (mock hardware)
**Reference:** `STAGE1_BENCH_BRINGUP.md` (full guide), `STAGE1_BENCH_ACCEPTANCE.md` (pass/fail criteria)

---

> Complete each section in order. Do not skip ahead. If any item fails, follow the abort
> procedure in `STAGE1_BENCH_BRINGUP.md` before continuing.

---

## A — Before Power

- [ ] Arm unit mechanically secured to bench mount; no loose connectors
- [ ] Tray fixture in place: slot_A (150,50,120mm) and slot_B (150,0,120mm) positions marked
- [ ] Handover zone clear (x=300,y=0,z=200mm): ≥ 80mm clearance radius, no obstacles
- [ ] Water bottle 500ml placed at slot_A
- [ ] Ceramic mug placed at slot_B (optional; required for secondary demo)
- [ ] E-stop button in reach of operator; wired to arm power rail
- [ ] Host machine on LAN; port 8080 reachable from test workstation
- [ ] Sessions directory writable: `/data/third-arm/sessions` (or env override confirmed)
- [ ] Bench config file in place: `configs/app/stage1_bench.yaml`
- [ ] Virtual environment set up: `python3 -m venv .venv && pip install -e ".[dev]"` completed

---

## B — Power On

- [ ] Host machine powered on; OS booted; network confirmed up
- [ ] Service started:
  ```bash
  export THIRD_ARM_SESSIONS_DIR=/data/third-arm/sessions
  export THIRD_ARM_CONFIG=configs/app/stage1_bench.yaml
  source .venv/bin/activate
  bash scripts/dev.sh
  ```
- [ ] Log shows: `Uvicorn running on http://0.0.0.0:8080`
- [ ] `GET /health` → `{"ok": true}` ✓
- [ ] Arm power rail ON (Stage 1: optional; do it to test E-stop wiring)

---

## C — Service Health and Safety Gate

- [ ] `GET /status` → `{"arm_state": "idle", ...}` ✓
- [ ] **`mock_mode: true` confirmed** — **ABORT IMMEDIATELY if `mock_mode: false`**
- [ ] No errors in service log at startup

---

## D — Arm / Actuator Bus Check (Stage 1: mock)

- [ ] `POST /arm/home` → `202 {"accepted": true, "new_state": "ready"}` ✓
- [ ] `GET /status` → `{"arm_state": "ready"}` ✓
- [ ] (Stage 1: mock) No physical arm motion occurred — expected and correct

---

## E — Guard Check: IDLE Rejection

- [ ] Restart service (Ctrl+C, restart) to reset to IDLE state
- [ ] **Without** calling `POST /arm/home`, attempt `POST /session/start`:
  ```json
  {"operator_id": "bench_op", "object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"}
  ```
- [ ] Response: `409` with `{"detail": {"current_state": "idle", "message": "..."}}` ✓

---

## F — Graceful Stop Check

- [ ] `POST /arm/home` → READY
- [ ] `POST /session/start {...}` → 200 with `session_id` ✓
- [ ] `POST /session/stop` → `200 {"status": "stopped"}` ✓
- [ ] `GET /artifacts` → `count >= 1`, session_id in list ✓

---

## G — Full Operator Flow (Primary Acceptance Flow)

- [ ] `POST /arm/home` → `{new_state: "ready"}` ✓
- [ ] `POST /session/start`:
  ```json
  {"operator_id": "bench_op", "object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"}
  ```
  → `200 {"session_id": "session_...", "started_at": "...", "operator_id": "bench_op"}` ✓
  Record `session_id`: ___________________________
- [ ] `POST /handover/request`:
  ```json
  {"object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"}
  ```
  → `202 {"handover_id": "hov_...", "status": "complete", ...}` ✓
  Record `handover_id`: ___________________________
- [ ] `GET /status` → `{"arm_state": "ready"}` (post-handover auto-return confirmed) ✓
- [ ] `POST /session/stop` → `200 {"status": "stopped"}` ✓

---

## H — Artifact Verification

- [ ] `GET /artifacts` → session_id in `bundles[]`; `count >= 1` ✓
- [ ] `GET /artifacts/{session_id}`:
  - [ ] `presence.manifest: true` ✓
  - [ ] `presence.trace: true` ✓
  - [ ] `presence.telemetry: true` ✓
  - [ ] `trace_summary.event_count >= 6` ✓
        (expected events: session_started, handover_requested, task_lifecycle_entered,
        handover_driver_started, handover_completed, task_lifecycle_completed, session_stopped)
  - [ ] `is_closed: true` ✓
  - [ ] `errors: []` (empty) ✓

---

## I — E-Stop Test (Stage 1)

- [ ] Start a new session: `POST /arm/home` + `POST /session/start {...}`
- [ ] Kill service: `Ctrl+C` in service terminal
- [ ] Service process terminated — confirmed
- [ ] Arm power rail OFF (physical E-stop button pressed)
- [ ] Inspect bundle on disk: `ls $THIRD_ARM_SESSIONS_DIR`
- [ ] Bundle directory exists (may be incomplete — expected for aborted session) ✓
- [ ] Restart service; confirm `GET /health` → `{ok: true}` ✓
- [ ] `GET /status` → `{arm_state: "idle"}` (fresh state after restart) ✓

---

## J — Smoke Gate on Bench Machine

- [ ] Run full smoke gate:
  ```bash
  source .venv/bin/activate
  pytest -m smoke -v
  ```
- [ ] Output: `1 passed` ✓
- [ ] Run full suite:
  ```bash
  pytest -q
  ```
- [ ] Output: `39 passed` ✓

---

## Bring-Up Result

| Result | Condition |
|--------|-----------|
| **PASS** | All checkboxes checked; 0 unexpected failures |
| **PARTIAL** | All items A–H pass; J (smoke gate on bench) not yet run |
| **FAIL** | Any abort criterion triggered; any acceptance criterion not met |

**Operator sign-off:** ___________________________
**Date:** ___________________________
**Bench host machine:** ___________________________
**Git commit on bench:** ___________________________
