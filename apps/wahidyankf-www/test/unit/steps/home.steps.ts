import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, within } from "@testing-library/react";
import { expect, vi } from "vitest";
import { HomeContent } from "@/features/home/shell/HomeContent";

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
// "When" does not survive into the following "Then"/"And" step. Each
// assertion step below renders HomeContent itself.
const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature"),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {});
  });

  Scenario("Home renders the welcome heading", ({ When, Then }) => {
    When("a visitor opens the home page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the welcome heading
    Then('the H1 shows "Welcome to My Portfolio"', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("heading", { level: 1, name: "Welcome to My Portfolio" })).toBeInTheDocument();
    });
  });

  Scenario("Home renders the About Me card", ({ When, Then }) => {
    When("a visitor opens the home page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the About Me card
    Then("an About Me card is visible", () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("heading", { name: "About Me" })).toBeInTheDocument();
    });
  });

  Scenario("Home renders the Skills & Expertise card with three subsections", ({ When, Then, And }) => {
    When("a visitor opens the home page", () => {});

    Then("a Skills & Expertise card is visible", () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("heading", { name: "Skills & Expertise" })).toBeInTheDocument();
    });

    And('the card has a "Top Skills Used in The Last 5 Years" subsection', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByText("Top Skills Used in The Last 5 Years")).toBeInTheDocument();
    });

    And('the card has a "Top Programming Languages Used in The Last 5 Years" subsection', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByText("Top Programming Languages Used in The Last 5 Years")).toBeInTheDocument();
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the Skills & Expertise card with three subsections
    And('the card has a "Top Frameworks & Libraries Used in The Last 5 Years" subsection', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByText("Top Frameworks & Libraries Used in The Last 5 Years")).toBeInTheDocument();
    });
  });

  Scenario("Home renders the Quick Links card with two internal links", ({ When, Then, And }) => {
    When("a visitor opens the home page", () => {});

    Then("a Quick Links card is visible", () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("heading", { name: "Quick Links" })).toBeInTheDocument();
    });

    And('the card contains a "View My CV" link to /cv', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("link", { name: "View My CV" })).toHaveAttribute("href", "/cv");
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the Quick Links card with two internal links
    And('the card contains a "Browse My Independent Projects" link to /personal-projects', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("link", { name: "Browse My Independent Projects" })).toHaveAttribute(
        "href",
        "/personal-projects",
      );
    });
  });

  Scenario("Home renders the Connect With Me card with five external links", ({ When, Then, And }) => {
    When("a visitor opens the home page", () => {});

    Then("a Connect With Me card is visible", () => {
      render(React.createElement(HomeContent));
      expect(screen.getByRole("heading", { name: "Connect With Me" })).toBeInTheDocument();
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the Connect With Me card with five external links
    And("the card has Github, GithubOrg, Linkedin, Website, and Email links", () => {
      render(React.createElement(HomeContent));
      const heading = screen.getByRole("heading", { name: "Connect With Me" });
      const section = heading.closest("section");
      expect(section).not.toBeNull();
      for (const name of ["Github", "GithubOrg", "Linkedin", "Website", "Email"]) {
        expect(within(section as HTMLElement).getByRole("link", { name })).toBeInTheDocument();
      }
    });
  });
});
