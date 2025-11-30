"""Command line entry point for Android workflow automation (core-neutral)."""

from __future__ import annotations

import argparse
import importlib
import inspect
import os
import pkgutil
from types import ModuleType
from typing import Sequence, Type

import workflow_core as core_pkg

from .workflow_interface import WorkflowInterface


class WorkflowCLIParser:
    """Argument parser helper for workflow CLI."""

    @classmethod
    def parse(
        cls,
        argv: list[str] | None = None,
        package_paths: list[tuple[Sequence[str], str]] | None = None,
    ) -> argparse.Namespace:
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
            "--delay",
            "-d",
            type=int,
            default=0,
            help="Override delay in minutes between workflow runs (0 to bypass delays).",
        )
        for workflow_cls in sorted(
            cls._discover_workflow_classes(package_paths),
            key=lambda cls: cls.__name__,
        ):
            workflow_cls.register_cli_arguments(parser)
        return parser.parse_args(argv)

    @classmethod
    def _discover_workflow_classes(
        cls, package_paths: list[tuple[Sequence[str], str]] | None
    ) -> set[Type[WorkflowInterface]]:
        """Find concrete workflow classes that implement register_cli_arguments."""
        classes: set[Type[WorkflowInterface]] = set()
        search_paths = package_paths or [(core_pkg.__path__, f"{core_pkg.__name__}.")]
        for paths, prefix in search_paths:
            for _, module_name, is_pkg in pkgutil.walk_packages(paths, prefix):
                if not is_pkg:
                    module = importlib.import_module(module_name)
                    classes.update(cls._collect_workflow_classes(module))
        return classes

    @staticmethod
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


# For backward compatibility with existing imports
workflow_cli_parser = WorkflowCLIParser
