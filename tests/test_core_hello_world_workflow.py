import argparse

from workflow_core.workflows.hello_world_workflow import HelloWorldWorkflow


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    HelloWorldWorkflow.register_cli_arguments(parser)
    return parser


def test_register_populates_default_greeting() -> None:
    parser = _build_parser()
    args = parser.parse_args([])
    assert args.hello_world_greeting == "hello"


def test_register_accepts_custom_greeting() -> None:
    parser = _build_parser()
    args = parser.parse_args(["--hello-world-greeting", "hi!"])
    assert args.hello_world_greeting == "hi!"
