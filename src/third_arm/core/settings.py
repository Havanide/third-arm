"""
third_arm.core.settings
─────────────────────────────────────────────────────────────────────────────
Application settings loaded from environment variables (with .env support)
and optionally merged with a YAML config profile.

Usage::

    from third_arm.core.settings import get_settings
    cfg = get_settings()
    print(cfg.port)
"""

from __future__ import annotations

import functools
from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Top-level application settings.

    All fields can be overridden via environment variables prefixed with
    ``THIRD_ARM_``.  E.g. ``THIRD_ARM_PORT=9090``.
    """

    model_config = SettingsConfigDict(
        env_prefix="THIRD_ARM_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Service identity ──────────────────────────────────────────────────────
    env: str = Field("dev", description="Runtime environment: dev | staging | production")
    config_profile: str = Field(
        "stage1_desktop",
        description="Config profile name (maps to configs/app/<profile>.yaml)",
    )

    # ── Server ────────────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "DEBUG"
    reload: bool = False

    # ── Storage ───────────────────────────────────────────────────────────────
    sessions_dir: Path = Path("./sessions")

    # ── Hardware ──────────────────────────────────────────────────────────────
    mock_hardware: bool = Field(True, description="Use mock arm driver (Stage 1)")
    # arm_serial_port: str = Field("", description="Stage 2+: real arm serial port")

    # ── Camera ────────────────────────────────────────────────────────────────
    camera_enabled: bool = False    # Stage 1.5+

    # ── Intent sensing ────────────────────────────────────────────────────────
    imu_enabled: bool = False       # Stage 2+
    semg_enabled: bool = False      # Stage 2+

    # ── TODO: add MQTT fields when transport is implemented ───────────────────


@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings singleton.

    Call ``get_settings.cache_clear()`` in tests to reset.
    """
    return Settings()


def load_yaml_profile(profile_name: str) -> dict:
    """Load a YAML config profile by name.

    Looks for ``configs/app/<profile_name>.yaml`` relative to the project root.
    Returns an empty dict if not found (graceful degradation).

    TODO: merge YAML values into Settings before env-var override layer.
    """
    path = Path("configs") / "app" / f"{profile_name}.yaml"
    if not path.exists():
        return {}
    with path.open() as fh:
        return yaml.safe_load(fh) or {}
