"""workflow_core: shared UI automation primitives and CLI."""

from . import cli, messaging
from .core import (
    Workflow,
    WorkflowConfig,
    WorkflowFactory,
    WorkflowInterface,
    WorkflowActionHandler,
    WorkflowActionName,
    WorkflowActionResult,
    WorkflowName,
)
from .workflows import HelloWorldWorkflow

__all__ = [
    "cli",
    "messaging",
    "HelloWorldWorkflow",
    "Workflow",
    "WorkflowConfig",
    "WorkflowFactory",
    "WorkflowInterface",
    "WorkflowActionHandler",
    "WorkflowActionName",
    "WorkflowActionResult",
    "WorkflowName",
]
