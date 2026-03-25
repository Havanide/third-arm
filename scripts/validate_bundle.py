"""
scripts/validate_bundle.py
─────────────────────────────────────────────────────────────────────────────
Smoke-validate a session bundle directory structure.

Usage::
    python scripts/validate_bundle.py sessions/<session_id>

Checks:
  - manifest.json exists and is valid JSON
  - session_trace.ndjson exists and every line is valid JSON
  - telemetry.mcap exists (content not validated in Stage 1)

Exit code 0 = valid, 1 = invalid.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def validate(bundle_dir: Path) -> list[str]:
    """Return a list of validation errors (empty = valid)."""
    errors = []

    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        errors.append("manifest.json is missing")
    else:
        try:
            manifest = json.loads(manifest_path.read_text())
            if "session_id" not in manifest:
                errors.append("manifest.json missing 'session_id'")
        except json.JSONDecodeError as exc:
            errors.append(f"manifest.json parse error: {exc}")

    trace_path = bundle_dir / "session_trace.ndjson"
    if not trace_path.exists():
        errors.append("session_trace.ndjson is missing")
    else:
        for i, line in enumerate(trace_path.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"session_trace.ndjson line {i}: parse error: {exc}")

    mcap_path = bundle_dir / "telemetry.mcap"
    if not mcap_path.exists():
        errors.append("telemetry.mcap is missing")

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_bundle.py <bundle_dir>")
        sys.exit(1)

    bundle_dir = Path(sys.argv[1])
    if not bundle_dir.exists():
        print(f"Bundle directory not found: {bundle_dir}")
        sys.exit(1)

    print(f"Validating bundle: {bundle_dir}\n")
    errors = validate(bundle_dir)

    if errors:
        print("❌ Validation FAILED:")
        for err in errors:
            print(f"   {err}")
        sys.exit(1)
    else:
        print("✅ Bundle is valid")


if __name__ == "__main__":
    main()
