# Stage 1 Smoke Gate — Implementation Note

**Date:** 2026-04-04
**Relates to:** `tests/integration/test_full_flow.py`, `.github/workflows/python-ci.yml`

---

## What the smoke path covers

`test_full_session_handover_flow` is marked `@pytest.mark.smoke`.
It is the single authoritative Stage 1 acceptance test.

The path it verifies:

```
app startup (lifespan)
  → POST /arm/home          IDLE → HOMING → READY
  → POST /session/start     bundle dir created, session_started trace emitted
  → POST /handover/request  mock sequence runs, handover_completed trace emitted
  → POST /session/stop      bundle closed, session_stopped trace emitted
  → GET  /artifacts         session visible in bundle listing
```

File-level assertions:
- `manifest.json` exists and `closed_at` is set
- `session_trace.ndjson` exists
- `telemetry.mcap` exists (Stage 1 placeholder — binary MCAP not yet written)

Trace event assertions:
- Events present: `session_started`, `handover_requested`, `handover_driver_started`,
  `handover_completed`, `session_stopped`
- Ordering: `session_started` is first, `session_stopped` is last

---

## How to run locally

```bash
# Smoke gate only (fast, ~2s)
pytest -m smoke -v

# Verify marker is registered (no PytestUnknownMarkWarning)
pytest --co -q -m smoke

# Full suite
pytest -q
```

---

## CI behaviour

The CI workflow (`.github/workflows/python-ci.yml`) has two test steps:

1. **Stage 1 smoke gate** — `pytest -m smoke -v`
   Runs first. If the smoke test fails, CI stops immediately. This is the fail-fast gate.

2. **Run tests** — `pytest -q`
   Runs the full suite, including the smoke test again.
   The smoke test is intentionally run twice: once explicitly as the gate, once as part of the suite.
   This is by design — the gate step makes failures immediately visible in CI logs.

GitHub branch protection on `main` requires the matrix checks:
- `test (3.10)`
- `test (3.11)`

Because the smoke step runs inside those required jobs, the Stage 1 smoke path is now an enforced merge gate for `main`.

---

## What the smoke path does NOT cover

- Real arm driver (serial/CAN) — MockArmDriver only
- GPIO trigger, e-stop, power monitor — all stubbed
- Camera pipeline / object detection — not wired in Stage 1
- IMU / sEMG intent sensing — Stage 2+
- Binary MCAP telemetry encoding — Stage 1.5+
- MQTT transport — future extension
- Auth / operator identity — not in Stage 1 scope

---

## Isolation

Artifact paths are isolated per test run using:
```python
monkeypatch.setenv("THIRD_ARM_SESSIONS_DIR", str(tmp_path))
```
No session files leak between test runs. Safe to run in parallel or in CI matrix.
