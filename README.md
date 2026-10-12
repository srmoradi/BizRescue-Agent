# BizRescue-Agent

**AI-Assisted Workflow Recovery Prototype by Avin AI**

BizRescue Agent is an experimental prototype that demonstrates how AI can help analyze workflow events and support recovery when a file export fails.

## Current Features

- AI-powered event analysis using an OpenAI-compatible API.
- Controlled export failure simulation.
- Fallback file export.
- Verification of the recovered output.
- Run reports and local event logging.
- API credentials loaded from environment variables.

## How It Works

1. Start a workflow run.
2. Attempt to export a report.
3. Detect a controlled export failure.
4. Write the report to a fallback location.
5. Verify the recovered output.
6. Ask an AI model to analyze the workflow events.
7. Save a run report and event log.

## Requirements

- Python 3.8 or later
- Access to a compatible language-model API
- A valid API key

## Configuration

Set the `LITELLM_API_KEY` environment variable before running the application.

Never commit API keys, passwords, or other secrets to the repository.

## Run

```bash
python bizrescue_agent.py
```

## Project Status

This is an early-stage prototype. The current recovery scenario deliberately uses a missing directory to simulate an export failure. It does not yet demonstrate recovery from a real external service outage.

Integrations with neatlogs, Entire, and cfo.ai are planned for development and must be implemented and tested before they can be considered complete.

## Security and Responsible Use

Keep credentials outside source code. Use environment variables and avoid publishing logs that contain sensitive information.

## Author

**Avin AI**

## License

MIT License — see the `LICENSE` file when available.
