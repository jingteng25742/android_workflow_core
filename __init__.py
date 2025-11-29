"""workflow_core package shim that exposes modules under workflow_core/core."""

from __future__ import annotations

from pathlib import Path

# Allow imports like `workflow_core.workflows` to resolve to the implementation in core/.
_core_path = Path(__file__).with_name("core")
if str(_core_path) not in __path__:
    __path__.append(str(_core_path))

from .core import cli, messaging, workflows

__all__ = ["cli", "messaging", "workflows"]
