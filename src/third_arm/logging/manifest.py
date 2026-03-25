"""
third_arm.logging.manifest
─────────────────────────────────────────────────────────────────────────────
Session bundle manifest — written at session open, updated at close.

The manifest is the index file for each session bundle directory:
    sessions/<session_id>/manifest.json

It records metadata needed to replay or export the session.
"""

from __future__ import annotations

import json
from pathlib import Path

from third_arm.core.clock import now_iso


def write_manifest(bundle_dir: Path, session_id: str, metadata: dict) -> Path:
    """Write (or overwrite) the bundle manifest.json.

    Args:
        bundle_dir: Path to the session bundle directory.
        session_id: Session identifier.
        metadata:   Arbitrary extra metadata dict.

    Returns:
        Path to the written manifest file.
    """
    manifest = {
        "schema_version": "1.0",
        "session_id": session_id,
        "created_at": now_iso(),
        "closed_at": None,
        "files": {
            "trace": "session_trace.ndjson",
            "mcap":  "telemetry.mcap",
        },
        **metadata,
    }
    path = bundle_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, default=str))
    return path


def close_manifest(bundle_dir: Path) -> None:
    """Update the manifest with close timestamp and file sizes."""
    path = bundle_dir / "manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text())
    manifest["closed_at"] = now_iso()
    # Record actual file sizes
    for key, filename in manifest.get("files", {}).items():
        fp = bundle_dir / filename
        if fp.exists():
            manifest.setdefault("file_sizes", {})[filename] = fp.stat().st_size
    path.write_text(json.dumps(manifest, indent=2, default=str))
