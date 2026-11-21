---
name: e2e-testing-patterns
description: Write deterministic, flake-free end-to-end UI tests using Playwright semantic locators, Page Object Models, and network isolation.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# E2E Testing Patterns (Playwright)

## Use This Skill When
- Writing end-to-end browser tests for critical user journeys (login, CRUD flows, dashboards, multi-pane UI).
- Debugging flaky UI tests or configuring headless CI browser checks.

## Flake-Free Playwright Discipline
1. **Test Critical Journeys Only:** Cover high-value end-to-end flows; leave granular branch logic to fast unit tests.
2. **User-Facing Locators:** Prefer `getByRole`, `getByLabel`, `getByText`, and `getByTestId` over brittle CSS/XPath selectors.
3. **Auto-Waiting Over Arbitrary Sleeps:** Never use `waitForTimeout(2000)`; rely on Playwright web-first assertions (`await expect(locator).toBeVisible()`).
4. **Isolation & Clean State:** Each test gets a fresh browser context and deterministic test data (API seeding or mocked backend routes via `page.route`).
5. **Page Object Model (POM):** Encapsulate page selectors and actions in small POM classes (`<= 150 lines/file`) so UI refactors update one place.
6. **Debug Artifacts on Failure:** Capture traces, screenshots, and console errors on retry/failure into `/tmp` or CI artifacts.
