"""POST /session/start  |  POST /session/stop"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from third_arm.api.deps import get_session_service, get_state_machine
from third_arm.api.schemas.commands import SessionStartRequest
from third_arm.core.errors import NoActiveSessionError, SessionAlreadyActiveError
from third_arm.domain.object_model import get_object
from third_arm.domain.session_service import SessionService
from third_arm.domain.slot_model import get_slot
from third_arm.domain.state_machine import ArmState, StateMachine

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/start", status_code=status.HTTP_200_OK)
async def start_session(
    body: SessionStartRequest,
    sm: StateMachine = Depends(get_state_machine),
    sessions: SessionService = Depends(get_session_service),
) -> dict:
    """Begin a new handover session.

    The arm must be in READY or IDLE state to start a session.

    TODO: trigger state machine ``home_cmd`` if arm is IDLE.
    TODO: open bundle writer session.
    """
    if sm.state not in (ArmState.READY, ArmState.IDLE):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot start session in state '{sm.state.value}'",
        )

    if body.object_id and not get_object(body.object_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown object_id: {body.object_id}")
    if body.slot_id and not get_slot(body.slot_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown slot_id: {body.slot_id}")

    try:
        session = sessions.start(
            operator_id=body.operator_id,
            object_id=body.object_id,
            slot_id=body.slot_id,
            notes=body.notes,
        )
    except SessionAlreadyActiveError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return {
        "session_id": session.session_id,
        "started_at": session.started_at,
        "operator_id": session.operator_id,
    }


@router.post("/stop", status_code=status.HTTP_200_OK)
async def stop_session(
    sessions: SessionService = Depends(get_session_service),
) -> dict:
    """End or abort the current session.

    TODO: trigger state machine ``abort`` if mid-task.
    TODO: close bundle writer session.
    """
    try:
        session = sessions.stop()
    except NoActiveSessionError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return {
        "session_id": session.session_id,
        "stopped_at": session.stopped_at,
        "status": "stopped",
    }
