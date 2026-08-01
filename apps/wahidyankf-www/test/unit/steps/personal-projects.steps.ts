import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";
import { PersonalProjectsContent } from "@/features/personal-projects/shell/PersonalProjectsContent";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  useSearchParams: () => new URLSearchParams(),
}));

vi.mock("@/features/app-shell/shell/Navigation", () => ({
  Navigation: () => React.createElement("div", { "data-testid": "navigation" }, "Navigation"),
}));

// @amiceli/vitest-cucumber registers every Given/When/Then/And as its own
// vitest test, and this project's src/test/setup.ts runs
// @testing-library/react's cleanup() after every test — a render() done in
// "When" does not survive into the following "Then" step. Each assertion step
// below renders PersonalProjectsContent itself.
const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature",
  ),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {});
  });

  Scenario("Personal projects page renders the heading", ({ When, Then }) => {
    When("a visitor opens the personal projects page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Personal projects page renders the heading
    Then('the H1 shows "Personal Projects"', () => {
      render(React.createElement(PersonalProjectsContent));
      expect(screen.getByRole("heading", { level: 1, name: "Personal Projects" })).toBeInTheDocument();
    });
  });

  Scenario("Personal projects page renders a search input", ({ When, Then }) => {
    When("a visitor opens the personal projects page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Personal projects page renders a search input
    Then('a search input with placeholder "Search projects..." is visible', () => {
      render(React.createElement(PersonalProjectsContent));
      expect(screen.getByPlaceholderText("Search projects...")).toBeInTheDocument();
    });
  });

  Scenario("Personal projects page lists at least one project card", ({ When, Then }) => {
    When("a visitor opens the personal projects page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Personal projects page lists at least one project card
    Then("at least one project card is visible", () => {
      render(React.createElement(PersonalProjectsContent));
      const headings = screen.getAllByRole("heading", { level: 2 });
      expect(headings.length).toBeGreaterThan(0);
    });
  });

  Scenario("Each project card exposes external links where applicable", ({ When, Then }) => {
    When("a visitor opens the personal projects page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Each project card exposes external links where applicable
    Then(
      "every project card exposes a Repository, Website, or YouTube link where the project has that resource",
      () => {
        render(React.createElement(PersonalProjectsContent));
        const links = screen.getAllByRole("link", { name: /Repository|Website|YouTube/i });
        expect(links.length).toBeGreaterThan(0);
      },
    );
  });
});
