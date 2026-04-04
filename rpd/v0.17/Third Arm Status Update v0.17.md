# Third Arm Status Update v0.17

**Date:** 2026-04-04
**Stage:** 1 (desktop-first, operator-triggered, mock hardware)
**Previous version:** v0.16

---

## What changed in v0.17

### Stage 1 smoke path — mandatory merge gate

The existing `test_full_session_handover_flow` integration test has been formally promoted
to a labelled, machine-enforced merge gate for all PRs targeting `main`.

**Changes made:**
- `@pytest.mark.smoke` added to `test_full_session_handover_flow` in `tests/integration/test_full_flow.py`
- `smoke` marker registered in `pyproject.toml`
- Dedicated CI step `Stage 1 smoke gate` added to `.github/workflows/python-ci.yml`,
  runs `pytest -m smoke -v` before the full test suite
- `AGENTS.md` updated: smoke path is now item 3 in "Required before finishing a task"
- Decision recorded in `docs/decisions/DECISIONS_LOG.md`

---

## PRD implication

Stage 1 baseline now includes a machine-enforced acceptance path.
Every PR to `main` must demonstrate that the full operator flow executes end-to-end
without real hardware before merge is permitted.

The acceptance path covers:
1. App starts cleanly (FastAPI lifespan)
2. `POST /arm/home` → arm reaches READY state
3. `POST /session/start` → session opened, bundle directory created
4. `POST /handover/request` → handover completes, trace events emitted
5. `POST /session/stop` → session closed, bundle finalized
6. Bundle files present on disk: `manifest.json`, `session_trace.ndjson`, `telemetry.mcap`
7. Manifest `closed_at` is set
8. Trace event ordering verified: `session_started` first, `session_stopped` last
9. `GET /artifacts` → session visible in bundle listing

---

## Architecture implication

The e2e flow runs exclusively against `MockArmDriver`. No real serial/CAN driver,
no GPIO, no camera pipeline, no IMU/sEMG. The `telemetry.mcap` file is a placeholder
(Stage 1 only writes the file; binary MCAP encoding deferred to Stage 1.5+).

Isolated artifact paths use `tmp_path` + `monkeypatch.setenv("THIRD_ARM_SESSIONS_DIR", ...)`,
making the test deterministic and side-effect-free.

---

## Stage 1 implementation milestone status

Stage 1 is now closed as an implementation milestone.

All Stage 1 deliverables confirmed:
- Operator REST flow: complete
- Bundle/replay logging: complete and wired
- Session lifecycle hardening: complete
- Catalog validation: complete
- E2E smoke gate: complete (this version)

**Next slice:** `GET /artifacts/{session_id}` — single-bundle artifact inspection endpoint.

---

## Files not changed in v0.17

- `Third Arm PRD v0.16.docx` — no product scope change; PRD implications noted above
- `Third Arm Architecture Spec v0.16.docx` — no architectural change; note above
- `Third Arm Assembly Print Pack v0.16.pdf` — no hardware change
- `Third Arm Procurement v0.16.xlsx` — no procurement change
