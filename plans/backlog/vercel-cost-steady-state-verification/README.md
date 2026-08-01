# Vercel Cost Steady-State Verification — grade the invoice against the $30 ceiling

Verify that [`vercel-function-cost-reduction`](../../in-progress/vercel-function-cost-reduction/README.md)
actually achieved its objective. That plan carries **three tiers**, and this plan grades against all
three rather than a single number:

| Tier                    | Gross metered usage | Invoice  | Verdict if missed                     |
| ----------------------- | ------------------- | -------- | ------------------------------------- |
| **Ceiling** (owner-set) | `<= $30/month`      | `<= $30` | **Failure** — the budget was breached |
| **Target**              | `< $20/month`       | `$20.00` | Shortfall, not a breach               |
| **Stretch**             | `< $10/month`       | `$20.00` | Missed upside                         |

Because `invoice = 20 + max(0, gross − 20)`, every tier above is a statement about **gross** metered
usage — the figure the dashboard reports as the Infrastructure Subtotal. The one number in the parent
plan that is _not_ gross is the Spend Management amount ($10), which meters post-credit charge only.
Do not compare those two figures directly.

That plan changes the code and the platform settings. **This plan grades it.** The split exists
because grading is gated on a calendar nobody controls — a full billing cycle must elapse — while
the engineering finishes in days. Holding the parent plan open in `plans/in-progress/` for two
months to wait on one dashboard reading would block its Knowledge Capture and archival for work
already delivered.

## Structure

Single-file per the [Plans Organization Convention §Structure Decision](../../../repo-governance/conventions/structure/plans.md#structure-decision):
one narrow concern (verification only), no new agents/workflows/conventions, well under 1000 lines,
no foreseen mid-execution growth.

## Dependencies and timing

| Field             | Value                                                                                                             |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| **blockedBy**     | `vercel-function-cost-reduction` — **hard**. All three delivery units merged and deployed to their prod branches. |
| **Earliest run**  | **2026-09-26.** See the cycle arithmetic below. Starting sooner produces an ungradeable answer.                   |
| **Delivery Mode** | `main-to-origin-main`                                                                                             |

**Checkable precondition** (both must hold before Phase 1 begins):

```bash
test ! -f apps/ayokoding-www/src/app/layout.tsx      # Cause A fixed
test ! -f apps/ayokoding-www/src/middleware.ts       # middleware eliminated
```

Before the parent plan lands, both exit non-zero. After it lands, both exit 0. Falsifiable in both
directions.

**Why 2026-09-26**: the billing cycle runs the 26th to the 26th. The Jul 26 – Aug 26 cycle contains
pre-fix days and is therefore polluted. The first cycle that is clean end-to-end is **Aug 26 –
Sep 26**, readable once it closes. Reading a partial or mixed cycle would answer a different
question than the one the parent plan asked.

### Delivery Mode rationale

`main-to-origin-main` rather than the repo-default `worktree-to-pr`. This plan's entire output is
evidence markdown inside its own plan folder — no `apps/`, `libs/`, `specs/`, or workflow file is
touched, so there is no code for a PR-review cycle to review and no CI signal that would differ.
Same reasoning as the plan-docs-only carve-out. If any remediation turns out to be needed, that
becomes its **own** plan (see Phase 3), which takes the normal default.

## Business rationale (condensed BRD)

The parent plan is a **cost** plan, not a refactor. Its objective is a dollar figure. Delivering the
code without ever reading the invoice would leave the stated goal unverified — and the projection it
rests on (~$57/month gross → ~$2–4/month) is largely **estimated**, not measured: only the
Observability (~$10/mo) and middleware (~$5/mo) rows carried measured rates. The largest single row,
the static conversion at −$30/mo or more, is an estimate.

An unverified cost plan can be wrong in the expensive direction silently. Reading one number closes
that.

**Value if the answer is bad**: equally high. A miss tells us the model of where the money goes is
wrong, which is worth more than a pass.

## Scope (condensed PRD)

**In scope** — grading only:

- The volume-side check: per-project and per-route invocation counts via the Vercel MCP, compared
  against the baseline the parent plan captured on 2026-08-01.
- The dollar-side check: full-cycle line items, Infrastructure Subtotal, on-demand charge, invoice
  total.
- Confirming the two platform migrations landed as billed reality, not just as toggles:
  Fluid Compute (Active CPU + Provisioned Memory line items present, "Function Duration (GB-Hrs)"
  absent) and Observability Plus (Observability Events line stopped accruing).
- Actual-versus-projected reconciliation per action, marking each figure measured or estimated.

**Out of scope**:

- Any remediation. If the target is missed, this plan records the gap and opens a follow-up; it does
  not widen into a second cost-reduction effort.
- Re-litigating the parent plan's design decisions (DD-1 … DD-8).
- Any code change to `apps/` or `libs/`.

## Baseline to compare against

From
[`vercel-function-cost-reduction/evidence/baseline-per-project.md`](../../in-progress/vercel-function-cost-reduction/evidence/baseline-per-project.md),
captured 2026-08-01:

| Metric                                | Pre-fix baseline           |
| ------------------------------------- | -------------------------- |
| `ayokoding-www` function events / 24h | 43,105                     |
| `ayokoding-www` function events / 72h | 273,487                    |
| `ayokoding-www` middleware / 72h      | 274,463                    |
| `/[locale]/[...slug]` / 24h           | 36,881 (85.6% of function) |
| `504` responses / 24h                 | 49                         |
| Share of all function volume          | 99.90% of seven projects   |
| Gross metered usage                   | ~$57/month extrapolated    |
| Of which Function Duration            | 27.04 GB-Hrs = $4.87 (65%) |

## The projection being graded

Inherited from the parent plan, which no longer carries it. Each row must get an actual, or an
explicit "not separable from the aggregate" with a reason:

| Action                            | Line item affected                    | Projected effect                  | Confidence                                                                 |
| --------------------------------- | ------------------------------------- | --------------------------------- | -------------------------------------------------------------------------- |
| Disable Observability Plus        | Observability Events                  | −$10/mo                           | **Measured rate**, certain                                                 |
| Eliminate middleware              | Edge Middleware Invocations           | −$5/mo                            | **Measured rate**, certain                                                 |
| Static conversion (ayokoding-www) | Function Duration + Invocations       | −$30/mo or more                   | Estimated; the 65% line item collapses when ~2,068 pages become CDN-served |
| Fluid Compute migration           | Function Duration on whatever remains | roughly halves the residue        | Estimated from Vercel's own comparison                                     |
| Bot/AI-bot blocking               | Invocations + Duration                | unknown but positive              | Unquantified — depends on the crawler share                                |
| wahidyankf-www static             | Function Duration + Invocations       | **≈$0** — 0.1% of function volume | **Measured 2026-08-01**: 45 invocations/24h. Correctness win, not a saving |
| **Projected total**               | —                                     | **~$2–4/mo gross**                | Claimed to be inside all three tiers — ceiling, target, and stretch        |

Note where the weight sits: the single largest row (−$30/mo, static conversion) is **estimated**, and
`ayokoding-www` carries 99.90% of all function volume, so essentially the entire projected saving
rides on Unit 1 plus the platform toggles. If the total misses, that row is the first place to look.

## Acceptance criteria

```gherkin
Feature: Steady-state Vercel cost verification

  Background:
    Given all three delivery units of vercel-function-cost-reduction are merged and deployed
    And a full billing cycle has elapsed since the last of them deployed

  Scenario: The invoice stays inside the authorised ceiling
    When the completed cycle's usage is read from the Vercel dashboard
    Then the Infrastructure Subtotal is at or below $30.00
    And the on-demand charge above the subscription is at or below $10.00
    And the invoice total is at or below $30.00

  Scenario: The invoice holds at the subscription
    When the completed cycle's usage is read from the Vercel dashboard
    Then the Infrastructure Subtotal is under $20.00
    And the on-demand charge above the subscription is $0.00
    And the invoice total equals the $20 Pro platform fee with no additional line

  Scenario: The spend cap did not have to fire
    When the Spend Management activity log is read for the completed cycle
    Then no project was paused during the cycle
    And no 100% spend-amount notification was sent

  Scenario: Function volume collapsed
    When runtime log counts for ayokoding-www are queried over a 72h window
    Then the function-source count is at least 90% below 273,487
    And the middleware-source count is 0
    And the "/[locale]/[...slug]" route count is at least 90% below 36,881

  Scenario: The billing model migrated
    When the completed cycle's line items are read
    Then an "Active CPU" line item is present
    And a "Provisioned Memory" line item is present
    And no "Function Duration (GB-Hrs)" line item is present

  Scenario: Observability Plus stopped billing
    When the completed cycle's line items are read
    Then the Observability Events line has stopped accruing

  Scenario: Timeouts eliminated
    When runtime log counts are grouped by status code over 24h
    Then the 504 count is 0

  Scenario Outline: A miss is escalated, not absorbed
    Given the Infrastructure Subtotal is <subtotal>
    When the reconciliation is written
    Then the verdict is recorded as "<verdict>"
    And a follow-up plan is opened in plans/backlog/
    And this plan is archived recording the gap rather than widening its own scope

    Examples:
      | subtotal            | verdict            |
      | above $30.00        | ceiling breached   |
      | $20.00 up to $30.00 | target missed      |
```

## Technical notes

**MCP call shape** — address resources by **slug, never by opaque ID**; this repo is public and its
history is permanent. `teamId: "wahidyan-kresna-fridayokas-projects"`,
`projectId: "ayokoding-www"`. Both parameters accept a slug in place of the `team_*`/`prj_*` ID.
See the parent plan's
[tech-docs §Identifiers in a public repo](../../in-progress/vercel-function-cost-reduction/tech-docs.md#identifiers-in-a-public-repo).

**Measured MCP limits** (from the parent plan's probe):

- `since: "72h"` is the widest usable window; `7d` fails with `Aggregate query failed: timed out`.
- Always pass `limit` — `group_by` truncates to the top _N_ with only a footer to say so.
- Counts are **log events**, not billed units. They prove volume, never dollars.
- The MCP has **no billing, usage, or invoice tool**. Every dollar figure below is `[HUMAN]`.

**Retention caveat, and why it matters here**: the parent plan's step 0.5 disables Observability
Plus, which shortens log retention. Run the volume queries **as early as the precondition allows**
rather than saving them for the same day as the invoice read — the 72h window may no longer reach
back far enough by then. The dollar read has no such constraint.

## Delivery

> `[AI]` unless marked. `[HUMAN]` steps need the Vercel dashboard, which no MCP tool reaches.

### Phase 0: Preconditions

- [ ] `[AI]` Confirm the parent plan's units all merged and deployed:
      `test ! -f apps/ayokoding-www/src/app/layout.tsx && test ! -f apps/ayokoding-www/src/middleware.ts`
  - Acceptance: both exit 0. If either exits non-zero the parent plan has not landed — stop, do not
    proceed to Phase 1.
- [ ] `[AI]` Confirm a full clean billing cycle has closed since the last unit deployed.
  - Acceptance: today's date is on or after the close of the first cycle containing no pre-fix days.
    State the cycle's exact start and end dates in the evidence file.
- [ ] `[HUMAN]` Confirm the parent plan's platform toggles are still in the state it left them
      (Spend Management with pause action, Fluid Compute, Bot Protection / AI Bots, Observability
      Plus disabled).
  - Acceptance: any drift is recorded before measurement, since it would confound the result.

> **Pause Safety**: nothing has been measured or changed. Safe to stop; re-run Phase 0 later.

### Phase 1: Measure

- [ ] `[AI]` Volume side — `get_runtime_logs` for all seven projects, `group_by` run as `source`,
      `route`, and `statusCode`, at both `since: "24h"` and `since: "72h"`,
      `environment: "production"`, explicit `limit`.
  - Acceptance: an after-table mirroring the baseline table's shape, committed to
    `evidence/steady-state.md`. Before this step the file does not exist; after it, `test -f` exits 0.
- [ ] `[HUMAN]` Dollar side — read the completed cycle's every line item from Vercel → Usage.
  - Acceptance: the evidence file records the Infrastructure Subtotal, the on-demand charge, the
    invoice total, and each line item by name. No MCP tool can supply these.
- [ ] `[HUMAN]` Record whether the Fluid Compute and Observability Plus migrations show up in the
      billing vocabulary as expected.
  - Acceptance: the file states, per the acceptance criteria above, whether Active CPU and
    Provisioned Memory appear and whether Function Duration (GB-Hrs) is gone.

> **Pause Safety**: measurement is captured and committed. The verdict can be written later.

### Phase 2: Reconcile

- [ ] `[AI]` Write actual-versus-projected per action, marking every figure **measured** or
      **estimated**, against the parent plan's projection table.
  - Acceptance: each of the parent's seven projection rows gets an actual, or an explicit "not
    separable from the aggregate" with a reason. No row is silently dropped.
- [ ] `[AI]` State the verdict against **all three tiers**: at or below $30.00 (ceiling, owner-set),
      under $20.00 (target), under $10.00 (stretch).
  - Acceptance: three bare pass/fail verdicts with the one measured figure, not a narrative. A
    ceiling breach and a target miss are different outcomes and must not be reported as one.

### Phase 3: Escalate or close

- [ ] `[AI]` If the hard target was missed, open a follow-up plan in `plans/backlog/` naming the
      specific line item that overran. Do **not** widen this plan.
  - Acceptance: either the follow-up plan folder exists, or the evidence file records that the
    target was met and no follow-up is warranted. Falsifiable both ways.
- [ ] `[AI]` If the volume-side check passed but the dollar-side failed, say so explicitly — that
      combination means the cost model, not the code, was wrong, and it is the most informative
      outcome available.

### Phase 4: Knowledge Capture

- [ ] `[AI]` Triage `learnings.md` — each entry finds a home or is discarded with a one-line reason.
- [ ] `[AI]` Candidate homes: whether log-event counts turned out to be a usable proxy for billed
      units (they are the cheap signal; this plan is the only chance to calibrate them against a real
      invoice), and whether the projected-versus-actual gap justifies revisiting how future cost
      plans estimate.

### Phase 5: Archival

- [ ] `[AI]` `git mv plans/backlog/vercel-cost-steady-state-verification plans/done/YYYY-MM-DD__vercel-cost-steady-state-verification`
- [ ] `[AI]` Update `plans/done/README.md` and `plans/backlog/README.md` indexes.

### Final Gate

- [ ] `[HUMAN]` Full-cycle gross metered usage figure recorded, with the on-demand charge.
- [ ] `[AI]` Volume-side after-table committed and compared against the 2026-08-01 baseline.
- [ ] `[AI]` Verdict stated against all three tiers (ceiling, target, stretch).
- [ ] `[AI]` Follow-up opened if the hard target was missed.
- [ ] `[AI]` `learnings.md` fully triaged.

## Risks

| Risk                                                                     | Mitigation                                                                                                                                                                |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **This plan is never executed** — its only trigger is a date passing     | Earliest-run date is stated in the dependency table above; the parent plan's Knowledge Capture records the reconciliation as an explicitly open question this plan closes |
| Log retention shortens after Observability Plus is disabled              | Run the volume queries as early as Phase 0 allows, not on invoice day (see Technical notes)                                                                               |
| Traffic changes between baseline and measurement, confounding comparison | Report per-route shares alongside absolute counts; a share shift is interpretable where a count drop alone is not                                                         |
| The cycle read is partial or mixed                                       | Phase 0 requires stating the cycle's exact boundaries before any figure is recorded                                                                                       |
