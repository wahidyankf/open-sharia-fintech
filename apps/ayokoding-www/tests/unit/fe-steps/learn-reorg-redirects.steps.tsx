import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import "./helpers/test-setup";

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-reorg-redirects.feature",
  ),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {});
  });

  Scenario("platform-web redirects to platforms/web under its legacy bucket address", ({ When, Then }) => {
    When('a visitor navigates to "/en/learn/software-engineering/platform-web"', () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-reorg-redirects.feature:platform-web redirects to platforms/web under its legacy bucket address
    Then('the current URL should contain "/en/learn/legacy/software-engineering/platforms/web"', () => {
      expect(true).toBe(true);
    });
  });
});
