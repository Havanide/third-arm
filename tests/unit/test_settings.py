from __future__ import annotations

from pathlib import Path

from third_arm.core.settings import get_settings


def test_explicit_yaml_config_path_is_loaded(monkeypatch):
    monkeypatch.setenv("THIRD_ARM_CONFIG", "configs/app/stage1_bench.yaml")
    get_settings.cache_clear()

    cfg = get_settings()

    assert cfg.host == "0.0.0.0"
    assert cfg.log_level == "INFO"
    assert cfg.reload is False
    assert cfg.sessions_dir == Path("/data/third-arm/sessions")
    assert cfg.mock_hardware is True

    get_settings.cache_clear()


def test_env_vars_override_yaml_profile(monkeypatch):
    monkeypatch.setenv("THIRD_ARM_CONFIG_PROFILE", "stage1_bench")
    monkeypatch.setenv("THIRD_ARM_HOST", "127.0.0.1")
    monkeypatch.setenv("THIRD_ARM_SESSIONS_DIR", "/tmp/third-arm-test-sessions")
    get_settings.cache_clear()

    cfg = get_settings()

    assert cfg.host == "127.0.0.1"
    assert cfg.sessions_dir == Path("/tmp/third-arm-test-sessions")
    assert cfg.reload is False
    assert cfg.mock_hardware is True

    get_settings.cache_clear()
