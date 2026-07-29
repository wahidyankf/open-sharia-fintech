// CONTENT — static (non-markdown) search docs (Rule-15 UWT-001 fix).
//
// The site's search index is built entirely from markdown `content/` files (see
// `shell/service.ts`'s `buildSearchIndexFromDocs`/`buildSearchIndexFromFiles`), which structurally
// excludes app-route pages that carry no markdown file at all — e.g. the Tools section
// (`/tools/ai-benchmark`, `/tools/cost-of-living-calculator`). A first-time user searching
// "benchmark", "AI model", "tool", or the Indonesian "tolok ukur" got zero matches for either tool,
// even though the Tools index links them prominently (a spec-blind usability finding).
//
// This is a small, explicit, hand-maintained list rather than a markdown file, because these pages
// are React route components, not content — but it reuses the SAME i18n strings the Tools index
// page itself already shows (`toolsPage*Link`/`toolsPage*Desc`), so there is no separate copy to
// keep in sync, and a bilingual doc set is produced with zero string duplication.
//
// No React, no fs, no side effects — pure over the locale list and the translation table.

import { SUPPORTED_LOCALES } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";

/** Structurally matches `shell/service.ts`'s `SearchDoc` (not imported, to keep this a pure core
 * module with no dependency on the `shell/` layer). */
export type StaticSearchDoc = {
  id: string;
  title: string;
  content: string;
  slug: string;
  locale: string;
};

type ToolEntry = { slug: string; titleKey: string; descKey: string };

/** Every app-route page that has no markdown file backing it, but should still be searchable. */
const TOOL_ENTRIES: readonly ToolEntry[] = [
  { slug: "tools/ai-benchmark", titleKey: "toolsPageAiBenchLink", descKey: "toolsPageAiBenchDesc" },
  { slug: "tools/cost-of-living-calculator", titleKey: "toolsPageCalcLink", descKey: "toolsPageCalcDesc" },
];

/** One `StaticSearchDoc` per (locale × tool entry) — appended onto the markdown-derived doc set. */
export function staticSearchDocs(): StaticSearchDoc[] {
  const docs: StaticSearchDoc[] = [];
  for (const locale of SUPPORTED_LOCALES) {
    for (const entry of TOOL_ENTRIES) {
      docs.push({
        id: `${locale}:${entry.slug}`,
        title: t(locale, entry.titleKey),
        content: t(locale, entry.descKey),
        slug: entry.slug,
        locale,
      });
    }
  }
  return docs;
}
