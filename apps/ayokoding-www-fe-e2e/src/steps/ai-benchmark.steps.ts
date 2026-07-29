import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

// AI Benchmark e2e step bindings. AC-1, AC-2, and AC-36 are the scenarios bound at the e2e layer
// in this plan; every other scenario is permanently unit-only (see DD-22 in tech-docs.md) and
// renders as `test.fixme` under this project's `missingSteps: "skip-scenario"` config — they are
// not deferred pending a later e2e binding.

// The active locale for the scenario — set by "Given the locale is …" and read by the navigation
// step. Module-scoped because playwright-bdd step functions are stateless over the fixture context.
let scenarioLocale = "en";

// ── Preconditions ─────────────────────────────────────────────────────────────

// Background step — the dataset is always loaded on the served page; nothing to set up. The empty
// fixture destructuring is the playwright-bdd idiom for a fixture-less step (an `no-empty-pattern`
// lint warning, non-failing, matching the project's generated step files).
Given("the AI benchmark dataset is loaded", async ({}) => {});

Given("the locale is {string}", async ({}, locale: string) => {
  scenarioLocale = locale;
});

// AC-36's precondition. The generic "the page renders" step (bound elsewhere, shared across
// features) only waits for load state, so navigation happens here.
Given("the full roster is loaded", async ({ page }) => {
  await page.goto(`/${scenarioLocale}/tools/ai-benchmark`);
});

// ── Navigation ────────────────────────────────────────────────────────────────

When("the AI benchmark page renders", async ({ page }) => {
  await page.goto(`/${scenarioLocale}/tools/ai-benchmark`);
  await page.waitForLoadState("networkidle");
});

// ── Page shell assertions (AC-1 / AC-2) ───────────────────────────────────────

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The English page renders its localized heading
Then("the page shows a level-one heading in English", async ({ page }) => {
  const h1 = page.locator("h1").first();
  await expect(h1).toBeVisible();
  const text = (await h1.textContent()) ?? "";
  expect(text.trim().length).toBeGreaterThan(0);
  // The served English H1 must carry the English copy, not the Indonesian one.
  expect(text.trim()).not.toBe("Tolok Ukur Model AI");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The Indonesian page renders its localized heading
Then("the page shows a level-one heading in Indonesian", async ({ page }) => {
  const h1 = page.locator("h1").first();
  await expect(h1).toBeVisible();
  const text = (await h1.textContent()) ?? "";
  expect(text.trim().length).toBeGreaterThan(0);
  // The served Indonesian H1 must carry the localized copy, distinct from English.
  expect(text.trim()).not.toBe("AI Model Benchmark");
});

Then("the document language attribute is {string}", async ({ page }, expectedLang: string) => {
  // The root layout sets <html lang> from the locale URL segment.
  await expect(page.locator("html")).toHaveAttribute("lang", expectedLang);
});

// ── Chart accessible-name assertions (AC-36) ──────────────────────────────────

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Each chart exposes an accessible name
Then("the capability chart exposes an accessible name", async ({ page }) => {
  await expect(page.getByTestId("capability-chart-svg")).toHaveAccessibleName(/.+/);
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Each chart exposes an accessible name
Then("the price chart exposes an accessible name", async ({ page }) => {
  await expect(page.getByTestId("price-chart-svg")).toHaveAccessibleName(/.+/);
});
