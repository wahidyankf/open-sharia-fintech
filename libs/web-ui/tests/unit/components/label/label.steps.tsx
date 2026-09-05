import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { axe } from "vitest-axe";
import { expect } from "vitest";

import { Label } from "../../../../src/components/label/label";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/label/label.feature"),
);

function renderLabelWithInput() {
  return render(
    <div>
      <Label htmlFor="email-input">Email</Label>
      <input id="email-input" type="email" />
    </div>,
  );
}

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders with text content", ({ When, Then, And }) => {
    let label: HTMLElement;

    When('the Label is rendered with text "Email"', () => {
      cleanup();
      render(<Label>Email</Label>);
      label = screen.getByText("Email");
    });

    Then('the label element with text "Email" should be present', () => {
      expect(label.textContent).toBe("Email");
    });

    And('the label should have data-slot "label"', () => {
      expect(label.getAttribute("data-slot")).toBe("label");
    });
  });

  Scenario("Associates with form control via htmlFor", ({ When, Then }) => {
    let container: HTMLElement;

    When('the Label is rendered with text "Email" associated to input "email-input"', () => {
      cleanup();
      container = renderLabelWithInput().container;
      expect(screen.getByLabelText("Email").getAttribute("id")).toBe("email-input");
    });

    Then("the label and input association should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  Scenario("Has no accessibility violations", ({ When, Then }) => {
    let container: HTMLElement;

    When('the Label is rendered with text "Email" associated to input "email-input"', () => {
      cleanup();
      container = renderLabelWithInput().container;
      expect(screen.getByLabelText("Email")).toBeDefined();
    });

    Then("the label and input association should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });
});
