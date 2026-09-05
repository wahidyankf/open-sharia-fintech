import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given } = createBdd();

Given("the app is running", async ({ page }) => {
  const response = await page.goto("/");
  expect(response?.ok()).toBe(true);
  await expect(page.locator("body")).toBeVisible();
});
