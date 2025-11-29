from workflow_core import cli


def test_no_delay_flag_and_action_present():
    args = cli.parse_args(
        ["--workflow", "workflow.hello.world", "--action", "login", "--nd"]
    )

    assert args.no_delay is True
    assert args.action == "login"
