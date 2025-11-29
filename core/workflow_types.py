from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeAlias

WorkflowName: TypeAlias = str


class WorkflowActionName(str):
    """Strongly-typed workflow action identifier."""
    pass

WorkflowActionHandler = Callable[[], bool]


@dataclass(slots=True, init=False)
class WorkflowActionResult:
    """Encapsulates the outcome of a workflow run."""

    workflow: WorkflowName | None
    action: WorkflowActionName | None
    success: bool
    error: Exception | None = None

    def __init__(
        self,
        workflow_name: WorkflowName | None,
        action_name: str,
        success: bool,
        error: Exception | None = None,
    ) -> None:
        self.workflow = workflow_name
        self.action = WorkflowActionName(action_name.lower())
        self.success = success
        self.error = error
