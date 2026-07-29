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

// ── Phase 8 — harness and class filters (AC-18, AC-22, AC-27) ─────────────────
// These three scenarios are also bound at the unit layer (test/unit/fe-steps/ai-benchmark.steps.tsx)
// — real browser navigation here proves the SAME behaviour survives an actual production request,
// not just a mocked render. "When the page renders" is already registered globally
// (cost-of-living-calculator.steps.ts) as a bare `waitForLoadState`, so navigation happens in each
// scenario's own Given/When step here, not there.

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
Given("the URL carries no query parameters", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
Then("every roster model is shown in the data table", async ({ page }) => {
  await page.waitForLoadState("networkidle");
  // Appendix A.2 roster — see apps/ayokoding-www's core/data/models.ts's own "38 rows" comment.
  await expect(page.locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]')).toHaveCount(38);
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A harness filter switches the price chart to that harness's rate
Given("a fixture model priced differently by two harnesses", async ({}) => {
  // The e2e layer exercises the REAL roster (no fixture injection over HTTP) — Grok 4.5
  // (core/data/models.ts) is genuinely priced differently by two harnesses: cursor/opencode-zen at
  // a metered $2/$6 rate, opencode-go at a flat-rate subscription instead.
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A harness filter switches the price chart to that harness's rate
When("the harness filter selects the more expensive harness", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=opencode-go");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A harness filter switches the price chart to that harness's rate
Then("that model's bars use that harness's rate", async ({ page }) => {
  // opencode-go carries Grok 4.5 as a flat-rate subscription, not a per-token rate — selecting it
  // must remove Grok 4.5's metered bar and list it in the subscription group instead.
  await expect(page.getByTestId("price-chart-bar-in-grok-4.5")).toHaveCount(0);
  await expect(page.getByTestId("price-chart-subscription-grok-4.5")).toBeVisible();
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
Given("the reader has applied a harness filter and a class filter", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=cursor&class=opus");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
When("the reader reloads the resulting URL", async ({ page }) => {
  await page.reload();
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
Then("the same filtered set of models is shown", async ({ page }) => {
  const rowIds = () =>
    page
      .locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]')
      .evaluateAll((els) => els.map((el) => el.getAttribute("data-model-id")));

  const idsAfterReload = (await rowIds()).sort();

  // Idempotence check: a FRESH, independent navigation to the exact same URL must decode to the
  // identical filtered set the reload just showed — proving the URL alone (not any client-side
  // navigation history) determines the view.
  await page.goto("/en/tools/ai-benchmark?harness=cursor&class=opus");
  await page.waitForLoadState("networkidle");
  const idsFreshLoad = (await rowIds()).sort();

  expect(idsAfterReload).toEqual(idsFreshLoad);
  // A genuine narrowing — neither empty (that combination has matches on the live roster) nor the
  // full 38-row roster (the filters really did narrow it).
  expect(idsAfterReload.length).toBeGreaterThan(0);
  expect(idsAfterReload.length).toBeLessThan(38);
});
