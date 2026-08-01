import path from "node:path";
import React from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, within } from "@testing-library/react";
import { afterAll, expect, vi } from "vitest";
import { CvContent } from "@/features/cv/shell/CvContent";

const mockPush = vi.fn();
const mockReplace = vi.fn();
let mockSearchParams = new URLSearchParams();
let renderedCv: HTMLElement | undefined;

function getRenderedCv(): HTMLElement {
  if (!renderedCv) {
    throw new Error("The shared CV URL must be opened before asserting its filtered state.");
  }

  return renderedCv;
}

afterAll(() => {
  renderedCv?.remove();
  renderedCv = undefined;
});

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush, replace: mockReplace }),
  useSearchParams: () => mockSearchParams,
}));

vi.mock("@/features/app-shell/shell/Navigation", () => ({
  Navigation: () => React.createElement("div", { "data-testid": "navigation" }, "Navigation"),
}));

vi.mock("@open-sharia-enterprise/web-ui", () => ({
  SearchComponent: ({ searchTerm, placeholder }: { searchTerm: string; placeholder: string }) =>
    React.createElement("input", {
      "data-testid": "search-component",
      value: searchTerm,
      placeholder,
      readOnly: true,
    }),
  HighlightText: ({ text }: { text: string }) => React.createElement("span", null, text),
}));

vi.mock("@/features/cv/core/data", () => ({
  cvData: [
    {
      type: "work",
      title: "Head of Engineering - Hijra Bank",
      organization: "Hijra",
      period: "March 2025 - Present",
      details: ["Leads the engineering organization."],
      skills: ["Software Engineering"],
      programmingLanguages: ["TypeScript"],
      frameworks: ["Next.js"],
    },
    {
      type: "certification",
      title: "Database Design Fundamentals for Software Engineers",
      organization: "Educative, Inc.",
      period: "June 2021",
      details: ["Credential ID: database-design"],
    },
  ],
  getTopSkillsLastFiveYears: () => [],
  getTopLanguagesLastFiveYears: () => [],
  getTopFrameworksLastFiveYears: () => [],
  formatDuration: (duration: number) => `${duration} months`,
  parseDate: vi.fn((date: string) => new Date(date)),
  calculateDuration: vi.fn(() => 12),
  calculateTotalDuration: vi.fn(() => 12),
}));

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature",
  ),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {
      mockSearchParams = new URLSearchParams();
      renderedCv = undefined;
    });
  });

  Scenario("Search-filtered portfolio routes are static yet still filterable", ({ When, Then, And }) => {
    When('a visitor opens the shared CV search URL for "TypeScript"', () => {
      mockSearchParams = new URLSearchParams("search=TypeScript");
      const { container } = render(React.createElement(CvContent));
      // vitest-cucumber registers each step as a separate test and the shared setup cleans the DOM
      // after each one. Preserve a clone of this exact render so the assertion steps observe the URL
      // state rendered here instead of independently remounting CvContent.
      renderedCv = container.cloneNode(true) as HTMLElement;
      document.body.append(renderedCv);
    });

    Then('the CV search input is prefilled with "TypeScript"', () => {
      expect(mockSearchParams.get("search")).toBe("TypeScript");
      expect(within(getRenderedCv()).getByPlaceholderText("Search CV entries...")).toHaveValue("TypeScript");
    });

    And('the "Head of Engineering - Hijra Bank" entry is visible', () => {
      expect(within(getRenderedCv()).getByText("Head of Engineering - Hijra Bank")).toBeVisible();
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Search-filtered portfolio routes are static yet still filterable
    And('the "Database Design Fundamentals for Software Engineers" entry is hidden', () => {
      expect(
        within(getRenderedCv()).queryByText("Database Design Fundamentals for Software Engineers"),
      ).not.toBeInTheDocument();
    });
  });
});
