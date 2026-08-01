# BRD: Plan Decision-Integrity Hardening

## Business goal

Stop plans from shipping pre-loaded with their own successor. A plan that eliminates a design option
on an unmeasured claim, or selects an option that loses the criterion the plan itself calls its
thesis, has not made a decision — it has deferred one. The deferred decision comes back as a second
plan, and sometimes a third.

The three AI Model Benchmark plans are the worked example. Every trigger for plans two and three was
observable in plan one's own documents, at plan-one authoring time. This plan converts those three
observations into rules an authoring agent must satisfy and a checker can verify.

## Measured evidence

All line references below are to files committed under `plans/done/`. Each was read directly from the
archive during this plan's authoring, not reconstructed from memory.

### C1 — The requester's phrasing was scored as a design criterion

`plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/prd.md`, the Stage-4 Justify table at lines
306-312, scored the finalists on six criteria. The first row is:

| Criterion                                             | A — Banded Stacked Panels | C — Side-by-Side Grid                       |
| ----------------------------------------------------- | ------------------------- | ------------------------------------------- |
| Matches the stated requirement (2 charts × 3 classes) | **Exact**                 | Partial — one merged grid, not two diagrams |
| Capability-vs-price trade-off legibility              | Good                      | **Best** — same row                         |

"2 charts × 3 classes" is the requester's phrasing of a **candidate solution**, not a statement of
the reader's job. The same document, at line 270, describes the second row as "the page's real
thesis". Option A was selected. Option A loses the page's real thesis.

The entire second plan —
`plans/done/2026-07-30__ayokoding-www-ai-benchmark-merged-chart/`, 2,628 lines of plan document plus
a full delivery cycle — exists to build Option C. Its own README states the pain point verbatim:
"Comparing one model's capability against its price today requires scrolling between two separate
chart sections."

### C2 — An option was eliminated on a responsive claim that was never rendered

The same Justify table's final row reads, for Option C: "Degenerates to A below 768px, having paid
for two layouts." Option C's mobile representation in the Diverge stage (same file, lines 260-261) is
a **prose note inside the desktop code fence**, not a wireframe:

```text
MOBILE — the two chart columns cannot survive < 768px; they stack, which
         degenerates into Option A with extra layout machinery.
```

No artefact for Option C at any width below 768px was ever produced. The claim that eliminated it was
never tested. The convention permitted this: `repo-governance/conventions/formatting/diagrams.md`
allows "an ASCII wireframe (or an inline note)" for the mobile layout, with no distinction between an
option being carried forward and an option being dropped.

The consequence compounds. The second plan, avoiding the failure mode it had just read about, chose
"identical DOM structure at every breakpoint" — which, combined with an SVG `viewBox`, leaves uniform
scale as the only responsive lever and makes typography a function of viewport width. Its sign-off
evidence (`plans/done/2026-07-30__ayokoding-www-ai-benchmark-merged-chart/delivery.md`, line 1392)
records "Responsive usability: pass at 320/375/768/1280/1440px for both locales — no content" issue,
while chart labels were rendering at 4.3 CSS pixels. The third plan reversed the strategy and deleted
the SVG chart entirely.

### C3 — A closed identifier set mixed two naming kinds and was renamed two plans later

The first plan's dataset defined three rated capability classes: `opus`, `sonnet`, `light` — two
model-tier proper nouns beside one weight adjective. The inconsistency is readable off the schema
with no execution required.

The third plan renamed the third class to `haiku`. Its own README records that the rename "answers
none of R1-R5 and fixes no measured defect" — it is a vocabulary correction. By then the identifier
had reached six binding surfaces: the feature's `core/` types, the `class` and `sortLight` URL query
values, the `--chart-band-light*` design tokens in `libs/web-ui-token/src/ayokoding.css`, both i18n
keys, and both step-binding layers. The PR-review cycle on that plan additionally caught seven stale
`sortLight` sites the rename sweep had missed.

### C4 — Knowledge Capture routings landed in one repo only

The third plan triaged five learnings and routed all five inline into `repo-governance/`. Verified by
grep on 2026-08-01, one file per row, across all three repos:

| Routing                                                                                  | `ose-public` | `ose-primer` | `ose-private` |
| ---------------------------------------------------------------------------------------- | ------------ | ------------ | ------------- |
| Identical-DOM design-review heuristic (`conventions/formatting/diagrams.md`)             | present      | absent       | absent        |
| Breakpoint legibility (`development/quality/manual-behavioral-verification.md`)          | present      | absent       | absent        |
| Progressive-disclosure density (`development/quality/user-facing-delivery-hardening.md`) | present      | absent       | absent        |
| Amendment numeric sweep (`conventions/writing/dynamic-collection-references.md`)         | present      | absent       | absent        |
| Capped-query undercount (`development/quality/plan-anti-hallucination.md`)               | present      | absent       | absent        |

All ten target files exist in all three repos, so this is drift, not a structural difference. The
rules the third plan wrote to prevent a recurrence protect one repo out of three.

## Business impact

**Pain points**

- A decision recorded as suspect inside a plan's own documents produces a successor plan whose entire
  cost — planning, gating, worktree, PR review cycles, CI, deploy — is spent reversing it. Two such
  successors were paid for here.
- Work built under the reversed decision is thrown away. The second plan's merged SVG chart was
  deleted wholesale by the third.
- A rename deferred past schema-design time scales with the number of binding surfaces the identifier
  has reached. Three surfaces at authoring became six at plan three, plus a missed-sites review cycle.
- A governance rule written to prevent a recurrence protects only the repo it was written in, unless
  propagation is an explicit step.

**Expected benefits**

- A funnel decision that loses its own job criterion becomes visible at authoring time, when changing
  it costs one table row, instead of at plan N+1, when it costs a plan.
- A drop reason that was never tested becomes inadmissible, so the design space is narrowed on
  evidence rather than on assertion.
- A legitimate reversal still happens — it just carries a record saying what changed, which is the
  difference between a decision and a drift.
- Identifier vocabularies are settled while the rename is a one-file edit.

## Affected roles

The maintainer wears each of these hats; the agents listed consume the affected files directly.

| Role                     | How this plan affects them                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Plan author (maintainer) | Must name a Primary Job Criterion and back every drop reason with an artefact                                 |
| `plan-maker`             | Emits the new funnel rows and reversal/vocabulary sections; grills when the selection loses the job criterion |
| `plan-checker`           | Gains Step 5o, the Successor-Plan Debt Scan, with six enumerated clauses                                      |
| `plan-fixer`             | Scaffolds each missing section the new step flags                                                             |
| `plan-execution-checker` | Unaffected — every new rule binds at authoring time, not execution time                                       |
| Repo governance owner    | Owns the three-repo parity of the changed files and the binding re-sync                                       |

## Business-level success metrics

Each metric below is an observable check, verifiable on demand. No numeric target is asserted where
no baseline exists.

1. **Rule presence, three repos.** Each of the four new rules and the new checker step is present in
   all three repos. Verified by a per-repo grep for the rule heading, expecting a non-zero count in
   nine of nine repo/file pairs.
2. **Parity backfill closed.** The C4 table above reads "present" in all fifteen cells.
3. **Open-plan retrofit complete.** Every plan currently in `plans/in-progress/` and `plans/backlog/`
   across the three repos (25 folders at authoring time) carries a recorded audit verdict, and every
   UI-bearing one among them satisfies R-A and R-B. Verified by the audit table this plan commits to
   its own `tech-docs.md`.
4. **The checker actually fires.** Step 5o's clauses are demonstrated against a deliberately
   non-compliant fixture during Phase 3's gate, so the step is proven non-vacuous rather than assumed
   to work. This is the direct application of the lesson that a test outside every configured glob
   silently protects nothing.
5. _Judgment call:_ we expect the rate of plans that exist principally to reverse a predecessor to
   fall. No baseline exists — three plans is not a rate — so this is stated as reasoning, not as a
   measured target.

## Business-scope non-goals

- **Not a rework of the benchmark page.** It is shipped and archived. Nothing in `apps/` changes.
- **Not a general decision-making framework.** The rules bind the UI design funnel, where the
  evidence is. Architecture and tooling option tables are named as out of scope with a reason rather
  than silently included.
- **Not a new validator surface.** No `apps/rhino-cli` command, no CI markdown gate. Enforcement is
  the `plan-checker` step the repo already runs on every plan.
- **Not a retroactive amendment of `plans/done/`.** The archive is immutable; the post-mortem is the
  only new document that reads it.

## Business risks and mitigations

| Risk                                                                                                    | Mitigation                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The Primary Job Criterion becomes a box-ticking row that restates the winner, defeating the rule        | The rule requires the criterion to be traceable to a specific `brd.md` problem statement, and forbids requester-phrasing criteria by pattern; Step 5o flags a criterion that cites no `brd.md` anchor |
| Step 5o produces false positives on plans whose funnel is legitimately unusual, adding gate friction    | Clause severities are split — structural absences are HIGH, pattern-matched heuristics are MEDIUM — and every clause names its escape (an explicit, written override record)                          |
| The retrofit of 25 open plans balloons the plan's blast radius                                          | Retrofit is scoped to the four new rules only, is split into three per-repo phases, and each phase records a per-plan verdict table so a plan needing no change is provably examined, not skipped     |
| The three-repo propagation drifts again, exactly as the five routings did                               | Propagation is two named phases with their own gates, not a trailing note; each gate re-runs the same grep table that detected the original drift                                                     |
| Writing four rules at once produces prose nobody reads, the same way a 16-rule convention already risks | Each rule states its gap, its application, and the Step 5o clause that enforces it; the enforcement clause is what makes the prose consequential                                                      |

## References

- [`prd.md`](./prd.md) — the testable acceptance criteria for every claim above
- [`tech-docs.md`](./tech-docs.md) — verbatim rule texts and the Step 5o specification
- [Post-Mortems Convention](../../../repo-governance/conventions/structure/post-mortems.md) — governs
  the narrative record this plan commits
- [`2026-06-19-ui-design-parity-shipped-past-green-gates.md`](../../../docs/explanation/post-mortems/2026-06-19-ui-design-parity-shipped-past-green-gates.md) —
  the prior post-mortem whose action items produced the User-Facing Delivery Hardening convention this
  plan extends
