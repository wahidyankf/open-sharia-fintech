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
});
