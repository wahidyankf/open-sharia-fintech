import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { axe } from "vitest-axe";
import { expect } from "vitest";

import { Input } from "../../../../src/components/input/input";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/input/input.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders with default props", ({ When, Then, And }) => {
    let input: HTMLElement;

    When('the Input is rendered with aria-label "test input"', () => {
      cleanup();
      render(<Input aria-label="test input" />);
      input = screen.getByRole("textbox");
    });

    Then("a textbox element should be present", () => {
      expect(input.getAttribute("aria-label")).toBe("test input");
    });

    And('the input should have data-slot "input"', () => {
      expect(input.getAttribute("data-slot")).toBe("input");
    });
  });

  Scenario("Supports disabled state", ({ When, Then }) => {
    let input: HTMLElement;

    When('the Input is rendered as disabled with aria-label "disabled input"', () => {
      cleanup();
      render(<Input aria-label="disabled input" disabled />);
      input = screen.getByRole("textbox");
    });

    Then("the textbox element should have the disabled attribute", () => {
      expect(input.hasAttribute("disabled")).toBe(true);
    });
  });

  Scenario("Has correct height class", ({ When, Then }) => {
    let input: HTMLElement;

    When("I render an Input", () => {
      cleanup();
      render(<Input aria-label="height test" />);
      input = screen.getByRole("textbox");
    });

    Then('the input should have class "h-11"', () => {
      expect(input.className).toContain("h-11");
    });
  });

  Scenario("Has no accessibility violations", ({ When, Then }) => {
    let container: HTMLElement;

    When('the Input is rendered with a label "Email" associated via htmlFor', () => {
      cleanup();
      container = render(
        <div>
          <label htmlFor="email-input">Email</label>
          <Input id="email-input" type="email" />
        </div>,
      ).container;
    });

    Then("the input should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });
});
