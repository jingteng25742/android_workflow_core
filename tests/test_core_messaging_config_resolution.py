from pathlib import Path

from workflow_core.messaging.messaging import load_config


def test_load_config_uses_default_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "messaging.json"
    config_file.write_text(
        """{
            "account_sid": "sid",
            "auth_token": "token",
            "from": "+123",
            "to": "+456"
        }""",
        encoding="utf-8",
    )

    loaded = load_config()

    assert loaded["account_sid"] == "sid"
    assert loaded["auth_token"] == "token"
    assert loaded["from"] == "+123"
    assert loaded["to"] == "+456"
