"""GET /artifacts — list and inspect session bundles."""

from __future__ import annotations

import re
from pathlib import Path

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
_SESSION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _resolve_bundle_dir(sessions_dir: Path, session_id: str) -> Path:
    """Resolve a bundle path only if the session id is a safe local directory name."""
    if not _SESSION_ID_RE.fullmatch(session_id):
        raise HTTPException(
            status_code=404,
            detail=f"Session bundle not found: {session_id}",
        )

    root = sessions_dir.resolve()
    bundle_dir = bundle_path(root, session_id).resolve()
    try:
        bundle_dir.relative_to(root)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Session bundle not found: {session_id}",
        ) from exc
    return bundle_dir


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

    Returns manifest summary, presence flags, file inventory with existence
    and size, trace event count, and inspection errors. Does not serve file
    contents.

    Raises 404 only if the bundle directory is unknown or the session id is
    unsafe. Existing but incomplete bundles return a degraded response.
    """
    cfg = get_settings()
    bdir = _resolve_bundle_dir(cfg.sessions_dir, session_id)
    manifest_path = bdir / "manifest.json"
    trace_path = bdir / "session_trace.ndjson"
    telemetry_path = bdir / "telemetry.mcap"

    if not bdir.exists() or not bdir.is_dir():
        raise HTTPException(
            status_code=404,
            detail=f"Session bundle not found: {session_id}",
        )

    errors: list[str] = []
    manifest: dict = {}
    try:
        if manifest_path.exists():
            manifest = read_json(manifest_path)
        else:
            errors.append("manifest_missing")
    except Exception:
        errors.append("manifest_unreadable")

    files = []
    for name, category in _BUNDLE_FILES:
        fp = bdir / name
        entry: dict = {"name": name, "category": category, "exists": fp.exists()}
        if fp.exists():
            entry["size_bytes"] = fp.stat().st_size
        files.append(entry)

    trace_summary: dict = {"event_count": 0}
    if trace_path.exists():
        try:
            reader = ReplayReader(bdir).load()
            trace_summary["event_count"] = len(list(reader.events()))
        except Exception:
            errors.append("trace_unreadable")

    resolved_session_id = manifest.get("session_id") or session_id
    is_closed = manifest.get("closed_at") is not None if manifest else False

    return {
        "session_id": resolved_session_id,
        "schema_version": manifest.get("schema_version"),
        "created_at": manifest.get("created_at"),
        "closed_at": manifest.get("closed_at"),
        "is_closed": is_closed,
        "presence": {
            "manifest": manifest_path.exists(),
            "trace": trace_path.exists(),
            "telemetry": telemetry_path.exists(),
        },
        "files": files,
        "trace_summary": trace_summary,
        "errors": errors,
    }
