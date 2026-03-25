"""
third_arm.main
─────────────────────────────────────────────────────────────────────────────
FastAPI application factory and lifespan manager.

Startup sequence
────────────────
1. Load settings
2. Initialise state machine (BOOT → IDLE via self_check)
3. Instantiate mock or real arm driver
4. Wire session + handover services
5. Mount routers and WebSocket endpoint

TODO: add structured logging setup (structlog).
TODO: add CORS middleware for desktop UI (Stage 1.5+).
TODO: add auth middleware (Stage 2+).
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from third_arm.api.routers import arm, artifacts, handover, health, session, status
from third_arm.api.ws import stream
from third_arm.core.settings import get_settings
from third_arm.domain.handover_service import HandoverService
from third_arm.domain.session_service import SessionService
from third_arm.domain.state_machine import StateMachine

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup → yield → shutdown."""
    cfg = get_settings()
    logger.info("Starting Third Arm service (env=%s, mock=%s)", cfg.env, cfg.mock_hardware)

    # ── State machine ────────────────────────────────────────────────────────
    sm = StateMachine()
    sm.trigger("boot_complete")     # BOOT → SELF_CHECK
    sm.trigger("self_check_ok")     # SELF_CHECK → IDLE
    app.state.state_machine = sm

    # ── Arm driver ───────────────────────────────────────────────────────────
    if cfg.mock_hardware:
        from third_arm.adapters.mock_arm.driver import MockArmDriver
        driver = MockArmDriver()
    else:
        # TODO: import and initialise real hardware driver (Stage 1.5+)
        raise NotImplementedError("Real hardware driver not implemented yet")

    app.state.arm_driver = driver

    # ── Services ─────────────────────────────────────────────────────────────
    session_service = SessionService()
    handover_service = HandoverService(state_machine=sm, driver=driver)
    app.state.session_service = session_service
    app.state.handover_service = handover_service

    logger.info("Third Arm service ready on %s:%s", cfg.host, cfg.port)
    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    logger.info("Shutting down Third Arm service")
    if sm.can_trigger("shutdown_cmd"):
        sm.trigger("shutdown_cmd")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    cfg = get_settings()

    app = FastAPI(
        title="Third Arm API",
        version="0.1.0",
        description="Intent-driven handover service — Stage 1 desktop skeleton",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS — allow all origins in dev; tighten for staging/prod ────────────
    if cfg.env == "dev":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # ── REST routers ─────────────────────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(status.router)
    app.include_router(session.router)
    app.include_router(arm.router)
    app.include_router(handover.router)
    app.include_router(artifacts.router)

    # ── WebSocket ────────────────────────────────────────────────────────────
    app.include_router(stream.router)

    return app


# Exported app instance — used by uvicorn and tests
app = create_app()
