"""
third_arm.storage.files
─────────────────────────────────────────────────────────────────────────────
Generic file I/O helpers.

TODO: add async file helpers (aiofiles) for non-blocking log writes.
TODO: add zip export for bundle download (Stage 1.5+).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path


def read_json(path: Path) -> dict:
    """Read and parse a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict, indent: int = 2) -> None:
    """Write a dict as a JSON file (creates parent dirs if needed)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=indent, default=str), encoding="utf-8")


def zip_bundle(bundle_dir: Path, dest: Path | None = None) -> Path:
    """Create a zip archive of a session bundle.

    Args:
        bundle_dir: Source session bundle directory.
        dest:       Destination path (default: <bundle_dir>.zip).

    Returns:
        Path to the created zip file.

    TODO: call this from cli/export_bundle.py.
    """
    dest = dest or bundle_dir.with_suffix(".zip")
    shutil.make_archive(str(dest.with_suffix("")), "zip", bundle_dir.parent, bundle_dir.name)
    return dest
