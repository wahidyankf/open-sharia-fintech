import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { act, cleanup, render, screen, within, fireEvent } from "@testing-library/react";
import { expect, vi } from "vitest";

// course-paths plan (ayokoding-learning-path-03-navigation-ui), Cycles 2.2, 2.8, 2.9 — step
// bindings for path-order-nav.feature's 3 scenarios, reusing the fixtures and rendering
// approach already proven in route-path-context.test.tsx / path-rail.test.tsx / mobile-nav.test.tsx.

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

let mockPathname = "/en/browse";
let mockSearchParams = new URLSearchParams();

vi.mock("next/navigation", () => ({
  usePathname: () => mockPathname,
  useSearchParams: () => mockSearchParams,
}));

vi.mock("@/lib/trpc/client", () => ({
  trpcClient: {
    content: {
      getTree: { query: vi.fn().mockResolvedValue([]) },
    },
  },
}));

const { fixtureManifest, courseTitles, contentMap, pages } = vi.hoisted(() => {
  const manifest = {
    pathId: "skills/python-fundamentals",
    arc: "python-fundamentals",
    title: "Python Fundamentals",
    description: "Learn Python from the ground up.",
    courseOrder: ["version-control-and-git", "just-enough-python", "data-structures-and-algorithms-essentials"],
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
    ["en:learn/courses/version-control-and-git", meta("learn/courses/version-control-and-git", "Git")],
    ["en:learn/courses/just-enough-python", meta("learn/courses/just-enough-python", "Just Enough Python")],
    [
      "en:learn/courses/data-structures-and-algorithms-essentials",
      meta("learn/courses/data-structures-and-algorithms-essentials", "Data Structures & Algorithms"),
    ],
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

  return {
    fixtureManifest: manifest,
    courseTitles: {
      "version-control-and-git": "Git",
      "just-enough-python": "Just Enough Python",
      "data-structures-and-algorithms-essentials": "Data Structures & Algorithms",
    },
    contentMap: map,
    pages: pageBySlug,
  };
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
// eslint-disable-next-line import/first
import { PathRail } from "@/features/course-paths/shell/path-rail";
// eslint-disable-next-line import/first
import { MobileNav } from "@/features/app-shell/shell/mobile-nav";
// eslint-disable-next-line import/first
import { PathBanner } from "@/features/course-paths/shell/path-banner";
// eslint-disable-next-line import/first
import { MobileNavOpenProvider } from "@/features/app-shell/shell/mobile-nav-open-provider";
// eslint-disable-next-line import/first
import { useMobileNavOpen } from "@/features/app-shell/shell/use-mobile-nav-open";

function MobileNavConsumer() {
  const { open, setOpen } = useMobileNavOpen();
  return (
    <MobileNav
      locale="en"
      open={open}
      onOpenChange={setOpen}
      manifests={[fixtureManifest]}
      courseTitles={courseTitles}
    />
  );
}

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviours/frontend/course-paths/path-order-nav.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Prev and next follow the active path's order", ({ Given, When, Then, And }) => {
    let jsx: React.ReactElement;

    Given("a reader is on a course with an active path context", async () => {
      jsx = await renderCoursePathPage({
        locale: "en",
        slug: ["learn", "courses", "just-enough-python"],
        search: { path: fixtureManifest.pathId },
      });
    });

    When("the reader reads the prev/next navigation", () => {
      cleanup();
      render(jsx);
    });

    Then("prev and next are the neighboring courses in that path's manifest", () => {
      const pageNav = within(screen.getByRole("navigation", { name: "Page navigation" }));
      expect(pageNav.getByRole("link", { name: /Git/i })).toBeTruthy();
      expect(pageNav.getByRole("link", { name: /Data Structures/i })).toBeTruthy();
    });

    And("both links preserve the path context query parameter", () => {
      const pageNav = within(screen.getByRole("navigation", { name: "Page navigation" }));
      expect(pageNav.getByRole("link", { name: /Git/i }).getAttribute("href")).toBe(
        `/en/learn/courses/version-control-and-git?path=${fixtureManifest.pathId}`,
      );
      expect(pageNav.getByRole("link", { name: /Data Structures/i }).getAttribute("href")).toBe(
        `/en/learn/courses/data-structures-and-algorithms-essentials?path=${fixtureManifest.pathId}`,
      );
    });
  });

  Scenario(
    "The path rail shows the whole ordered arc beside a course at desktop width",
    ({ Given, When, Then, And }) => {
      Given("a reader opens a course in path context on a desktop-width viewport", () => {
        Object.defineProperty(window, "innerWidth", { configurable: true, value: 1280 });
        expect(window.innerWidth).toBeGreaterThanOrEqual(768);
      });

      When("the page renders", () => {
        cleanup();
        render(
          <PathRail
            locale="en"
            manifest={fixtureManifest}
            currentCourseId="just-enough-python"
            courseTitles={courseTitles}
          />,
        );
      });

      Then("the left rail lists that path's courses in manifest order with the current course marked", () => {
        const rail = screen.getByRole("navigation", { name: "Python Fundamentals course list" });
        const items = rail.querySelectorAll("li");
        expect(items.length).toBe(3);
        expect(items[0]?.textContent).toContain("Git");
        expect(items[1]?.textContent).toContain("Just Enough Python");
        expect(items[2]?.textContent).toContain("Data Structures");
      });

      And("the current course is distinguished by a marker and weight, not by colour alone", () => {
        const current = screen.getByRole("link", { name: /Just Enough Python/i });
        expect(current.getAttribute("aria-current")).toBe("page");
        expect(current.textContent).toContain("▸");
        expect(current.className).toContain("font-semibold");
      });

      And("the rail offers a link back to the full path and to the whole course library", () => {
        expect(screen.getByRole("link", { name: /view full path/i })).toBeTruthy();
        expect(screen.getByRole("link", { name: /browse all courses/i })).toBeTruthy();
      });
    },
  );

  Scenario("The path rail collapses into the existing navigation drawer on a phone", ({ Given, When, Then, And }) => {
    let trigger: HTMLElement;

    Given("a reader opens a course in path context on a phone-width viewport", () => {
      mockPathname = "/en/learn/courses/just-enough-python";
      mockSearchParams = new URLSearchParams({ path: fixtureManifest.pathId });
    });

    When('they activate the path readout\'s "open path course list" control', () => {
      cleanup();
      render(
        <MobileNavOpenProvider>
          <PathBanner locale="en" pathTitle="Python Fundamentals" courseIndex={2} totalCourses={3} />
          <MobileNavConsumer />
        </MobileNavOpenProvider>,
      );
      trigger = screen.getByRole("button", { name: /Open path course list/i });
      fireEvent.click(trigger);
    });

    Then("the existing left navigation drawer opens showing that path's ordered courses", () => {
      expect(screen.getByRole("navigation", { name: "Python Fundamentals course list" })).toBeTruthy();
    });

    And("focus moves into the drawer and returns to the control when the drawer is dismissed", async () => {
      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });
      expect(document.activeElement).not.toBe(trigger);
      fireEvent.keyDown(document, { key: "Escape", code: "Escape" });
      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });
      expect(document.activeElement).toBe(trigger);
    });
  });
});
