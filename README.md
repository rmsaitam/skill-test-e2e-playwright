# Test E2E Playwright

A cross-platform skill for coding agents to inspect web applications in a browser, inventory their navigable routes, and implement stable Playwright end-to-end tests.

Repository: [rmsaitam/skill-test-e2e-playwright](https://github.com/rmsaitam/skill-test-e2e-playwright)

## Supported agents

The canonical skill lives in `skills/test-e2e-playwright/SKILL.md`. Plugin manifests integrate it with:

- Codex: `.codex-plugin/` and `.agents/plugins/`
- Claude Code: `.claude-plugin/`
- Antigravity: the root `plugin.json`
- Cursor: `.cursor-plugin/`
- GitHub Copilot: `plugin.json` and `.github/plugin/`
- Other agents that support skills: the `skills/` directory

Commands are in `commands/`. Plugin installation and activation can vary by host and version; refer to the current documentation for your agent.

## Usage

Activate `test-e2e-playwright` or use `/test-e2e-playwright` in a compatible host. Choose an execution mode for each run. If you do not specify one in your request, the agent will ask before exploring screens.

### Autonomous mode

The agent explores the discovered routes, records the inventory, implements the tests, and runs verification without pausing for per-screen approval. The browser remains visible so you can observe the work, but the agent does not wait for confirmation between screens.

Example request: `Use test-e2e-playwright in autonomous mode to cover the project's screens.`

### Guided mode

The agent works through one screen at a time: it opens the route in the visible browser, tells you which screen it is showing and what it observed, and waits for you to review and confirm or correct it before moving on. You can also request a specific interaction on that screen. After exploration, the agent implements and runs tests one screen at a time, shows you each test and its result, and waits for your review before proceeding.

Example request: `Use test-e2e-playwright in guided mode and wait for my confirmation on every screen.`

In guided mode, review checkpoints are real pauses. If the agent host cannot wait for your response, the agent must stop at the checkpoint instead of continuing silently. You can switch modes at a checkpoint.

`8931` is the MCP server's SSE port, not the application's port. The browser is a visible, isolated Playwright session; it does not reuse your regular browser profile or credentials. Screen coverage means inventoried navigable routes with passing tests, not 100% code coverage.

## Installation with skills.sh

Install the skill with:

```bash
npx skills add rmsaitam/skill-test-e2e-playwright
```

For marketplace or plugin installation, follow the current documentation for the relevant agent.

## Development and validation

Requirements: Python 3.10 or newer. No additional Python dependencies are required.

```bash
make test
make validate
make check
```

The validator checks manifests, required files, and essential parts of the skill contract. See `skills/test-e2e-playwright/references/` for browser, inventory, stability, and failure-triage guidance.
