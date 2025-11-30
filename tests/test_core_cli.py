from workflow_core.core.workflow_cli_parser import WorkflowCLIParser


def test_delay_flag_and_action_present():
    args = WorkflowCLIParser.parse(
        ["--workflow", "workflow.hello.world", "-d", "3"]
    )

    assert args.delay == 3
