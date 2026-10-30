# Route inventory and screen coverage

The inventory is the source of truth for the screen-coverage denominator. Create `E2E-COVERAGE.md` in the project root unless the repository already has an equivalent artifact.

## Discovering the denominator

Build the candidate list from the application router, navigation and in-app links, route configuration, README/product documentation, and known roles or feature flags. Confirm each in-scope route in the running application. A list of only homepage links is not sufficient when the router or product documentation reveals additional routes.

Represent parameterized paths as stable route patterns, such as `/users/:userId`. Group concrete IDs only when they use the same screen and behavior. List a route separately when a role, feature flag, query state, or workflow produces a materially different screen. Do not invent infinite permutations: record the chosen representative values and relevant variants.

For authentication-protected routes, use only the project's documented test-auth mechanism or credentials supplied for testing. If access is unavailable, record the route as `blocked`; do not remove it from the denominator. Exclude a route only with a documented reason (for example, an explicitly out-of-scope third-party system).

## Suggested table

| ID | Route pattern | Role/precondition | Screen purpose | Test | Exploration | Test result | Notes |
|---|---|---|---|---|---|---|---|
| SCR-001 | `/example` | Anonymous | Landing screen | `landing.spec.ts` | inspected | passed | — |

Use stable IDs and keep links from each screen to its spec. Record changes to the route list so the denominator can be reviewed.

## Status and calculation

- `covered`: a test exists for the screen and passed in the reported run.
- `pending`: discovered but not yet explored or tested.
- `blocked`: execution was prevented by an explicit environment, credential, or permission barrier.
- `excluded`: deliberately outside scope, with a reason and (when relevant) user approval.

Report screen coverage as `covered in-scope screens / total in-scope screens`. Claim 100% only if every in-scope screen has a passing test in the same verification run and no pending or blocked screen remains. Excluded routes must be listed separately and never hidden by reducing the denominator without explanation.

This metric covers screens/routes only. It is not line, branch, component, accessibility, browser-engine, or all-state coverage. Report important interaction states and browser matrices separately.
