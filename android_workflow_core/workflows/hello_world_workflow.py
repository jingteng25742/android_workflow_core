from __future__ import annotations

import argparse

from .core.workflow_config import WorkflowConfig
from .core.workflow_interface import WorkflowInterface
from .core.workflow_types import (
    WorkflowActionHandler,
    WorkflowActionName,
    WorkflowActionResult,
    WorkflowName,
)


class HelloWorldWorkflow(WorkflowInterface):
    """Minimal workflow used for testing the workflow factory."""

    def __init__(self, config: "WorkflowConfig") -> None:
        self._device = config.device
        self._actions: dict[WorkflowActionName, WorkflowActionHandler] = {
            WorkflowActionName('login') : self.login,
            WorkflowActionName('start') : self.start,
            WorkflowActionName('stop') : self.stop,
            WorkflowActionName('status') : self.status,
        }

    def workflow_name(self) -> WorkflowName:
        return "workflow.hello.world"

    def package_name(self) -> WorkflowName:
        return self.workflow_name()

    @staticmethod
    def register_cli_arguments(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--hello-world-greeting",
            default="hello",
            help="Greeting string exposed by the hello world workflow CLI.",
        )


    def action_handler(self, action: WorkflowActionName) -> WorkflowActionHandler:
        return self._actions[action]

    def run(self, action: WorkflowActionName) -> bool:
        handler = self.action_handler(action)
        return handler()

    def login(self) -> bool:
        return True

    def start(self) -> bool:
        return True

    def stop(self) -> bool:
        return True

    def status(self) -> bool:
        return True

    def _noop(self) -> bool:
        """No-op action handler for testing."""
        return True
