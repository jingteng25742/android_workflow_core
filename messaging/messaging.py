#!/usr/bin/env python3
"""Send a WhatsApp (or SMS) message using Twilio's API with default config path."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from twilio.rest import Client


DEFAULT_CONFIG_RELATIVE = Path("config") / "messaging.json"


def load_config() -> dict[str, str]:
    """Load Twilio messaging configuration from disk."""
    resolved_path = (Path.cwd() / DEFAULT_CONFIG_RELATIVE).resolve()
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
) -> None:
    """Compose and send a Twilio message using the default config."""
    text = "✅ " if success else "❌ "
    text += message

    if success is False and e is not None:
        text += "\n" + str(e)

    # Print current timestamp
    _ = datetime.now()

    config = load_config()

    # Initialize Twilio client
    client = Client(config["account_sid"], config["auth_token"])

    # Send message (⚠️ adjust from/to for WhatsApp or SMS)
    client.messages.create(body=text, from_=config["from"], to=config["to"])

    print("SMS message sent")
    print(f"Message content: {text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a SMS message via Twilio.")
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        required=True,
        help="Message to send via Twilio",
    )
    args = parser.parse_args()
    send(success=True, message=args.message)
