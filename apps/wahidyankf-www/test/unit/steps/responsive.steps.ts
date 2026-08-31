import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, fireEvent } from "@testing-library/react";
import { expect, vi } from "vitest";
import { ThemeToggle } from "@open-sharia-enterprise/web-ui";
import { Navigation } from "@/features/app-shell/shell/Navigation";

vi.mock("next/navigation", () => ({
  usePathname: () => "/",
}));

// @amiceli/vitest-cucumber registers every Given/When/Then/And as its own vitest
// test, and this project's src/test/setup.ts runs @testing-library/react's
// cleanup() after every test — a render() done in "When" does not survive into
// the following "Then"/"And" step. Every assertion step below renders
// Navigation itself rather than depending on a previous step's render.
const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/responsive.feature",
  ),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {});
  });

  Scenario("Desktop viewport shows a fixed left sidebar", ({ When, Then, And }) => {
    // jsdom does not evaluate CSS media queries, so viewport-conditional
    // visibility is approximated structurally: Navigation renders both the
    // desktop sidebar and the mobile tab bar unconditionally and relies on
    // Tailwind's `lg:` breakpoint classes to show/hide each at runtime. We
    // assert the breakpoint classes are wired the way a 1440x900 (>=1024px,
    // i.e. "lg") viewport requires: the sidebar becomes visible and the tab
    // bar becomes hidden.
    When("a visitor opens the home page at 1440 by 900 viewport", () => {});

    Then("a left sidebar is visible with Home, CV, and Independent Projects links", () => {
      render(React.createElement(Navigation));
      const desktopNav = screen.getByTestId("desktop-nav");
      expect(desktopNav.className).toContain("lg:block");
      for (const name of ["Home", "CV", "Independent Projects"]) {
        expect(screen.getAllByRole("link", { name }).length).toBeGreaterThan(0);
      }
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/responsive.feature:Desktop viewport shows a fixed left sidebar
    And("no bottom tab bar is rendered", () => {
      render(React.createElement(Navigation));
      const mobileNav = screen.getByTestId("mobile-nav");
      expect(mobileNav.className).toContain("lg:hidden");
    });
  });

  Scenario("Tablet viewport hides the sidebar and renders a bottom tab bar", ({ When, Then, And }) => {
    When("a visitor opens the home page at 768 by 1024 viewport", () => {});

    Then("no left sidebar is visible", () => {
      render(React.createElement(Navigation));
      const desktopNav = screen.getByTestId("desktop-nav");
      // Hidden below the "lg" (1024px) breakpoint; 768px is below it.
      expect(desktopNav.className).toContain("hidden");
      expect(desktopNav.className).toContain("lg:block");
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/responsive.feature:Tablet viewport hides the sidebar and renders a bottom tab bar
    And("a bottom tab bar is visible with Home, CV, and Independent Projects items", () => {
      render(React.createElement(Navigation));
      const mobileNav = screen.getByTestId("mobile-nav");
      expect(mobileNav.className).toContain("flex");
      for (const name of ["Home", "CV", "Independent Projects"]) {
        expect(screen.getAllByRole("link", { name }).length).toBeGreaterThan(0);
      }
    });
  });

  Scenario("Mobile viewport hides the sidebar and renders a bottom tab bar", ({ When, Then, And }) => {
    When("a visitor opens the home page at 375 by 812 viewport", () => {});

    Then("no left sidebar is visible", () => {
      render(React.createElement(Navigation));
      const desktopNav = screen.getByTestId("desktop-nav");
      // Hidden below the "lg" (1024px) breakpoint; 375px is below it.
      expect(desktopNav.className).toContain("hidden");
      expect(desktopNav.className).toContain("lg:block");
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/responsive.feature:Mobile viewport hides the sidebar and renders a bottom tab bar
    And("a bottom tab bar is visible with Home, CV, and Independent Projects items", () => {
      render(React.createElement(Navigation));
      const mobileNav = screen.getByTestId("mobile-nav");
      expect(mobileNav.className).toContain("flex");
      for (const name of ["Home", "CV", "Independent Projects"]) {
        expect(screen.getAllByRole("link", { name }).length).toBeGreaterThan(0);
      }
    });
  });

  Scenario("The theme toggle is always reachable", ({ When, Then }) => {
    When("a visitor opens the home page at any viewport", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/responsive.feature:The theme toggle is always reachable
    Then("the theme toggle button is present in the DOM and clickable", () => {
      render(React.createElement(ThemeToggle));
      const toggle = screen.getByRole("button", { name: /Switch to (light|dark) theme/ });
      expect(toggle).toBeInTheDocument();
      expect(toggle).not.toBeDisabled();
      fireEvent.click(toggle);
    });
  });
});
