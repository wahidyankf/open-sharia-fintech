import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { When, Then } = createBdd();
const publicPortfolioRoutes = ["/", "/cv", "/personal-projects", "/robots.txt", "/sitemap.xml"];

let emittedStaticRoutes: string[] = [];
let emittedDynamicRoutes: string[] = [];
let robotsText = "";
let sitemapText = "";

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

When("the portfolio build output is inspected", async () => {
  const appRoot = resolve(process.cwd(), "../wahidyankf-www");
  const prerenderManifest = JSON.parse(
    readFileSync(resolve(appRoot, ".next/prerender-manifest.json"), "utf8"),
  ) as { routes: Record<string, unknown> };
  const routesManifest = JSON.parse(readFileSync(resolve(appRoot, ".next/routes-manifest.json"), "utf8")) as {
    dynamicRoutes: Array<{ page: string }>;
  };

  emittedStaticRoutes = Object.keys(prerenderManifest.routes);
  emittedDynamicRoutes = routesManifest.dynamicRoutes.map(({ page }) => page);
});

Then("the portfolio route table contains no dynamic route", async () => {
  expect(emittedDynamicRoutes).toEqual([]);
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Public portfolio routes are emitted as static build routes
Then("the static route table contains every public portfolio route", async () => {
  expect(emittedStaticRoutes).toEqual(expect.arrayContaining(publicPortfolioRoutes));
});

When("a crawler requests the robots and sitemap routes", async ({ page }) => {
  const [robotsResponse, sitemapResponse] = await Promise.all([
    page.request.get("/robots.txt"),
    page.request.get("/sitemap.xml"),
  ]);

  expect(robotsResponse.status()).toBe(200);
  expect(sitemapResponse.status()).toBe(200);
  [robotsText, sitemapText] = await Promise.all([robotsResponse.text(), sitemapResponse.text()]);
});

Then("robots permits crawling and names the canonical sitemap", async () => {
  expect(robotsText).toContain("User-Agent: *");
  expect(robotsText).toContain("Allow: /");
  expect(robotsText).toContain("Sitemap: https://www.wahidyankf.com/sitemap.xml");
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Crawlers receive discovery directives for every public route
Then("the sitemap lists every public portfolio route", async () => {
  for (const route of publicPortfolioRoutes.slice(0, 3)) {
    expect(sitemapText).toContain(`https://www.wahidyankf.com${route === "/" ? "" : route}`);
  }
});
