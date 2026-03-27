# Bundle Writer — Implementation Note

## What was done

`BundleWriter` is now wired into the Stage 1 runtime path.
Previously all infrastructure existed but was unused (TODO comments in `SessionService`, `HandoverService`, `main.py`).

## Wiring points

| Location | Change |
|----------|--------|
| `main.py` lifespan | `BundleWriter(sessions_dir)` initialised and stored in `app.state.bundle_writer` |
| `SessionService.__init__` | Accepts `bundle_writer: BundleWriterABC` |
| `SessionService.start()` | Opens bundle **before** creating the Session; aborts if open fails |
| `SessionService.stop()` | Writes `session_stopped` event, then closes bundle |
| `HandoverService.__init__` | Accepts `session_service` and `bundle_writer` |
| `HandoverService.request()` | Requires active session; writes three trace events |
| `POST /session/start` response | Now includes `artifact_path` |
| `POST /handover/request` response | Now includes `session_id` |

## Trace events emitted per operator flow

```
session_started          ← on POST /session/start
handover_requested       ← on POST /handover/request (before arm moves)
handover_driver_started  ← after driver.start_handover() call
handover_completed       ← after state machine reaches TASK_COMPLETE
session_stopped          ← on POST /session/stop
```

## Bundle layout

```
sessions/<session_id>/
    manifest.json          ← metadata + file index; closed_at set on stop
    session_trace.ndjson   ← one JSON line per event, with ts timestamp
    telemetry.mcap         ← placeholder (empty); binary content in Stage 1.5+
```

## Validation

```bash
python scripts/validate_bundle.py sessions/<session_id>
```

## What is still a stub

`telemetry.mcap` is created as an empty file. Real MCAP binary content (joint angles, gripper state) is deferred to Stage 1.5 when the hardware driver is active.
