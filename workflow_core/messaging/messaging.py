#!/usr/bin/env python3
"""Send a WhatsApp (or SMS) message using Twilio's API with configurable config path."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from twilio.rest import Client


CONFIG_ENV_VAR = "MESSAGING_CONFIG_PATH"
DEFAULT_CONFIG_PATH = Path("config") / "messaging.json"


def resolve_config_path(config_path: Path | str | None = None) -> Path:
    """Resolve the messaging config path from argument, env var, or default."""
    if config_path:
        return Path(config_path)

    env_value = os.getenv(CONFIG_ENV_VAR)
    if env_value:
        return Path(env_value)

    return (Path.cwd() / DEFAULT_CONFIG_PATH).resolve()


def load_config(config_path: Path | str | None = None) -> dict[str, str]:
    """Load Twilio messaging configuration from disk."""
    resolved_path = resolve_config_path(config_path)
    try:
        config = json.loads(resolved_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Failed to load messaging config from {resolved_path}") from exc

    required = ("account_sid", "auth_token", "from", "to")
    missing = [field for field in required if not config.get(field)]
    if missing:
        raise RuntimeError(
            "Messaging config missing required field(s): " + ", ".join(missing)
        )

    return config


def send(
    success: bool,
    message: str,
    e: Optional[Exception] = None,
    config_path: Path | str | None = None,
) -> None:
    text = "✅ " if success else "❌ "
    text += message

    if success is False and e is not None:
        text += "\n" + str(e)

    _send(text, config_path=config_path)


def _send(message: str, config_path: Path | str | None = None) -> None:
    # Print current timestamp
    _ = datetime.now()

    config = load_config(config_path)

    # Initialize Twilio client
    client = Client(config["account_sid"], config["auth_token"])

    # Send message (⚠️ adjust from/to for WhatsApp or SMS)
    client.messages.create(body=message, from_=config["from"], to=config["to"])

    print("SMS message sent")
    print(f"Message content: {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a SMS message via Twilio.")
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        required=True,
        help="Message to send via Twilio",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Optional path to messaging config JSON; defaults to env or config/messaging.json.",
    )
    args = parser.parse_args()
    _send(args.message, config_path=args.config)
