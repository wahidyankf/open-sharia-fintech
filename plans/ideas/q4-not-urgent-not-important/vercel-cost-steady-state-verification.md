# Grade the Vercel invoice against the $30 budget once a clean billing cycle closes

One-line summary: the `vercel-function-cost-reduction` work shipped on a cost projection that is
mostly **estimated**, not measured — one full clean billing cycle must close before anyone can read
the single number that says whether the ~$43/month gross usage actually fell inside the $30 invoice
ceiling, and that reading is the only thing that closes the question.

> Split out of `vercel-function-cost-reduction` (completed and archived 2026-08-02) because the
> grading is calendar-gated while the engineering finished in days; demoted from `backlog/` to a
> two-pager on 2026-08-05.

## Problem / context

The parent plan is a cost plan: its objective is a dollar figure, not a refactor. It measured a
starting rate of **$9.79 of the $20 included credit consumed in seven days** ($1.399/day),
extrapolating to **~$43/month gross metered usage**, of which **Function Duration alone was $6.62 of
$9.79 — 68%**. Because Vercel bills `invoice = 20 + max(0, gross − 20)`, every target the plan set is
a statement about gross usage: a **$30 invoice ceiling** (owner-set budget goal), a **$20 target**
(gross under $20, so the included credit absorbs everything and no on-demand line appears), a `<$10`
stretch, and a**$35 armed spend cap** as the platform backstop. That cap is configured as $15 of
post-credit on-demand charge — deliberately $5 above the goal, so it bounds a runaway rather than
enforcing the budget. The two figures are not comparable directly.

The plan then shipped code and platform changes against a projection whose largest single row is an
**estimate**: the static conversion of `apps/ayokoding-www` (2,183 content pages that prerendered
none of themselves) was projected at −$30/month or more, unmeasured. Only two rows carried measured
rates — Observability Plus (−$7.5/mo) and middleware elimination (−$2.9/mo). Since `ayokoding-www`
carried **99.90% of all function volume** (43,105 of 43,150 events across seven projects in 24h),
essentially the entire projected saving rides on that one estimated row plus the platform toggles.
Nobody has read the resulting invoice. An unverified cost plan can be wrong in the expensive
direction silently.

## Why now

**It is not "now" — this is calendar-gated, and that is the whole point of the brief existing
separately.** The billing cycle runs the 26th to the 26th. The Jul 26 – Aug 26 cycle contains
pre-fix days and is therefore polluted; the first cycle clean end to end is **Aug 26 – Sep 26**,
readable only once it closes. The earliest honest start is therefore **2026-09-26**, and starting
sooner produces an ungradeable answer to a different question. Nothing can accelerate this; the only
"why now" is that the date will arrive, and the risk is that a plan whose sole trigger is a date
passing simply never gets executed. One thing genuinely is urgent ahead of that date: disabling
Observability Plus shortened log retention, and the volume-side queries have a widest usable window
of 72h, so the volume evidence should be captured as early as the preconditions allow rather than
saved for invoice day.

## Prior art / precedents

- **The parent plan itself** — carries the four-tier table (backstop / budget / target / stretch),
  the root-cause analysis verified three independent ways, and the projection table this brief
  grades. [vercel-function-cost-reduction](../../done/2026-08-02__vercel-function-cost-reduction/README.md)
- **The 2026-08-01 per-project baseline** — the measured before-picture the after-table must mirror:
  43,105 function events/24h and 273,487/72h for `ayokoding-www`, 274,463 middleware events/72h,
  36,881 on `/[locale]/[...slug]` (85.6% of function volume), and 49 × `504` in 24h.
  [evidence/baseline-per-project.md](../../done/2026-08-02__vercel-function-cost-reduction/evidence/baseline-per-project.md)
- **The parent plan's MCP identifier discipline** — address Vercel resources by slug, never by
  opaque `team_*`/`prj_*` ID, because this repo is public and its history is permanent.
  [tech-docs §Identifiers in a public repo](../../done/2026-08-02__vercel-function-cost-reduction/tech-docs.md#identifiers-in-a-public-repo)
- **Knowledge Capture Convention** — the mechanism that routed this open question here rather than
  letting it evaporate when the parent plan archived.
  [knowledge-capture](../../../repo-governance/development/quality/knowledge-capture.md)
- **Plans Organization Convention §Ideas Folder** — the promotion gate this brief will be judged
  against.
  [plans §Ideas Folder (Two-Pagers)](../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#ideas-folder-two-pagers)

## Proposed direction (sketch)

Grade in two independent halves and refuse to collapse them into one verdict. The **volume side** is
`[AI]`-readable through the Vercel MCP's runtime-log tooling — per-project and per-route counts
grouped by source, route, and status code, at 24h and 72h, compared against the 2026-08-01 baseline.
The **dollar side** is `[HUMAN]`-only: the MCP exposes no billing, usage, or invoice tool, so the
completed cycle's line items, Infrastructure Subtotal, on-demand charge, and invoice total come off
the dashboard by hand. Two further checks confirm the platform migrations landed as _billed reality_
rather than as toggles — the Fluid Compute lines carrying non-zero charges while Function Duration
has stopped accruing (presence alone proves nothing; both Fluid lines already appeared at $0.00 under
legacy billing), and the Observability Events line having stopped accruing. Then reconcile
actual-versus-projected per action, marking each figure measured or estimated, and state four
separate verdicts: below $35 (backstop never fired), at or below $30 (budget goal), under $20
(target), under $10 (stretch). A fired backstop, a missed budget, and a missed target are three
different outcomes. The output is evidence markdown only, so a direct-to-main delivery mode fits;
any remediation becomes its own plan.

## Rough scope & non-goals

**In scope** — grading only: the volume-side after-table against the 2026-08-01 baseline; the
dollar-side full-cycle line items, Infrastructure Subtotal, on-demand charge, and invoice total;
confirmation that the Fluid Compute and Observability Plus migrations show up in the billing
vocabulary as expected; and a per-action actual-versus-projected reconciliation in which every
projection row gets an actual or an explicit "not separable from the aggregate" with a reason.

**Out of scope**:

- Any remediation. A missed target is recorded as a gap and escalated into a follow-up plan naming
  the specific line item that overran — this effort does not widen into a second cost-reduction push.
- Re-litigating the parent plan's design decisions.
- Any code change under `apps/` or `libs/`.

## Risks & open questions

- **This is never executed** — its only trigger is a date passing, with no CI signal, no reviewer,
  and no blocked downstream work to force the issue. The mitigation is that the date is stated
  explicitly and the parent plan's Knowledge Capture records the reconciliation as an open question.
  (open)
- **Log retention shortens once Observability Plus is disabled**, and 72h is the widest usable query
  window. Whether the volume queries can still reach back far enough by the grading date is unknown
  until tried. (open)
- **Traffic may shift between baseline and measurement**, confounding a raw count comparison. Likely
  mitigation is reporting per-route shares alongside absolute counts, but whether shares stay
  interpretable across a two-month gap is untested. (open)
- **Log-event counts are not billed units.** They prove volume and never dollars, so the volume side
  can pass while the dollar side fails. That combination is the most informative outcome available —
  it means the cost model, not the code, was wrong — but the brief has no way to predict it. (open)
- Whether a partial or mixed cycle read would be tolerated under schedule pressure. Stating the
  cycle's exact start and end boundaries before recording any figure is the guard. (settled: state
  the boundaries first, or do not measure)

## What success looks like + promotion signal

**Promotion signal: the calendar.** This is ripe to promote once the Aug 26 – Sep 26 billing cycle
has closed — **on or after 2026-09-26** — with the parent plan's changes confirmed still deployed and
its platform toggles unchanged. Before that date, promotion is premature by construction.

Success is a stated, falsifiable verdict backed by one dashboard reading, not a narrative. The
grading closes **either way**: a pass is the Infrastructure Subtotal at or below $30 with the
volume-side after-table showing the `ayokoding-www` function and `/[locale]/[...slug]` counts at
least 90% below their 273,487 and 36,881 baselines, the middleware count at zero, the `504` count at
zero, and no project paused during the cycle. A miss is equally closing: the subtotal figure, which
tier it breached, which projection row the overrun attaches to, and a follow-up plan opened against
that line item. A miss is worth more than a pass, because it says the model of where the money goes
was wrong.
