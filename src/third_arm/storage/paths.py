"""
third_arm.storage.paths
─────────────────────────────────────────────────────────────────────────────
File system path helpers and bundle directory enumeration.
"""

from __future__ import annotations

from pathlib import Path


def ensure_sessions_dir(sessions_dir: Path) -> Path:
    """Create sessions directory if it does not exist."""
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir


def bundle_path(sessions_dir: Path, session_id: str) -> Path:
    """Return the path for a specific session bundle directory."""
    return sessions_dir / session_id


def list_session_bundles(sessions_dir: Path) -> list[dict]:
    """Return a list of session bundle metadata dicts.

    Each entry contains: session_id, path (str), size_bytes (total dir size).
    Only directories with a manifest.json are included.
    """
    sessions_dir = Path(sessions_dir)
    if not sessions_dir.exists():
        return []

    bundles = []
    for entry in sorted(sessions_dir.iterdir()):
        if not entry.is_dir():
            continue
        if not (entry / "manifest.json").exists():
            continue
        size = sum(f.stat().st_size for f in entry.rglob("*") if f.is_file())
        bundles.append({"session_id": entry.name, "path": str(entry), "size_bytes": size})

    return bundles
