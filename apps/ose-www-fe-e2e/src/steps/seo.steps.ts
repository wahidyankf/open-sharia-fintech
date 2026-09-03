import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { backendState } from "./backend-helpers";

const { When, Then } = createBdd();

When("the sitemap is generated", async ({ request }) => {
  const response = await request.get("/sitemap.xml");
  expect(response.ok()).toBeTruthy();
  backendState.sitemapBody = await response.text();
});

Then("the sitemap contains a URL for the landing page", async () => {
  const body = backendState.sitemapBody as string;
  expect(body).toContain("<loc>");
});

Then("the sitemap contains a URL for the about page", async () => {
  const body = backendState.sitemapBody as string;
  expect(body).toContain("/about");
});

// @covers specs/apps/ose/www/behaviors/backend/seo/seo.feature:Sitemap contains all public pages
Then("the sitemap contains URLs for all update pages", async () => {
  const body = backendState.sitemapBody as string;
  expect(body).toContain("/updates/");
});

When("the robots.txt is generated", async ({ request }) => {
  const response = await request.get("/robots.txt");
  expect(response.ok()).toBeTruthy();
  backendState.robotsBody = await response.text();
});

Then("it allows all user agents", async () => {
  const body = backendState.robotsBody as string;
  expect(body.toLowerCase()).toContain("user-agent");
});

// @covers specs/apps/ose/www/behaviors/backend/seo/seo.feature:Robots.txt allows all crawlers
Then("it references the sitemap URL", async () => {
  const body = backendState.robotsBody as string;
  expect(body.toLowerCase()).toContain("sitemap");
});
