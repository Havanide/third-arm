"""POST /session/start  |  POST /session/stop"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from third_arm.api.deps import get_session_service, get_state_machine
from third_arm.api.schemas.commands import (
    SessionStartConflictResponse,
    SessionStartRequest,
    SessionResponse,
    SessionStopResponse,
)
from third_arm.core.errors import NoActiveSessionError, SessionAlreadyActiveError
from third_arm.domain.object_model import get_object
from third_arm.domain.session_service import SessionService
from third_arm.domain.slot_model import get_slot
from third_arm.domain.state_machine import ArmState, StateMachine

router = APIRouter(prefix="/session", tags=["session"])


@router.post(
    "/start",
    status_code=status.HTTP_200_OK,
    response_model=SessionResponse,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": SessionStartConflictResponse,
            "description": "Arm is not in READY state or a session is already active",
        },
    },
)
async def start_session(
    body: SessionStartRequest,
    sm: StateMachine = Depends(get_state_machine),
    sessions: SessionService = Depends(get_session_service),
) -> SessionResponse:
    """Begin a new handover session.

    The arm must already be in READY state to start a session.
    Opens a session bundle on disk for later discovery via ``GET /artifacts``.

    No implicit homing or auto-transition occurs here.
    """
    if sm.state is not ArmState.READY:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Session start requires arm state 'ready'; call POST /arm/home first",
                "current_state": sm.state.value,
            },
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": str(exc),
                "current_state": sm.state.value,
            },
        ) from exc

    return {
        "session_id": session.session_id,
        "started_at": session.started_at,
        "operator_id": session.operator_id,
    }


@router.post(
    "/stop",
    status_code=status.HTTP_200_OK,
    response_model=SessionStopResponse,
)
async def stop_session(
    sessions: SessionService = Depends(get_session_service),
) -> SessionStopResponse:
    """End or abort the current session.

    Writes a session_stopped trace event and closes the bundle.

    TODO: trigger state machine ``abort`` if mid-task.
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
