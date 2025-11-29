from __future__ import annotations

import argparse
from typing import Protocol, runtime_checkable

from .workflow_config import WorkflowConfig
from .workflow_types import WorkflowActionHandler, WorkflowActionName, WorkflowActionResult, WorkflowName


@runtime_checkable
class WorkflowInterface(Protocol):
    """Interface for common workflow automation actions."""

    def __init__(self, config: "WorkflowConfig") -> None: ...

    def workflow_name(self) -> WorkflowName: ...
    
    def package_name(self) -> WorkflowName: ...

    def action_handler(self, action: WorkflowActionName) -> WorkflowActionHandler: ...

    def actions(self) -> dict[WorkflowActionName, WorkflowActionHandler]: ...
    
    def run(self, action: WorkflowActionName) -> bool: ...
    
    @staticmethod
    def register_cli_arguments(parser: argparse.ArgumentParser) -> None: ...
    
