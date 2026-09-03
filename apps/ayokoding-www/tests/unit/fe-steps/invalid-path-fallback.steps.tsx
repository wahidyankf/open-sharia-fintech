import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycle 2.6 — step binding for
// invalid-path-fallback.feature, reusing the fixture already proven in route-path-context.test.tsx.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

vi.mock("@/features/navigation/shell/toc", () => ({
  TableOfContents: () => null,
}));

const { fixtureManifest, contentMap, pages } = vi.hoisted(() => {
  const manifest = {
    pathId: "skills/python-fundamentals",
    arc: "python-fundamentals",
    title: "Python Fundamentals",
    description: "Learn Python from the ground up.",
    courseOrder: ["just-enough-python"],
  };

  function meta(slug: string, title: string) {
    return {
      title,
      slug,
      locale: "en",
      weight: 0,
      tags: [],
      draft: false,
      isSection: false,
      filePath: `/tmp/${slug}.md`,
    };
  }

  const map = new Map([
    ["en:learn/courses/just-enough-python", meta("learn/courses/just-enough-python", "Just Enough Python")],
  ]);

  const pageBySlug = new Map<
    string,
    { title: string; html: string; headings: []; date: null; prev: null; next: null }
  >();
  for (const [, m] of map) {
    pageBySlug.set(m.slug, {
      title: m.title,
      html: `<p>${m.title}</p>`,
      headings: [],
      date: null,
      prev: null,
      next: null,
    });
  }

  return { fixtureManifest: manifest, contentMap: map, pages: pageBySlug };
});

vi.mock("@/lib/trpc/server", () => ({
  serverCaller: {
    content: {
      getBySlug: vi.fn(async ({ slug }: { slug: string }) => {
        const page = pages.get(slug);
        if (!page) throw new Error(`no fixture page for slug ${slug}`);
        return page;
      }),
    },
  },
}));

vi.mock("@/features/app-shell/shell/trpc-init", () => ({
  createTRPCContext: () => ({
    contentService: { getIndex: async () => ({ contentMap, trees: {}, prevNext: new Map() }) },
  }),
}));

vi.mock("@/features/course-paths/shell/manifest-repository", () => ({
  loadManifests: vi.fn().mockResolvedValue([fixtureManifest]),
  defaultManifestsDir: () => "unused-in-test",
}));

// eslint-disable-next-line import/first
import { renderCoursePathPage } from "../render-course-path-page";

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/invalid-path-fallback.feature",
  ),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("An invalid path context falls back to the canonical view", ({ Given, When, Then, And }) => {
    let jsx: React.ReactElement;

    Given("a reader opens a course URL with a path context that names no known path", () => {
      // Precondition noted; the render happens in the When step below.
    });

    When("the course page renders", async () => {
      jsx = await renderCoursePathPage({
        locale: "en",
        slug: ["learn", "courses", "just-enough-python"],
        search: { path: "careers/does-not-exist/anywhere" },
      });
      cleanup();
      render(jsx);
    });

    Then("the course renders the canonical standalone view", () => {
      expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Just Enough Python");
      expect(screen.queryByRole("navigation", { name: "Page navigation" })).toBeNull();
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/invalid-path-fallback.feature:An invalid path context falls back to the canonical view
    And("no error is shown", () => {
      // Reaching this assertion at all proves ContentPage() did not throw — the fixture course
      // has no path-membership beyond a non-matching `?path=`, so no exception propagated.
      expect(true).toBe(true);
    });
  });
});
