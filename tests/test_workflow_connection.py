import pytest

import workflow_core.core.workflow as workflow_module
from workflow_core.core.workflow import Workflow
from workflow_core.core.workflow_config import WorkflowConfig
from workflow_core.core.workflow_types import WorkflowActionName


class DummyAdbDevice:
    def __init__(self, serial: str) -> None:
        self.serial = serial


class DummyU2Device:
    info = {}

    def screen_on(self) -> None:
        pass

    def swipe(self, *args, **kwargs) -> None:
        pass

    def app_stop(self, pkg: str) -> None:
        pass

    def press(self, key: str) -> None:
        pass


def _base_config() -> WorkflowConfig:
    return WorkflowConfig(
        workflow="workflow.hello.world",
        action=WorkflowActionName("login"),
        device_id=None,
        delay_minutes=0,
    )


def test_connect_defaults_to_first_device(monkeypatch):
    devices = [DummyAdbDevice("serial-one"), DummyAdbDevice("serial-two")]
    monkeypatch.setattr(workflow_module.adbutils.adb, "device_list", lambda: devices)

    connected_serials: list[str] = []

    def fake_connect(serial: str | None = None):
        connected_serials.append(serial)
        return DummyU2Device()

    monkeypatch.setattr(workflow_module.u2, "connect", fake_connect)

    config = _base_config()
    workflow = Workflow(config)

    assert connected_serials == ["serial-one"]
    assert isinstance(workflow.config.device, DummyU2Device)
    


def test_no_devices_connected_raises(monkeypatch):
    monkeypatch.setattr(workflow_module.adbutils.adb, "device_list", lambda: [])

    with pytest.raises(RuntimeError, match="No connected Android devices"):
        Workflow(_base_config())
