import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import * as webUiToken from "../../src/index";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../specs/libs/web-ui-token/behaviours/tokens/tokens-export.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("The package exports every structural token module", ({ Given, When, Then, And }) => {
    let importedPackage: typeof webUiToken | undefined;

    Given("the web-ui-token package", () => {
      expect(webUiToken).toBeTypeOf("object");
    });

    When('I import from "@open-sharia-enterprise/web-ui-token"', () => {
      importedPackage = webUiToken;
    });

    Then('"colorTokens" should be exported', () => {
      expect(importedPackage?.colorTokens).toBeDefined();
    });

    And('"radius" should be exported', () => {
      expect(importedPackage?.radius).toBeDefined();
    });

    And('"spacing" should be exported', () => {
      expect(importedPackage?.spacing).toBeDefined();
    });

    And('"typography" should be exported', () => {
      expect(importedPackage?.typography).toBeDefined();
    });
  });
});
