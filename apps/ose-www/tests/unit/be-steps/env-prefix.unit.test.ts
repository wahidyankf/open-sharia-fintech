/**
 * Unit proof for the injected draft-visibility policy. The production composition root translates
 * OSE_WEB_SHOW_DRAFTS into this boolean; Unit never mutates the real process environment.
 */
import { describe, it, expect } from "vitest";
import { InMemoryContentRepository } from "@/features/content/core/repository-memory";
import { ContentService } from "@/features/content/shell/service";

describe("ose-www draft visibility policy", () => {
  it("includes draft posts when the injected policy enables drafts", async () => {
    const repo = new InMemoryContentRepository([
      {
        meta: {
          title: "Draft Post",
          slug: "updates/draft-env-test",
          date: new Date("2026-01-01T00:00:00Z"),
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
    const service = new ContentService(repo, undefined, { showDrafts: true });

    const updates = await service.listUpdates();
    expect(updates.some((u) => u.draft)).toBe(true);
  });

  it("excludes draft posts when the injected policy disables drafts", async () => {
    const repo = new InMemoryContentRepository([
      {
        meta: {
          title: "Draft Post",
          slug: "updates/draft-env-test-2",
          date: new Date("2026-01-01T00:00:00Z"),
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
    const service = new ContentService(repo, undefined, { showDrafts: false });
    const updates = await service.listUpdates();
    expect(updates.some((u) => u.draft)).toBe(false);
  });
});
