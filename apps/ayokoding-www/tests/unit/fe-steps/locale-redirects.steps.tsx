import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";

import { localeEntryRedirects, resolveLocaleEntryRedirect } from "@/redirects/locale-entry";
const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviours/frontend/i18n/locale-redirects.feature"),
);

describeFeature(feature, ({ Background, Scenario, ScenarioOutline }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      expect(localeEntryRedirects.length).toBeGreaterThan(0);
    });
  });

  Scenario("The root URL enters the default locale", ({ Given, When, Then }) => {
    Given("a visitor requests the root URL", () => {
      expect(localeEntryRedirects).toContainEqual({ source: "/", destination: "/en", permanent: true });
    });

    When("locale redirects are applied", () => {
      expect(resolveLocaleEntryRedirect("/")).toBe("/en");
    });

    Then('the visitor reaches the default locale at "/en"', () => {
      expect(resolveLocaleEntryRedirect("/")).toBe("/en");
    });
  });

  ScenarioOutline("Uppercase locale URLs redirect to lowercase canonical URLs", ({ Given, When, Then }, variables) => {
    const source = String(variables.source_url);
    const destination = String(variables.destination_url);

    Given('a visitor requests the uppercase locale URL "<source_url>"', () => {
      expect(source).toMatch(/^\/[A-Z]{2}(?:\/|$)/);
    });

    When("locale redirects are applied", () => {
      expect(resolveLocaleEntryRedirect(source)).toBe(destination);
    });

    Then('the visitor is permanently redirected to "<destination_url>"', () => {
      expect(resolveLocaleEntryRedirect(source)).toBe(destination);
    });
  });
});
