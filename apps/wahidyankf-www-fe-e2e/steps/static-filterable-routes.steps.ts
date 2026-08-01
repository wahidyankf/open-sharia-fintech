import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { When, Then } = createBdd();

When('a visitor opens the shared CV search URL for "TypeScript"', async ({ page }) => {
  await page.goto("/cv?search=TypeScript");
  await page.waitForLoadState("load");
});

Then('the CV search input is prefilled with "TypeScript"', async ({ page }) => {
  await expect(page.getByPlaceholder("Search CV entries...")).toHaveValue("TypeScript");
});

Then('the "Head of Engineering - Hijra Bank" entry is visible', async ({ page }) => {
  await expect(page.getByText("Head of Engineering - Hijra Bank")).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Search-filtered portfolio routes are static yet still filterable
Then('the "Database Design Fundamentals for Software Engineers" entry is hidden', async ({ page }) => {
  await expect(page.getByText("Database Design Fundamentals for Software Engineers")).not.toBeVisible();
});
