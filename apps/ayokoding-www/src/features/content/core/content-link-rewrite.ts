import path from "node:path";
import type { Locale } from "@/features/i18n/core/config";
import { contentUrl } from "./content-url";

/**
 * Content-tree-relative links authored in markdown bodies (e.g. `../../overview.md`,
 * `./beginner.md`, `../_index.md`) mirror the on-disk file tree per the repo's Linking
 * convention (relative paths with a literal `.md` extension). The rendered site uses a
 * different, clean-URL namespace (`/{locale}/c/{slug}`, no `.md`), so these links must be
 * resolved against the *current page's slug* and remapped through {@link contentUrl} before
 * they reach the browser — otherwise they ship as literal `href="../../overview.md"` and
 * 404 on click.
 */

const ABSOLUTE_HREF = /^(https?:|mailto:|tel:|\/|#)/i;

/**
 * Resolve one markdown-authored `href` against the current page's content slug.
 *
 * Returns `href` unchanged when it is already absolute (external URL, `mailto:`/`tel:`,
 * a site-root path, or an in-page anchor), when `context` is not provided (no slug to
 * resolve against), or when the relative target does not end in `.md` (not a content
 * link per the repo's Linking convention — e.g. an image or PDF asset). Otherwise
 * resolves the relative path against `context.slug`'s directory, strips the
 * `.md`/`_index` suffix the same way the content reader derives slugs from file paths,
 * and maps the result through {@link contentUrl}.
 */
export function resolveContentHref(href: string, context?: { locale: Locale; slug: string }): string {
  if (!context || ABSOLUTE_HREF.test(href)) {
    return href;
  }

  const [pathPart, hash] = splitHash(href);

  if (!pathPart.endsWith(".md")) {
    return href;
  }

  const currentDir = path.posix.dirname(`/${context.slug}`);
  const resolved = path.posix.normalize(path.posix.join(currentDir, pathPart));

  let slug = resolved.replace(/^\/+/, "").replace(/\.md$/, "");
  slug = slug.replace(/(^|\/)_index$/, "");

  const url = contentUrl(context.locale, slug);
  return hash ? `${url}${hash}` : url;
}

function splitHash(href: string): [string, string] {
  const hashIndex = href.indexOf("#");
  if (hashIndex === -1) return [href, ""];
  return [href.slice(0, hashIndex), href.slice(hashIndex)];
}
