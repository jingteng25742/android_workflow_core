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

    def __init__(self) -> None:
        self.stopped_packages: list[str] = []
        self.pressed_keys: list[str] = []

    def screen_on(self) -> None:
        pass

    def swipe(self, *args, **kwargs) -> None:
        pass

    def app_stop(self, pkg: str) -> None:
        self.stopped_packages.append(pkg)

    def press(self, key: str) -> None:
        self.pressed_keys.append(key)


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


def test_return_to_home_stops_workflow_package_name(monkeypatch):
    devices = [DummyAdbDevice("serial-one")]
    monkeypatch.setattr(workflow_module.adbutils.adb, "device_list", lambda: devices)

    u2_device = DummyU2Device()
    monkeypatch.setattr(workflow_module.u2, "connect", lambda serial=None: u2_device)

    class DummyWorkflow:
        def package_name(self) -> str:
            return "com.example.workflow"

    monkeypatch.setattr(
        workflow_module.WorkflowFactory,
        "get_workflow",
        lambda config: DummyWorkflow(),
    )

    workflow = Workflow(_base_config())
    workflow._return_to_home()

    assert u2_device.stopped_packages == ["com.example.workflow"]
    assert u2_device.pressed_keys == ["home"]
