import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

// <ROUTE>-level integration tests (course-paths plan) for Cycles 2.2 (path-aware prev/next),
// 2.6 (invalid path falls back), and 2.7 (course omitted from a path shows no path nav for that
// path). Follows the established pattern for unit-testing an async Server Component directly
// (see `apps/ayokoding-www/src/features/i18n/shell/tools-page.test.tsx`): call the page function
// directly and `render()` its returned JSX, with `serverCaller`/`createTRPCContext` mocked.

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// TableOfContents uses IntersectionObserver (unavailable in jsdom) and is not this test's
// concern — stub it, matching the coverage-exclusion of navigation/shell presentation files.
vi.mock("@/features/navigation/shell/toc", () => ({
  TableOfContents: () => null,
}));

const { fixtureManifest, contentMap, pages } = vi.hoisted(() => {
  const manifest = {
    pathId: "skills/python-fundamentals",
    arc: "python-fundamentals",
    title: "Python Fundamentals",
    description: "Learn Python from the ground up.",
    courseOrder: ["version-control-and-git", "just-enough-python", "data-structures-and-algorithms-essentials"],
  };

  function meta(slug: string, title: string, prerequisites?: string[]) {
    return {
      title,
      slug,
      locale: "en",
      weight: 0,
      tags: [],
      draft: false,
      isSection: false,
      filePath: `/tmp/${slug}.md`,
      prerequisites,
    };
  }

  const map = new Map([
    ["en:learn/courses/version-control-and-git", meta("learn/courses/version-control-and-git", "Git")],
    [
      "en:learn/courses/just-enough-python",
      meta("learn/courses/just-enough-python", "Just Enough Python", ["version-control-and-git"]),
    ],
    [
      "en:learn/courses/data-structures-and-algorithms-essentials",
      meta("learn/courses/data-structures-and-algorithms-essentials", "Data Structures & Algorithms"),
    ],
    // Deliberately absent from `manifest.courseOrder` — Cycle 2.7's omitted-course fixture.
    ["en:learn/courses/capstone-forge-ready", meta("learn/courses/capstone-forge-ready", "Capstone: Forge Ready")],
  ]);

  const pageBySlug = new Map<
    string,
    { title: string; html: string; headings: []; date: null; prev: null; next: null }
  >();
  for (const [, m] of map) {
    pageBySlug.set(m.slug, {
      title: m.title,
      html: `<p>${m.title} content</p>`,
      headings: [],
      date: null,
      // The weight-based fallback prev/next — deliberately distinct from any manifest
      // neighbour so a test can tell whether the manifest or the fallback rendered.
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
import { renderCoursePathPage } from "../../../render-course-path-page";

afterEach(cleanup);

function renderCoursePage(slug: string[], searchParams: Record<string, string | string[] | undefined> = {}) {
  return renderCoursePathPage({ locale: "en", slug, search: searchParams });
}

describe("Cycle 2.2 — route wiring: prev/next follow the active path's order", () => {
  it("resolves prev/next from the manifest neighbours, both hrefs carrying the path context", async () => {
    const jsx = await renderCoursePage(["learn", "courses", "just-enough-python"], {
      path: fixtureManifest.pathId,
    });
    render(jsx);

    const pageNav = within(screen.getByRole("navigation", { name: "Page navigation" }));
    const prevLink = pageNav.getByRole("link", { name: /Git/i });
    const nextLink = pageNav.getByRole("link", { name: /Data Structures/i });

    expect(prevLink.getAttribute("href")).toBe(
      `/en/learn/courses/version-control-and-git?path=${fixtureManifest.pathId}`,
    );
    expect(nextLink.getAttribute("href")).toBe(
      `/en/learn/courses/data-structures-and-algorithms-essentials?path=${fixtureManifest.pathId}`,
    );
  });
});

// UWT-004 fix (phase-5 rule-15 usability retest) — regression: `PathBanner` used to render after
// the syllabus/prerequisites, so a mobile reader scrolled past the entire course body before
// learning they were even inside a path. It must render immediately below the `<h1>`, above both
// the body and the prerequisite list — asserted here via DOM tree order so a future refactor that
// silently moves it back down fails this test instead of shipping unnoticed (no existing test
// asserted this order before this fix).
describe("Cycle 2.9/UWT-004 — the mobile path banner renders above the body and prerequisites", () => {
  it("places PathBanner's DOM node before the course body and before the prerequisite list", async () => {
    const jsx = await renderCoursePage(["learn", "courses", "just-enough-python"], {
      path: fixtureManifest.pathId,
    });
    render(jsx);

    const banner = screen.getByRole("button", { name: /View path/i });
    const body = screen.getByText("Just Enough Python content");
    const prerequisites = screen.getByRole("navigation", { name: "Prerequisites" });

    // `compareDocumentPosition` bit 4 (DOCUMENT_POSITION_FOLLOWING) set on the result means the
    // argument follows `banner` in tree order — i.e. `banner` precedes it.
    expect(banner.compareDocumentPosition(body) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(banner.compareDocumentPosition(prerequisites) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });
});

describe("Cycle 2.6 — an invalid path context falls back to the canonical view", () => {
  it("renders the canonical view with no error when ?path= names no loaded manifest", async () => {
    const jsx = await renderCoursePage(["learn", "courses", "just-enough-python"], {
      path: "careers/does-not-exist/anywhere",
    });

    // No thrown exception — rendering completes and produces the canonical body.
    render(jsx);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Just Enough Python");
    // No path-aware prev/next: the fallback (fixture) prev/next is null/null, so no <nav> at all.
    expect(screen.queryByRole("navigation", { name: "Page navigation" })).toBeNull();
  });
});

describe("Cycle 2.7 — a course omitted from a path shows no path nav for that path", () => {
  it("renders the canonical standalone view when the course is absent from the named path's courseOrder", async () => {
    const jsx = await renderCoursePage(["learn", "courses", "capstone-forge-ready"], {
      path: fixtureManifest.pathId,
    });
    render(jsx);

    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Capstone: Forge Ready");
    // Canonical breadcrumb — no path crumb, since the course isn't a path member.
    expect(screen.queryByText("Python Fundamentals")).toBeNull();
    // "Part of paths" affordance renders (canonical branch), listing no paths for this course.
    expect(screen.queryByRole("navigation", { name: "This course is part of" })).toBeNull();
  });
});
