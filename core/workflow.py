"""Workflow primitives built on top of uiautomator2."""

from __future__ import annotations

import time
from functools import wraps
import random

import uiautomator2 as u2
import adbutils

from ..messaging.messaging import send
from .workflow_config import WorkflowConfig
from .workflow_factory import WorkflowFactory
from .workflow_types import WorkflowActionName, WorkflowActionResult, WorkflowName
class Workflow:
    """High-level orchestrator for automating an Android application."""

    def __init__(self, config: WorkflowConfig) -> None:
        self.config: WorkflowConfig = config
        device_id = config.device_id or self._get_first_connected_device_id()
        if config.device_id:
            print(f"Connecting to explicitly provided device '{device_id}'.")
        self.device = u2.connect(device_id)
        self.config.device = self.device
        print(f"Device connection established for '{device_id}'.")

    @staticmethod 
    def _random_delay():
        """
        Decorator that delays the execution of a function by a random number
        of minutes between 1 minute and max_minutes (inclusive).
        """
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                delay_minutes_max = getattr(self.config, "delay_minutes", 0)
                if delay_minutes_max == 0:
                    print(f"Delay bypassed for '{func.__name__}'")
                else:
                    delay_minutes = random.randint(1, delay_minutes_max)
                    print(f"Delaying '{func.__name__}' for {delay_minutes} minute(s)...")
                    delay_seconds = delay_minutes * 60
                    time.sleep(delay_seconds)
                
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    @_random_delay()
    def run(self) -> WorkflowActionResult:
        """Entry point for the workflow."""
        workflow_name = self.config.workflow_name
        action_name = self.config.action_name
        success = False
        error = None

        self._wake_device()
        print(f"Executing '{workflow_name}:{action_name}'.")
        
        """Execute workflow-specific automation steps."""
        try:
            workflow = WorkflowFactory.get_workflow(self.config)
            success = workflow.run(self.config.action_name)
        except Exception as exc:
            error = exc
            print (f"Workflow '{workflow_name}:{action_name}' failed with exception: {exc!r}")
            
        send(success, f"{workflow_name}:{action_name} {success}", error)
        
        return WorkflowActionResult(
            workflow_name=workflow_name,
            action_name=action_name,
            success=success,
            error=error,
        ) 

    def _get_first_connected_device_id(self) -> str:
        """Return the first connected adb device serial or raise if none."""
        devices = adbutils.adb.device_list()
        if not devices:
            raise RuntimeError("No connected Android devices found.")
        if len(devices) > 1:
            print(
                f"Multiple devices detected; defaulting to first device '{devices[0].serial}'."
            )
        return devices[0].serial
        
    def _wake_device(self) -> None:
        """Turn on the screen and unlock the device if needed."""
        device_info = self.device.info
        print(f"Device screen status: {'on' if device_info.get('screenOn', False) else 'off'}.")
        if not device_info.get("screenOn", False):
            print("Screen is off. Turning screen on.")
            self.device.screen_on()
            time.sleep(0.5)

        if self.device.info.get("currentPackageName") == "com.android.systemui":
            # Basic swipe to unlock gesture; adjust coordinates to match the device.
            print("Unlocking device with swipe gesture.")
            self.device.swipe(500, 1600, 500, 400, 0.2)
            time.sleep(0.5)
        else:
            print("Device already unlocked.")

    def _return_to_home(self) -> None:
        """Bring the device back to a neutral state."""
        print(f"Stopping package '{self.config.workflow_name}' and returning to home screen.")
        self.device.app_stop(self.config.workflow_name)
        self.device.press("home")
    
