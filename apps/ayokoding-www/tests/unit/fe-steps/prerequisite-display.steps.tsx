import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 2.4 — step binding for
// prerequisite-display.feature, reusing the fixture already proven in prerequisite-list.test.tsx.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { PrerequisiteList } from "@/features/course-paths/shell/prerequisite-list";
import type { PrerequisiteLink } from "@/features/course-paths/shell/course-path-nav";

const prerequisites: PrerequisiteLink[] = [
  { title: "Version Control and Git", slug: "learn/courses/version-control-and-git" },
];

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviours/frontend/course-paths/prerequisite-display.feature",
  ),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("A course page surfaces its declared prerequisites", ({ Given, When, Then, And }) => {
    Given("a course declares prerequisites in its canonical metadata", () => {
      expect(prerequisites).toEqual([
        { title: "Version Control and Git", slug: "learn/courses/version-control-and-git" },
      ]);
    });

    When("a reader opens the course page with or without a path context", () => {
      cleanup();
      render(
        <PrerequisiteList
          locale="en"
          prerequisites={[
            {
              ...prerequisites[0]!,
              pathId: "skills/python-fundamentals",
            },
          ]}
        />,
      );
    });

    Then("the page lists each prerequisite course with a link to its canonical URL", () => {
      expect(screen.getByRole("link", { name: "Version Control and Git" }).getAttribute("href")).toBe(
        "/en/learn/courses/version-control-and-git?path=skills/python-fundamentals",
      );
    });

    And("the prerequisite list renders even in the canonical no-path view", () => {
      cleanup();
      render(<PrerequisiteList locale="en" prerequisites={prerequisites} />);
      expect(screen.getByRole("link", { name: "Version Control and Git" }).getAttribute("href")).toBe(
        "/en/learn/courses/version-control-and-git",
      );
    });
  });
});
