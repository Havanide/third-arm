"""
third_arm.cli.replay_session
─────────────────────────────────────────────────────────────────────────────
CLI tool: replay a session bundle and print events to stdout.

Usage::
    python -m third_arm.cli.replay_session sessions/session_xyz
    # or, if installed:
    third-arm-replay sessions/session_xyz

TODO: add --speed flag for time-scaled playback.
TODO: add --filter flag to select event types.
TODO: add Foxglove WebSocket bridge for MCAP replay (Stage 1.5+).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from third_arm.logging.replay_reader import ReplayReader


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: replay_session <bundle_dir>")
        sys.exit(1)

    bundle_dir = Path(sys.argv[1])
    if not bundle_dir.exists():
        print(f"Bundle directory not found: {bundle_dir}")
        sys.exit(1)

    reader = ReplayReader(bundle_dir).load()
    print(f"\n── Replaying: {reader.session_id} ──────────────────")
    summary = reader.summary()
    print(f"   Events : {summary['event_count']}")
    print(f"   Started: {summary['created_at']}")
    print(f"   Closed : {summary['closed_at']}")
    print()

    for event in reader.events():
        print(json.dumps(event, default=str))

    print(f"\n── Replay complete ({summary['event_count']} events) ──")


if __name__ == "__main__":
    main()
