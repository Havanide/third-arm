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
import os
from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


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

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlProfileSettingsSource(settings_cls),
            file_secret_settings,
        )


class YamlProfileSettingsSource:
    """Load bench/desktop YAML profiles as a low-priority settings source."""

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        self.settings_cls = settings_cls

    def __call__(self) -> dict:
        raw_path = os.getenv("THIRD_ARM_CONFIG")
        if raw_path:
            payload = load_yaml_file(Path(raw_path))
        else:
            profile_name = os.getenv("THIRD_ARM_CONFIG_PROFILE", "stage1_desktop")
            payload = load_yaml_profile(profile_name)
        return flatten_profile_payload(payload)


@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings singleton.

    Call ``get_settings.cache_clear()`` in tests to reset.
    """
    return Settings()


def flatten_profile_payload(payload: dict) -> dict:
    """Translate nested app-profile YAML into flat Settings field names."""
    server = payload.get("server") or {}
    hardware = payload.get("hardware") or {}
    camera = payload.get("camera") or {}
    intent = payload.get("intent") or {}
    logging_cfg = payload.get("logging") or {}

    flat: dict[str, object] = {}

    if "host" in server:
        flat["host"] = server["host"]
    if "port" in server:
        flat["port"] = server["port"]
    if "log_level" in server:
        flat["log_level"] = server["log_level"]
    if "reload" in server:
        flat["reload"] = server["reload"]

    if "sessions_dir" in logging_cfg:
        flat["sessions_dir"] = logging_cfg["sessions_dir"]

    if "mock" in hardware:
        flat["mock_hardware"] = hardware["mock"]

    if "enabled" in camera:
        flat["camera_enabled"] = camera["enabled"]

    if "imu_enabled" in intent:
        flat["imu_enabled"] = intent["imu_enabled"]
    if "semg_enabled" in intent:
        flat["semg_enabled"] = intent["semg_enabled"]

    return flat


def load_yaml_file(path: Path) -> dict:
    """Load a YAML config file and return an empty dict if missing."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_yaml_profile(profile_name: str) -> dict:
    """Load a YAML config profile by name.

    Looks for ``configs/app/<profile_name>.yaml`` relative to the project root.
    Returns an empty dict if not found (graceful degradation).

    TODO: merge YAML values into Settings before env-var override layer.
    """
    path = Path("configs") / "app" / f"{profile_name}.yaml"
    return load_yaml_file(path)
