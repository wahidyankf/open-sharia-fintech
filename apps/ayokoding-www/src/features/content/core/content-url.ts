import type { Locale } from "@/features/i18n/core/config";
import { normalizeSlug } from "./slug";

/**
 * Map an on-disk content slug to its public URL — the single source of truth for
 * the content URL namespace.
 *
 * Rules (uniform bare join — DD-48 de-namespacing removed the namespace-prefix
 * branch this function used to have):
 * - empty / root / `_index` slug → `/{locale}` (the locale home)
 * - everything else → `/{locale}/{normalizeSlug(slug)}`
 *
 * An optional `pathId` (course-paths plan, cycle 2.4) appends `?path=<path-id>` to whichever of
 * the above the first two arguments already produce — additive only, every existing return shape
 * is unchanged when `pathId` is omitted.
 *
 * Pure function — no IO. Every URL emitter (content page, sidebar tree,
 * breadcrumb, prev/next, search results, sitemap, feed) imports it so the rule
 * lives in exactly one place.
 *
 * @example contentUrl("en", "learn/software-engineering") // "/en/learn/software-engineering"
 * @example contentUrl("en", "about-ayokoding")            // "/en/about-ayokoding"
 * @example contentUrl("en", "")                            // "/en"
 * @example contentUrl("en", "learn/courses/x", "careers/interview-ready/software-engineer")
 *          // "/en/learn/courses/x?path=careers/interview-ready/software-engineer"
 */
export function contentUrl(locale: Locale, slug: string, pathId?: string): string {
  const normalized = normalizeSlug(slug);

  const base = normalized === "" || normalized === "_index" ? `/${locale}` : `/${locale}/${normalized}`;

  return pathId === undefined ? base : `${base}?path=${pathId}`;
}
