# Business Requirements — Vercel Function Cost Reduction

## Business goal

Keep the monthly Vercel invoice **at or below $30**, permanently, while keeping every public site
fully functional and indexable — with a platform-enforced backstop at **$35** so a runaway cannot
climb indefinitely.

The Pro platform fee of $20/month includes $20/month of usage credit that applies to Managed
Infrastructure resources. Vercel charges usage against that credit before switching to on-demand
billing, so `invoice = 20 + max(0, gross_metered_usage − 20)`. The owner's goal of **$30/month
total** therefore permits up to $10/month of on-demand charge on top of the subscription, and the
armed spend cap allows $15 before it intervenes.

Four numbers, all stated as **gross** metered usage — the figure the dashboard reports as the
Infrastructure Subtotal — except the spend cap, which is the one post-credit number:

- **Budget goal (owner-set, advisory)**: gross metered usage stays **at or below $30/month**, so the
  invoice never exceeds $30. This is the number the plan is sized to hold. It is **not mechanically
  enforced** — see the backstop below.
- **Enforced worst case (backstop)**: the Vercel spend cap is armed at **$15 of on-demand charge**,
  i.e. gross $35 / an invoice of**$35**. It sits $5 above the goal so it fires only on a genuine
  runaway rather than on an ordinary overrun. **The cap stops catastrophe, not overspend**, and the
  accepted cost is that a quiet month can reach $35 without it ever intervening.
- **Target**: gross metered usage stays **below $20/month**, so the credit absorbs all of it and the
  on-demand charge is $0.00 — the invoice sits at exactly $20.00.
- **Stretch**: gross metered usage stays **below $10/month**, leaving 50% headroom inside the credit
  so a traffic spike or a crawler surge cannot push the invoice off the subscription at all.

Holding $30 is the engineering work's job; the cap's job is only to bound the disaster. They are
different numbers on purpose — a cap you are expected to hit is not a cap, it is an outage schedule.

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

**Superseded 2026-08-01 — the working baseline is now ~$43/month, not ~$57.** A second dashboard
reading of the same cycle, taken 2 days later over a 7-day window instead of a 4-day one, shows
**$9.79 of the $20 credit consumed with $0.00 on-demand**, a rate of **$1.399/day → ~$43/month
gross**. The table above is retained as the dated 2026-07-30 measurement; it over-projected because
a 4-day window is too short to extrapolate from. Full detail in
[evidence/baseline-per-project.md](./evidence/baseline-per-project.md).

At ~$43/month gross against a $20 credit, the business is exposed to roughly **$23/month of
on-demand overage** — an invoice around $43 against the **$30 goal**, i.e. roughly **$13 over the
budget** and $23 over the flat subscription. It is also **above the $35 armed cap**, so at this rate
the cap fires before the cycle closes. The revision lowers the magnitude of the problem; it does not
change any decision in the plan, since $43 still misses the goal, still overruns the credit, and
still trips the backstop.

Two derived diagnostics quantify the failure mode:

- **89%** of all requests invoke middleware (342.79K middleware ÷ 384.41K edge requests).
- **0.285 GB-s per invocation** (27.04 GB-Hrs ÷ 341.26K). These are genuine renders, not cheap
  cache hits — consistent with a site where nothing is prerendered.

## Affected roles

| Role                       | Impact                                                                                                                                       |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Site owner (billing payer) | Invoice targeted at the flat $20 subscription, budgeted at $30, backstopped at $35; gains a spend cap and alerting that does not exist today |
| Readers of ayokoding.com   | Substantially faster page loads — CDN-cached static HTML instead of a cold function rendering 70 MB of markdown                              |
| Readers of wahidyankf.com  | Same: three routes move from uncached per-request rendering to CDN-cached static                                                             |
| Search engines / crawlers  | Gain a `robots.txt` and `sitemap.xml` on wahidyankf.com, which currently has neither                                                         |
| AI scrapers                | Denied at the firewall, before the billing meter                                                                                             |

## Business-level success metrics

| Metric                                                              | Baseline (2026-08-01) | Target                                                |
| ------------------------------------------------------------------- | --------------------- | ----------------------------------------------------- |
| Gross metered infrastructure usage per month                        | ~$43 (was ~$57)       | **<= $30** goal; **< $20** target; **< $10** stretch  |
| On-demand charge above the subscription per month                   | ~$23 (was ~$37)       | **<= $10.00** goal; **$0.00** target; $15 cap armed   |
| Monthly invoice total                                               | ~$43 (was ~$57)       | **<= $30.00** goal; **$35.00** enforced worst case    |
| Configured Spend Management amount (post-credit, not gross)         | none                  | **$15**, with the pause action armed                  |
| Prerendered pages in the `apps/ayokoding-www` build                 | 4 (none a page)       | `>= 2,000` (2,183 content files today, still growing) |
| `x-vercel-cache` on a repeat request to a content page              | `MISS`                | `HIT`                                                 |
| Dynamic (`ƒ`) routes in the `apps/wahidyankf-www` build route table | 3 of 4                | 0 of 4                                                |
| A configured spend cap with an automatic pause action               | none                  | enabled                                               |

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

| Risk                                                                                                         | Severity | Mitigation                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enabling Bot Protection challenges a legitimate crawler and search rankings drop                             | HIGH     | Documentation does not confirm that verified crawlers such as Googlebot are auto-allowlisted. Phase 0 carries a mandatory indexability smoke-test and a one-toggle rollback                                                              |
| Spend Management is not a true hard cap — checks run every few minutes, so usage can overshoot the threshold | LOW      | Immaterial here: the cap sits at $15 (post-credit), $5 above the $30 goal, so a few minutes of lag costs cents against that margin. DD-9                                                                                                 |
| The $30 goal is advisory, so an ordinary overrun reaches the invoice unchallenged up to $35                  | MEDIUM   | Accepted by design (DD-9) — the alternative pins the cap to the goal and turns every bad week into an outage. Alerts fire at 50/75/100% of $15, and the successor plan grades the goal at cycle close                                    |
| The armed pause takes every production site down mid-cycle before the fix lands                              | HIGH     | Expected, not accidental: at the measured $1.399/day the cap trips ~Aug 19 and each project must be resumed by hand. This is the schedule pressure that makes Phases 1–4 urgent, and the reason Phase 0's platform wins are banked first |
| Promoting the root layout is a structural change that could break every page at once                         | MEDIUM   | Isolated to its own phase with a full `next build` gate and a live smoke-test before the delivery boundary; rollback is a single revert commit                                                                                           |
| The Pro credit may not cover Observability Plus (Vercel's own docs are internally inconsistent)              | LOW      | Rendered moot: Observability Plus is being disabled outright, removing the ambiguity along with the ~$10/month                                                                                                                           |
| Three concurrent worktrees trip the known `nx affected` cross-worktree contamination issue                   | LOW      | Documented in a filed two-pager; keep each worktree's tree clean and commit promptly                                                                                                                                                     |
| Traffic genuinely grows and costs rise again later                                                           | LOW      | The stretch target (< $10) exists precisely to absorb growth; the spend cap provides the backstop                                                                                                                                        |
