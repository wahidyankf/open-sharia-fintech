/**
 * Slug normalization shared by the widened `[...slug]` content catch-all
 * route (which now serves the full content tree — the retired `c/[...slug]`
 * route was merged into it, DD-48) and by
 * {@link import("./content-url").contentUrl}.
 *
 * Pure functions — no IO.
 */

/**
 * Normalize a content slug string: trim, collapse internal whitespace away by
 * stripping a single leading and trailing slash. Returns a canonical
 * `a/b/c` (or `""`) form. The empty string represents the locale root.
 */
export function normalizeSlug(slug: string): string {
  return slug.trim().replace(/^\/+/, "").replace(/\/+$/, "");
}

/**
 * Join a Next.js catch-all `slug` array segment into the canonical bare content
 * slug. Empty / undefined arrays collapse to the root slug `""`.
 *
 * The captured segments are the bare content slug directly (no namespace
 * prefix to strip, DD-48), so this is a plain normalized join.
 */
export function slugFromSegments(segments: string[] | undefined): string {
  if (!segments || segments.length === 0) return "";
  return normalizeSlug(segments.join("/"));
}
