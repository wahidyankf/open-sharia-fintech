import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { expect } from "vitest";

import { StatCard } from "../../../../src/components/stat-card/stat-card";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/stat-card/stat-card.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders label and value", ({ When, Then, And }) => {
    let renderedText = "";

    When('I render a StatCard with label "Steps" value "12500" unit "steps" hue "teal" icon "trend"', () => {
      cleanup();
      const { container } = render(<StatCard label="Steps" value="12500" unit="steps" hue="teal" icon="trend" />);
      renderedText = container.textContent ?? "";
    });

    Then('the text "Steps" should be visible', () => {
      expect(renderedText).toContain("Steps");
    });

    And('the text "12500" should be visible', () => {
      expect(renderedText).toContain("12500");
    });

    And('the text "steps" should be visible', () => {
      expect(renderedText).toContain("steps");
    });
  });

  Scenario("Renders InfoTip when info is provided", ({ When, Then }) => {
    let infoTip: HTMLElement;

    When(
      'I render a StatCard with label "Steps" value "12500" unit "steps" hue "teal" icon "trend" and info "Daily step count"',
      () => {
        cleanup();
        render(<StatCard label="Steps" value="12500" unit="steps" hue="teal" icon="trend" info="Daily step count" />);
        infoTip = screen.getByRole("button", { name: "Steps" });
      },
    );

    Then("an InfoTip trigger should be visible", () => {
      expect(infoTip.getAttribute("aria-label")).toBe("Steps");
    });
  });

  Scenario("Does not render InfoTip when info is absent", ({ When, Then }) => {
    let infoTip: HTMLElement | null;

    When(
      'I render a StatCard with label "Steps" value "12500" unit "steps" hue "teal" icon "trend" without info',
      () => {
        cleanup();
        render(<StatCard label="Steps" value="12500" unit="steps" hue="teal" icon="trend" />);
        infoTip = screen.queryByRole("button", { name: "Steps" });
      },
    );

    Then("no InfoTip trigger should be present", () => {
      expect(infoTip).toBeNull();
    });
  });
});
