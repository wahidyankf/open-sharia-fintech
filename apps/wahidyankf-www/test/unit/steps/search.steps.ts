import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, fireEvent } from "@testing-library/react";
import { expect, vi } from "vitest";
import { HomeContent } from "@/features/home/shell/HomeContent";

const mockPush = vi.fn();
let mockSearchParams = new URLSearchParams();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
  useSearchParams: () => mockSearchParams,
}));

vi.mock("@/features/app-shell/shell/Navigation", () => ({
  Navigation: () => React.createElement("div", { "data-testid": "navigation" }, "Navigation"),
}));

// @amiceli/vitest-cucumber registers every Given/When/Then/And as its own
// vitest test, and this project's src/test/setup.ts runs
// @testing-library/react's cleanup() after every test — a render() done in one
// step does not survive into the next. mockPush's call history is a plain JS
// object, though, and persists regardless of DOM teardown, so each step that
// interacts with the page renders + interacts in one atomic step, and the
// following "Then" step only inspects mockPush's recorded calls.
const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/search.feature"),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      mockPush.mockClear();
      mockSearchParams = new URLSearchParams();
      window.history.replaceState({}, "", "/");
    });
  });

  Scenario("Typing a term updates the URL query string", ({ When, And, Then }) => {
    When("a visitor opens the home page", () => {});

    And('the visitor types "TypeScript" in the search input', () => {
      render(React.createElement(HomeContent));
      const input = screen.getByPlaceholderText("Search skills, languages, or frameworks...");
      fireEvent.change(input, { target: { value: "TypeScript" } });
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/search.feature:Typing a term updates the URL query string
    Then("the URL becomes /?search=TypeScript", () => {
      expect(mockPush).toHaveBeenCalledWith("/?search=TypeScript", { scroll: false });
    });
  });

  Scenario("Matching content is highlighted with a yellow mark", ({ When, Then }) => {
    When('a visitor opens the home page with search term "TypeScript"', () => {
      window.history.replaceState({}, "", "/?search=TypeScript");
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/search.feature:Matching content is highlighted with a yellow mark
    Then('the matching pill wraps "TypeScript" in a mark element', () => {
      render(React.createElement(HomeContent));
      const marks = Array.from(document.querySelectorAll("mark"));
      expect(marks.some((mark) => /TypeScript/i.test(mark.textContent ?? ""))).toBe(true);
    });
  });

  Scenario("Non-matching About Me shows a placeholder", ({ When, Then }) => {
    When('a visitor opens the home page with search term "NoSuchTerm"', () => {
      window.history.replaceState({}, "", "/?search=NoSuchTerm");
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/search.feature:Non-matching About Me shows a placeholder
    Then('the About Me card shows "No matching content in the About Me section."', () => {
      render(React.createElement(HomeContent));
      expect(screen.getByText("No matching content in the About Me section.")).toBeInTheDocument();
    });
  });

  Scenario("Clicking a skill pill navigates to the CV with scrollTop", ({ When, And, Then }) => {
    When("a visitor opens the home page", () => {});

    And('the visitor clicks the "TypeScript" skill pill', () => {
      render(React.createElement(HomeContent));
      fireEvent.click(screen.getByRole("button", { name: "TypeScript" }));
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/search.feature:Clicking a skill pill navigates to the CV with scrollTop
    Then("the URL becomes /cv?search=TypeScript&scrollTop=true", () => {
      expect(mockPush).toHaveBeenCalledWith("/cv?search=TypeScript&scrollTop=true");
    });
  });
});
