---
description: Explore application screens and implement stable Playwright E2E coverage
argument-hint: App URL, workflow, or E2E testing scope
---

# Test E2E with Playwright

Load and follow the `test-e2e-playwright` skill.

User brief: `$ARGUMENTS`

At the start, honor an explicitly requested execution mode (autonomous or guided); if none was specified, ask the user to choose before exploring screens. In guided mode, pause on each screen for review before continuing and pause after implementing/testing each screen. Never continue through checkpoints without user confirmation.

Inspect the repository first and reuse its test conventions. After reconnaissance, start the Playwright MCP service with `npx --yes @playwright/mcp@latest --port 8931`, verify that this agent has a connected browser tool, then start or reuse the application using its own project command. Explore and inventory all in-scope navigable routes before implementing tests. Never confuse the MCP port with the app port.

Use the visible Playwright-controlled browser session, not the user's saved browser profile. Apply the route coverage rules and stable test patterns from the skill. Fix only confirmed application defects within scope, add regression tests, run the relevant checks, and report exact coverage and any blocked routes without overstating results.
