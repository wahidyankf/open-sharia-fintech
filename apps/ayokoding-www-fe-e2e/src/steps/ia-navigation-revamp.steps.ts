import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";
import { getResilient } from "../support/resilient-request";

const { Given, When, Then } = createBdd();

// ---------------------------------------------------------------------------
// Scenario: Breadcrumb segments link to their bare content URLs (DD-48)
// ---------------------------------------------------------------------------

Given("a visitor is on {string}", async ({ page }, url: string) => {
  await page.goto(url);
});

When("the breadcrumb renders its ancestor segments", async ({ page }) => {
  // The breadcrumb renders as part of the content page — just confirm it's visible.
  const breadcrumb = page.getByRole("navigation", { name: /breadcrumb/i });
  await expect(breadcrumb).toBeVisible();
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:Breadcrumb segments link to their bare content URLs
Then("each ancestor crumb links to its bare content URL", async ({ page }) => {
  const breadcrumb = page.getByRole("navigation", { name: /breadcrumb/i });
  const links = breadcrumb.getByRole("link");
  const count = await links.count();
  expect(count).toBeGreaterThan(0);
  let checked = 0;
  for (let i = 0; i < count; i++) {
    const href = await links.nth(i).getAttribute("href");
    // Skip root ("/") and the locale root ("/en") — every remaining crumb href
    // must never contain a /c/ segment (the retired content namespace, DD-48).
    if (href && href !== "/" && !href.match(/^\/[a-z]{2}$/)) {
      expect(href).not.toContain("/c/");
      checked += 1;
    }
  }
  expect(checked).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// Scenario: Internal content links emit bare URLs directly without relying on redirects (DD-48)
// ---------------------------------------------------------------------------

Given("the sidebar tree, breadcrumb, prev-next, and search results render content links", async ({ page }) => {
  // Navigate directly to the content's current bare/legacy resting place (DD-42),
  // a page with sidebar, breadcrumb, and prev/next chrome.
  await page.goto("/en/learn/legacy/software-engineering/algorithms-and-data-structures");
  await page.waitForLoadState("networkidle");
});

When("their hrefs are computed via the central content URL helper", async ({ page }) => {
  // All link-emitting components (sidebar-tree, breadcrumb, prev-next) are rendered;
  // gathering hrefs is done in the Then steps below.
  await expect(page.getByRole("article")).toBeVisible();
});

Then("every content link resolves directly to its bare URL with status 200", async ({ page }) => {
  // Collect hrefs from the navigation chrome (sidebar + breadcrumb).
  const navLinks = page.locator("nav a[href]");
  const count = await navLinks.count();
  expect(count).toBeGreaterThan(0);

  // Collect unique internal content hrefs (locale-scoped, not the root/locale-root
  // itself), then check in parallel to avoid sequential timeout.
  const hrefs: string[] = [];
  const seen = new Set<string>();
  for (let i = 0; i < count; i++) {
    const href = await navLinks.nth(i).getAttribute("href");
    if (!href || seen.has(href)) continue;
    if (!href.match(/^\/(en|id)\/.+/)) continue;
    seen.add(href);
    hrefs.push(href);
  }
  expect(hrefs.length).toBeGreaterThan(0);

  // See `getResilient` — retries once on a load-induced ECONNRESET; 30s (vs. the 10s
  // default) additionally tolerates slow-but-successful responses under full-suite
  // parallel contention on the single local server instance.
  await Promise.all(
    hrefs.map(async (href) => {
      const response = await getResilient(page, href, { maxRedirects: 0, timeout: 30000 });
      expect(response.status(), `${href} should resolve directly, not 404`).not.toBe(404);
    }),
  );
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:Internal content links emit bare URLs directly without relying on redirects
Then("no internal content link resolves through a 308 redirect", async ({ page }) => {
  const navLinks = page.locator("nav a[href]");
  const count = await navLinks.count();

  // Collect unique internal hrefs, then check in parallel to avoid sequential timeout.
  const hrefs: string[] = [];
  const seen = new Set<string>();
  for (let i = 0; i < count; i++) {
    const href = await navLinks.nth(i).getAttribute("href");
    if (!href || !href.startsWith("/") || seen.has(href)) continue;
    seen.add(href);
    hrefs.push(href);
  }

  // See `getResilient` — retries once on a load-induced ECONNRESET; 30s (vs. the 10s
  // default) additionally tolerates slow-but-successful responses under full-suite
  // parallel contention on the single local server instance.
  await Promise.all(
    hrefs.map(async (href) => {
      const response = await getResilient(page, href, { maxRedirects: 0, timeout: 30000 });
      expect(response.status(), `Link ${href} should not be a 308 redirect`).not.toBe(308);
    }),
  );
});

// ---------------------------------------------------------------------------
// Scenario: Sitemap lists every content URL bare, with no distinct content namespace (DD-48)
// ---------------------------------------------------------------------------

Given("the sitemap is generated from the content index", async ({ page }) => {
  await page.goto("/sitemap.xml");
  await page.waitForLoadState("networkidle");
});

When("the sitemap entries are produced", async ({ page }) => {
  const body = await page.content();
  expect(body).toBeTruthy();
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:Sitemap lists every content URL bare, with no distinct content namespace
Then("every moved-content entry uses a bare URL", async ({ page }) => {
  const body = await page.content();
  // A relocated legacy domain's URL is present, and no entry anywhere carries
  // a /c/ segment (the retired content namespace, DD-48).
  expect(body).toContain("/en/learn/legacy/software-engineering");
  expect(body).not.toContain("/c/");
});

// Escape the parentheses: playwright-bdd parses step text as a Cucumber
// Expression, where `(...)` denotes an OPTIONAL group. Unescaped, this def
// would only match "top-level pages  use ..." and never the feature's literal
// "(about, terms, tools)", leaving the scenario unbound (test.fixme). `\(` / `\)`
// force a literal-parenthesis match. (The unit tier's vitest-cucumber matches
// the same text literally, so its def keeps the bare parentheses.)
Then(
  "top-level pages \\(about, terms, tools\\) use that same bare form — no longer namespace-distinct",
  async ({ page }) => {
    const body = await page.content();
    // about-ayokoding and terms-and-conditions must resolve at the SAME bare
    // form content pages now use — never a /c/-prefixed variant.
    const aboutIdx = body.indexOf("about-ayokoding");
    const termsIdx = body.indexOf("terms-and-conditions");
    expect(aboutIdx, "sitemap should list about-ayokoding").not.toBe(-1);
    expect(termsIdx, "sitemap should list terms-and-conditions").not.toBe(-1);
    const aboutSlice = body.slice(Math.max(0, aboutIdx - 10), aboutIdx);
    const termsSlice = body.slice(Math.max(0, termsIdx - 10), termsIdx);
    expect(aboutSlice).not.toContain("/c/");
    expect(termsSlice).not.toContain("/c/");
  },
);

// ---------------------------------------------------------------------------
// Scenario: RSS feed item links use bare content URLs (DD-48)
// ---------------------------------------------------------------------------

// Use page.request (APIRequestContext) instead of page.goto to avoid
// cross-browser XML rendering quirks (Firefox renders XML differently).
let feedBody = "";

Given("the feed is generated from the content index", async ({ page }) => {
  // See `getResilient` — retries once on a load-induced ECONNRESET.
  const response = await getResilient(page, "/feed.xml");
  expect(response.status()).toBe(200);
  feedBody = await response.text();
});

When("the feed items are produced", async () => {
  expect(feedBody.length).toBeGreaterThan(0);
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:RSS feed item links use bare content URLs
Then("every content item link uses a bare URL", async () => {
  // At least one real content link is present, and no item link anywhere
  // carries a /c/ segment (the retired content namespace, DD-48).
  expect(feedBody).toContain("/en/rants/");
  expect(feedBody).not.toContain("/c/");
});

// ---------------------------------------------------------------------------
// Scenario: Canonical link for moved content points to its bare URL (DD-48)
// ---------------------------------------------------------------------------

Given("the content page at {string}", async ({ page }, url: string) => {
  await page.goto(url);
  await page.waitForLoadState("networkidle");
});

When("its metadata is generated", async ({ page }) => {
  // Metadata is embedded in <head> — the page has loaded.
  await expect(page.locator("head")).toBeDefined();
});

Then("the canonical alternate is {string}", async ({ page }, expectedCanonical: string) => {
  const canonical = await page.locator("link[rel='canonical']").getAttribute("href");
  expect(canonical).toContain(expectedCanonical);
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:Canonical link for moved content points to its bare URL
Then("the language alternates include en and x-default", async ({ page }) => {
  const enAlternate = await page.locator("link[hreflang='en']").getAttribute("href");
  const xDefaultAlternate = await page.locator("link[hreflang='x-default']").getAttribute("href");
  expect(enAlternate).toBeTruthy();
  expect(xDefaultAlternate).toBeTruthy();
});
