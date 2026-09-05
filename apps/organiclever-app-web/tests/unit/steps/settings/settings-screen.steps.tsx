import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, fireEvent, render, screen, waitFor, type RenderResult } from "@testing-library/react";
import { expect, vi } from "vitest";
import type { AppRuntime } from "@/shared/runtime";
import type { AppSettings } from "@/contexts/settings/application";

const settingsHarness = vi.hoisted(() => ({
  settings: { name: "Tester", restSeconds: 60, darkMode: false, lang: "en" } as AppSettings,
  update: vi.fn(),
}));

vi.mock("@/contexts/settings/presentation/use-settings", () => ({
  useSettings: () => ({
    state: { status: "ready", settings: settingsHarness.settings },
    update: settingsHarness.update,
  }),
}));

import { SettingsScreen } from "@/contexts/settings/presentation/components/settings-screen";

const feature = await loadFeature(
  path.resolve(
    __dirname,
    "../../../../../../specs/apps/organiclever/app-web/behaviours/settings/settings-screen.feature",
  ),
);

const runtime = { runPromise: vi.fn().mockResolvedValue(undefined) } as unknown as AppRuntime;
let rendered: RenderResult;

function renderSettings() {
  rendered = render(<SettingsScreen runtime={runtime} darkMode={false} onToggleDarkMode={vi.fn()} />);
}

describeFeature(feature, ({ Scenario, AfterEachScenario }) => {
  AfterEachScenario(() => {
    cleanup();
    settingsHarness.settings = { name: "Tester", restSeconds: 60, darkMode: false, lang: "en" };
    settingsHarness.update.mockReset().mockImplementation(async (patch: Partial<AppSettings>) => {
      settingsHarness.settings = { ...settingsHarness.settings, ...patch };
    });
  });

  Scenario("Settings screen loads user profile", ({ When, Then }) => {
    When("the settings screen is loaded", () => renderSettings());
    Then("the user name input is visible", () => {
      expect(screen.getByLabelText("Your name")).toBeVisible();
      expect(screen.getByLabelText("Your name")).toHaveValue("Tester");
    });
  });

  Scenario("Change rest setting", ({ Given, When, Then }) => {
    Given("the settings screen is loaded", () => renderSettings());
    When("the user selects 30s rest", async () => {
      fireEvent.click(screen.getByTestId("rest-chip-30"));
      await waitFor(() => expect(settingsHarness.update).toHaveBeenCalledWith({ restSeconds: 30 }));
      rendered.rerender(<SettingsScreen runtime={runtime} darkMode={false} onToggleDarkMode={vi.fn()} />);
    });
    Then("the 30s rest chip is active", () => {
      expect(screen.getByTestId("rest-chip-30")).toHaveAttribute("data-active", "true");
    });
  });

  Scenario("Saved toast appears after save", ({ Given, When, Then }) => {
    Given("the settings screen is loaded", () => renderSettings());
    When("the user saves settings", async () => {
      fireEvent.click(screen.getByTestId("rest-chip-30"));
      await waitFor(() => expect(settingsHarness.update).toHaveBeenCalled());
    });
    Then("the saved toast appears", async () => {
      expect(await screen.findByTestId("saved-toast")).toHaveTextContent("Saved");
    });
  });
});
