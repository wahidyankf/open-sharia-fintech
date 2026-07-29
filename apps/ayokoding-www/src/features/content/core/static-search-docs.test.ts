import { describe, expect, it } from "vitest";
import { t } from "@/features/i18n/core/translations";
import { staticSearchDocs } from "./static-search-docs";

// Regression test for Rule-15 UWT-001: the site's search index was built entirely from markdown
// `content/` files, so app-route pages with no markdown file (the Tools section) never appeared in
// search results for any query, including exact matches on the tool's own name. `staticSearchDocs`
// is the fix — a small, explicit, pure list of extra docs merged into the index by
// `shell/service.ts`.
describe("staticSearchDocs", () => {
  it("produces one doc per (locale x tool) pair", () => {
    const docs = staticSearchDocs();
    expect(docs).toHaveLength(4);
  });

  it("includes the AI benchmark tool for both locales, with slug matching its real route", () => {
    const docs = staticSearchDocs();
    const en = docs.find((d) => d.locale === "en" && d.slug === "tools/ai-benchmark");
    const id = docs.find((d) => d.locale === "id" && d.slug === "tools/ai-benchmark");

    expect(en).toBeDefined();
    expect(en?.title).toBe(t("en", "toolsPageAiBenchLink"));
    expect(en?.content).toBe(t("en", "toolsPageAiBenchDesc"));

    expect(id).toBeDefined();
    expect(id?.title).toBe(t("id", "toolsPageAiBenchLink"));
    expect(id?.content).toBe(t("id", "toolsPageAiBenchDesc"));
  });

  it("includes the cost-of-living calculator tool for both locales, with slug matching its real route", () => {
    const docs = staticSearchDocs();
    const en = docs.find((d) => d.locale === "en" && d.slug === "tools/cost-of-living-calculator");
    const id = docs.find((d) => d.locale === "id" && d.slug === "tools/cost-of-living-calculator");

    expect(en).toBeDefined();
    expect(en?.title).toBe(t("en", "toolsPageCalcLink"));

    expect(id).toBeDefined();
    expect(id?.title).toBe(t("id", "toolsPageCalcLink"));
  });

  it("gives each doc a unique, locale-prefixed id", () => {
    const docs = staticSearchDocs();
    const ids = docs.map((d) => d.id);
    expect(new Set(ids).size).toBe(ids.length);
    expect(ids).toContain("en:tools/ai-benchmark");
    expect(ids).toContain("id:tools/ai-benchmark");
  });
});
