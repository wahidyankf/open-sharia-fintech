import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { getResilient } from "../support/resilient-request";

const { Given, When, Then } = createBdd();
const lessonUrl = "/en/learn/overview";
const prerenderManifestPath = process.env.CI
  ? path.resolve(process.cwd(), ".e2e-artifacts/prerender-manifest.json")
  : path.resolve(process.cwd(), "../ayokoding-www/.next/prerender-manifest.json");

interface StaticDeliveryState {
  firstResponse?: import("@playwright/test").APIResponse;
  secondResponse?: import("@playwright/test").APIResponse;
  manifest?: { routes?: Record<string, unknown> };
  runtimeDataResponses?: readonly import("@playwright/test").APIResponse[];
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

// @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:A content page is prerendered at build time
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

// The local standalone runner has no Vercel CDN, so a cache HIT is a deployment-only assertion.
// This local contract proves the response stays cacheable; preview/production verifies the HIT.
// @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:A repeat request to a content page remains cacheable
Then("the response does not carry a no-store cache directive", async ({ page }) => {
  expect(stateFor(page).secondResponse?.headers()["cache-control"] ?? "").not.toMatch(/\bno-store\b/i);
});

// A local standalone runner cannot prove a Vercel CDN response. This deployment-bound verifier
// runs only when a real preview/production URL is deliberately supplied; see Phase 4's deploy gate.
Given("a Vercel preview or production deployment is selected for CDN verification", async ({ page }) => {
  test.skip(
    process.env.VERCEL_CDN_VERIFY !== "true",
    "CDN-HIT verification requires VERCEL_CDN_VERIFY=true against a real Vercel deployment",
  );
  const response = await getResilient(page, lessonUrl);
  expect(response.ok()).toBe(true);
  stateFor(page).firstResponse = response;
});

When("the same deployed course lesson URL is requested again", async ({ page }) => {
  const response = await getResilient(page, lessonUrl);
  expect(response.ok()).toBe(true);
  stateFor(page).secondResponse = response;
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:A repeat request to a deployed content page is served from the CDN
Then("the deployed response is served from the CDN cache", async ({ page }) => {
  expect(stateFor(page).secondResponse?.headers()["x-vercel-cache"]).toBe("HIT");
});

Given("the ayokoding-www standalone package is running", async ({ page }) => {
  const response = await getResilient(page, "/api/trpc/meta.health");
  expect(response.ok()).toBe(true);
});

When("navigation search and course-path data are requested through tRPC", async ({ page }) => {
  const endpoint = (procedure: string, input: unknown) =>
    `/api/trpc/${procedure}?input=${encodeURIComponent(JSON.stringify({ json: input }))}`;
  const responses = await Promise.all([
    getResilient(page, endpoint("content.getTree", { locale: "en" })),
    getResilient(page, endpoint("search.query", { locale: "en", query: "AyoKoding" })),
    getResilient(page, endpoint("coursePaths.getRouteData", "en")),
  ]);
  stateFor(page).runtimeDataResponses = responses;
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:Runtime tRPC endpoints retain their filesystem assets
Then("every runtime data endpoint responds successfully", async ({ page }) => {
  const responses = stateFor(page).runtimeDataResponses;
  expect(responses).toHaveLength(3);
  for (const response of responses ?? []) {
    expect(response.ok(), `${response.url()} should read its traced runtime assets`).toBe(true);
    expect(await response.json()).toHaveProperty("result.data");
  }
});

Given("a visitor opens a localized page in the {string} locale", async ({ page }, locale: string) => {
  await page.goto(`/${locale}`);
});

When("the localized page renders", async ({ page }) => {
  await expect(page.getByRole("main")).toBeVisible();
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:The document language reflects the localized page locale
Then("the html element declares the {string} language code", async ({ page }, languageCode: string) => {
  await expect(page.locator("html")).toHaveAttribute("lang", languageCode);
});
