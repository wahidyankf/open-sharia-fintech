import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { vi, expect } from "vitest";

import { AppHeader } from "../../../../src/components/app-header/app-header";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/app-header/app-header.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders title", ({ When, Then }) => {
    let header: HTMLElement;

    When('I render an AppHeader with title "Workouts"', () => {
      cleanup();
      render(<AppHeader title="Workouts" />);
      header = screen.getByText("Workouts");
    });

    Then('the heading "Workouts" should be visible', () => {
      expect(header.textContent).toBe("Workouts");
    });
  });

  Scenario("Back button appears when onBack provided", ({ When, Then }) => {
    let backButton: HTMLElement;

    When('I render an AppHeader with title "Details" and an onBack handler', () => {
      cleanup();
      render(<AppHeader title="Details" onBack={vi.fn()} />);
      backButton = screen.getByRole("button", { name: /go back/i });
    });

    Then('a button with aria-label "Go back" should be visible', () => {
      expect(backButton.getAttribute("aria-label")).toBe("Go back");
    });
  });

  Scenario("Back button absent when onBack not provided", ({ When, Then }) => {
    let backButton: HTMLElement | null;

    When('I render an AppHeader with title "Home" without onBack', () => {
      cleanup();
      render(<AppHeader title="Home" />);
      backButton = screen.queryByRole("button", { name: /go back/i });
    });

    Then('no button with aria-label "Go back" should be present', () => {
      expect(backButton).toBeNull();
    });
  });

  Scenario("Back button click triggers onBack", ({ Given, When, Then }) => {
    const onBackMock = vi.fn();

    Given('I render an AppHeader with title "Details" and an onBack handler', () => {
      cleanup();
      render(<AppHeader title="Details" onBack={onBackMock} />);
      expect(screen.getByRole("button", { name: /go back/i })).toBeDefined();
    });

    When("the user clicks the back button", () => {
      cleanup();
      render(<AppHeader title="Details" onBack={onBackMock} />);
      fireEvent.click(screen.getByRole("button", { name: /go back/i }));
    });

    Then("onBack should be called", () => {
      expect(onBackMock).toHaveBeenCalled();
    });
  });

  Scenario("Renders subtitle when provided", ({ When, Then }) => {
    let subtitle: HTMLElement;

    When('I render an AppHeader with title "Workouts" and subtitle "Today"', () => {
      cleanup();
      render(<AppHeader title="Workouts" subtitle="Today" />);
      subtitle = screen.getByText("Today");
    });

    Then('the text "Today" should be visible', () => {
      expect(subtitle.textContent).toBe("Today");
    });
  });
});
