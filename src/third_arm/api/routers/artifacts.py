"""GET /artifacts — list and inspect session bundles."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from third_arm.core.settings import get_settings
from third_arm.logging.replay_reader import ReplayReader
from third_arm.storage.files import read_json
from third_arm.storage.paths import bundle_path, list_session_bundles

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

_BUNDLE_FILES = [
    ("manifest.json",        "manifest"),
    ("session_trace.ndjson", "trace"),
    ("telemetry.mcap",       "telemetry"),
]


@router.get("")
async def list_artifacts() -> dict:
    """List session bundle directories available for replay/export.

    TODO: add pagination and filtering (date range, operator).
    TODO: add GET /artifacts/{session_id}/download for zip export.
    """
    cfg = get_settings()
    bundles = list_session_bundles(cfg.sessions_dir)
    return {"bundles": bundles, "count": len(bundles)}


@router.get("/{session_id}")
async def get_artifact(session_id: str) -> dict:
    """Return bundle-level metadata and file inventory for one session.

    Returns manifest summary, file inventory with existence and size,
    and trace event count. Does not serve file contents.

    Raises 404 if the session bundle directory or its manifest is missing.
    Returns a degraded response (files with exists=False) if expected
    bundle files are absent.
    """
    cfg = get_settings()
    bdir = bundle_path(cfg.sessions_dir, session_id)
    manifest_path = bdir / "manifest.json"

    if not bdir.exists() or not manifest_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Session bundle not found: {session_id}",
        )

    try:
        manifest = read_json(manifest_path)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Session bundle not found: {session_id}",
        )

    files = []
    for name, category in _BUNDLE_FILES:
        fp = bdir / name
        entry: dict = {"name": name, "category": category, "exists": fp.exists()}
        if fp.exists():
            entry["size_bytes"] = fp.stat().st_size
        files.append(entry)

    trace_summary: dict = {"event_count": 0}
    try:
        reader = ReplayReader(bdir).load()
        trace_summary["event_count"] = len(list(reader.events()))
    except Exception:
        pass

    return {
        "session_id": session_id,
        "schema_version": manifest.get("schema_version"),
        "created_at": manifest.get("created_at"),
        "closed_at": manifest.get("closed_at"),
        "is_closed": manifest.get("closed_at") is not None,
        "files": files,
        "trace_summary": trace_summary,
    }
