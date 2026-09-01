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

const prerequisites = [{ title: "Version Control and Git", slug: "learn/courses/version-control-and-git" }];

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/prerequisite-display.feature",
  ),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("A course page surfaces its declared prerequisites", ({ Given, When, Then, And }) => {
    Given("a course declares prerequisites in its canonical metadata", () => {
      // Fixture: `prerequisites` above (one declared prerequisite: Version Control and Git).
    });

    When("a reader opens the course page with or without a path context", () => {
      // Both rendering branches are asserted directly in the Then/And steps below — no shared
      // render happens here since each branch needs its own props.
    });

    Then("the page lists each prerequisite course with a link to its canonical URL", () => {
      cleanup();
      // EWT-002 fix: `pathId` is now carried per-item (set only when that prerequisite is itself a
      // member of the active manifest) rather than as a blanket prop applied to every prerequisite.
      const pathAwarePrerequisites = [
        {
          title: "Version Control and Git",
          slug: "learn/courses/version-control-and-git",
          pathId: "skills/python-fundamentals",
        },
      ];
      render(<PrerequisiteList locale="en" prerequisites={pathAwarePrerequisites} />);
      expect(screen.getByRole("link", { name: "Version Control and Git" }).getAttribute("href")).toBe(
        "/en/learn/courses/version-control-and-git?path=skills/python-fundamentals",
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/prerequisite-display.feature:A course page surfaces its declared prerequisites
    And("the prerequisite list renders even in the canonical no-path view", () => {
      cleanup();
      render(<PrerequisiteList locale="en" prerequisites={prerequisites} />);
      expect(screen.getByRole("link", { name: "Version Control and Git" }).getAttribute("href")).toBe(
        "/en/learn/courses/version-control-and-git",
      );
    });
  });
});
