import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 3.1a — step binding for
// category-landing-empty-state.feature's unit-only scenario (delivery.md's Cycle 3.1a carries no
// e2e command for it). Reuses the fixtures/approach already proven in category-landing.test.tsx.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { CategoryLanding } from "@/features/course-paths/shell/category-landing";

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/category-landing-empty-state.feature",
  ),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario(
    "A category landing with no populated manifest renders an explicit empty state",
    ({ Given, When, Then, And }) => {
      Given("a structural category index exists with zero published path manifests", () => {
        // Fixture: `manifests={[]}` below — the structural category page exists (the route
        // resolves) but no manifest has been loaded for it yet.
      });

      When("a reader opens that category's landing page", () => {
        cleanup();
        render(<CategoryLanding locale="en" category="careers" manifests={[]} />);
      });

      Then('the page renders a stated "being written, check back soon" message with a fallback link', () => {
        expect(screen.getByText(/being written/i)).toBeTruthy();
        expect(screen.getByText(/check back soon/i)).toBeTruthy();
        expect(screen.getByRole("link")).toBeTruthy();
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/category-landing-empty-state.feature:A category landing with no populated manifest renders an explicit empty state
      And("the page never renders a blank content area with no message", () => {
        const status = screen.getByRole("alert");
        expect(status.textContent?.trim().length).toBeGreaterThan(0);
      });
    },
  );
});
