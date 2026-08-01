import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then } = createBdd();

Given("a visitor requests the root URL", async ({ page }) => {
  await page.goto("/");
});

Given("a visitor requests the uppercase locale URL {string}", async ({ page }, sourceUrl: string) => {
  await page.goto(sourceUrl);
});

When("locale redirects are applied", async ({ page }) => {
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/i18n/locale-redirects.feature:The root URL enters the default locale
Then("the visitor reaches the default locale at {string}", async ({ page }, destinationUrl: string) => {
  await expect(page).toHaveURL(new RegExp(`${destinationUrl.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`));
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/i18n/locale-redirects.feature:Uppercase locale URLs redirect to lowercase canonical URLs
Then("the visitor is permanently redirected to {string}", async ({ page }, destinationUrl: string) => {
  await expect(page).toHaveURL(new RegExp(`${destinationUrl.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`));
});
