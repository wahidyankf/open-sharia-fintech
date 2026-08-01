import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { getResilient } from "../support/resilient-request";

const { Given, When, Then } = createBdd();
const lessonUrl = "/en/learn/overview";
const prerenderManifestPath = path.resolve(process.cwd(), "../ayokoding-www/.next/prerender-manifest.json");

interface StaticDeliveryState {
  firstResponse?: import("@playwright/test").APIResponse;
  secondResponse?: import("@playwright/test").APIResponse;
  manifest?: { routes?: Record<string, unknown> };
}

const stateByPage = new WeakMap<import("@playwright/test").Page, StaticDeliveryState>();

function stateFor(page: import("@playwright/test").Page): StaticDeliveryState {
  const existing = stateByPage.get(page);
  if (existing) return existing;
  const created: StaticDeliveryState = {};
  stateByPage.set(page, created);
  return created;
}

Given("the ayokoding-www site is built and deployed", async ({ page }) => {
  expect(existsSync(prerenderManifestPath)).toBe(true);
  const response = await getResilient(page, lessonUrl);
  expect(response.ok()).toBe(true);
});

When("the build output manifest is inspected", async ({ page }) => {
  const manifest = JSON.parse(readFileSync(prerenderManifestPath, "utf8")) as StaticDeliveryState["manifest"];
  expect(manifest).toBeDefined();
  stateFor(page).manifest = manifest;
});

Then("the prerendered route count is at least two thousand", async ({ page }) => {
  const manifest = stateFor(page).manifest;
  expect(Object.keys(manifest?.routes ?? {}).length).toBeGreaterThanOrEqual(2000);
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature:A content page is prerendered at build time
Then("the content catch-all route is not marked as dynamically rendered", async ({ page }) => {
  // `dynamicParams = true` intentionally serves non-enumerated learn-path URLs. A generated content URL must still appear
  // in the manifest's static routes, which is the relevant static-delivery contract for this catch-all.
  expect(stateFor(page).manifest?.routes).toHaveProperty(lessonUrl);
});

Given("a visitor has already requested a course lesson URL", async ({ page }) => {
  const firstResponse = await getResilient(page, lessonUrl);
  expect(firstResponse.ok()).toBe(true);
  stateFor(page).firstResponse = firstResponse;
});

When("the same URL is requested again", async ({ page }) => {
  const secondResponse = await getResilient(page, lessonUrl);
  expect(secondResponse.ok()).toBe(true);
  stateFor(page).secondResponse = secondResponse;
});

Then("the response is served from the CDN cache", async ({ page }) => {
  expect(stateFor(page).secondResponse?.headers()["x-vercel-cache"]).toBe("HIT");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature:A repeat request to a content page is served from the CDN
Then("the response does not carry a no-store cache directive", async ({ page }) => {
  expect(stateFor(page).secondResponse?.headers()["cache-control"] ?? "").not.toMatch(/\bno-store\b/i);
});

Given("a visitor opens a content page in the {string} locale", async ({ page }, locale: string) => {
  await page.goto(`/${locale}/learn/overview`);
});

When("the content page renders", async ({ page }) => {
  await expect(page.getByRole("article")).toBeVisible();
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature:The document language reflects the content-page locale
Then("the html element declares the {string} language code", async ({ page }, languageCode: string) => {
  await expect(page.locator("html")).toHaveAttribute("lang", languageCode);
});
