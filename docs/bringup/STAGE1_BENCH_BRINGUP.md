# Stage 1 — Bench Bring-Up Guide

**Version:** v0.22 (2026-04-07)
**Stage:** 1 (mock hardware, desktop-first)
**Status:** Software baseline frozen — see `rpd/v0.21/`. This guide covers physical bench setup and validation.

---

## Objective

Validate the Stage 1 operator flow on the physical bench, running the software stack on the
target host machine (not the development laptop). This is the gate before Stage 1.5 real-driver
integration begins.

**What this bring-up validates:**
- Software stack deploys and runs on bench host hardware
- Operator flow executes end-to-end via REST API from bench network
- All 12 acceptance criteria in `STAGE1_BENCH_ACCEPTANCE.md` pass
- Physical bench environment is correctly configured for Stage 1.5 readiness

---

## Scope and Safety Baseline

> **SAFETY NOTE:** Stage 1 uses `MockArmDriver`. The arm does **NOT physically move** during
> Stage 1 bring-up. All state transitions (IDLE→HOMING→READY→…) are simulated in software.
> The arm must still be mechanically secured and the E-stop wired — this prepares the bench
> for Stage 1.5 when real arm motion begins.

> **`mock_mode: true` is the Stage 1 safety invariant.** If `GET /status` returns
> `mock_mode: false`, STOP immediately and do not proceed with any handover operations.

---

## Required Hardware on Bench

| Item | Requirement | Stage 1 status |
|------|-------------|----------------|
| Host machine | Python 3.10+, git, LAN-accessible, port 8080 open | Required |
| Arm unit | Powered, mechanically secured to bench mount | Present (will not move) |
| E-stop button | Wired to arm power rail | Bench-ready; not wired to software (Stage 1.5) |
| Tray fixture | slot_A and slot_B marked; ≥ 80 mm clearance around handover zone | Required |
| Water bottle 500 ml | Default object for slot_A | Required for acceptance test |
| Ceramic mug | Default object for slot_B | Optional (secondary demo object) |

**Slot positions (from `configs/slots/stage1_slots.yaml`):**

| Slot | Position (x, y, z mm) | Approach angle | Status |
|------|----------------------|----------------|--------|
| slot_A | 150, 50, 120 | 45° | Enabled |
| slot_B | 150, 0, 120 | 0° | Enabled |
| slot_C | 150, -50, 120 | -45° | Disabled — calibration pending |

**Handover zone:** x=300, y=0, z=200 mm — clearance radius 80 mm. Keep this area clear of obstacles.

---

## Wiring and Power Assumptions

- Arm power rail is isolated from the host machine supply and switched separately
- Host → arm communications interface (USB/serial/CAN) is physically prepared but **not
  connected in Stage 1** (mock driver; no comms traffic)
- E-stop button is wired to the arm power rail (NOT to software in Stage 1; this wiring is
  for Stage 1.5 readiness)
- E-stop button is within reach of the operator at all times during bring-up

---

## Software Setup

```bash
# 1. Clone or pull the repo onto the bench host machine
git clone <repo-url> third-arm && cd third-arm
# OR: git pull origin main (if already cloned)

# 2. Create and activate virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install with dev extras
pip install -e ".[dev]"

# 4. Set the sessions directory (persistent storage on bench)
export THIRD_ARM_SESSIONS_DIR=/data/third-arm/sessions
mkdir -p /data/third-arm/sessions

# 5. Point to the bench config
export THIRD_ARM_CONFIG=configs/app/stage1_bench.yaml

# 6. Start the service (scripts/dev.sh now reads runtime settings)
bash scripts/dev.sh
# OR: uvicorn third_arm.main:app --host 0.0.0.0 --port 8080 --log-level info
```

Service is ready when the log shows:
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

---

## Safe Power-On Sequence

Follow this order exactly:

1. Verify arm is mechanically locked and E-stop is in reach
2. Power on host machine; confirm network is up
3. Start the service (step 6 above); wait for "Uvicorn running" log line
4. Verify health: `GET /health` → `{"ok": true}`
5. **Verify mock mode:** `GET /status` → confirm `"mock_mode": true`
   - **STOP** and do not proceed if `mock_mode` is `false`
6. Power on arm power rail (Stage 1: optional since arm will not move; do it now to test
   the E-stop wiring for Stage 1.5 readiness)

---

## Initial API Verification Sequence

Run these in order. Use `curl`, `httpie`, Postman, or any REST client:

```bash
# 1. Liveness check
curl -s http://bench-host:8080/health
# Expected: {"ok": true, "ts": "...", "message": "..."}

# 2. Arm state check — must show idle and mock_mode: true
curl -s http://bench-host:8080/status
# Expected: {"arm_state": "idle", "mock_mode": true, "session_id": null, ...}

# 3. Home the arm (mock: IDLE → HOMING → READY)
curl -s -X POST http://bench-host:8080/arm/home
# Expected: {"accepted": true, "new_state": "ready"}

# 4. Confirm READY
curl -s http://bench-host:8080/status
# Expected: {"arm_state": "ready", ...}
```

---

## Manual Operator Flow on Bench

After initial verification completes:

```bash
# 5. Start a session
curl -s -X POST http://bench-host:8080/session/start \
  -H "Content-Type: application/json" \
  -d '{"operator_id": "bench_op", "object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"}'
# Expected: {"session_id": "session_...", "started_at": "...", "operator_id": "bench_op"}
# Save the session_id from this response.

# 6. Request a handover
curl -s -X POST http://bench-host:8080/handover/request \
  -H "Content-Type: application/json" \
  -d '{"object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"}'
# Expected: {"handover_id": "hov_...", "status": "complete", ...}

# 7. Verify arm auto-returned to READY
curl -s http://bench-host:8080/status
# Expected: {"arm_state": "ready", ...}

# 8. Stop the session
curl -s -X POST http://bench-host:8080/session/stop
# Expected: {"session_id": "...", "status": "stopped", "stopped_at": "..."}

# 9. Verify bundle in artifacts list
curl -s http://bench-host:8080/artifacts
# Expected: {"bundles": [...], "count": 1}  — session_id from step 5 appears in list

# 10. Inspect the bundle
curl -s http://bench-host:8080/artifacts/<session_id>
# Expected: presence.manifest=true, presence.trace=true, presence.telemetry=true
# trace_summary.event_count >= 6
```

---

## Stop Criteria (Normal Completion)

Bring-up is complete when all of the following are true:
- Session stopped; `status: stopped`
- Bundle present with all 3 files; trace event count ≥ 7
- `arm_state` is `"ready"` or `"idle"` after all operations
- No errors in service log
- All 12 criteria in `STAGE1_BENCH_ACCEPTANCE.md` marked PASS

---

## Abort Criteria

Stop the bring-up immediately if any of these occur:

| Condition | Action |
|-----------|--------|
| `mock_mode: false` from `GET /status` | Kill service, do NOT proceed |
| Any 5xx response from service | Kill service, inspect logs |
| `arm_state` stuck (not returning to `"ready"` after handover) | Kill service, inspect logs |
| `task_lifecycle_completed` event missing from bundle | Inspect service logs, file bug |
| Unhandled exception in service log | Kill service before retrying |
| (Stage 1.5+) Any uncontrolled arm motion | E-stop → power off arm rail immediately |

---

## E-Stop Procedure (Stage 1)

> Stage 1 has no `/arm/estop` REST endpoint. SAFE_STOP state exists in the state machine
> but is not reachable via REST in Stage 1. This will be addressed in Stage 1.5.

**Immediate stop (Stage 1):**
1. Press `Ctrl+C` in the terminal running the service (or send `SIGTERM`)
2. Turn off arm power rail
3. Do NOT attempt to inspect a running session via the API (service is stopped)
4. Inspect the last session bundle on disk: `ls $THIRD_ARM_SESSIONS_DIR`
5. Do NOT restart the service without reviewing the service log for the root cause

**Physical E-stop button (Stage 1):**
The button is wired to the arm power rail but is not wired to the software trigger. Pressing it
cuts power to the arm (Stage 1: no arm motion to stop). This wiring is confirmed during bring-up
so Stage 1.5 can rely on it.

---

## Quick-Reference curl Script

Save as `scripts/bench_quickcheck.sh` for repeatable validation:

```bash
#!/usr/bin/env bash
set -e
HOST=${THIRD_ARM_HOST:-localhost}
PORT=${THIRD_ARM_PORT:-8080}
BASE="http://${HOST}:${PORT}"

echo "=== Health ==="
curl -sf "$BASE/health" | python3 -m json.tool

echo "=== Status ==="
curl -sf "$BASE/status" | python3 -m json.tool

echo "=== Home ==="
curl -sf -X POST "$BASE/arm/home" | python3 -m json.tool

echo "=== Session Start ==="
SESSION=$(curl -sf -X POST "$BASE/session/start" \
  -H "Content-Type: application/json" \
  -d '{"operator_id":"bench_op","object_id":"obj_water_bottle_500ml","slot_id":"slot_A"}')
echo "$SESSION" | python3 -m json.tool
SESSION_ID=$(echo "$SESSION" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

echo "=== Handover ==="
curl -sf -X POST "$BASE/handover/request" \
  -H "Content-Type: application/json" \
  -d '{"object_id":"obj_water_bottle_500ml","slot_id":"slot_A"}' | python3 -m json.tool

echo "=== Post-handover status ==="
curl -sf "$BASE/status" | python3 -m json.tool

echo "=== Session Stop ==="
curl -sf -X POST "$BASE/session/stop" | python3 -m json.tool

echo "=== Artifacts ==="
curl -sf "$BASE/artifacts" | python3 -m json.tool

echo "=== Bundle ==="
curl -sf "$BASE/artifacts/$SESSION_ID" | python3 -m json.tool

echo "=== DONE ==="
```

Usage: `THIRD_ARM_HOST=bench-host bash scripts/bench_quickcheck.sh`
