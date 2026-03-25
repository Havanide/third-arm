"""
third_arm.cli.run_dev
─────────────────────────────────────────────────────────────────────────────
CLI entry point: start the dev server.

Equivalent to:
    uvicorn third_arm.main:app --reload --host 0.0.0.0 --port 8080

Usage::
    python -m third_arm.cli.run_dev
    # or, if installed:
    third-arm-dev
"""

from __future__ import annotations

import uvicorn

from third_arm.core.settings import get_settings


def main() -> None:
    cfg = get_settings()
    uvicorn.run(
        "third_arm.main:app",
        host=cfg.host,
        port=cfg.port,
        reload=cfg.reload,
        log_level=cfg.log_level.lower(),
    )


if __name__ == "__main__":
    main()
