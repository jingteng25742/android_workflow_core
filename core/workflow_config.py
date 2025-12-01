from __future__ import annotations
import argparse

from dataclasses import dataclass
from typing import Any, Optional

import uiautomator2 as u2

from .workflow_types import WorkflowActionName, WorkflowName
import argparse

@dataclass(init=False)
class WorkflowConfig:
    """Configuration for the automated workflow."""

    workflow_name: WorkflowName
    action_name: WorkflowActionName
    device_id: Optional[str] = None
    delay_minutes: int = 0
    device: Optional[u2.Device] = None
    args: argparse.Namespace = None

    def __init__(
        self,
        workflow: WorkflowName,
        action: WorkflowActionName,
        device_id: Optional[str] = None,
        delay_minutes: int = 0,
        args: argparse.Namespace = None,
    ) -> None:
        self.workflow_name = workflow
        self.action_name = action
        self.device_id = device_id
        self.delay_minutes = delay_minutes
        self.device = None
        self.args = args
        
