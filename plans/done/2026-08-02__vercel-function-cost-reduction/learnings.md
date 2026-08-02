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

Added 2026-08-01 during Phase 0 execution:

- **A probe that spoofs an identity cannot test a control that verifies identity.** The plan's
  indexability smoke-test fetched a page with a Googlebot `User-Agent` and expected `200`. But
  Vercel's verified-bot exclusion is decided by source IP and reverse DNS, so a `curl` claiming to
  be Googlebot **is** an unverified bot and challenging it is correct behaviour. The probe could
  therefore only ever fail, whatever the firewall did — it could not distinguish "correctly
  configured" from "switched off entirely". The fix was to add a **deny-side** probe: assert search
  crawlers get `200` **and** AI-bot UAs get `403` in the same run, so the test has a passing state
  and a failing state that mean different things. This is the same defect as the four above, in a
  new dress: **a one-sided check is not a check**. Possible home: the same "prove the check can
  fail" standard, as the identity-spoofing corollary.
- **Vercel's Bot Protection "Challenge" mode gates any client that cannot execute JavaScript, not
  just bot-shaped traffic.** With it on, a Chrome-140 `User-Agent` control was challenged alongside
  `robots.txt` and `sitemap.xml` — all returning `HTTP/2 429` with a `Vercel Security Checkpoint`
  body. Real browsers solve the challenge and proceed, so human traffic is fine, but every non-JS
  consumer is not: crawlers, feed readers, link checkers, uptime monitors, social-card unfurlers.
  For a content site whose value is organic search, that risk dwarfs the cost saving. **AI Bots =
  Deny is the half worth keeping** — verified as live by GPTBot and ClaudeBot both returning `403`
  while Googlebot and Bingbot returned `200`. This qualifies the planning-time note above that the
  WAF "mitigates before the billing meter": true, but the two rulesets are not interchangeable, and
  only one of them is safe to leave on unattended. Possible home: the Vercel billing/ops reference
  note, together with the Spend Management entry.
- **`generateStaticParams` running is not evidence that anything is prerendered.** The
  `ayokoding-www` build logs `✓ Generating static pages using 11 workers (2103/2103) in 3.8min`,
  then emits exactly **one** HTML file and marks all nine routes `ƒ`. Next.js renders every page
  and discards the output when a dynamic API in the root layout forces on-demand rendering. A build
  log that looks like success is not success — only `.next/prerender-manifest.json` and the route
  table's `○`/`ƒ` markers are. Possible home: the same Next.js guidance as the root-layout entry
  above; the two are halves of one lesson.
- **A "dashboard setting" in a plan step is an assumption about who serves the hostname, and it
  should be verified before the step is written.** Step 0.9 called the apex-redirect HTTPS
  downgrade "a Vercel domain setting". One `dig` showed the apex on Squarespace A records with
  `server: Squarespace`, while only `www` is CNAME'd to Vercel — so Vercel never sees the offending
  hop and no Vercel setting could fix it. Cost: a `[HUMAN]` step scoped to the wrong console.
  Possible home: the planning guidance, as a "verify the control plane before assigning the step"
  rule.

Added 2026-08-02 during Phase 4 production verification:

- **A plan cannot disable the only aggregate telemetry source before scheduling a required
  post-deploy aggregate comparison.** The completed Observability Plus shutdown correctly removes
  the paid metrics surface, but the later 24-hour runtime-log requirement still asks for its
  function, middleware, route, and status-code aggregates. Vercel's base runtime-log endpoint
  streams live deployment logs only; it cannot recreate the requested historical aggregation.
  Possible home: the plan-making guidance as a dependency-order rule — collect all required
  post-deploy telemetry before disabling the product that supplies it, or make the later check an
  explicit successor-plan task.

## Triage — 2026-08-02

Both safety gates passed for the surviving entries: this log contains no credentials or private
infrastructure details, and every retained route belongs to `ose-public`.

| Candidate learning                                             | Terminal state                                                                                                                                                  |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Legacy-versus-Fluid billing vocabulary                         | Routed to the existing [steady-state successor](../../backlog/vercel-cost-steady-state-verification/README.md), which owns the completed-cycle line-item check. |
| Dynamic locale-root APIs defeat static generation              | Routed inline to `apps/ayokoding-www/README.md` and the current static-delivery regression coverage.                                                            |
| Production `next build` is required Suspense evidence          | Routed inline to the same app guide and current build/manifest checks.                                                                                          |
| WAF rules can reduce metered traffic                           | Discarded: provider behaviour and current pricing cannot be made into a repository-owned automatic guard; the successor retains the platform-state review.      |
| Spend Management pause action lags                             | Discarded: the provider-specific timing fact does not yield an automatic repository guard; its configured threshold remains an owner-side control.              |
| A check can pass while observing nothing                       | Folded into [acceptance-clause-vacuity](../../ideas/acceptance-clause-vacuity.md), including the telemetry-order example.                                       |
| A spoofed identity cannot test an identity-verifying control   | Folded into [acceptance-clause-vacuity](../../ideas/acceptance-clause-vacuity.md).                                                                              |
| `generateStaticParams` logs do not prove output is static      | Routed inline to the app guide and current route-table/prerender-manifest checks.                                                                               |
| A dashboard action can be assigned to the wrong control plane  | Folded into [acceptance-clause-vacuity](../../ideas/acceptance-clause-vacuity.md).                                                                              |
| Aggregate telemetry was disabled before a later aggregate gate | Folded into [acceptance-clause-vacuity](../../ideas/acceptance-clause-vacuity.md); the successor carries the deliberately deferred measurement.                 |

### Open question carried forward

The projected reduction from approximately **$57/month to $2–4/month** remains **unverified at
archival**. The measured projection rows are Observability (−$10) and middleware (−$5); the largest
static-conversion row (−$30) is estimated. The
[`vercel-cost-steady-state-verification`](../../backlog/vercel-cost-steady-state-verification/README.md)
plan owns the full-cycle reconciliation and is the only plan that may close this question.
