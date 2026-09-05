import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { resolveAppRoute, type AppRouteResult } from "@/contexts/routing/application";

const feature = await loadFeature(
  path.resolve(
    __dirname,
    "../../../../../../specs/apps/organiclever/app-web/behaviours/routing/disabled-routes.feature",
  ),
);

describeFeature(feature, ({ ScenarioOutline, Scenario }) => {
  let result: AppRouteResult;

  ScenarioOutline("Disabled routes return 404", ({ Given, When, Then }, examples) => {
    const method = String(examples["method"] ?? "");
    const routePath = String(examples["path"] ?? "");
    Given("the application is running in local-first mode", () => {
      expect(resolveAppRoute("GET", "/app/home").status).toBe(200);
    });
    When("a visitor requests <method> <path>", () => {
      result = resolveAppRoute(method, routePath);
    });
    Then("the response status is 404", () => expect(result.status).toBe(404));
  });

  Scenario("Old /app URL permanent-redirects to /app/home", ({ Given, When, Then }) => {
    Given("the application is running in local-first mode", () => {
      expect(resolveAppRoute("GET", "/app/home").status).toBe(200);
    });
    When('a visitor requests GET "/app"', () => {
      result = resolveAppRoute("GET", "/app");
    });
    Then('the response is a 308 redirect to "/app/home"', () => {
      expect(result).toMatchObject({ status: 308, location: "/app/home" });
    });
  });
});
