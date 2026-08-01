import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";
import { CvContent } from "@/features/cv/shell/CvContent";

const mockPush = vi.fn();
const mockReplace = vi.fn();
let mockSearchParams = new URLSearchParams();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush, replace: mockReplace }),
  useSearchParams: () => mockSearchParams,
}));

vi.mock("@/features/app-shell/shell/Navigation", () => ({
  Navigation: () => React.createElement("div", { "data-testid": "navigation" }, "Navigation"),
}));

vi.stubGlobal("scrollTo", vi.fn());

// @amiceli/vitest-cucumber registers every Given/When/Then/And as its own
// vitest test, and this project's src/test/setup.ts runs
// @testing-library/react's cleanup() after every test — a render() done in
// "When" does not survive into the following "Then" step. Each assertion step
// below renders CvContent itself.
const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature"),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      vi.mocked(window.scrollTo).mockClear();
      mockSearchParams = new URLSearchParams();
    });
  });

  Scenario("CV renders the Curriculum Vitae heading", ({ When, Then }) => {
    When("a visitor opens the CV page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV renders the Curriculum Vitae heading
    Then('the H1 shows "Curriculum Vitae"', () => {
      render(React.createElement(CvContent));
      expect(screen.getByRole("heading", { level: 1, name: "Curriculum Vitae" })).toBeInTheDocument();
    });
  });

  Scenario("CV renders a search input", ({ When, Then }) => {
    When("a visitor opens the CV page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV renders a search input
    Then('a search input with placeholder "Search CV entries..." is visible', () => {
      render(React.createElement(CvContent));
      expect(screen.getByPlaceholderText("Search CV entries...")).toBeInTheDocument();
    });
  });

  Scenario("CV renders the Highlights section header", ({ When, Then }) => {
    When("a visitor opens the CV page", () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV renders the Highlights section header
    Then('a "Highlights" section header is visible', () => {
      render(React.createElement(CvContent));
      expect(screen.getByRole("heading", { name: "Highlights" })).toBeInTheDocument();
    });
  });

  Scenario("CV cross-linked via scrollTop query scrolls into the entries", ({ When, Then }) => {
    When('a visitor opens the CV page with search term "TypeScript" and scrollTop true', () => {});

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV cross-linked via scrollTop query scrolls into the entries
    Then("the page scrolls past Highlights into the matching entries", () => {
      mockSearchParams = new URLSearchParams("search=TypeScript&scrollTop=true");
      render(React.createElement(CvContent));
      expect(window.scrollTo).toHaveBeenCalledWith(0, 0);
      expect(screen.getByRole("heading", { level: 1, name: "Curriculum Vitae" })).toBeInTheDocument();
      expect(screen.getByPlaceholderText("Search CV entries...")).toBeInTheDocument();
    });
  });
});
