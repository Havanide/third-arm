"""POST /handover/request — trigger a handover sequence."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from third_arm.api.deps import get_handover_service
from third_arm.api.schemas.commands import HandoverRequestBody
from third_arm.core.errors import ArmNotReadyError, NoActiveSessionError
from third_arm.domain.handover_service import HandoverService
from third_arm.domain.object_model import get_object
from third_arm.domain.slot_model import get_slot

router = APIRouter(prefix="/handover", tags=["handover"])


@router.post("/request", status_code=status.HTTP_202_ACCEPTED)
async def request_handover(
    body: HandoverRequestBody,
    svc: HandoverService = Depends(get_handover_service),
) -> dict:
    """Trigger an object handover sequence.

    The arm must be in READY state.

    TODO: validate object_id and slot_id against catalogues before dispatch.
    TODO: return a task_id the client can poll for completion.
    TODO: push state events via WebSocket during execution.
    """
    if not get_object(body.object_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown object_id: {body.object_id}")
    if not get_slot(body.slot_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown slot_id: {body.slot_id}")

    try:
        result = await svc.request(object_id=body.object_id, slot_id=body.slot_id)
    except NoActiveSessionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ArmNotReadyError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return result
