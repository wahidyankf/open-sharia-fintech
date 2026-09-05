/**
 * Permanent (308) redirects that move the 37 re-homed course bundles (the 33
 * shipped `fundamentally-strong/software-engineer` topics + 4 existing capstones,
 * incl. `capstone-solid-core` per DD-20) from their legacy content path to their
 * canonical `courses/` location.
 *
 * `course-id === slug` — the re-home renames no directory, only its parent. This
 * module — never a `fundamentally-strong` prefix rule — owns that redirect
 * namespace (DD-43): the sibling `learn-three-bucket.ts` module carries no
 * `fundamentally-strong` rule at all, so the two rule sets are disjoint.
 *
 * `REHOMED_COURSE_SLUGS` is the single exported source of truth: every rule's
 * `source` and `destination` are derived from the same array element, so a slug
 * typo cannot produce a half-correct rule (mismatched source/destination pair).
 *
 * Each per-course rule is scoped with a `:path*` wildcard (maintainer decision,
 * 2026-07-23, broadening delivery.md §2.1(c)'s original exact-source design):
 * a bare exact-source rule only 308s the course's own root URL, leaving every
 * deep sub-page (`.../learning/beginner`, `.../drilling/kata-01`, …) — roughly
 * 520 pages across the 37 courses — to 404 after the `git mv`, a production
 * deep-link/SEO regression. `:path*` is Next.js's path-to-regexp "zero or more
 * segments" wildcard, so it matches BOTH the bare course root (`path` resolves
 * to an empty segment list) AND any deep sub-path, exactly like the existing
 * `contentNamespaceRedirects`' `/en/learn/:path*` rule already does for the
 * whole `learn` section (empirically verified against this exact Next.js
 * version: `curl -I http://localhost:3101/en/learn` — no trailing
 * segment — still 308s via that `:path*` rule). One wildcard rule per course
 * therefore fully replaces what would otherwise need two rules (an exact root
 * rule plus a separate `:path*` rule) per course.
 *
 * Next.js forwards the query string by default on a redirect, so a
 * `?path=`-carrying inbound link survives the move without extra code here.
 *
 * Spread into `next.config.ts` `redirects()` AFTER `contentNamespaceRedirects`
 * and `learnReorgRedirects`, and BEFORE `learnThreeBucketRedirects` — the
 * final converged order (DD-48); see the ordering comment in
 * `next.config.ts` for the full rationale.
 */
export const REHOMED_COURSE_SLUGS = [
  "advanced-algorithms",
  "advanced-networking",
  "advanced-sql-and-query-performance",
  "agentic-coding",
  "backend-essentials",
  "build-your-own-orm-and-query-builder",
  "capstone-first-working-software",
  "capstone-forge-ready",
  "capstone-full-stack-app",
  "capstone-solid-core",
  "computer-architecture",
  "computer-science-foundations",
  "concurrency-and-parallelism",
  "data-access-orms-and-query-builders",
  "data-structures-and-algorithms-essentials",
  "debugging-and-profiling",
  "engineering-management",
  "extending-neovim",
  "frontend-essentials",
  "functional-programming",
  "just-enough-bash",
  "just-enough-lua",
  "just-enough-nvim",
  "just-enough-python",
  "just-enough-typescript",
  "networking-essentials",
  "object-oriented-design-and-patterns",
  "object-oriented-programming-essentials",
  "programming-paradigms",
  "project-management",
  "security-essentials",
  "software-engineering-practices",
  "software-product-engineering",
  "software-testing",
  "sql-essentials",
  "technical-communication",
  "version-control-and-git",
] as const;

const perCourseRedirects: Array<{
  source: string;
  destination: string;
  permanent: boolean;
}> = REHOMED_COURSE_SLUGS.map((slug) => ({
  source: `/en/learn/fundamentally-strong/software-engineer/${slug}/:path*`,
  destination: `/en/learn/courses/${slug}/:path*`,
  permanent: true,
}));

/**
 * Q-E=C override (RESOLVED 2026-07-23): the three `fundamentally-strong` browse
 * roots are deleted (`git rm`) rather than updated in place — the one deviation
 * from this plan's "legacy `_index.md` UPDATED, never deleted" default (DD-19).
 * Their old URLs 308 to the course library landing so no URL goes bare-404.
 */
export const RETIRED_FUNDAMENTALLY_STRONG_ROOTS = [
  "/en/learn/fundamentally-strong",
  "/en/learn/fundamentally-strong/software-engineer",
  "/en/learn/fundamentally-strong/software-engineer/overview",
] as const;

const fundamentallyStrongRootRedirects: Array<{
  source: string;
  destination: string;
  permanent: boolean;
}> = RETIRED_FUNDAMENTALLY_STRONG_ROOTS.map((source) => ({
  source,
  destination: "/en/learn/courses",
  permanent: true,
}));

export const courseRehomeRedirects: Array<{
  source: string;
  destination: string;
  permanent: boolean;
}> = [...perCourseRedirects, ...fundamentallyStrongRootRedirects];

/**
 * Resolve the redirect destination for a concrete pathname using the same
 * source-of-truth rows exported to Next.js. This pure seam gives Unit tests a
 * faithful way to prove exact and `:path*` behaviour without starting a server.
 */
export function resolveCourseRehomeRedirect(pathname: string): string | null {
  for (const redirect of courseRehomeRedirects) {
    if (!redirect.source.endsWith("/:path*")) {
      if (pathname === redirect.source) return redirect.destination;
      continue;
    }

    const sourceRoot = redirect.source.slice(0, -"/:path*".length);
    if (pathname !== sourceRoot && !pathname.startsWith(`${sourceRoot}/`)) continue;

    const destinationRoot = redirect.destination.slice(0, -"/:path*".length);
    return `${destinationRoot}${pathname.slice(sourceRoot.length)}`;
  }
  return null;
}
