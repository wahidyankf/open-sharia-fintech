<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: vercel-function-cost-reduction

Candidate entries identified during planning (2026-07-30), to be confirmed or discarded during
execution:

- Vercel's billing model is readable from line-item **names** alone: "Function Duration" in GB-Hrs
  plus a standalone priced "Edge Middleware Invocations" line exist only in the legacy pre-Fluid
  vocabulary. Possible home: a new reference doc or an idea two-pager.
- A dynamic API (`headers()`, `cookies()`) called in a **root** layout forfeits static generation for
  the entire app; the documented fix for a multilingual site is to delete `app/layout.tsx` and let
  `app/[locale]/layout.tsx` become the root layout. Possible home: the Next.js/web-app development
  guidance under `repo-governance/development/`.
- `next build` is the only valid evidence that a `useSearchParams()` call is correctly wrapped in
  `<Suspense>` — the dev server hides a missing boundary, and production builds fail on it. Possible
  home: the testing/verification guidance, as a "dev-mode is not evidence" rule.
- Vercel's WAF mitigates **before** the billing meter, which makes the free Bot Protection and AI
  Bots rulesets a cost-control mechanism rather than only a security one.
- Spend Management's "pause production deployment" action is off by default and its checks lag by
  minutes, so the threshold must be set below the true ceiling.
