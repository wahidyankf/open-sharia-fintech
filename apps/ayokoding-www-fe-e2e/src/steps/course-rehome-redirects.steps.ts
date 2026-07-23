import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Then } = createBdd();

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:The course library the retired browse roots redirect to resolves every re-homed course
Then(
  "every course catalog entry should resolve to live content, not a drained or missing location",
  async ({ page }) => {
    await page.waitForLoadState("networkidle");
    const main = page.getByRole("main");
    // Bare href (DD-48 de-namespacing) — the /c/ content route was retired.
    const links = main.locator("a[href*='/learn/courses/']");
    const count = await links.count();
    expect(count).toBeGreaterThan(0);

    const hrefs = new Set<string>();
    for (let i = 0; i < count; i++) {
      const href = await links.nth(i).getAttribute("href");
      if (href) hrefs.add(href);
    }

    await Promise.all(
      [...hrefs].map(async (href) => {
        const response = await page.request.get(href, { timeout: 10000 });
        expect(response.status(), `Course catalog entry ${href} should not be a drained/missing location`).not.toBe(
          404,
        );
      }),
    );
  },
);

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:A course reached via its legacy course URL resolves to the single canonical course body
Then(
  "the resolved page title should equal the canonical course page title at {string}",
  async ({ page }, canonicalUrl: string) => {
    await page.waitForLoadState("networkidle");
    const legacyTitle = await page.title();
    expect(legacyTitle.length).toBeGreaterThan(0);

    await page.goto(canonicalUrl);
    await page.waitForLoadState("networkidle");
    const canonicalTitle = await page.title();

    expect(legacyTitle).toBe(canonicalTitle);
  },
);
