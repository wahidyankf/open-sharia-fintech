import { createBdd } from "playwright-bdd";
import { expect, type Locator } from "@playwright/test";
import { getResilient } from "../support/resilient-request";

const { Given, When, Then } = createBdd();
let internalHrefsBySurface: Record<"sidebar" | "breadcrumb" | "prevNext" | "search", string[]>;
let internalLinkStatuses: Array<{ href: string; status: number }> = [];

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
  await page.goto("/en/learn/courses/just-enough-python/learning/beginner");
  await page.waitForLoadState("networkidle");
  await expect(page.getByRole("navigation", { name: "Sidebar navigation" })).toBeAttached();
  await expect(page.getByRole("navigation", { name: "Breadcrumb" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Page navigation" })).toBeVisible();
  await page
    .getByRole("button", { name: /search/iu })
    .first()
    .click();
  const searchDialog = page.getByRole("dialog");
  await searchDialog.getByRole("combobox").fill("programming");
  await expect(searchDialog.getByRole("option").first()).toBeVisible({ timeout: 15000 });
});

When("their hrefs are computed via the central content URL helper", async ({ page }) => {
  const hrefs = async (locator: Locator): Promise<string[]> =>
    (await locator.evaluateAll((links) => links.map((link) => link.getAttribute("href") ?? ""))).filter((href) =>
      /^\/(en|id)\/.+/u.test(href),
    );
  const searchSlugs = await page
    .getByRole("dialog")
    .getByRole("option")
    .evaluateAll((options) => options.map((option) => option.getAttribute("data-result-slug") ?? ""));
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();

  internalHrefsBySurface = {
    sidebar: await hrefs(page.getByRole("navigation", { name: "Sidebar navigation" }).locator("a[href]")),
    breadcrumb: await hrefs(page.getByRole("navigation", { name: "Breadcrumb" }).locator("a[href]")),
    prevNext: await hrefs(page.getByRole("navigation", { name: "Page navigation" }).locator("a[href]")),
    search: searchSlugs.filter(Boolean).map((slug) => `/en/${slug}`),
  };

  const uniqueHrefs = [...new Set(Object.values(internalHrefsBySurface).flat())];
  internalLinkStatuses = await Promise.all(
    uniqueHrefs.map(async (href) => ({
      href,
      status: (await getResilient(page, href, { maxRedirects: 0, timeout: 30000 })).status(),
    })),
  );
});

Then("every content link resolves directly to its bare URL with status 200", async () => {
  for (const [surface, hrefs] of Object.entries(internalHrefsBySurface)) {
    expect(hrefs.length, `${surface} must contribute at least one content destination`).toBeGreaterThan(0);
    expect(hrefs.every((href) => /^\/(en|id)\/(?!c\/).+/u.test(href))).toBe(true);
  }
  for (const { href, status } of internalLinkStatuses) {
    expect(status, `${href} should resolve directly with HTTP 200`).toBe(200);
  }
});

Then("no internal content link resolves through a 308 redirect", async () => {
  expect(internalLinkStatuses.every(({ status }) => status !== 308)).toBe(true);
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

Then("the language alternates include en and x-default", async ({ page }) => {
  const enAlternate = await page.locator("link[hreflang='en']").getAttribute("href");
  const xDefaultAlternate = await page.locator("link[hreflang='x-default']").getAttribute("href");
  expect(enAlternate).toBeTruthy();
  expect(xDefaultAlternate).toBeTruthy();
});
