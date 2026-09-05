import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, cleanup } from "@testing-library/react";
import { expect } from "vitest";

import { Icon } from "../../../../src/components/icon/icon";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/icon/icon.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Known icon renders SVG", ({ When, Then }) => {
    let svg: SVGSVGElement | null;

    When('I render an Icon with name "check"', () => {
      cleanup();
      svg = render(<Icon name="check" />).container.querySelector("svg");
    });

    Then("the SVG element should be present", () => {
      expect(svg).toBeTruthy();
    });
  });

  Scenario("Unknown name renders fallback circle", ({ When, Then }) => {
    let fallback: SVGCircleElement | null;

    When('I render an Icon with name "nonexistent-icon"', () => {
      cleanup();
      fallback = render(<Icon name={"nonexistent-icon" as string} />).container.querySelector("circle");
    });

    Then("the SVG should contain a fallback circle", () => {
      expect(fallback).toBeTruthy();
    });
  });

  Scenario("Decorative icon has aria-hidden", ({ When, Then }) => {
    let svg: SVGSVGElement | null;

    When('I render an Icon with name "home" without aria-label', () => {
      cleanup();
      svg = render(<Icon name="home" />).container.querySelector("svg");
    });

    Then("the icon should have aria-hidden set to true", () => {
      expect(svg?.getAttribute("aria-hidden")).toBe("true");
    });
  });

  Scenario("Icon with aria-label has accessible name", ({ When, Then }) => {
    let svg: SVGSVGElement | null;

    When('I render an Icon with name "home" and aria-label "Home"', () => {
      cleanup();
      svg = render(<Icon name="home" aria-label="Home" />).container.querySelector("svg");
    });

    Then('the icon should have role "img" and aria-label "Home"', () => {
      expect(svg?.getAttribute("role")).toBe("img");
      expect(svg?.getAttribute("aria-label")).toBe("Home");
    });
  });
});
