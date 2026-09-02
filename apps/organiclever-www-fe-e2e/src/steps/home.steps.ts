/**
 * Step definitions for the OrganicLever marketing home page feature.
 *
 * Covers: specs/apps/organiclever/www/behaviors/frontend/home/home.feature
 *
 * playwright-bdd treats all keyword registrations (Given/When/Then) as synonyms,
 * so each unique step pattern must be registered exactly once.
 */
import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, Then } = createBdd();

Given("I navigate to the marketing home page", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("domcontentloaded");
});

// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Hero heading visible
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Footer link present
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Pre-Alpha badge visible in nav
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Alpha warning banner visible
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:All five event type cards visible
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Custom event card visible
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Weekly rhythm demo visible
// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:All six principles visible
Then("I see text {string}", async ({ page }, text: string) => {
  await expect(page.getByText(text).first()).toBeVisible();
});

// @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Primary call-to-action button present
Then("I see a button {string}", async ({ page }, name: string) => {
  await expect(page.getByRole("button", { name })).toBeVisible();
});
