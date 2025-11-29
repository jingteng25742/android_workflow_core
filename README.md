# workflow_core

Shared core for Android UI automation workflows. Provides:
- Workflow protocol, configuration, and discovery utilities.
- A neutral CLI that discovers registered workflows and runs actions.
- Twilio-based messaging helper with configurable credentials path.
- A HelloWorld sample workflow for testing/integration.

Usage (local editable install example):
1. `pip install -e ./workflow_core`
2. Implement a workflow class under your app repo that subclasses `WorkflowInterface` and exposes `register_cli_arguments`.
3. Run via `python -m workflow_core.cli --workflow your.workflow --action start --device-id <serial>`.

Messaging config is resolved from `MESSAGING_CONFIG_PATH` or defaults to `config/messaging.json` relative to the working directory.
