"""
third_arm.api.ws.stream
─────────────────────────────────────────────────────────────────────────────
WebSocket endpoint  ``/ws/stream``

Server pushes TelemetryFrame JSON at a fixed interval and state/session
events on demand.  Client can send ping frames; server echoes pong.

Stage 1: mock telemetry only.  State events are not yet wired to the
         real state machine — that requires an event bus (Stage 1.5+).

TODO: replace polling loop with a proper async pub/sub event bus.
TODO: add connection registry so state machine callbacks can broadcast.
TODO: add auth token check on handshake (Stage 2+).
"""

from __future__ import annotations

import asyncio
import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from third_arm.api.schemas.telemetry import TelemetryFrame
from third_arm.core.clock import now_iso
from third_arm.core.settings import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["websocket"])

TELEMETRY_INTERVAL_S = 0.5  # push rate (seconds)


@router.websocket("/ws/stream")
async def websocket_stream(ws: WebSocket) -> None:
    """Real-time telemetry and event stream.

    Clients receive JSON-encoded TelemetryFrame messages at
    ~{TELEMETRY_INTERVAL_S}s intervals until disconnected.
    """
    await ws.accept()
    cfg = get_settings()
    logger.info("WebSocket client connected: %s", ws.client)

    # Grab singletons from app state
    sm = ws.app.state.state_machine
    sessions = ws.app.state.session_service

    try:
        while True:
            active = sessions.active
            frame = TelemetryFrame(
                ts=now_iso(),
                session_id=active.session_id if active else None,
                arm_state=sm.state.value,
                # TODO: replace stubs below with real driver telemetry
                joint_angles_deg=[0.0, -30.0, 90.0, 0.0, 0.0, 0.0],
                gripper_pct=0.0,
                mock=cfg.mock_hardware,
            )
            await ws.send_text(frame.model_dump_json())
            await asyncio.sleep(TELEMETRY_INTERVAL_S)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected: %s", ws.client)
    except Exception as exc:  # noqa: BLE001
        logger.error("WebSocket error: %s", exc)
        await ws.close(code=1011)
