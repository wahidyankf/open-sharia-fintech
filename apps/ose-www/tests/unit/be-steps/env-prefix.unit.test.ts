/**
 * Tests that ose-www reads prefixed env vars (OSE_WEB_*) not bare names.
 * RED: fails before renaming process.env.SHOW_DRAFTS → process.env.OSE_WEB_SHOW_DRAFTS
 * GREEN: passes after the rename in service.ts
 */
import { vi, describe, it, expect, afterEach } from "vitest";

// createEnv snapshots process.env at module load time; mock it with a live Proxy
// so that per-test process.env mutations are visible to the service.
vi.mock("@/env", () => ({
  env: new Proxy({} as Record<string, string | undefined>, {
    get: (_, key: string) => process.env[key],
  }),
}));
import { InMemoryContentRepository } from "@/features/content/core/repository-memory";
import { ContentService } from "@/features/content/shell/service";

afterEach(() => {
  delete process.env["OSE_WEB_SHOW_DRAFTS"];
});

describe("ose-www env var prefix: OSE_WEB_SHOW_DRAFTS", () => {
  it("includes draft posts when OSE_WEB_SHOW_DRAFTS=true", async () => {
    const repo = new InMemoryContentRepository([
      {
        meta: {
          title: "Draft Post",
          slug: "updates/draft-env-test",
          date: new Date(),
          draft: true,
          tags: [],
          summary: "Draft summary",
          weight: 0,
          isSection: false,
          filePath: "/mock/updates/draft-env-test.md",
          readingTime: 1,
          category: "updates",
        },
        content: "## Draft\n\nDraft content.",
      },
    ]);
    const service = new ContentService(repo);

    // Set only the prefixed name (OSE_WEB_SHOW_DRAFTS) — bare names not read by source
    process.env["OSE_WEB_SHOW_DRAFTS"] = "true";

    const updates = await service.listUpdates();
    expect(updates.some((u) => u.draft)).toBe(true);
  });

  it("excludes draft posts when OSE_WEB_SHOW_DRAFTS is not set", async () => {
    const repo = new InMemoryContentRepository([
      {
        meta: {
          title: "Draft Post",
          slug: "updates/draft-env-test-2",
          date: new Date(),
          draft: true,
          tags: [],
          summary: "Draft summary",
          weight: 0,
          isSection: false,
          filePath: "/mock/updates/draft-env-test-2.md",
          readingTime: 1,
          category: "updates",
        },
        content: "## Draft\n\nDraft content.",
      },
    ]);
    const service = new ContentService(repo);

    // Neither set
    const updates = await service.listUpdates();
    expect(updates.some((u) => u.draft)).toBe(false);
  });
});
