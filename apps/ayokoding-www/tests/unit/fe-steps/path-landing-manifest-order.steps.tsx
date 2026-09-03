import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen, within } from "@testing-library/react";
import { expect, vi } from "vitest";
import type { PathManifest } from "@/features/course-paths/core/schemas";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 3.1 — step binding for
// breadcrumb.feature's "A path landing page lists its courses in manifest order" scenario, reusing
// the fixture already proven in path-landing.test.tsx. Named for the scenario it binds (not the
// feature file) since `course-paths-breadcrumb.steps.tsx` is the breadcrumb-only binder and
// deliberately excludes this @e2e-tagged scenario (see its own header comment).

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { PathLanding } from "@/features/course-paths/shell/path-landing";

const fixtureManifest: PathManifest = {
  pathId: "careers/interview-ready/example-role",
  arc: "interview-ready",
  title: "Interview-Ready Example Role",
  description: "An interview-first track.",
  courseOrder: ["just-enough-python", "just-enough-bash", "version-control-and-git"],
};

const courseTitles = {
  "just-enough-python": "Just Enough Python",
  "just-enough-bash": "Just Enough Bash",
  "version-control-and-git": "Version Control & Git",
};

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/breadcrumb.feature"),
);

describeFeature(
  feature,
  ({ Scenario }) => {
    Scenario("A path landing page lists its courses in manifest order", ({ Given, When, Then, And }) => {
      Given("a fixture path manifest is loaded by the manifest repository", () => {
        // Fixture: `fixtureManifest` above.
      });

      When("a reader opens that fixture path's landing page under /en/learn/paths/", () => {
        cleanup();
        render(<PathLanding locale="en" manifest={fixtureManifest} courseTitles={courseTitles} />);
      });

      Then("the courses appear in the fixture manifest's courseOrder", () => {
        const ol = document.querySelector("ol");
        expect(ol).not.toBeNull();
        const items = within(ol as HTMLElement).getAllByRole("listitem");
        expect(items.map((item) => item.textContent)).toEqual([
          "Just Enough Python",
          "Just Enough Bash",
          "Version Control & Git",
        ]);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/breadcrumb.feature:A path landing page lists its courses in manifest order
      And("every course link carries the path context query parameter", () => {
        const link = screen.getByRole("link", { name: "Just Enough Python" });
        expect(link.getAttribute("href")).toBe(
          "/en/learn/courses/just-enough-python?path=careers/interview-ready/example-role",
        );
      });
    });
  },
  // Scopes to exactly the one scenario tagged BOTH @unit and @e2e (vitest-cucumber's array-form
  // filter item is an AND, per Taggable.js) — the other two scenarios in this feature file are
  // bound by course-paths-breadcrumb.steps.tsx (@unit only) and stay @wip respectively; neither is
  // this file's concern.
  { includeTags: [["unit", "e2e"]] },
);
