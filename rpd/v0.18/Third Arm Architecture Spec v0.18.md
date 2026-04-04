# Third Arm Architecture Spec v0.18

**Stage:** 1
**Based on:** v0.17 Architecture Spec
**Date:** 2026-04-04

---

## Architecture is unchanged from v0.17

The addition of `GET /artifacts/{session_id}` is a read-only extension to the existing artifact router.
No new services, no new adapters, no state machine changes, no new bundle writes.

---

## GET /artifacts/{session_id} — endpoint design

### Location
`src/third_arm/api/routers/artifacts.py` — added to existing `APIRouter(prefix="/artifacts")`

### Reused utilities

| Utility | File | Purpose |
|---------|------|---------|
| `bundle_path(sessions_dir, session_id)` | `storage/paths.py` | Resolve bundle dir path |
| `read_json(path)` | `storage/files.py` | Parse manifest.json |
| `ReplayReader(bdir).load()` | `logging/replay_reader.py` | Count trace events |
| `get_settings()` | `core/settings.py` | Resolve `sessions_dir` |

### Response contract

```
GET /artifacts/{session_id}
→ 200 OK
{
  "session_id":      string,
  "schema_version":  string | null,
  "created_at":      ISO8601 string | null,
  "closed_at":       ISO8601 string | null,
  "is_closed":       bool,
  "files": [
    {
      "name":       string,      // filename
      "category":   string,      // "manifest" | "trace" | "telemetry"
      "exists":     bool,
      "size_bytes": int          // only present when exists=true
    }
  ],
  "trace_summary": {
    "event_count": int
  }
}

→ 404 Not Found
{ "detail": "Session bundle not found: <session_id>" }
```

### Degraded response (partial bundle)

If a bundle directory has `manifest.json` but is missing other files, the endpoint returns 200
with `exists: false` for missing files and `event_count: 0`. This makes incomplete bundles
visible for debugging without crashing the API.

### Role in Stage 1 observability

`GET /artifacts` — discovery: what sessions exist
`GET /artifacts/{session_id}` — inspection: is this bundle complete, what events were recorded

Together they form the read side of the Stage 1 replay/audit layer.
Stage 1.5 will add MCAP decoding and richer trace summaries.

---

## Frozen constraints (unchanged)

- API response shapes for session/handover endpoints: frozen
- Slot model: frozen
- State machine transitions: frozen
- Bundle layout (manifest.json + session_trace.ndjson + telemetry.mcap): frozen
- `pytest -m smoke` as merge gate: enforced via CI
