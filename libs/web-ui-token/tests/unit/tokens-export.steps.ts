import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import * as webUiToken from "../../src/index";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../specs/libs/web-ui-token/behaviors/tokens/tokens-export.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("The package exports every structural token module", ({ Given, When, Then, And }) => {
    Given("the web-ui-token package", () => {});

    When('I import from "@open-sharia-enterprise/web-ui-token"', () => {});

    // @covers specs/libs/web-ui-token/behaviors/tokens/tokens-export.feature:The package exports every structural token module
    Then('"colorTokens" should be exported', () => {
      expect(webUiToken.colorTokens).toBeDefined();
    });

    And('"radius" should be exported', () => {
      expect(webUiToken.radius).toBeDefined();
    });

    And('"spacing" should be exported', () => {
      expect(webUiToken.spacing).toBeDefined();
    });

    And('"typography" should be exported', () => {
      expect(webUiToken.typography).toBeDefined();
    });
  });
});
