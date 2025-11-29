from __future__ import annotations

import importlib
import inspect
import os
import pkgutil
from typing import Type

from .. import __path__ as workflows_path
from .workflow_interface import WorkflowInterface
from .workflow_types import WorkflowName
from .workflow_config import WorkflowConfig

class WorkflowFactory:
    """Factory utilities for resolving workflow implementations by name."""

    @staticmethod
    def get_workflow(
        config: WorkflowConfig,
    ) -> WorkflowInterface:
        """
        Retrieve a workflow implementation matching the provided name.

        Raises:
            ValueError: If no workflow implementation matches ``name``.
        """
        for workflow_cls in WorkflowFactory._discover_workflow_classes():
            if WorkflowFactory._workflow_name(workflow_cls) == config.workflow_name:
                return workflow_cls(config)
        raise ValueError(f"No workflow found for name '{config.workflow_name}'.")
    
    

    @staticmethod
    def _discover_workflow_classes() -> set[Type[WorkflowInterface]]:
        classes: set[Type[WorkflowInterface]] = set()

        # Discover built-in workflows under workflow_core
        package_name = __package__ or __name__
        parent_package = package_name.rsplit(".", 1)[0] if "." in package_name else package_name
        package_prefix = f"{parent_package}."
        for _, module_name, is_pkg in pkgutil.iter_modules(
            workflows_path, prefix=package_prefix
        ):
            if is_pkg:
                continue
            module = importlib.import_module(module_name)
            for value in vars(module).values():
                if (
                    inspect.isclass(value)
                    and value is not WorkflowInterface
                    and issubclass(value, WorkflowInterface)
                ):
                    classes.add(value)

        # Optionally discover workflows from extra packages (comma-separated)
        extra_packages = os.getenv("WORKFLOW_EXTRA_PACKAGES", "workflows")
        for pkg_name in [p.strip() for p in extra_packages.split(",") if p.strip()]:
            try:
                pkg = importlib.import_module(pkg_name)
            except ModuleNotFoundError:
                continue
            pkg_path = getattr(pkg, "__path__", None)
            if not pkg_path:
                continue
            for _, module_name, is_pkg in pkgutil.iter_modules(pkg_path, prefix=f"{pkg_name}."):
                if is_pkg:
                    continue
                module = importlib.import_module(module_name)
                for value in vars(module).values():
                    if (
                        inspect.isclass(value)
                        and value is not WorkflowInterface
                        and issubclass(value, WorkflowInterface)
                    ):
                        classes.add(value)

        return classes

    @staticmethod
    def _workflow_name(workflow_cls: Type[WorkflowInterface]) -> WorkflowName:
        name_attr = getattr(workflow_cls, "workflow_name", None)
        if not callable(name_attr):
            raise ValueError(
                f"Workflow '{workflow_cls.__name__}' is missing a callable workflow_name()."
            )

        try:
            result = name_attr()
        except TypeError:
            # Instance method; bypass __init__ to avoid side effects.
            instance = workflow_cls.__new__(workflow_cls)  # type: ignore[misc]
            result = name_attr(instance)
        except Exception as exc:  # pragma: no cover - defensive guardrail
            raise ValueError(
                f"Failed to resolve workflow name for '{workflow_cls.__name__}'"
            ) from exc

        if not isinstance(result, str):
            raise TypeError(
                f"Workflow '{workflow_cls.__name__}' returned non-string name: {result!r}"
            )

        return result
