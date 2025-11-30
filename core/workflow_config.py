from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import uiautomator2 as u2

from .workflow_types import WorkflowActionName, WorkflowName


@dataclass(init=False)
class WorkflowConfig:
    """Configuration for the automated workflow."""

    workflow_name: WorkflowName
    action_name: WorkflowActionName
    device_id: Optional[str] = None
    delay_minutes: int = 0
    device: Optional[u2.Device] = None

    def __init__(
        self,
        workflow: WorkflowName,
        action: WorkflowActionName,
        device_id: Optional[str] = None,
        delay_minutes: int = 0,
    ) -> None:
        self.workflow_name = workflow
        self.action_name = action
        self.device_id = device_id
        self.delay_minutes = delay_minutes
        self.device = None
        
