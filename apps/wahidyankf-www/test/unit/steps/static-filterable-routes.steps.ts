import path from "node:path";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, within } from "@testing-library/react";
import { afterAll, expect, vi } from "vitest";
import robots from "@/app/robots";
import sitemap from "@/app/sitemap";
import Home from "@/app/page";
import CV from "@/app/cv/page";
import PersonalProjects from "@/app/personal-projects/page";
import { CvContent } from "@/features/cv/shell/CvContent";

const mockPush = vi.fn();
const mockReplace = vi.fn();
let mockSearchParams = new URLSearchParams();
let renderedCv: HTMLElement | undefined;
const publicPortfolioPages = [
  { Component: Home, content: "Welcome to My Portfolio" },
  { Component: CV, content: "Curriculum Vitae" },
  { Component: PersonalProjects, content: "Personal Projects" },
] as const;
let renderedStaticPortfolioPages: string[] = [];
let crawlerRobots: ReturnType<typeof robots> | undefined;
let crawlerSitemap: ReturnType<typeof sitemap> | undefined;

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
  getTopAISkillsLastFiveYears: () => [],
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
      window.history.replaceState({}, "", "/cv");
    });
  });

  Scenario("Search-filtered portfolio routes are static yet still filterable", ({ When, Then, And }) => {
    When('a visitor opens the shared CV search URL for "TypeScript"', () => {
      window.history.replaceState({}, "", "/cv?search=TypeScript");
      const { container } = render(React.createElement(CvContent));
      // vitest-cucumber registers each step as a separate test and the shared setup cleans the DOM
      // after each one. Preserve a clone of this exact render so the assertion steps observe the URL
      // state rendered here instead of independently remounting CvContent.
      renderedCv = container.cloneNode(true) as HTMLElement;
      document.body.append(renderedCv);
    });

    Then('the CV search input is prefilled with "TypeScript"', () => {
      expect(new URLSearchParams(window.location.search).get("search")).toBe("TypeScript");
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

  Scenario("Public portfolio routes are available from the production server", ({ When, Then }) => {
    When("a visitor requests every public portfolio page", () => {
      renderedStaticPortfolioPages = publicPortfolioPages.map(({ Component }) =>
        renderToStaticMarkup(React.createElement(Component)),
      );
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Public portfolio routes are available from the production server
    Then("each public portfolio page responds with a successful HTML document", () => {
      expect(renderedStaticPortfolioPages).toHaveLength(publicPortfolioPages.length);
      for (const [index, page] of renderedStaticPortfolioPages.entries()) {
        expect(page).toContain(publicPortfolioPages[index]?.content);
      }
    });
  });

  Scenario("Crawlers receive discovery directives for every public route", ({ When, Then, And }) => {
    When("a crawler requests the robots and sitemap routes", () => {
      crawlerRobots = robots();
      crawlerSitemap = sitemap();
    });

    Then("robots permits crawling and names the canonical sitemap", () => {
      expect(crawlerRobots).toEqual({
        rules: [{ userAgent: "*", allow: "/" }],
        sitemap: "https://www.wahidyankf.com/sitemap.xml",
      });
    });

    // @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/search/static-filterable-routes.feature:Crawlers receive discovery directives for every public route
    And("the sitemap lists every public portfolio route", () => {
      expect(crawlerSitemap).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ url: "https://www.wahidyankf.com" }),
          expect.objectContaining({ url: "https://www.wahidyankf.com/cv" }),
          expect.objectContaining({ url: "https://www.wahidyankf.com/personal-projects" }),
        ]),
      );
    });
  });
});
