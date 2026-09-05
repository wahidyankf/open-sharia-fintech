import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { vi, expect } from "vitest";

import { Sheet } from "../../../../src/components/sheet/sheet";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/sheet/sheet.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Title renders", ({ When, Then }) => {
    let title: HTMLElement;

    When('I render a Sheet with title "Settings"', () => {
      cleanup();
      render(<Sheet title="Settings" onClose={vi.fn()} />);
      title = screen.getByText("Settings");
    });

    Then('the heading "Settings" should be visible', () => {
      expect(title.textContent).toBe("Settings");
    });
  });

  Scenario("Close button closes sheet", ({ Given, When, Then }) => {
    const onCloseMock = vi.fn();

    Given('I render a Sheet with title "Settings" and an onClose handler', () => {
      cleanup();
      render(<Sheet title="Settings" onClose={onCloseMock} />);
      expect(screen.getByRole("button", { name: /close/i })).toBeDefined();
    });

    When("the user clicks the close button", () => {
      cleanup();
      render(<Sheet title="Settings" onClose={onCloseMock} />);
      fireEvent.click(screen.getByRole("button", { name: /close/i }));
    });

    Then("onClose should be called", () => {
      expect(onCloseMock).toHaveBeenCalled();
    });
  });

  Scenario("Has accessible title", ({ When, Then }) => {
    let dialog: HTMLElement;

    When('I render a Sheet with title "My Sheet"', () => {
      cleanup();
      render(<Sheet title="My Sheet" onClose={vi.fn()} />);
      dialog = screen.getByRole("dialog", { name: "My Sheet" });
    });

    Then('the dialog should have accessible label "My Sheet"', () => {
      expect(dialog.getAttribute("aria-labelledby")).not.toBeNull();
    });
  });
});
