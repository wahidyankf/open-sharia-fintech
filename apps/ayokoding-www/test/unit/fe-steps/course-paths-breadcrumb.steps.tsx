import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 2.3 — step binding for
// breadcrumb.feature's single Phase-2-owned scenario ("The breadcrumb reflects the active path");
// its two sibling scenarios stay @wip (see specs README.md) so are not bound here. Reuses the
// fixture already proven in breadcrumb.test.tsx's "Cycle 2.3" describe block.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { Breadcrumb } from "@/features/navigation/shell/breadcrumb";

const courseSegments = [
  { label: "Home", slug: "" },
  { label: "Browse", slug: "browse", href: "/en/browse" },
  { label: "Learn", slug: "learn" },
  { label: "Courses", slug: "learn/courses" },
  { label: "Just Enough Python", slug: "learn/courses/just-enough-python" },
];

const pathContext = {
  pathId: "skills/python-fundamentals",
  pathTitle: "Python Fundamentals",
  learnLabel: "Learn",
  learnHref: "/en/browse",
};

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/breadcrumb.feature"),
);

// This file binds exactly one of this feature's three scenarios. The other two stay unbound here:
// "A legacy fundamentally-strong URL redirects..." is @wip (see specs README.md), and "A path
// landing page lists its courses in manifest order" (@unit @e2e) is bound elsewhere per its own
// inline comment above (`path-landing.test.tsx`, `route-paths-hub.test.tsx`, and e2e's
// `course-paths.steps.ts`) — not by this breadcrumb-only unit binder. excludeTags (passed to
// describeFeature itself, not loadFeature) keeps vitest-cucumber from demanding a Scenario() call
// for either: "wip" excludes the legacy-redirect scenario, and "e2e" excludes the path-landing one
// (the scenario this file does bind carries only @unit, never @e2e).
describeFeature(
  feature,
  ({ Scenario }) => {
    Scenario("The breadcrumb reflects the active path", ({ Given, When, Then, And }) => {
      Given("a reader is on a course with an active path context", () => {
        // Fixture: `pathContext` above, matching a reader who arrived via a path landing page.
      });

      When("the breadcrumb renders", () => {
        cleanup();
        render(
          <Breadcrumb
            locale="en"
            slug="learn/courses/just-enough-python"
            segments={courseSegments}
            showCurrent
            pathContext={pathContext}
          />,
        );
      });

      Then("it shows Home, Learn, the path title, and the course title", () => {
        expect(screen.getByRole("link", { name: "Home" })).toBeTruthy();
        expect(screen.getByRole("link", { name: "Learn" })).toBeTruthy();
        expect(screen.getByRole("link", { name: "Python Fundamentals" })).toBeTruthy();
        const current = screen.getByText("Just Enough Python");
        expect(current.getAttribute("aria-current")).toBe("page");
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/breadcrumb.feature:The breadcrumb reflects the active path
      And(
        "the path crumb links to the path landing page /en/learn/paths/<path-id> with the path context preserved",
        () => {
          expect(screen.getByRole("link", { name: "Python Fundamentals" }).getAttribute("href")).toBe(
            "/en/learn/paths/skills/python-fundamentals?path=skills/python-fundamentals",
          );
        },
      );
    });
  },
  { excludeTags: ["wip", "e2e"] },
);
