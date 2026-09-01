import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen, within } from "@testing-library/react";
import { expect, vi } from "vitest";
import type { PathManifest } from "@/features/course-paths/core/schemas";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 3.1b-i — step binding for
// category-landing-arc-chooser.feature, reusing the careers fixture already proven in
// category-landing.test.tsx.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { CategoryLanding } from "@/features/course-paths/shell/category-landing";

function manifest(overrides: Partial<PathManifest> & Pick<PathManifest, "pathId" | "arc">): PathManifest {
  return { title: overrides.pathId, description: "desc", courseOrder: [], ...overrides };
}

const interviewReady = manifest({ pathId: "careers/interview-ready/role-a", arc: "interview-ready" });
const immediatelyA = manifest({ pathId: "careers/immediately-effective/role-b", arc: "immediately-effective" });
const immediatelyB = manifest({ pathId: "careers/immediately-effective/role-c", arc: "immediately-effective" });
const fundamentallyStrong = manifest({ pathId: "careers/fundamentally-strong/role-d", arc: "fundamentally-strong" });

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/category-landing-arc-chooser.feature",
  ),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("The careers category landing offers an arc chooser", ({ Given, When, Then, And }) => {
    Given("a fixture careers manifest set with three arcs is loaded", () => {
      // Fixture: `interviewReady`, `immediatelyA`+`immediatelyB` (same arc, two roles), and
      // `fundamentallyStrong` above — three distinct arcs.
    });

    When("a reader opens the careers category landing at /en/learn/paths/careers/", () => {
      cleanup();
      render(
        <CategoryLanding
          locale="en"
          category="careers"
          manifests={[interviewReady, immediatelyA, immediatelyB, fundamentallyStrong]}
        />,
      );
    });

    Then("the page renders one arc card per arc with its member role(s) previewed", () => {
      const nav = within(screen.getByRole("navigation", { name: "Careers arcs" }));
      expect(nav.getAllByRole("link").length).toBe(3);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/category-landing-arc-chooser.feature:The careers category landing offers an arc chooser
    And("the immediately-effective arc card previews exactly two member roles", () => {
      // No `contentMap` is passed, so the arc title falls back to `humanizeKebabSlug` (UWT-001
      // fix) — "Immediately Effective", not the raw "immediately-effective" slug.
      const card = screen.getByRole("link", { name: /immediately effective/i });
      expect(within(card).getAllByRole("listitem").length).toBe(2);
    });
  });
});
