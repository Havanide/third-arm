"""GET /artifacts — list session bundles."""

from __future__ import annotations

from fastapi import APIRouter

from third_arm.core.settings import get_settings
from third_arm.storage.paths import list_session_bundles

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get("")
async def list_artifacts() -> dict:
    """List session bundle directories available for replay/export.

    TODO: add pagination and filtering (date range, operator).
    TODO: add GET /artifacts/{session_id} to inspect a specific bundle.
    TODO: add GET /artifacts/{session_id}/download for zip export.
    """
    cfg = get_settings()
    bundles = list_session_bundles(cfg.sessions_dir)
    return {"bundles": bundles, "count": len(bundles)}
