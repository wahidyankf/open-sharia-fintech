import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Then } = createBdd();

// ---------------------------------------------------------------------------
// Landing homepage — hero assertions
//
// The hero `<section>` contains the page's single H1 (heroHeading) and an
// intro paragraph (heroIntro).  We assert visibility scoped to the hero region
// so we avoid collisions with any same-text occurrences elsewhere on the page.
// ---------------------------------------------------------------------------

Then("the hero heading should be visible on the landing page", async ({ page }) => {
  // The hero renders the single H1 on the page.  Wait for networkidle so
  // the Next.js RSC payload has settled before asserting.
  await page.waitForLoadState("networkidle");
  const h1 = page.getByRole("heading", { level: 1 });
  await expect(h1).toBeVisible();
});

Then("the hero intro should be visible on the landing page", async ({ page }) => {
  // The intro paragraph sits directly beneath the H1 inside the hero <section>.
  // Scope to the first <section> (the hero) to avoid collisions with any later
  // section intro text.
  await page.waitForLoadState("networkidle");
  // The hero is the first <section> on the page.
  const heroSection = page.locator("section").first();
  const intro = heroSection.locator("p").first();
  await expect(intro).toBeVisible();
});

// ---------------------------------------------------------------------------
// Landing homepage — section grid assertions
//
// SectionCard renders as a full-block <a> link whose href contains /c/{slug}.
// We scope to <main> so we do not accidentally match same-slug links that may
// appear in header/footer nav (those link to /c, not /c/{slug}).
// ---------------------------------------------------------------------------

Then("the landing section grid should include a card linking to {string}", async ({ page }, href: string) => {
  const main = page.getByRole("main");
  const card = main.locator(`a[href="${href}"]`);
  await expect(card).toBeVisible();
});

// ---------------------------------------------------------------------------
// Landing homepage — tools teaser assertions
//
// The ToolsTeaser always links to /{locale}/tools/cost-of-living-calculator.
// Scoping to <main> guards against any same-href link in footer nav.
// ---------------------------------------------------------------------------

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:Landing homepage renders hero, sections, and tools teaser in English
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/ia-navigation-revamp.feature:Landing homepage renders hero, sections, and tools teaser in Indonesian
Then("the tools teaser should link to {string}", async ({ page }, href: string) => {
  const main = page.getByRole("main");
  const teaserLink = main.locator(`a[href="${href}"]`);
  await expect(teaserLink).toBeVisible();
});
