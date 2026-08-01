# Business Requirements — Vercel Function Cost Reduction

## Business goal

Keep the monthly Vercel invoice **at or below $30**, permanently, while keeping every public site
fully functional and indexable.

The Pro platform fee of $20/month includes $20/month of usage credit that applies to Managed
Infrastructure resources. Vercel charges usage against that credit before switching to on-demand
billing, so `invoice = 20 + max(0, gross_metered_usage − 20)`. The owner's ceiling of **$30/month
total** therefore permits up to $10/month of on-demand charge on top of the subscription.

Three tiers, all stated as **gross** metered usage — the figure the dashboard reports as the
Infrastructure Subtotal:

- **Hard ceiling (owner-set)**: gross metered usage stays **at or below $30/month**, so the invoice
  never exceeds $30. Breaching this is a failure of the plan.
- **Target**: gross metered usage stays **below $20/month**, so the credit absorbs all of it and the
  on-demand charge is $0.00 — the invoice sits at exactly $20.00.
- **Stretch**: gross metered usage stays **below $10/month**, leaving 50% headroom inside the credit
  so a traffic spike or a crawler surge cannot push the invoice off the subscription at all.

The ceiling is what the spend cap enforces mechanically; the target is what the engineering work is
sized to reach. They are different numbers on purpose — a cap you are expected to hit is not a cap.

## Business impact

Measured baseline (2026-07-30, four days into the Jul 26 – Aug 26 cycle):

| Line item                          | 4-day usage  | 4-day charge | Derived unit rate | ~Monthly gross |
| ---------------------------------- | ------------ | ------------ | ----------------- | -------------- |
| Functions → **Function Duration**  | 27.04 GB-Hrs | **$4.87**    | $0.180 / GB-Hr    | **~$36**       |
| Observability → Events             | 1.08M        | $1.30        | $1.204 / M        | ~$10           |
| CDN → Edge Middleware Invocations  | 342.79K      | $0.65        | $1.90 / M         | ~$5            |
| Functions → Fast Origin Transfer   | 4 GB         | $0.40        | $0.10 / GB        | ~$3            |
| Functions → Function Invocations   | 341.26K      | $0.20        | $0.586 / M        | ~$1.50         |
| CDN → Edge Requests                | 384.41K      | $0.00        | 10M included      | $0             |
| CDN → Fast Data Transfer           | 3 GB         | $0.00        | 1 TB included     | $0             |
| Build & Deploy → Build CPU Minutes | 6 hours      | $0.00        | included          | $0             |
| **Infrastructure subtotal**        | —            | **$7.43**    | —                 | **~$57**       |

At ~$57/month gross against a $20 credit, the business is exposed to roughly **$37/month of
on-demand overage** — the invoice runs at ~$57/month against a **$30 ceiling**, i.e. roughly **$27
over the maximum** the owner has authorised, and $37 over the flat subscription.

Two derived diagnostics quantify the failure mode:

- **89%** of all requests invoke middleware (342.79K middleware ÷ 384.41K edge requests).
- **0.285 GB-s per invocation** (27.04 GB-Hrs ÷ 341.26K). These are genuine renders, not cheap
  cache hits — consistent with a site where nothing is prerendered.

## Affected roles

| Role                       | Impact                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Site owner (billing payer) | Invoice capped at $30 and targeted at the flat $20 subscription; gains a spend cap and alerting that does not exist today |
| Readers of ayokoding.com   | Substantially faster page loads — CDN-cached static HTML instead of a cold function rendering 70 MB of markdown           |
| Readers of wahidyankf.com  | Same: three routes move from uncached per-request rendering to CDN-cached static                                          |
| Search engines / crawlers  | Gain a `robots.txt` and `sitemap.xml` on wahidyankf.com, which currently has neither                                      |
| AI scrapers                | Denied at the firewall, before the billing meter                                                                          |

## Business-level success metrics

| Metric                                                              | Baseline (2026-07-30) | Target                                                  |
| ------------------------------------------------------------------- | --------------------- | ------------------------------------------------------- |
| Gross metered infrastructure usage per month                        | ~$57                  | **<= $30** ceiling; **< $20** target; **< $10** stretch |
| On-demand charge above the subscription per month                   | ~$37                  | **<= $10.00** ceiling; **$0.00** target                 |
| Monthly invoice total                                               | ~$57                  | **<= $30.00** ceiling; **$20.00** target                |
| Configured Spend Management amount (post-credit, not gross)         | none                  | **$10**, with the pause action armed                    |
| Prerendered pages in the `apps/ayokoding-www` build                 | 4 (none a page)       | `>= 2,000` (2,183 content files today, still growing)   |
| `x-vercel-cache` on a repeat request to a content page              | `MISS`                | `HIT`                                                   |
| Dynamic (`ƒ`) routes in the `apps/wahidyankf-www` build route table | 3 of 4                | 0 of 4                                                  |
| A configured spend cap with an automatic pause action               | none                  | enabled                                                 |

## Business-scope non-goals

- **Not** downgrading from Pro to Hobby. Pro is deliberately retained; the goal is to live inside
  its included credit, not to leave the plan.
- **Not** reducing published content, page count, or site features to save money. All **2,183**
  content files stay live, and the count is expected to keep growing under the `ayokoding-learning-path-*`
  plans — the cost fix must scale with content, not cap it.
- **Not** accepting degraded search visibility in exchange for cost. Any measure that risks
  indexability carries a mandatory verification step and a documented rollback.
- **Not** optimising build minutes as a cost centre — they currently bill $0.00. The one build-side
  change in scope removes pure waste (a daily rebuild of an unchanged project), not a cost overage.

## Business risks and mitigations

| Risk                                                                                                         | Severity | Mitigation                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enabling Bot Protection challenges a legitimate crawler and search rankings drop                             | HIGH     | Documentation does not confirm that verified crawlers such as Googlebot are auto-allowlisted. Phase 0 carries a mandatory indexability smoke-test and a one-toggle rollback                                                                   |
| Spend Management is not a true hard cap — checks run every few minutes, so usage can overshoot the threshold | MEDIUM   | Threshold set at $10 (post-credit) with the "pause production deployment" action armed. The full allowance is used with no lag margin, a deliberate owner decision recorded as DD-9                                                           |
| The armed pause takes every production site down mid-cycle before the fix lands                              | HIGH     | Expected, not accidental: at the pre-fix burn rate the cap trips around day 16 and each project must be resumed manually. This is the schedule pressure that makes Phases 1–4 urgent, and the reason Phase 0's platform wins are banked first |
| Promoting the root layout is a structural change that could break every page at once                         | MEDIUM   | Isolated to its own phase with a full `next build` gate and a live smoke-test before the delivery boundary; rollback is a single revert commit                                                                                                |
| The Pro credit may not cover Observability Plus (Vercel's own docs are internally inconsistent)              | LOW      | Rendered moot: Observability Plus is being disabled outright, removing the ambiguity along with the ~$10/month                                                                                                                                |
| Three concurrent worktrees trip the known `nx affected` cross-worktree contamination issue                   | LOW      | Documented in a filed two-pager; keep each worktree's tree clean and commit promptly                                                                                                                                                          |
| Traffic genuinely grows and costs rise again later                                                           | LOW      | The stretch target (< $10) exists precisely to absorb growth; the spend cap provides the backstop                                                                                                                                             |
