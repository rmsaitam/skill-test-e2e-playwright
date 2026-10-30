# Stable Playwright test patterns

Inspect existing tests first. Preserve the project's language, package manager, Playwright configuration, fixture conventions, and test directory when they are already established.

## Locators and assertions

Prefer selectors that express what a user can identify:

1. `page.getByRole(role, { name })`
2. `page.getByLabel(name)` for labeled form controls
3. `page.getByPlaceholder(text)` where the placeholder is the intended user affordance
4. `page.getByText(text)` for visible content
5. `getByTestId()` only when no stable semantic locator is practical and a stable test ID exists or is justified

Avoid generated CSS classes, positional selectors, brittle XPath, and broad selectors that match multiple elements. Scope ambiguous locators to a meaningful landmark or container and assert uniqueness where appropriate.

Use web-first assertions:

```ts
await expect(page).toHaveURL(/\/dashboard$/);
await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
await expect(page.getByRole('button', { name: 'Save' })).toBeEnabled();
```

Do not read a locator once and assert on a stale value. Do not use fixed `page.waitForTimeout()` sleeps; wait for a user-visible condition, URL, response, or other explicit state.
Do not treat one-shot `textContent()` or `isVisible()` reads as assertions; use retrying web-first `expect` assertions for observable UI outcomes.

## Page Object Model

Default to `tests/pages/` for reusable page objects and `tests/specs/` for user-facing specs. Follow an existing equivalent when present. Keep page objects focused on that page's locators and meaningful actions; assertions about the scenario's outcome generally belong in the test.

```ts
import { type Locator, type Page } from '@playwright/test';

export class LoginPage {
  readonly email: Locator;
  readonly password: Locator;
  readonly submit: Locator;

  constructor(private readonly page: Page) {
    this.email = page.getByLabel('Email');
    this.password = page.getByLabel('Password');
    this.submit = page.getByRole('button', { name: 'Sign in' });
  }

  async open(): Promise<void> {
    await this.page.goto('/login');
  }

  async signIn(email: string, password: string): Promise<void> {
    await this.email.fill(email);
    await this.password.fill(password);
    await this.submit.click();
  }
}
```

Adapt labels, routes, fields, and assertions to the real application; this example is a pattern, not a claim about a project's UI.

## Configuration and reliability

Preserve existing configuration. For a new Playwright Test setup, configure the actual base URL, test directory, and artifacts from project evidence. The expected failure evidence includes:

```ts
use: {
  trace: 'on-first-retry',
  screenshot: 'only-on-failure',
}
```

Use auto-waiting, isolated test data, and deterministic setup/cleanup. Do not share mutable accounts across parallel tests unless the application supports isolation. Make every test safe to retry; retries must not duplicate real external actions.

Use `storageState` only with a dedicated test identity and safe project setup. Keep auth-state files and secrets out of version control; add targeted ignore rules when creating a local state file. Never read or log secret values.

Use the repository's existing browser matrix. Do not expand tests to Chromium, Firefox, and WebKit automatically if the project does not support them or the user did not request them; state the actual matrix in the report.

## Artifacts and dependencies

Reuse `@playwright/test` if present. If not, inspect the package manager and add only the required dev dependency and browser setup required by the task. Avoid replacing lockfiles or installing global packages. Save traces/screenshots in the configured test-results location and avoid committing user data or bulky exploration artifacts.

Official references:

- [Locators](https://playwright.dev/docs/locators)
- [Assertions](https://playwright.dev/docs/test-assertions)
- [Test configuration](https://playwright.dev/docs/test-configuration)
- [Trace Viewer](https://playwright.dev/docs/trace-viewer)
