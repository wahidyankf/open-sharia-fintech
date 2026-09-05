import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { createActor, type Actor } from "xstate";
import { appMachine } from "@/contexts/app-shell/presentation/app-machine";
import { refreshAppRoute, resolveAppRoute, type AppRouteResult } from "@/contexts/routing/application";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/apps/organiclever/app-web/behaviours/app-shell/navigation.feature"),
);

function makeOverlayActor() {
  return createActor(appMachine, { input: { initialDarkMode: false } }).start();
}

describeFeature(feature, ({ Scenario, ScenarioOutline }) => {
  let route: AppRouteResult;
  let overlayActor: Actor<typeof appMachine>;

  Scenario("Default tab is Home on first load", ({ When, Then, And }) => {
    When("the app is freshly loaded", () => {
      const redirect = resolveAppRoute("GET", "/app");
      route = resolveAppRoute("GET", redirect.location ?? "/app");
    });
    Then("the Home tab is active", () => expect(route.activeTab).toBe("home"));
    And("the app shell is visible", () => expect(route).toMatchObject({ status: 200, screen: "Home" }));
  });

  Scenario("Navigate to History tab", ({ Given, When, Then }) => {
    Given("the app shell is visible", () => {
      route = resolveAppRoute("GET", "/app/home");
    });
    When("the user taps the History tab", () => {
      route = resolveAppRoute("GET", "/app/history");
    });
    Then("the History tab is active", () => expect(route.activeTab).toBe("history"));
  });

  Scenario("Navigate to Progress tab", ({ Given, When, Then }) => {
    Given("the app shell is visible", () => {
      route = resolveAppRoute("GET", "/app/home");
    });
    When("the user taps the Progress tab", () => {
      route = resolveAppRoute("GET", "/app/progress");
    });
    Then("the Progress tab is active", () => expect(route.activeTab).toBe("progress"));
  });

  Scenario("Navigate to Settings tab", ({ Given, When, Then }) => {
    Given("the app shell is visible", () => {
      route = resolveAppRoute("GET", "/app/home");
    });
    When("the user taps the Settings tab", () => {
      route = resolveAppRoute("GET", "/app/settings");
    });
    Then("the Settings tab is active", () => expect(route.activeTab).toBe("settings"));
  });

  Scenario("Open and close Add Entry sheet", ({ Given, When, Then, And }) => {
    Given("the app shell is visible", () => {
      overlayActor = makeOverlayActor();
    });
    When("the user taps the FAB button", () => overlayActor.send({ type: "OPEN_ADD_ENTRY" }));
    Then("the Add Entry sheet is open", () => expect(overlayActor.getSnapshot().value).toBe("addEntry"));
    And("the user closes the Add Entry sheet", () => overlayActor.send({ type: "CLOSE_ADD_ENTRY" }));
    And("the Add Entry sheet is closed", () => expect(overlayActor.getSnapshot().value).toBe("none"));
  });

  ScenarioOutline("URL persists across page refresh on each tab", ({ Given, When, Then, And }, examples) => {
    const refreshPath = String(examples["path"] ?? "");
    const expectedScreen = String(examples["screen"] ?? "");
    Given('the user is on "<path>"', () => {
      route = resolveAppRoute("GET", refreshPath);
    });
    When("the user refreshes the page", () => {
      route = refreshAppRoute(route.path);
    });
    Then('the URL is still "<path>"', () => expect(route.path).toBe(refreshPath));
    And('the "<screen>" screen is visible', () => expect(route.screen).toBe(expectedScreen));
  });
});
