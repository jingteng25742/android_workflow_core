"""Command line entry point for Android workflow automation (core-neutral)."""

from __future__ import annotations

import argparse
import importlib
import inspect
import os
import pkgutil
import sys
from types import ModuleType
from typing import Type

from . import __path__ as package_path
from .core.workflow import Workflow
from .core.workflow_config import WorkflowConfig
from .core.workflow_interface import WorkflowInterface


def _discover_workflow_classes() -> set[Type[WorkflowInterface]]:
    """Find concrete workflow classes that implement register_cli_arguments."""
    classes: set[Type[WorkflowInterface]] = set()
    package_prefix = f"{__package__}."
    for _, module_name, is_pkg in pkgutil.walk_packages(package_path, package_prefix):
        if not is_pkg:
            module = importlib.import_module(module_name)
            classes.update(_collect_workflow_classes(module))
    return classes


def _collect_workflow_classes(module: ModuleType) -> set[Type[WorkflowInterface]]:
    found: set[Type[WorkflowInterface]] = set()
    for value in vars(module).values():
        if not inspect.isclass(value):
            continue
        if value is WorkflowInterface:
            continue
        if issubclass(value, WorkflowInterface):
            register = getattr(value, "register_cli_arguments", None)
            if callable(register):
                found.add(value)
    return found


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an Android UI automation workflow (core-neutral).",
    )
    parser.add_argument(
        "--workflow",
        "--wf",
        required=True,
        help="Workflow to launch (no default to encourage explicit selection).",
    )
    parser.add_argument(
        "--device-id",
        default=os.getenv("ANDROID_DEVICE_ID"),
        help="Optional adb device serial; defaults to ANDROID_DEVICE_ID env var.",
    )
    parser.add_argument(
        "--no-delay",
        "--nd",
        action="store_true",
        help="Disable any configured workflow delays.",
    )
    for workflow_cls in sorted(_discover_workflow_classes(), key=lambda cls: cls.__name__):
        workflow_cls.register_cli_arguments(parser)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    config = WorkflowConfig(
        workflow=args.workflow,
        action=args.action,
        device_id=args.device_id,
        no_delay=args.no_delay,
    )
    workflow = Workflow(config)
    result = workflow.run()
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
