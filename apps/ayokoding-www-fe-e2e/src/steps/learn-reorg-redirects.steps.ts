import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Then } = createBdd();

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-reorg-redirects.feature:platform-web redirects to platforms/web under the /c namespace
Then("the current URL should contain {string}", async ({ page }, expectedPath: string) => {
  await page.waitForLoadState("networkidle");
  expect(page.url()).toContain(expectedPath);
});
