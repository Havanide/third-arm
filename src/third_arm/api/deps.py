"""
third_arm.api.deps
─────────────────────────────────────────────────────────────────────────────
FastAPI dependency injection providers.

Singletons are stored on ``app.state`` and injected via ``Depends()``.
This keeps routers decoupled from concrete implementations.

Usage in a router::

    from fastapi import Depends
    from third_arm.api.deps import get_session_service

    @router.post("/session/start")
    async def start(svc: SessionService = Depends(get_session_service)):
        ...
"""

from __future__ import annotations

from fastapi import Request

from third_arm.domain.handover_service import HandoverService
from third_arm.domain.session_service import SessionService
from third_arm.domain.state_machine import StateMachine
from third_arm.logging.bundle_writer import BundleWriter


def get_state_machine(request: Request) -> StateMachine:
    """Return the shared StateMachine from app state."""
    return request.app.state.state_machine


def get_session_service(request: Request) -> SessionService:
    """Return the shared SessionService from app state."""
    return request.app.state.session_service


def get_handover_service(request: Request) -> HandoverService:
    """Return the shared HandoverService from app state."""
    return request.app.state.handover_service


def get_bundle_writer(request: Request) -> BundleWriter:
    """Return the shared BundleWriter from app state."""
    return request.app.state.bundle_writer
