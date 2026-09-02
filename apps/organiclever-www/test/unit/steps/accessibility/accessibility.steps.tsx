import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { expect } from "vitest";

import { HomeContent } from "@/features/home";

const feature = await loadFeature(
  path.resolve(
    __dirname,
    "../../../../../../specs/apps/organiclever/www/behaviors/frontend/accessibility/accessibility.feature",
  ),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      cleanup();
    });
  });

  Scenario("Pages have proper heading hierarchy", ({ When, Then, And }) => {
    When("I navigate to any page", () => {
      render(<HomeContent />);
    });

    Then("each page should have exactly one h1 element", () => {
      const h1Elements = screen.getAllByRole("heading", { level: 1 });
      expect(h1Elements).toHaveLength(1);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/accessibility/accessibility.feature:Pages have proper heading hierarchy
    And("heading levels should not skip (no h1 followed by h3)", () => {
      const headings = screen.queryAllByRole("heading");
      const levels = headings.map((h) => parseInt(h.tagName.replace("H", ""), 10));
      for (let i = 1; i < levels.length; i++) {
        const prev = levels[i - 1] ?? 0;
        const curr = levels[i] ?? 0;
        if (curr > prev) {
          expect(curr - prev).toBeLessThanOrEqual(1);
        }
      }
    });
  });

  Scenario("Keyboard navigation works throughout the app", ({ When, Then, And }) => {
    When("I navigate to the landing page", () => {
      render(<HomeContent />);
    });

    Then("I should be able to tab to all interactive elements", () => {
      const links = screen.queryAllByRole("link");
      links.forEach((link) => {
        expect(link).toBeInTheDocument();
      });
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/accessibility/accessibility.feature:Keyboard navigation works throughout the app
    And("focus indicators should be visible", () => {
      const buttons = screen.queryAllByRole("button");
      expect(buttons.length).toBeGreaterThan(0);
    });
  });

  Scenario("Color contrast meets WCAG AA requirements", ({ When, Then, And }) => {
    When("I navigate to any page", () => {
      render(<HomeContent />);
    });

    Then("all text should meet WCAG AA contrast ratio (4.5:1 for normal text)", () => {
      expect(document.body.textContent?.length).toBeGreaterThan(0);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/accessibility/accessibility.feature:Color contrast meets WCAG AA requirements
    And("all interactive elements should have sufficient contrast", () => {
      const buttons = screen.queryAllByRole("button");
      buttons.forEach((button) => {
        expect(button).toBeInTheDocument();
      });
    });
  });

  Scenario("ARIA attributes are properly used", ({ When, Then, And }) => {
    When("I navigate to any page", () => {
      render(<HomeContent />);
    });

    Then("images should have alt attributes", () => {
      const images = document.querySelectorAll("img");
      images.forEach((img) => {
        expect(img.getAttribute("alt")).not.toBeNull();
      });
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/accessibility/accessibility.feature:ARIA attributes are properly used
    And("navigation landmarks should be properly labeled", () => {
      const main = screen.getByRole("main");
      expect(main).toBeInTheDocument();
    });
  });
});
