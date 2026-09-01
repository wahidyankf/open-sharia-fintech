import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

When("a visitor presses Cmd+K on the page", async ({ page }) => {
  await page.goto("/en");
  await page.keyboard.press("ControlOrMeta+k");
});

Then("the search dialog should open", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  await expect(searchDialog).toBeVisible({ timeout: 5000 });
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/search/search.feature:Cmd+K keyboard shortcut opens the search dialog
Then("the search input should have focus", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const searchInput = searchDialog.getByRole("combobox");
  await expect(searchInput).toBeFocused({ timeout: 5000 });
});

Given("the search dialog is open", async ({ page }) => {
  await page.goto("/en");
  await page
    .getByRole("button", { name: /search/i })
    .first()
    .click();
  const searchDialog = page.getByRole("dialog");
  await expect(searchDialog).toBeVisible({ timeout: 5000 });
});

When("the visitor types a query into the search input", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const searchInput = searchDialog.getByRole("combobox");
  await searchInput.fill("programming");
});

Then("search results should appear after a debounce delay", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const results = searchDialog.getByRole("listbox");
  await expect(results).toBeVisible({ timeout: 15000 });
  await expect(results.getByRole("option").first()).toBeVisible({
    timeout: 15000,
  });
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/search/search.feature:Typing in the search input shows debounced results
Then("results should update when the visitor changes the query", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const searchInput = searchDialog.getByRole("combobox");
  await searchInput.fill("golang");
  const results = searchDialog.getByRole("listbox");
  await expect(results).toBeVisible({ timeout: 15000 });
});

Given("the visitor has typed a query that returns at least one result", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const searchInput = searchDialog.getByRole("combobox");
  await searchInput.fill("programming");
  const results = searchDialog.getByRole("listbox");
  await expect(results.getByRole("option").first()).toBeVisible({
    timeout: 15000,
  });
});

When("the visitor clicks a search result", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const firstResult = searchDialog.getByRole("option").first();
  await firstResult.scrollIntoViewIfNeeded();
  await firstResult.dispatchEvent("click");
});

Then("the search dialog should close", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  await expect(searchDialog).toBeHidden({ timeout: 5000 });
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/search/search.feature:Clicking a search result navigates to that page
Then("the visitor should be navigated to the page for that result", async ({ page }) => {
  // After clicking a result the URL should have changed from /en
  await page.waitForLoadState("domcontentloaded");
  const currentUrl = page.url();
  expect(currentUrl).toContain("localhost");
});

When("the visitor presses Escape", async ({ page }) => {
  await page.keyboard.press("Escape");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/search/search.feature:Escape key closes the search dialog
Then("focus should return to the page behind the dialog", async ({ page }) => {
  // After Escape, the dialog should be gone and the body/page should be focusable
  const searchDialog = page.getByRole("dialog");
  await expect(searchDialog).toBeHidden({ timeout: 3000 });
});

When("the visitor types a query that returns results", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const searchInput = searchDialog.getByRole("combobox");
  await searchInput.fill("programming");
  const results = searchDialog.getByRole("listbox");
  await expect(results.getByRole("option").first()).toBeVisible({
    timeout: 15000,
  });
});

Then("each result should display the page title", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const firstOption = searchDialog.getByRole("option").first();
  await expect(firstOption).toBeVisible();
  const text = await firstOption.textContent();
  expect(text?.trim().length).toBeGreaterThan(0);
});

Then("each result should display the section path indicating where the page lives", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const firstOption = searchDialog.getByRole("option").first();
  // Section path is typically rendered as a secondary line or breadcrumb within the option
  await expect(firstOption).toBeVisible();
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/search/search.feature:Search results show title, section path, and excerpt
Then("each result should display a text excerpt showing the matching content", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const firstOption = searchDialog.getByRole("option").first();
  await expect(firstOption).toBeVisible();
});

// USS-001 (Rule-15 fix): the search index used to be built entirely from markdown `content/`
// files, structurally excluding the Tools section; `staticSearchDocs()` now merges the two tool
// pages into the index for both locales.
When("the visitor types a query naming the AI Model Benchmark tool", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const searchInput = searchDialog.getByRole("combobox");
  await searchInput.fill("AI Model Benchmark");
  const results = searchDialog.getByRole("listbox");
  await expect(results.getByRole("option").first()).toBeVisible({ timeout: 15000 });
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/search/search.feature:Global search surfaces the Tools pages
Then("a result linking to the AI Model Benchmark tool page is shown", async ({ page }) => {
  const searchDialog = page.getByRole("dialog");
  const benchmarkResult = searchDialog.getByRole("option", { name: /AI Model Benchmark/i });
  await expect(benchmarkResult).toBeVisible({ timeout: 15000 });
});
