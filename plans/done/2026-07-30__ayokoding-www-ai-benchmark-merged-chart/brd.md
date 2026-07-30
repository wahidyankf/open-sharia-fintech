# Business Requirements — AI Benchmark Merged Chart

## Business goal

Reduce the effort a reader spends comparing a model's **capability** against its **price** on the
AI Benchmark tool. Today the two figures live in separate full-width chart sections; a reader must
scroll down, remember the capability number, scroll back, and compare it against a price bar in a
different section. Merging the two into one row per model removes that round-trip entirely.

## Business impact

**Pain point** `[Judgment call]`: a reader evaluating "is the pricier model actually more capable"
has to hold one number in working memory while scrolling to find its counterpart — a small but real
friction cost on a page whose entire purpose is fast trade-off comparison. This is the user's own
stated complaint about the current page ("tiring to scroll down" between the two chart sections).

**Expected benefit** `[Judgment call]`: a single glance at one model's row shows both figures
together, and the new per-band sort control lets a reader re-rank a band by price without leaving
the chart — both changes directly target the "compare capability against price" reading task the
page exists to serve.

## Affected roles

Solo-maintainer repo — no sign-off or stakeholder ceremony. The roles below are the hats the
maintainer wears, plus the agents that consume this plan:

- **Content maintainer** (the plan author/executor) — implements the merge, keeps
  `core/data/models.ts` and the scoring/pricing core untouched.
- **Reader** — the public visitor to `ayokoding.com/en/tools/ai-benchmark` (or `/id/...`) comparing
  coding-harness models.
- **Consuming agents** — `plan-execution` (executes this plan), `plan-checker` (validates it),
  `web-exploratory-tester`/`web-usability-tester`/`web-design-tester` (Rule-15 retest before
  archival).

## Business-level success metrics

- **Observable fact**: the two existing chart components (`capability-chart.tsx`, `price-chart.tsx`)
  are deleted and replaced by exactly one merged chart component — verifiable by `git status`/`grep`
  at delivery time, not a subjective claim.
- **Observable fact**: every existing Gherkin scenario in
  `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` that described the
  removed two-chart layout is rewritten (none left describing removed UI) — verifiable via `grep`.
- **Qualitative reasoning** `[Judgment call]`: the merge is judged successful if a reader can
  identify, for any single model, both its capability index and its input/output price without
  scrolling past that model's own row — this is the acceptance criteria in `prd.md`, not a numeric
  KPI, since no traffic/analytics instrumentation exists on this static site to measure "time to
  compare" empirically.

No fabricated numeric targets (e.g., "reduces scroll distance by 40%") are claimed — this repo has
no analytics on this page, so any such number would be invented, not measured.

## Business-scope Non-Goals

- No new benchmark, price, or model data enters the roster as part of this plan.
- No change to the harness/class filter bar's own behavior or URL params (`harness`, `class` stay
  exactly as `core/url-state.ts` defines them today).
- No change to `model-table.tsx` — the accessible full-data table stays the single source of truth
  for every figure, unaffected by the chart merge.
- No analytics, A/B testing, or user-research instrumentation added to measure the "less scrolling"
  claim quantitatively — out of scope for a static-content site with no such infrastructure today.

## Business risks and mitigations

| Risk                                                                                                | Mitigation                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Merging two charts into one could make an already-dense page feel more cluttered per row            | The selected design (see `prd.md`'s UI-design-funnel) keeps the SAME identical structure at every breakpoint — no responsive layout switch — so density is controlled by vertical stacking, not horizontal cramming |
| A rated model billed only by subscription has no natural price bar to plot (DD-1 in `tech-docs.md`) | Reuses `model-table.tsx`'s already-shipped, already-tested inline "Subscription ($cost)" text cell rather than inventing new UI                                                                                     |
| Rewriting 39 existing Gherkin scenarios in place risks silently dropping test coverage              | `delivery.md`'s RED steps enumerate every scenario touched, and the Phase Gate for that phase requires a 1:1 audit of removed vs. added scenario count                                                              |
| The prior plan explicitly rejected a similar side-by-side merge (Option C) for mobile reasons       | This plan's selected design is a different layout (vertical stack, not side-by-side columns) specifically chosen to avoid that exact failure mode — documented in `tech-docs.md`                                    |
