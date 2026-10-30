# Failure triage and minimal fixes

Do not treat every red test as an application bug. Reproduce the failure and classify it before editing.

| Category | Evidence to collect | Response |
|---|---|---|
| Startup/environment | App or MCP process output, actual URL, port ownership, runtime version | Repair the documented setup or report the external blocker; do not edit application behavior to mask it. |
| Test/locator defect | Duplicate matches, wrong accessible name, invalid assumption, order dependence | Correct the test to reflect the actual UI and intended behavior. Keep the assertion meaningful. |
| Authentication/test data | Test identity unavailable, expired state, shared mutable record | Use a safe documented fixture or ask for test access; do not extract profile data or invent credentials. |
| Confirmed product defect | Reproducible user-visible mismatch against a requirement or repository specification | Add a regression test, fix the smallest relevant app code, and rerun focused and surrounding checks. |
| Flaky timing | Failure varies and evidence identifies a real async readiness condition | Wait for that condition using Playwright's auto-waiting or explicit event/assertion. Do not add arbitrary sleeps or unbounded retries. |

## Product-defect procedure

1. Reproduce the issue against the intended local/test environment and record the failing route and observable result.
2. Read the user requirement or repository documentation that establishes expected behavior. If intent is unclear, do not guess.
3. Add or adjust a regression test that fails for the observed defect without weakening other checks.
4. Make a minimal fix in the directly responsible code. Avoid unrelated refactors or dependency changes.
5. Search for the same incorrect construct in the project and fix or report other confirmed instances.
6. Rerun the regression test, affected E2E specs, and relevant project checks.

Do not submit payments, delete real records, send communications, or otherwise mutate production data while reproducing a defect. If the product fix is outside the authorized repository or cannot be verified, report that limitation.
