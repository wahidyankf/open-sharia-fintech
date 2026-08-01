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
    });
  });

  Scenario("Search-filtered portfolio routes are static yet still filterable", ({ When, Then, And }) => {
    When('a visitor opens the shared CV search URL for "TypeScript"', () => {});

    Then('the CV search input is prefilled with "TypeScript"', () => {
      mockSearchParams = new URLSearchParams("search=TypeScript");
      render(React.createElement(CvContent));
      expect(screen.getByPlaceholderText("Search CV entries...")).toHaveValue("TypeScript");
    });

    And('the "Head of Engineering - Hijra Bank" entry is visible', () => {
      mockSearchParams = new URLSearchParams("search=TypeScript");
      render(React.createElement(CvContent));
      expect(screen.getByText("Head of Engineering - Hijra Bank")).toBeInTheDocument();
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Search-filtered portfolio routes are static yet still filterable
    And('the "Database Design Fundamentals for Software Engineers" entry is hidden', () => {
      mockSearchParams = new URLSearchParams("search=TypeScript");
      render(React.createElement(CvContent));
      expect(screen.queryByText("Database Design Fundamentals for Software Engineers")).not.toBeInTheDocument();
    });
  });
});
