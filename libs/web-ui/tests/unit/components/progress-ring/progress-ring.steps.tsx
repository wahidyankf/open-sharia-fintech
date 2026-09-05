import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, cleanup } from "@testing-library/react";
import { expect } from "vitest";

import { ProgressRing } from "../../../../src/components/progress-ring/progress-ring";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/progress-ring/progress-ring.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Full progress ring", ({ When, Then }) => {
    let progressbar: Element | null;

    When("I render a ProgressRing with progress 1", () => {
      cleanup();
      progressbar = render(<ProgressRing progress={1} />).container.querySelector("[role='progressbar']");
    });

    Then('the progressbar should have aria-valuenow "100"', () => {
      expect(progressbar?.getAttribute("aria-valuenow")).toBe("100");
    });
  });

  Scenario("Half progress ring", ({ When, Then }) => {
    let progressbar: Element | null;

    When("I render a ProgressRing with progress 0.5", () => {
      cleanup();
      progressbar = render(<ProgressRing progress={0.5} />).container.querySelector("[role='progressbar']");
    });

    Then('the progressbar should have aria-valuenow "50"', () => {
      expect(progressbar?.getAttribute("aria-valuenow")).toBe("50");
    });
  });

  Scenario("Empty progress ring", ({ When, Then }) => {
    let progressbar: Element | null;

    When("I render a ProgressRing with progress 0", () => {
      cleanup();
      progressbar = render(<ProgressRing progress={0} />).container.querySelector("[role='progressbar']");
    });

    Then('the progressbar should have aria-valuenow "0"', () => {
      expect(progressbar?.getAttribute("aria-valuenow")).toBe("0");
    });
  });

  Scenario("Has correct aria attributes", ({ When, Then, And }) => {
    let progressbar: Element | null;

    When("I render a ProgressRing with progress 0.75", () => {
      cleanup();
      progressbar = render(<ProgressRing progress={0.75} />).container.querySelector("[role='progressbar']");
    });

    Then('the progressbar should have aria-valuemin "0"', () => {
      expect(progressbar?.getAttribute("aria-valuemin")).toBe("0");
    });

    And('the progressbar should have aria-valuemax "100"', () => {
      expect(progressbar?.getAttribute("aria-valuemax")).toBe("100");
    });
  });
});
