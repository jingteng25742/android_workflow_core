from workflow_core.workflows.hello_world_workflow import HelloWorldWorkflow
from workflow_core.core.workflow_factory import WorkflowFactory
from workflow_core.core.workflow_types import WorkflowActionName
from workflow_core.core.workflow_config import WorkflowConfig


def test_get_returns_registered_workflow_class():
    config = WorkflowConfig(
        workflow="workflow.hello.world",
        action=WorkflowActionName("login"),
        device_id=None,
        delay_minutes=0,
    )
    workflow_cls = WorkflowFactory.get_workflow(config)
    assert isinstance(workflow_cls, HelloWorldWorkflow)


def test_get_raises_for_unknown_workflow():
    config = WorkflowConfig(
        workflow="workflow.does.not.exist",
        action=WorkflowActionName("login"),
        device_id=None,
        delay_minutes=0,
    )
    try:
        WorkflowFactory.get_workflow(config)
    except ValueError as exc:
        assert "No workflow found" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown workflow")
