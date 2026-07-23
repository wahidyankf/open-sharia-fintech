import type { Locale } from "@/features/i18n/core/config";
import { normalizeSlug } from "./slug";

/**
 * Map an on-disk content slug to its public URL — the single source of truth for
 * the content URL namespace.
 *
 * Rules (uniform bare join — DD-48 de-namespacing removed the `/c/`-prefix
 * branch this function used to have):
 * - empty / root / `_index` slug → `/{locale}` (the locale home)
 * - everything else → `/{locale}/{normalizeSlug(slug)}`
 *
 * Pure function — no IO. Every URL emitter (content page, sidebar tree,
 * breadcrumb, prev/next, search results, sitemap, feed) imports it so the rule
 * lives in exactly one place.
 *
 * @example contentUrl("en", "learn/software-engineering") // "/en/learn/software-engineering"
 * @example contentUrl("en", "about-ayokoding")            // "/en/about-ayokoding"
 * @example contentUrl("en", "")                            // "/en"
 */
export function contentUrl(locale: Locale, slug: string): string {
  const normalized = normalizeSlug(slug);

  if (normalized === "" || normalized === "_index") {
    return `/${locale}`;
  }

  return `/${locale}/${normalized}`;
}
