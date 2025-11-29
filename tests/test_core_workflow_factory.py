from android_workflow_core.workflows.hello_world_workflow import HelloWorldWorkflow
from android_workflow_core.workflows.core.workflow_factory import WorkflowFactory
from android_workflow_core.workflows.core.workflow_types import WorkflowActionName
from android_workflow_core.workflows.core.workflow_config import WorkflowConfig


def test_get_returns_registered_workflow_class():
    config = WorkflowConfig(
        workflow="workflow.hello.world",
        action=WorkflowActionName("login"),
        device_id=None,
        no_delay=False,
    )
    workflow_cls = WorkflowFactory.get_workflow(config)
    assert isinstance(workflow_cls, HelloWorldWorkflow)


def test_get_raises_for_unknown_workflow():
    config = WorkflowConfig(
        workflow="workflow.does.not.exist",
        action=WorkflowActionName("login"),
        device_id=None,
        no_delay=False,
    )
    try:
        WorkflowFactory.get_workflow(config)
    except ValueError as exc:
        assert "No workflow found" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown workflow")
