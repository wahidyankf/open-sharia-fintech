/**
 * Step definitions for the OSE Application Web smoke feature.
 *
 * Covers: specs/apps/ose/app-web/behaviours/smoke/smoke.feature
 */
import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

Given("the ose-app-web dev server is running", async ({ request }) => {
  const baseUrl = process.env["WEB_BASE_URL"] ?? "http://localhost:3300";
  const response = await request.get(baseUrl);
  expect(response.status(), "the public application boundary must be reachable").toBeLessThan(400);
});

When("I navigate to {string}", async ({ page }, path: string) => {
  await page.goto(`${process.env["WEB_BASE_URL"] ?? "http://localhost:3300"}${path}`);
});

Then("I see the heading {string}", async ({ page }, heading: string) => {
  const h1 = page.getByRole("heading", { level: 1 });
  await expect(h1).toHaveText(heading);
});
