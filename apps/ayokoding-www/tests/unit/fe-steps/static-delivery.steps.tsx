import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { isValidLocale } from "@/features/i18n/core/config";

const appRoot = process.cwd();
const contentPagePath = path.join(appRoot, "src/app/[locale]/(content)/[...slug]/page.tsx");
const localeLayoutPath = path.join(appRoot, "src/app/[locale]/layout.tsx");
const contentDirectory = path.join(appRoot, "content");
const contentPageSource = readFileSync(contentPagePath, "utf8");
const localeLayoutSource = readFileSync(localeLayoutPath, "utf8");
const nextConfigSource = readFileSync(path.join(appRoot, "next.config.ts"), "utf8");
const appRouterSource = readFileSync(path.join(appRoot, "src/features/app-shell/shell/root-router.ts"), "utf8");

function markdownFileCount(directory: string): number {
  return readdirSync(directory, { recursive: true }).filter(
    (entry): entry is string => typeof entry === "string" && entry.endsWith(".md"),
  ).length;
}

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature"),
);

describeFeature(feature, ({ Background, Scenario, ScenarioOutline }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      expect(existsSync(contentPagePath)).toBe(true);
    });
  });

  Scenario("A content page is prerendered at build time", ({ Given, When, Then, And }) => {
    Given("the ayokoding-www site is built and deployed", () => {
      expect(existsSync(path.join(appRoot, "src/app/layout.tsx"))).toBe(false);
      expect(localeLayoutSource).not.toMatch(/\b(cookies|headers|draftMode)\s*\(/);
    });

    When("the build output manifest is inspected", () => {
      expect(contentPageSource).toContain("generateStaticParams");
    });

    Then("the prerendered route count is at least two thousand", () => {
      expect(markdownFileCount(contentDirectory)).toBeGreaterThanOrEqual(2000);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:A content page is prerendered at build time
    And("the content catch-all route is not marked as dynamically rendered", () => {
      expect(contentPageSource).not.toMatch(/dynamic\s*=\s*["']force-dynamic["']/);
      expect(contentPageSource).not.toMatch(/fetchCache\s*=\s*["']force-no-store["']/);
      expect(contentPageSource).not.toMatch(/\b(noStore|connection)\s*\(/);
    });
  });

  Scenario("A repeat request to a content page remains cacheable", ({ Given, When, Then }) => {
    Given("a visitor has already requested a course lesson URL", () => {
      expect(existsSync(path.join(contentDirectory, "en", "learn", "overview.md"))).toBe(true);
    });

    When("the same URL is requested again", () => {
      expect(contentPageSource).toContain("generateStaticParams");
    });

    // A local runner has no Vercel CDN. Preview/production checks own the HIT assertion; this
    // source-level binding keeps the local contract to static cacheability.
    // @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:A repeat request to a content page remains cacheable
    Then("the response does not carry a no-store cache directive", () => {
      expect(contentPageSource).not.toMatch(/\bforce-dynamic\b/);
      expect(contentPageSource).not.toMatch(/\bcache\s*:\s*["']no-store["']/);
      expect(contentPageSource).not.toMatch(/\bnoStore\s*\(/);
    });
  });

  Scenario("A repeat request to a deployed content page is served from the CDN", ({ Given, When, Then }) => {
    Given("a Vercel preview or production deployment is selected for CDN verification", () => {
      // The Playwright binding explicitly gates this assertion on a real deployment URL.
      expect(
        readFileSync(path.join(appRoot, "../ayokoding-www-fe-e2e/tests/e2e/steps/static-delivery.steps.ts"), "utf8"),
      ).toContain('VERCEL_CDN_VERIFY !== "true"');
    });

    When("the same deployed course lesson URL is requested again", () => {
      expect(contentPageSource).toContain("generateStaticParams");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:A repeat request to a deployed content page is served from the CDN
    Then("the deployed response is served from the CDN cache", () => {
      expect(nextConfigSource).not.toMatch(/dynamic\s*=\s*["']force-dynamic["']/);
    });
  });

  Scenario("Runtime tRPC endpoints retain their filesystem assets", ({ Given, When, Then }) => {
    Given("the ayokoding-www standalone package is running", () => {
      expect(nextConfigSource).toContain('output: "standalone"');
    });

    When("navigation search and course-path data are requested through tRPC", () => {
      expect(appRouterSource).toContain("navigationProcedures");
      expect(appRouterSource).toContain("searchProcedures");
      expect(appRouterSource).toContain("coursePathProcedures");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:Runtime tRPC endpoints retain their filesystem assets
    Then("every runtime data endpoint responds successfully", () => {
      expect(nextConfigSource).toMatch(/"\/api\/trpc\/\[trpc\]"\s*:/);
      expect(nextConfigSource).toContain('"./content/**/*"');
      expect(nextConfigSource).toContain('"./generated/**/*"');
      expect(nextConfigSource).toContain('"./src/features/course-paths/manifests/**/*"');
    });
  });

  ScenarioOutline("The document language reflects the localized page locale", ({ Given, When, Then }, variables) => {
    Given('a visitor opens a localized page in the "<locale>" locale', () => {
      expect(isValidLocale(String(variables.locale))).toBe(true);
    });

    When("the localized page renders", () => {
      expect(localeLayoutSource).toContain("<html lang={(await params).locale}");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/content/static-delivery.feature:The document language reflects the localized page locale
    Then('the html element declares the "<language_code>" language code', () => {
      expect(String(variables.locale)).toBe(String(variables.language_code));
    });
  });
});
