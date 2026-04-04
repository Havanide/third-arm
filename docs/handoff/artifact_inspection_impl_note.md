# Artifact Inspection Endpoint — Implementation Note

**Date:** 2026-04-04
**Relates to:** `src/third_arm/api/routers/artifacts.py`

---

## What the endpoint does

`GET /artifacts/{session_id}` returns bundle-level metadata for one session:

- **Manifest metadata:** `session_id`, `schema_version`, `created_at`, `closed_at`, `is_closed`
- **Presence flags:** whether manifest / trace / telemetry files are present
- **File inventory:** for each expected file (`manifest.json`, `session_trace.ndjson`, `telemetry.mcap`):
  `exists` (bool) + `size_bytes` (int, only when exists=true)
- **Trace summary:** `event_count` — total events in `session_trace.ndjson`
- **Errors:** a short list such as `manifest_missing`, `manifest_unreadable`, `trace_unreadable`

Does not serve file contents. Does not decode MCAP. Does not download or export.

---

## Reused utilities

All logic uses existing utilities — no new modules:

| Utility | Purpose |
|---------|---------|
| `bundle_path(sessions_dir, session_id)` | Resolve bundle dir without fs calls |
| `read_json(manifest_path)` | Parse manifest.json |
| `ReplayReader(bdir).load()` | Read trace events to count them |
| `get_settings()` | Resolve sessions_dir from env/config |

---

## Error handling

| Case | Response |
|------|----------|
| bundle dir does not exist | 404 |
| unsafe path-like session_id (`..`, slash, etc.) | 404 |
| bundle dir exists but no manifest.json | 200, degraded response + `errors=["manifest_missing"]` |
| manifest.json present but malformed JSON | 200, degraded response + `errors=["manifest_unreadable"]` |
| expected files missing (partial bundle) | 200, files with `exists: false` |
| trace file missing | 200, `event_count: 0`, no trace error |
| trace file present but unreadable | 200, `event_count: 0`, `errors=["trace_unreadable"]` |

The degraded-response design makes incomplete bundles inspectable without crashing the API —
useful for diagnosing aborted sessions.

---

## What this does NOT cover

- Raw file download / zip export (future: `GET /artifacts/{session_id}/download`)
- MCAP binary decoding (Stage 1.5+)
- Trace content — only count, not event list
- Pagination / filtering (future enhancement to `GET /artifacts`)
- Auth / operator identity (not in Stage 1 scope)

---

## Tests

`tests/integration/test_artifact_inspection.py`:
- `test_artifact_inspection_happy_path` — full flow → 200, all files present, event_count ≥ 5
- `test_artifact_inspection_not_found` — unknown session_id → 404
- `test_artifact_inspection_partial_bundle` — bundle with manifest only → 200, degraded
- `test_artifact_inspection_missing_manifest_returns_degraded_response` — missing manifest → 200, degraded
- `test_artifact_inspection_malformed_manifest_returns_degraded_response` — bad manifest JSON → 200, degraded
- `test_artifact_inspection_rejects_unsafe_session_id` — path traversal style id → 404
