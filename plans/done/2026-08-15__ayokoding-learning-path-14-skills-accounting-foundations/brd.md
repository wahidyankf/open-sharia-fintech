# Business Requirements — Skills Paths: Accounting Foundations & Transactional Cycles

> **Programme decisions** — the `R*`/`A*` decisions cited below are restated verbatim from the
> retired the superseded accounting-programme draft/tech-docs.md` and are now owned locally by
> this plan; see [tech-docs.md §Programme decisions](./tech-docs.md#programme-decisions).

## Business Goal

Open a **second subject domain** on ayokoding.com, as the **first of two** paths this plan begins
authoring: `/en/learn/paths/skills/conventional-accounting` and
`/en/learn/paths/skills/sharia-accounting` (A10), as immediately-effective arcs for the reader who
has to build or reason about financial systems and has no accounting background. This plan carries
that opening through courses #1–#11 — a working, correctly balancing ledger (course #3) and the
full transactional-and-cost-accounting cycle (courses #4–#11): journal entries, revenue
recognition, procure-to-pay, order-to-cash, managerial/cost accounting, fixed assets, inventory/COGS,
and leases.

The goal is not "teach accounting." The goal is **accounting for people who build systems**: within
this plan's own range, the reader leaves able to design a chart of accounts as a schema, produce a
balancing ledger, and run a mid-size company's day-to-day transactional cycle correctly — including
naming the mistakes that still balance.

Three business consequences follow, all load-bearing:

1. **It opens the sequential chain that eventually unblocks ERP.** `ayokoding-learning-path-18-skills-erp-enterprise-depth`
   cannot deliver its record-to-report capability without a balanced ledger to post into — but this
   plan itself emits no ERP-facing signal; that is plan 15's and plan 16's responsibility, once
   their own stages complete (see [tech-docs.md §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-18-handoff-stage-granularity)
   for why the signal is deferred rather than split across all three).
2. **It is the platform's proof that the path machinery is subject-agnostic — twice over**, restated
   from the retired plan's own rationale: two accounting paths sharing courses through one manifest
   schema is evidence the machinery generalises to shared course reuse across paths in the same
   category.
3. **It establishes the staged manifest-growth pattern** this three-plan chain depends on: both
   manifests are created here, grown partially here, and handed to plan 15 (then plan 16) to grow
   further — a pattern no prior `skills/` plan needed, because no prior subject spanned more than one
   plan.

## Why this plan is first in a three-plan chain (not the original single plan)

The retired the superseded accounting-programme draft authored all 24 courses and both
manifests' full growth in one plan. **This plan (14), together with sibling plans 15 and 16,
replaces that single plan with a strict sequential chain** — 14 → 15 → 16, each historical source context its
predecessor — so that:

- **Each plan is independently reviewable and mergeable at a materially smaller scope** (11 courses
  here, versus 24 in the original design), reducing the size of any single PR verification scope and the
  blast radius of a single plan's rollback.
- **The manifest-growth staging is explicit and falsifiable at each boundary**, rather than one plan
  asserting three internal stage boundaries that a reader has to trust are each genuinely gated.
- **The business/product context — personas, the silent-failure constraint, the licensing posture —
  is shared verbatim across all three**, so splitting the plan does not fragment the domain
  reasoning; only the delivery unit size changes. This plan states that shared context in full; plans
  15 and 16 restate it identically rather than diverging.

Nothing about **why** the domain is taught, **what** the silent-failure constraint requires, or
**how** the licensing posture binds changes across the split — only **how much work lands in a
single plan** changes.

## Why courses #1–#11 land here, not more or fewer

This plan's course range is not an arbitrary first-eleven cut. It is the **first two ramp
segments** of the retired plan's own three-stage design:

- **Courses #1–#3 (Dangerous-1 boundary)**: unchanged from the retired plan — the three foundation
  courses that buy a reader a correctly balancing ledger and the three financial statements. This
  boundary was always going to be an early, independently-meaningful milestone; it now also happens
  to be this plan's own first sub-phase.
- **Courses #4–#11 (the transactional-and-cost-accounting cycle)**: journal-entry mechanics,
  accrual/revenue recognition, accounts payable, accounts receivable, managerial/cost accounting,
  fixed assets/depreciation, inventory/COGS, and leases/intangibles. This range is a genuine,
  coherent unit — the operational cycle a mid-size company runs day to day — and it is exactly the
  half of the retired plan's sixteen-course "Stage 2" that does **not** depend on anything past
  course #11. The remaining eight Stage-2 courses (#12–#19: multi-currency, consolidation, IFRS/GAAP,
  audit, payroll/tax, treasury, XBRL, GL architecture) are the **enterprise-reporting-and-architecture**
  half, assigned to plan 15 because each of those eight courses is either a reporting/consolidation
  concern (multi-entity, multi-currency, cross-standard) or the terminal architecture course — a
  different flavour of complexity than the transactional cycle this plan owns.

**This split point is a judgment call** [Judgment call], stated as such: the exact prerequisite
graph (see [tech-docs.md §The eleven-course catalog slice](./tech-docs.md#the-eleven-course-catalog-slice-courses-111))
makes #1–#11 a valid, self-contained topological unit (no course in this range cites a prerequisite
outside it, and no course outside this range is a prerequisite for anything inside it, other than
the two linked SWE courses), but the specific boundary at #11 rather than, say, #9 or #13 reflects
the "foundations vs. enterprise reporting" thematic split described in this plan's naming, not a
sourced fact.

## Business Impact

**Pain points addressed** (restated verbatim from the retired plan, applicable to this plan's slice)

- **The platform teaches one subject.** A reader who needs a domain other than software engineering
  has nothing here, until this plan's first published courses land.
- **The existing accounting material is the wrong artefact for the wrong reader.**
  `business/accounting.md` is a 34 KB single page for small-business owners; course #1 mines it
  without adopting its framing.
- **ERP is blocked with no path forward** — this plan is the first step in unblocking it, though the
  unblock signal itself is emitted later, by plan 15.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **The first working, correctly balancing ledger on the platform**, reachable in three courses.
- **A complete transactional-and-cost-accounting cycle**, reachable in eleven courses, covering the
  operational reality of a mid-size company's books.
- **Both manifests exist and are independently inspectable** from this plan's own merge onward,
  rather than only becoming visible once the full 24-course corpus lands — a materially earlier
  proof point that the two-path, shared-course design works end to end.
- **A reusable staged-growth pattern** — creating both manifests at a small initial size and growing
  them across plan boundaries — that plans 15 and 16 (and any future multi-plan subject) can follow
  without re-deriving the mechanics from scratch.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns this plan's slice of both ramps and the boundary at course #11.
- **Domain researcher** — owns this plan's own verification debt (courses #1–#11 carry no Sharia
  doctrinal claims, so this plan's verification debt is materially lighter than plans 15/16's).
- **Licensing steward** — owns the clean-room posture (A8) for this plan's eleven courses.
- **Content author** — authors 11 syllabus specs and 11 course bodies via the ayokoding maker agents.
- **Frontend engineer** — creates and initially grows two JSON manifests the `course-paths` feature
  loads and validates at build time.
- **Content reviewer** — validates the bodies and both landings via the ayokoding checkers.

Consuming agents: `apps-ayokoding-www-by-example-maker` (all eleven course bodies in this plan's
range are By Example format), its matching checker and fixer, `apps-ayokoding-www-general-maker`
(landing prose), `apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`,
`web-researcher` (per-course accuracy pre-verify and the post-authoring syllabus coverage pass),
`apps-ayokoding-www-deployer` [Repo-grounded — each verified present under `.claude/agents/`].

## Business-Level Success Metrics

Every metric is an **observable check**, falsifiable in both directions.

- **Two skills manifests created and grown to eleven entries** (observable):
  `manifests/skills/conventional-accounting.json` and `manifests/skills/sharia-accounting.json` each
  hold exactly the same 11 IDs, in order. Before Phase 2 neither file exists; after Phase 2 both hold
  3; after Phase 3, both hold 11.
- **Eleven course bundles resolve** (observable): each of the 11 course IDs resolves to a directory
  under `content/en/learn/courses/`. Before Phase 2 all 11 are missing.
- **Both 2-segment `pathId`s resolve end-to-end** (observable):
  `/en/learn/paths/skills/conventional-accounting` and `/en/learn/paths/skills/sharia-accounting`
  each render their (partial, 11-entry) ordered course list; `?path=` propagates through prev/next
  and the breadcrumb for both.
- **The silent-failure requirement is met for this plan's applicable range** (observable): every
  course from #4 through #11 carries an explicit "what still balances while being wrong" section;
  courses #1–#3 do not (Stage 1 is pre-Dangerous-1, matching the retired plan's own rule).
- **No prerequisite is walked that should be linked** (observable): neither manifest's
  `courseOrder` contains `sql-essentials`.
- **the current rendering baseline is recorded** (observable):
  `git log origin/main --oneline | grep -q "vercel-function-cost-reduction"` returns non-empty.
- **No regressions** (observable): `ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **Courses #12–#24.** Plan 15 authors #12–#19; plan 16 authors #20–#24.
- **Growing either manifest past 11 entries.**
- **Any ERP content.**
- **Any structural `_index.md` under `paths/`.**
- **Re-authoring or editing any existing library course.**
- **Accountancy certification coverage, tax jurisdiction depth, corporate finance.**
- **An Indonesian mirror of either path.**
- **A second skills arc.**
- **Building a system, anywhere in the corpus (A6).**
- **Reproducing any standards text, proprietary chart-of-accounts structure, or copyleft
  reference-implementation code (A8).**

## Business Risks and Mitigations

| Risk                                                                                                                           | Mitigation                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **A course teaches a plausible, silently wrong model.**                                                                        | Every course from #4 onward carries a mandatory "what still balances while being wrong" section, grep-verifiable at its authoring step.                                                                                                |
| **A course reproduces licensed standards text or a proprietary chart-of-accounts structure (A8).**                             | The eleven safe-authoring rules bind every course; every chart of accounts is originally authored; a reading audit runs at the Phase 5 gate.                                                                                           |
| **Either manifest is silently grown past 11 entries, stealing plan 15's work.**                                                | The Phase 3 gate asserts both manifests hold exactly 11 entries; the Phase 5/7 sweeps re-assert it.                                                                                                                                    |
| **Plan 15 starts before this plan's course bodies and manifests are actually on `origin/main`.**                               | Plan 15's own Phase 0 precondition checks `git log origin/main --oneline                                                                                                                                                               | grep -q "ayokoding-learning-path-14"` before any authoring begins — the same per-plan grep-loop pattern the retired plan used for 01/02/03. |
| **This plan's landings ship on an app whose rendering state has changed.**                                                     | Record the current rendering baseline at Phase 0 as implementation context; it is not an additional plan prerequisite.                                                                                                                 |
| **Scope creep into courses #12+.**                                                                                             | Each course's overview states its scope boundary; the Phase 3 gate asserts exactly 11 course directories exist, never more.                                                                                                            |
| **The linked prerequisite (`sql-essentials`) gets walked.**                                                                    | Both manifests are asserted to never contain `sql-essentials`; the corresponding course's frontmatter is asserted to declare it.                                                                                                       |
| **This plan's Rule-15 retest, scoped to 11 courses, misses a defect that only manifests once either manifest grows to 19/24.** | Plans 15 and 16 each run their own follow-up Rule-15 retest scoped to their own incremental delta; see [README.md §Rule-15 disposition](./README.md#rule-15-disposition-for-this-plan--scoped-retest-against-the-eleven-course-slice). |
