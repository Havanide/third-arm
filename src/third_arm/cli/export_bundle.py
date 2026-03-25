"""
third_arm.cli.export_bundle
─────────────────────────────────────────────────────────────────────────────
CLI tool: export a session bundle as a zip archive.

Usage::
    python -m third_arm.cli.export_bundle sessions/session_xyz
    # or, if installed:
    third-arm-export sessions/session_xyz

TODO: add --output / --dest flag.
TODO: add --format flag (zip | tar.gz).
"""

from __future__ import annotations

import sys
from pathlib import Path

from third_arm.storage.files import zip_bundle


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: export_bundle <bundle_dir>")
        sys.exit(1)

    bundle_dir = Path(sys.argv[1])
    if not bundle_dir.exists():
        print(f"Bundle directory not found: {bundle_dir}")
        sys.exit(1)

    dest = zip_bundle(bundle_dir)
    print(f"Exported: {dest}")


if __name__ == "__main__":
    main()
