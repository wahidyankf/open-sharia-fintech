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

Added 2026-08-01 during the pre-execution readiness review:

- **Vercel's Spend Management amount meters spend _beyond_ the plan credit, not gross usage.**
  Verbatim: "covers metered resources that go beyond your Pro plan credits and usage allocation."
  An earlier draft of this plan reasoned that $10 was "well inside the $20 credit" — exactly
  backwards; $10 is $10 _past_ the credit, i.e. a $30 invoice. Any budget arithmetic that mixes the
  spend threshold with the dashboard's Infrastructure Subtotal is comparing a post-credit number to
  a pre-credit one. Possible home: a reference note on Vercel billing arithmetic.
- **A check that silently observes nothing still exits 0** — and reads as a pass. This review found
  four instances of the class in one plan: a test path matching no vitest include glob; a gate
  invoking an `nx` target that does not exist (declared only in `targetDefaults`, which merges into
  existing targets and never creates one); build-output assertions routed through a cached target
  with no `dependsOn: ["build"]`; and an acceptance clause whose stated pre-state (10 hits) did not
  match reality (9), so its "falsifiable both ways" check failed in the "before" direction. Possible
  home: the testing/verification guidance, generalising the existing "dev-mode is not evidence" and
  UGREP `-L` rules into one "prove the check can fail" standard.
