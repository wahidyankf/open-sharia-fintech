/**
 * Permanent (308) redirects that move each of the six relocated learn-section
 * domains (`software-engineering`, `artificial-intelligence`,
 * `information-security`, `personal-development`, `it-governance`, `business`)
 * from its former top-level position under `/en/learn/` to its new address
 * under the `legacy/` bucket (DD-41/DD-42, three-bucket learn-section IA).
 *
 * **Single tier, six rules — no `/c`-form tier.** An earlier design considered
 * doubling this to 12 rules (a bare tier plus a `/c`-prefixed tier), but that
 * second tier would be unreachable dead code once `content-namespace.ts`'s
 * DD-48 inversion is wired FIRST in `next.config.ts`: any `/c/`-prefixed
 * request is already stripped to its bare form before this module's rules
 * ever run, so a `/c`-prefixed rule here could never match a live request.
 *
 * **Blanket-source ban (DD-42).** No rule here may ever have `source` equal
 * to `/en/learn/:path*` — a blanket rule at that shape would swallow every
 * URL under `/en/learn/`, including the `courses/` and `paths/` buckets this
 * module must never touch, plus the `fundamentally-strong` legacy course
 * prefix that `course-rehome.ts` alone owns (DD-43). Deriving every rule from
 * `RELOCATED_DOMAINS` (rather than six hand-written literals) means this
 * module structurally cannot also contain that blanket rule, or a rule
 * shadowing `courses`, `paths`, or `fundamentally-strong`, or a rule whose
 * source or destination contains a `/c/` segment (loop-safety invariant,
 * DD-48) — the array only ever produces `/en/learn/<domain>/:path*` shapes
 * for the six named domains.
 *
 * Spread into `next.config.ts` `redirects()` LAST, after `contentNamespaceRedirects`,
 * `learnReorgRedirects`, and `courseRehomeRedirects` — the more specific
 * per-course rules in `courseRehomeRedirects` must win before this module's
 * broader per-domain wildcard ever evaluates (DD-48, re-derived order).
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
}> = RELOCATED_DOMAINS.map((domain) => ({
  source: `/en/learn/${domain}/:path*`,
  destination: `/en/learn/legacy/${domain}/:path*`,
  permanent: true,
}));
