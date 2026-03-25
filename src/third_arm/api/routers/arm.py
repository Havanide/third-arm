"""POST /arm/home — command arm to home position."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from third_arm.api.deps import get_state_machine
from third_arm.core.errors import InvalidTransitionError
from third_arm.domain.state_machine import StateMachine

router = APIRouter(prefix="/arm", tags=["arm"])


@router.post("/home", status_code=status.HTTP_202_ACCEPTED)
async def arm_home(sm: StateMachine = Depends(get_state_machine)) -> dict:
    """Command the arm to move to its home position.

    Accepted from: IDLE, READY, TASK_COMPLETE, TASK_ABORTED, SAFE_STOP.

    TODO: await actual driver home() call here.
    TODO: fire state machine ``home_complete`` / ``home_fail`` callbacks.
    """
    if not sm.can_trigger("home_cmd"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"home_cmd not valid in state '{sm.state.value}'",
        )

    try:
        new_state = sm.trigger("home_cmd")
    except InvalidTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    # TODO: in Stage 1.5 replace with: await driver.home(); sm.trigger("home_complete")
    # For now, fast-forward to READY
    if sm.can_trigger("home_complete"):
        sm.trigger("home_complete")

    return {"accepted": True, "new_state": sm.state.value}
