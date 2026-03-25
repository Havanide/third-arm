"""
scripts/seed_stage1_configs.py
─────────────────────────────────────────────────────────────────────────────
Validate that Stage 1 YAML config files exist and are parseable.

Usage::
    python scripts/seed_stage1_configs.py

TODO: extend to generate missing config files from templates.
TODO: add JSON Schema validation against config schemas.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REQUIRED_FILES = [
    "configs/app/default.yaml",
    "configs/app/dev.yaml",
    "configs/app/stage1_desktop.yaml",
    "configs/slots/stage1_slots.yaml",
    "configs/slots/stage1_objects.yaml",
    "configs/calibration/placeholder.yaml",
]

ROOT = Path(__file__).parent.parent


def main() -> None:
    print("Checking Stage 1 config files...\n")
    all_ok = True

    for rel_path in REQUIRED_FILES:
        path = ROOT / rel_path
        if not path.exists():
            print(f"  ❌ MISSING: {rel_path}")
            all_ok = False
            continue

        try:
            data = yaml.safe_load(path.read_text())
            if data is None:
                print(f"  ⚠  EMPTY:   {rel_path}")
            else:
                print(f"  ✅ OK:      {rel_path}  ({len(data)} top-level keys)")
        except yaml.YAMLError as exc:
            print(f"  ❌ PARSE ERROR: {rel_path} — {exc}")
            all_ok = False

    print()
    if all_ok:
        print("All Stage 1 config files are present and valid.")
    else:
        print("Some config files are missing or invalid.")
        sys.exit(1)


if __name__ == "__main__":
    main()
