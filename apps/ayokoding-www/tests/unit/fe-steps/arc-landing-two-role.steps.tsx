import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen, within } from "@testing-library/react";
import { expect, vi } from "vitest";
import type { PathManifest } from "@/features/course-paths/core/schemas";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 3.1c-i — step binding for
// arc-landing-two-role.feature, reusing the two-role fixture already proven in
// arc-landing.test.tsx.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { ArcLanding } from "@/features/course-paths/shell/arc-landing";

const roleA: PathManifest = {
  pathId: "careers/immediately-effective/role-a",
  arc: "immediately-effective",
  title: "Role A",
  description: "desc",
  courseOrder: ["just-enough-python"],
};
const roleB: PathManifest = {
  pathId: "careers/immediately-effective/role-b",
  arc: "immediately-effective",
  title: "Role B",
  description: "desc",
  courseOrder: ["just-enough-bash"],
};

const courseTitles = {
  "just-enough-python": "Just Enough Python",
  "just-enough-bash": "Just Enough Bash",
};

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/arc-landing-two-role.feature",
  ),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario(
    "An arc landing with two paths renders both role cards without a placeholder",
    ({ Given, When, Then, And }) => {
      Given("the fixture immediately-effective arc manifest lists two roles", () => {
        // Fixture: `roleA`/`roleB` above.
      });

      When("a reader opens the arc landing at /en/learn/paths/careers/immediately-effective/", () => {
        cleanup();
        render(
          <ArcLanding locale="en" arc="immediately-effective" manifests={[roleA, roleB]} courseTitles={courseTitles} />,
        );
      });

      Then("both role cards render side by side with their own course counts", () => {
        const nav = within(screen.getByRole("navigation", { name: "immediately-effective paths" }));
        expect(nav.getAllByRole("link").length).toBe(2);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/arc-landing-two-role.feature:An arc landing with two paths renders both role cards without a placeholder
      And("neither card is a placeholder or an empty grid cell", () => {
        const nav = screen.getByRole("navigation", { name: "immediately-effective paths" });
        expect(nav.querySelectorAll("li").length).toBe(2);
      });
    },
  );
});
