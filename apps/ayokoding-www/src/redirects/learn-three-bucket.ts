/**
 * Permanent (308) redirects that move each of the six relocated learn-section
 * domains (`software-engineering`, `artificial-intelligence`,
 * `information-security`, `personal-development`, `it-governance`, `business`)
 * from its former top-level position under `/en/learn/` to its new address
 * under the `legacy/` bucket (DD-41/DD-42, three-bucket learn-section IA).
 *
 * **Two rules per domain — exact bare, then wildcard (EWT-001 single-hop fix).**
 * Each domain gets an exact bare rule (`/en/learn/<domain>` -> no `:path*`, no
 * trailing slash) immediately followed by its wildcard rule
 * (`/en/learn/<domain>/:path*`). Next.js redirects are first-match-wins, so
 * ordering the exact rule first matters: a bare top-level request like
 * `/en/learn/software-engineering` matches the exact rule and redirects in a
 * single 308 hop. Without it, the wildcard alone expands `:path*` to a
 * trailing slash on the bare request, and the site's `trailingSlash: false`
 * normalization then strips that slash in a second 308 — the double-hop
 * defect this pair of rules exists to prevent. Nested paths (non-empty
 * `:path*`) already matched the wildcard rule in one hop and are unaffected.
 *
 * **No `/c`-form tier.** An earlier design considered a third, `/c`-prefixed
 * tier, but that tier would be unreachable dead code once `content-namespace.ts`'s
 * DD-48 inversion is wired FIRST in `next.config.ts`: any `/c/`-prefixed
 * request is already stripped to its bare form before this module's rules
 * ever run, so a `/c`-prefixed rule here could never match a live request.
 *
 * **Blanket-source ban (DD-42).** No rule here may ever have `source` equal
 * to `/en/learn/:path*` — a blanket rule at that shape would swallow every
 * URL under `/en/learn/`, including the `courses/` and `paths/` buckets this
 * module must never touch, plus the `fundamentally-strong` legacy course
 * prefix that `course-rehome.ts` alone owns (DD-43). Deriving every rule from
 * `RELOCATED_DOMAINS` (rather than twelve hand-written literals) means this
 * module structurally cannot also contain that blanket rule, or a rule
 * shadowing `courses`, `paths`, or `fundamentally-strong`, or a rule whose
 * source or destination contains a `/c/` segment (loop-safety invariant,
 * DD-48) — the array only ever produces `/en/learn/<domain>` and
 * `/en/learn/<domain>/:path*` shapes for the six named domains.
 *
 * Spread into `next.config.ts` `redirects()` LAST, after `contentNamespaceRedirects`,
 * `learnReorgRedirects`, and `courseRehomeRedirects` — the more specific
 * per-course rules in `courseRehomeRedirects` must win before this module's
 * broader per-domain rules ever evaluate (DD-48, re-derived order).
 */
export const RELOCATED_DOMAINS = [
  "software-engineering",
  "artificial-intelligence",
  "information-security",
  "personal-development",
  "it-governance",
  "business",
] as const;

export const learnThreeBucketRedirects: Array<{
  source: string;
  destination: string;
  permanent: boolean;
}> = RELOCATED_DOMAINS.flatMap((domain) => [
  {
    source: `/en/learn/${domain}`,
    destination: `/en/learn/legacy/${domain}`,
    permanent: true,
  },
  {
    source: `/en/learn/${domain}/:path*`,
    destination: `/en/learn/legacy/${domain}/:path*`,
    permanent: true,
  },
]);
