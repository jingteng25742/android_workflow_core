"""workflow_core: shared UI automation primitives and CLI."""

from . import messaging
from .core import (
    Workflow,
    WorkflowConfig,
    WorkflowFactory,
    WorkflowInterface,
    WorkflowActionHandler,
    WorkflowActionName,
    WorkflowActionResult,
    WorkflowName,
    WorkflowCLIParser,
)
from .workflows import HelloWorldWorkflow

__all__ = [
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
    "WorkflowCLIParser",
]
