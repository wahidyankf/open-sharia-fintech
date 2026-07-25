import { describe, expect, it } from "vitest";
import { ContentService } from "./service";
import type { ContentRepository } from "../core/repository";
import type { ContentMeta } from "../core/types";

/**
 * Regression: the course-paths plan's Phase 3 e2e run surfaced a real, previously-undetected race
 * in `ContentService.getIndex()`. Its lazy-build guard (`if (!this.contentIndex) { ... }`) is
 * synchronous-check / asynchronous-fill, so multiple callers that all arrive before the very first
 * build resolves (a routine event under Playwright's multi-worker, multi-project concurrent load,
 * where several requests hit the shared server before its content index is warm) each independently
 * trigger their own full `buildContentIndex()` — whichever finishes LAST silently overwrites the
 * cached index for the lifetime of the process. If that last-finishing build ever raced against
 * transient resource pressure (many concurrent full-tree scans opening file handles at once) and
 * came back incomplete, every subsequent request — including totally unrelated ones — would see a
 * permanently wrong, silently-degraded content index for as long as the server keeps running.
 */
function makeFakeRepository(readAllContent: () => Promise<ContentMeta[]>): ContentRepository {
  return {
    readAllContent,
    readFileContent: async () => ({ content: "", frontmatter: {} }),
  };
}

describe("ContentService.getIndex — concurrent build deduplication", () => {
  it("builds the content index only once when multiple callers request it concurrently before the first build resolves", async () => {
    let callCount = 0;
    const repo = makeFakeRepository(async () => {
      callCount++;
      await new Promise((resolve) => setTimeout(resolve, 10));
      return [];
    });
    const service = new ContentService(repo);

    const [a, b, c] = await Promise.all([service.getIndex(), service.getIndex(), service.getIndex()]);

    expect(callCount).toBe(1);
    expect(a).toBe(b);
    expect(b).toBe(c);
  });

  it("still returns a usable index after the single in-flight build resolves (later callers hit the warm cache)", async () => {
    let callCount = 0;
    const repo = makeFakeRepository(async () => {
      callCount++;
      return [];
    });
    const service = new ContentService(repo);

    await service.getIndex();
    await service.getIndex();

    expect(callCount).toBe(1);
  });
});
