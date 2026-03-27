"""
third_arm.domain.handover_service
─────────────────────────────────────────────────────────────────────────────
Orchestrates a single handover sequence by coordinating the state machine,
arm driver, and bundle writer.

Stage 1: no-op / mock sequence. The real sequence will block while the arm
moves; this stub returns immediately.

TODO: implement actual async handover coroutine using driver callbacks.
TODO (Stage 1.5): add vision-gated grasp confirmation.
TODO (Stage 2+): intent-triggered release.
"""

from __future__ import annotations

import asyncio
import logging

from third_arm.core.clock import now_iso
from third_arm.core.errors import ArmNotReadyError, NoActiveSessionError
from third_arm.core.ids import new_handover_id
from third_arm.domain.contracts import ArmDriverABC, BundleWriterABC
from third_arm.domain.session_service import SessionService
from third_arm.domain.state_machine import ArmState, StateMachine

logger = logging.getLogger(__name__)


class HandoverService:
    """Executes and monitors a handover sequence.

    Args:
        state_machine:   Shared arm state machine instance.
        driver:          Concrete arm driver (mock or real).
        session_service: Active session registry; handover requires a live session.
        bundle_writer:   Port for trace event logging.
    """

    def __init__(
        self,
        state_machine: StateMachine,
        driver: ArmDriverABC,
        session_service: SessionService,
        bundle_writer: BundleWriterABC,
    ) -> None:
        self._sm = state_machine
        self._driver = driver
        self._session_service = session_service
        self._bundle_writer = bundle_writer

    async def request(self, object_id: str, slot_id: str) -> dict:
        """Initiate a handover for *object_id* from *slot_id*.

        Returns a summary dict with handover_id, session_id, and status.

        Raises:
            NoActiveSessionError: if no session is currently active.
            ArmNotReadyError: if the arm is not in READY state.
        """
        session = self._session_service.require_active()

        if self._sm.state != ArmState.READY:
            raise ArmNotReadyError(self._sm.state.value)

        handover_id = new_handover_id()
        logger.info("Handover requested: %s (slot=%s, object=%s)", handover_id, slot_id, object_id)

        self._bundle_writer.write_trace_event({
            "event": "handover_requested",
            "handover_id": handover_id,
            "session_id": session.session_id,
            "object_id": object_id,
            "slot_id": slot_id,
        })

        # ── Stage 1: skeleton sequence (mock, no real blocking) ───────────────
        # TODO: replace each step with real async driver calls + state guards

        self._sm.trigger("session_start")   # READY → TASK_ARMING
        await asyncio.sleep(0)              # yield to event loop

        self._sm.trigger("task_arm")        # TASK_ARMING → ACQUIRE
        await self._driver.start_handover(slot_id=slot_id, object_id=object_id)

        self._bundle_writer.write_trace_event({
            "event": "handover_driver_started",
            "handover_id": handover_id,
        })

        self._sm.trigger("lift_cmd")        # ACQUIRE → LIFT
        await asyncio.sleep(0)

        self._sm.trigger("present_cmd")     # LIFT → PRESENT
        await asyncio.sleep(0)

        self._sm.trigger("transfer_complete")  # PRESENT → TRANSFER_WAIT
        await asyncio.sleep(0)

        self._sm.trigger("release_cmd")     # TRANSFER_WAIT → RELEASE
        await asyncio.sleep(0)

        self._sm.trigger("retract_cmd")     # RELEASE → RETRACT
        await asyncio.sleep(0)

        self._sm.trigger("task_done")       # RETRACT → TASK_COMPLETE
        logger.info("Handover complete: %s", handover_id)

        self._bundle_writer.write_trace_event({
            "event": "handover_completed",
            "handover_id": handover_id,
            "session_id": session.session_id,
        })

        session.handover_ids.append(handover_id)

        return {
            "handover_id": handover_id,
            "session_id": session.session_id,
            "object_id": object_id,
            "slot_id": slot_id,
            "completed_at": now_iso(),
            "status": "complete",
        }
