import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

// ── AC-13 (UWT-009): Tools index calculator entry has a description ───────────

Given("I am on the tools index page", async ({ page }) => {
  await page.goto("/en/tools");
  await page.waitForLoadState("networkidle");
});

When("the calculator entry renders", async ({ page }) => {
  await page.waitForLoadState("networkidle");
});

Then("the calculator entry shows a description distinct from its link text", async ({ page }) => {
  // Scope to the main content area to avoid matching the footer Tools column
  // which also links to the calculator (added in Phase 3 footer nav update).
  const main = page.locator("#main-content");
  const calcLink = main.getByRole("link", { name: /cost of living/i });
  await expect(calcLink).toBeVisible();
  const linkText = (await calcLink.textContent())?.trim() ?? "";

  const descEl = page.locator("[data-testid='tool-desc-calculator']");
  await expect(descEl).toBeVisible();
  const descText = (await descEl.textContent())?.trim() ?? "";

  // The description must be non-empty and differ from the link text
  expect(descText.length).toBeGreaterThan(0);
  expect(descText).not.toBe(linkText);
});

// ── AC-3: Phase 10 reveal — tools index AI benchmark entry ─────────────────────

When("the AI benchmark entry renders", async ({ page }) => {
  await page.waitForLoadState("networkidle");
});

Then("the AI benchmark entry shows a description distinct from its link text", async ({ page }) => {
  // Scope to the main content area to avoid matching the footer Tools column
  // which will also link to the AI benchmark tool once R-3 wires it up.
  const main = page.locator("#main-content");
  const benchLink = main.getByRole("link", { name: /ai (model )?benchmark/i });
  await expect(benchLink).toBeVisible();
  const linkText = (await benchLink.textContent())?.trim() ?? "";

  const descEl = page.locator("[data-testid='tool-desc-ai-benchmark']");
  await expect(descEl).toBeVisible();
  const descText = (await descEl.textContent())?.trim() ?? "";

  // The description must be non-empty and differ from the link text
  expect(descText.length).toBeGreaterThan(0);
  expect(descText).not.toBe(linkText);
});

// ── EWT-001 regression: exactly one <main> landmark per page ───────────────────

Given("I navigate to {string}", async ({ page }, path: string) => {
  await page.goto(path);
  await page.waitForLoadState("networkidle");
});

Then("exactly one main landmark is present", async ({ page }) => {
  await expect(page.locator("main")).toHaveCount(1);
});
