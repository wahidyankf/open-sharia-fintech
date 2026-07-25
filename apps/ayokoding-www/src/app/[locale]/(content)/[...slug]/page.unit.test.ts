import { describe, expect, it, vi } from "vitest";

vi.mock("@/lib/trpc/server", () => ({
  serverCaller: {
    content: {
      getBySlug: vi.fn().mockResolvedValue({
        title: "Software Engineering",
        description: "Learn SE",
        html: "<p>content</p>",
        headings: [],
        date: null,
        prev: null,
        next: null,
      }),
    },
  },
}));

vi.mock("@/features/app-shell/shell/trpc-init", () => ({
  createTRPCContext: () => ({
    contentService: { getIndex: async () => ({ contentMap: new Map() }) },
  }),
}));

// eslint-disable-next-line import/first
import { generateMetadata } from "./page";

// Carried over from the retired c/[...slug]/page.unit.test.ts (DD-48 route
// merge) — same assertions, updated for the uniform bare join (no /c/).
describe("generateMetadata", () => {
  it("sets canonical to the bare URL (DD-48 — no /c/ namespace)", async () => {
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "en", slug: ["learn", "software-engineering"] }),
    });
    expect(meta.alternates?.canonical).toBe("/en/learn/software-engineering");
  });

  it("includes alternates.languages with en and x-default", async () => {
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "en", slug: ["learn", "software-engineering"] }),
    });
    const langs = meta.alternates?.languages as Record<string, string> | undefined;
    expect(langs).toBeDefined();
    expect(langs?.["en"]).toBeDefined();
    expect(langs?.["x-default"]).toBeDefined();
  });

  it("returns 'Not Found' metadata when the slug does not resolve", async () => {
    const { serverCaller } = await import("@/lib/trpc/server");
    vi.mocked(serverCaller.content.getBySlug).mockRejectedValueOnce(new Error("not found"));
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "en", slug: ["does-not-exist"] }),
    });
    expect(meta.title).toBe("Not Found");
  });

  // Option C (Screen-4 design funnel, §3.4): noindex the whole legacy bucket
  // rather than adding an in-page landing-notice component.
  it("noindexes a legacy-bucket slug, still allowing crawlers to follow its links", async () => {
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "en", slug: ["learn", "legacy", "software-engineering"] }),
    });
    expect(meta.robots).toEqual({ index: false, follow: true });
  });

  it("does not noindex a non-legacy slug (e.g. under learn/courses)", async () => {
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "en", slug: ["learn", "courses", "some-course"] }),
    });
    expect(meta.robots).toBeUndefined();
  });

  it("titles a careers arc route (even a zero-manifest/empty-state one) with the arc slug, not a bare 'Not Found' (phase-5 EWT finding)", async () => {
    // `learn/paths/careers/<arc>` has no `_index.md` of its own (the arc is a synthetic grouping,
    // not a real content page), so `getBySlug` always rejects for it — live at
    // http://localhost:3101/en/learn/paths/careers/no-fixture-arc this fell through to a bare
    // "Not Found" tab title even though the page renders a 200 empty-state, not an error.
    const { serverCaller } = await import("@/lib/trpc/server");
    vi.mocked(serverCaller.content.getBySlug).mockRejectedValueOnce(new Error("not found"));
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "en", slug: ["learn", "paths", "careers", "no-fixture-arc"] }),
    });
    expect(meta.title).toBe("no-fixture-arc");
  });
});
