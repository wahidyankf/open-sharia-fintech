import { readFileSync } from "node:fs";
import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";

const configSource = readFileSync(path.resolve(process.cwd(), "next.config.ts"), "utf8");
const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviors/frontend/i18n/locale-redirects.feature"),
);

function expectPermanentRedirect(source: string, destination: string) {
  if (source === "/") {
    expect(configSource).toContain(`{ source: "${source}", destination: "${destination}", permanent: true }`);
    return;
  }

  const sourceLocale = source.split("/")[1];
  const destinationLocale = destination.split("/")[1];

  expect(sourceLocale).toMatch(/^[A-Z]{2}$/);
  expect(destinationLocale).toMatch(/^[a-z]{2}$/);
  expect(configSource).toContain(
    `{ source: "/${sourceLocale}/:path*", destination: "/${destinationLocale}/:path*", permanent: true }`,
  );
}

describeFeature(feature, ({ Background, Scenario, ScenarioOutline }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      expect(configSource).toContain("const localeEntryRedirects");
      expect(configSource).toMatch(/experimental:\s*\{[\s\S]*?caseSensitiveRoutes:\s*true,/);
    });
  });

  Scenario("The root URL enters the default locale", ({ Given, When, Then }) => {
    Given("a visitor requests the root URL", () => {
      expect(configSource).toContain('source: "/"');
    });

    When("locale redirects are applied", () => {
      expect(configSource).toContain("...localeEntryRedirects");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/i18n/locale-redirects.feature:The root URL enters the default locale
    Then('the visitor reaches the default locale at "/en"', () => {
      expectPermanentRedirect("/", "/en");
    });
  });

  ScenarioOutline("Uppercase locale URLs redirect to lowercase canonical URLs", ({ Given, When, Then }, variables) => {
    const source = String(variables.source_url);
    const destination = String(variables.destination_url);

    Given('a visitor requests the uppercase locale URL "<source_url>"', () => {
      expect(source).toMatch(/^\/[A-Z]{2}(?:\/|$)/);
    });

    When("locale redirects are applied", () => {
      expect(configSource).toContain("...localeEntryRedirects");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/i18n/locale-redirects.feature:Uppercase locale URLs redirect to lowercase canonical URLs
    Then('the visitor is permanently redirected to "<destination_url>"', () => {
      expectPermanentRedirect(source, destination);
    });
  });
});
