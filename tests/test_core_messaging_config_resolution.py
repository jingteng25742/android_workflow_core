import os
from pathlib import Path

from android_workflow_core.messaging.messaging import CONFIG_ENV_VAR, resolve_config_path


def test_resolve_config_path_prefers_argument(tmp_path):
    explicit = tmp_path / "custom.json"
    resolved = resolve_config_path(explicit)
    assert resolved == explicit


def test_resolve_config_path_uses_env(monkeypatch, tmp_path):
    env_path = tmp_path / "env.json"
    monkeypatch.setenv(CONFIG_ENV_VAR, str(env_path))

    resolved = resolve_config_path()
    assert resolved == env_path


def test_resolve_config_path_defaults_to_config_dir(tmp_path, monkeypatch):
    # Simulate cwd by switching into a temp dir
    monkeypatch.chdir(tmp_path)
    expected = Path.cwd() / "config" / "messaging.json"
    resolved = resolve_config_path()
    assert resolved == expected
