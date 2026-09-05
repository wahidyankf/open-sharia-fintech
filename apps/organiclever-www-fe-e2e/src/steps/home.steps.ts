/**
 * Step definitions for the OrganicLever marketing home page feature.
 *
 * Covers: specs/apps/organiclever/www/behaviours/frontend/home/home.feature
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

Then("I see text {string}", async ({ page }, text: string) => {
  await expect(page.getByText(text).first()).toBeVisible();
});

Then("I see a button {string}", async ({ page }, name: string) => {
  await expect(page.getByRole("button", { name })).toBeVisible();
});
