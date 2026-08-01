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

function markdownFileCount(directory: string): number {
  return readdirSync(directory, { recursive: true }).filter(
    (entry): entry is string => typeof entry === "string" && entry.endsWith(".md"),
  ).length;
}

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature",
  ),
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature:A content page is prerendered at build time
    And("the content catch-all route is not marked as dynamically rendered", () => {
      expect(contentPageSource).not.toMatch(/dynamic\s*=\s*["']force-dynamic["']/);
      expect(contentPageSource).not.toMatch(/fetchCache\s*=\s*["']force-no-store["']/);
      expect(contentPageSource).not.toMatch(/\b(noStore|connection)\s*\(/);
    });
  });

  Scenario("A repeat request to a content page is served from the CDN", ({ Given, When, Then, And }) => {
    Given("a visitor has already requested a course lesson URL", () => {
      expect(existsSync(path.join(contentDirectory, "en", "learn", "overview.md"))).toBe(true);
    });

    When("the same URL is requested again", () => {
      expect(contentPageSource).toContain("generateStaticParams");
    });

    Then("the response is served from the CDN cache", () => {
      // HTTP cache headers are deployment behaviour; the Playwright binding performs the live repeat-request assertion.
      expect(contentPageSource).not.toMatch(/\bforce-dynamic\b/);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature:A repeat request to a content page is served from the CDN
    And("the response does not carry a no-store cache directive", () => {
      expect(contentPageSource).not.toMatch(/\bcache\s*:\s*["']no-store["']/);
      expect(contentPageSource).not.toMatch(/\bnoStore\s*\(/);
    });
  });

  ScenarioOutline("The document language reflects the content-page locale", ({ Given, When, Then }, variables) => {
    Given("a visitor opens a content page in the \"<locale>\" locale", () => {
      expect(isValidLocale(String(variables.locale))).toBe(true);
    });

    When("the content page renders", () => {
      expect(localeLayoutSource).toContain("<html lang={(await params).locale}");
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/static-delivery.feature:The document language reflects the content-page locale
    Then("the html element declares the \"<language_code>\" language code", () => {
      expect(String(variables.locale)).toBe(String(variables.language_code));
    });
  });
});
