import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, within } from "@testing-library/react";
import { expect, vi } from "vitest";
import { ThemeToggle } from "@open-sharia-enterprise/web-ui";
import { HomeContent } from "@/features/home/shell/HomeContent";
import { CvContent } from "@/features/cv/shell/CvContent";
import { PersonalProjectsContent } from "@/features/personal-projects/shell/PersonalProjectsContent";

// Navigation reads the current route via usePathname() and HomeContent/CvContent/
// PersonalProjectsContent navigate via useRouter() — both need a router shim since
// jsdom has no Next.js App Router context.
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  usePathname: () => "/",
  useSearchParams: () => new URLSearchParams(),
}));

// @amiceli/vitest-cucumber registers every Given/When/Then/And as its own vitest
// test, and this project's src/test/setup.ts runs @testing-library/react's
// cleanup() after every test. That means a render() performed in a "When" step
// is torn down before the next "Then"/"And" step runs. Each assertion step
// below therefore renders the page it needs itself instead of relying on a
// previous step's render surviving.
const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/accessibility.feature",
  ),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {});
  });

  Scenario("Home page has zero axe-core WCAG 2.1 AA violations", ({ When, Then }) => {
    When("a visitor opens the home page", () => {});

    // A full axe-core WCAG 2.1 AA scan runs against the live page in the e2e tier
    // (apps/wahidyankf-www-fe-e2e/steps/accessibility.steps.ts). At unit tier we
    // approximate by asserting the page exposes a landmark region and every
    // interactive control has an accessible name — the structural preconditions
    // an axe scan checks for.
    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/accessibility.feature:Home page has zero axe-core WCAG 2.1 AA violations
    Then("an axe-core scan against WCAG 2.1 AA reports zero violations", () => {
      render(React.createElement(HomeContent));

      const main = screen.getByRole("main");
      expect(main).toBeInTheDocument();

      const links = screen.getAllByRole("link");
      expect(links.length).toBeGreaterThan(0);
      for (const link of links) {
        expect(link).toHaveAccessibleName();
      }

      const buttons = screen.getAllByRole("button");
      for (const button of buttons) {
        expect(button).toHaveAccessibleName();
      }
    });
  });

  Scenario("CV page has zero axe-core WCAG 2.1 AA violations", ({ When, Then }) => {
    When("a visitor opens the CV page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/accessibility.feature:CV page has zero axe-core WCAG 2.1 AA violations
    Then("an axe-core scan against WCAG 2.1 AA reports zero violations", () => {
      render(React.createElement(CvContent));

      const main = screen.getByRole("main");
      expect(main).toBeInTheDocument();

      const links = screen.getAllByRole("link");
      expect(links.length).toBeGreaterThan(0);
      for (const link of links) {
        expect(link).toHaveAccessibleName();
      }
    });
  });

  Scenario("Every page has exactly one H1", ({ When, Then }) => {
    When("a visitor opens any of the home, CV, or personal-projects pages", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/accessibility.feature:Every page has exactly one H1
    Then("each of those pages has exactly one H1 element", () => {
      const { unmount: unmountHome } = render(React.createElement(HomeContent));
      expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
      unmountHome();

      const { unmount: unmountCv } = render(React.createElement(CvContent));
      expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
      unmountCv();

      const { unmount: unmountProjects } = render(React.createElement(PersonalProjectsContent));
      expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
      unmountProjects();
    });
  });

  Scenario("Interactive controls expose accessible names", ({ When, Then, And }) => {
    When("a visitor opens the home page", () => {});

    Then("the theme toggle button exposes an aria-label", () => {
      render(React.createElement(ThemeToggle));
      const toggle = screen.getByRole("button", { name: /Switch to (light|dark) theme/ });
      expect(toggle).toBeInTheDocument();
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/app-shell/accessibility.feature:Interactive controls expose accessible names
    And("every navigation link exposes link text or an aria-label", () => {
      render(React.createElement(HomeContent));
      const desktopNav = screen.getByTestId("desktop-nav");
      for (const name of ["Home", "CV", "Independent Projects"]) {
        expect(within(desktopNav).getByRole("link", { name })).toBeInTheDocument();
      }
    });
  });
});
