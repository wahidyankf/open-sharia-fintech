/**
 * Permanent (308) redirects that strip the retired `/c/` content namespace
 * (`/{locale}/c/{section}/...`) back to the bare content URLs
 * (`/{locale}/{section}/...`) — de-namespacing (DD-48).
 *
 * INVERTED from this module's original direction: before DD-48 this module
 * moved bare URLs INTO `/c/`. Now it strips a stale `/c/`-prefixed bookmark
 * back to the bare form. **No rule below may ever gain a `/c/`-containing
 * destination** — doing so alongside this module's own source pattern would
 * recreate the exact infinite-308-loop hazard this inversion exists to
 * retire (`/en/learn/x` → `/en/c/learn/x` → `/en/learn/x`).
 *
 * One rule per locale + moved section, scoped with a `:path*` wildcard so that
 * loose top-level pages (`about-ayokoding`, `terms-and-conditions`, …), the
 * `/{locale}/tools` route, and the locale home are NOT matched — a blanket
 * `/{locale}/:path*` rule would wrongly swallow them.
 *
 * Section slugs are per-locale (the `id` library lives under `belajar`, not
 * `learn`); see the Locale Slug Asymmetry table in the plan tech-docs.
 *
 * `permanent: true` yields a method-preserving 308 that clients and search
 * engines cache. Spread into `next.config.ts` `redirects()` FIRST — every
 * other redirect module's rules pattern-match bare URLs only, so a
 * `/c`-prefixed request must be normalized by this module before any
 * downstream module gets a chance to see it.
 */
export const contentNamespaceRedirects: Array<{
  source: string;
  destination: string;
  permanent: boolean;
}> = [
  // en — moved sections: learn, rants
  { source: "/en/c/learn/:path*", destination: "/en/learn/:path*", permanent: true },
  { source: "/en/c/rants/:path*", destination: "/en/rants/:path*", permanent: true },
  // id — moved sections: belajar, celoteh, konten-video
  { source: "/id/c/belajar/:path*", destination: "/id/belajar/:path*", permanent: true },
  { source: "/id/c/celoteh/:path*", destination: "/id/celoteh/:path*", permanent: true },
  { source: "/id/c/konten-video/:path*", destination: "/id/konten-video/:path*", permanent: true },
];
