import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { vi, expect } from "vitest";

import { Toggle } from "../../../../src/components/toggle/toggle";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/toggle/toggle.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders in off state", ({ When, Then }) => {
    let toggle: HTMLElement;

    When("I render a Toggle with value false", () => {
      cleanup();
      render(<Toggle value={false} onChange={vi.fn()} />);
      toggle = screen.getByRole("switch");
    });

    Then('the toggle switch should have aria-checked "false"', () => {
      expect(toggle.getAttribute("aria-checked")).toBe("false");
    });
  });

  Scenario("Renders in on state", ({ When, Then }) => {
    let toggle: HTMLElement;

    When("I render a Toggle with value true", () => {
      cleanup();
      render(<Toggle value={true} onChange={vi.fn()} />);
      toggle = screen.getByRole("switch");
    });

    Then('the toggle switch should have aria-checked "true"', () => {
      expect(toggle.getAttribute("aria-checked")).toBe("true");
    });
  });

  Scenario("Click triggers onChange", ({ Given, When, Then }) => {
    const onChangeMock = vi.fn();

    Given("I render a Toggle with value false", () => {
      cleanup();
      render(<Toggle value={false} onChange={onChangeMock} />);
      expect(screen.getByRole("switch").getAttribute("aria-checked")).toBe("false");
    });

    When("the user clicks the toggle", () => {
      cleanup();
      render(<Toggle value={false} onChange={onChangeMock} />);
      fireEvent.click(screen.getByRole("switch"));
    });

    Then("onChange should be called with true", () => {
      expect(onChangeMock).toHaveBeenCalledWith(true);
    });
  });

  Scenario("Disabled toggle does not trigger onChange", ({ Given, When, Then }) => {
    const onChangeMock = vi.fn();

    Given("I render a Toggle with value false and disabled", () => {
      cleanup();
      render(<Toggle value={false} onChange={onChangeMock} disabled />);
      expect(screen.getByRole("switch", { hidden: true }).hasAttribute("disabled")).toBe(true);
    });

    When("the user clicks the toggle", () => {
      cleanup();
      render(<Toggle value={false} onChange={onChangeMock} disabled />);
      fireEvent.click(screen.getByRole("switch", { hidden: true }));
    });

    Then("onChange should not be called", () => {
      expect(onChangeMock).not.toHaveBeenCalled();
    });
  });

  Scenario("Renders with label", ({ When, Then }) => {
    let label: HTMLElement;

    When('I render a Toggle with value false and label "Enable notifications"', () => {
      cleanup();
      render(<Toggle value={false} onChange={vi.fn()} label="Enable notifications" />);
      label = screen.getByText("Enable notifications");
    });

    Then('the label "Enable notifications" should be visible', () => {
      expect(label.textContent).toBe("Enable notifications");
    });
  });
});
