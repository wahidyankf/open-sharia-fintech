import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Then } = createBdd();

Then("the current URL should contain {string}", async ({ page }, expectedPath: string) => {
  await page.waitForLoadState("networkidle");
  expect(page.url()).toContain(expectedPath);
});
