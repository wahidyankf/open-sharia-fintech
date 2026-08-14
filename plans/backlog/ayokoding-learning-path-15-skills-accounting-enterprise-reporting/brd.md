# Business Requirements — Skills Paths: Accounting Enterprise Reporting & Architecture

> **Programme decisions** — the `R*`/`A*` decisions cited below are restated verbatim from
> `ayokoding-learning-path-14-skills-accounting-foundations/tech-docs.md`, itself restated from the
> retired the superseded accounting-programme draft; see
> [tech-docs.md §Programme decisions](./tech-docs.md#programme-decisions).

## Business Goal

Complete the **conventional half** of the two-path accounting corpus (A10). This plan is the second
of three sequential plans and carries `conventional-accounting` from its plan-14 starting state (11
of 19 courses) to full completion: courses #12–#19 — multi-currency translation, consolidation,
IFRS-vs-GAAP reporting, audit and controls, payroll and tax, treasury and cash management, XBRL
reporting, and the terminal `general-ledger-system-architecture` course.

The goal is not "teach accounting." The goal is **accounting for people who build systems**, and by
the end of this plan a reader on `conventional-accounting` leaves able to model most conventional
systems a mid-size company runs — multi-currency, multi-entity, cross-standard reporting, audit
controls, payroll/tax, and treasury — and to **architect** (never build, A6) the general-ledger
system itself.

Three business consequences follow, all load-bearing:

1. **It completes `conventional-accounting` as a genuinely standalone, production-shippable path.**
   Unlike plan 14's own eleven-course milestone (a coherent but explicitly non-terminal state), this
   plan's own course #19 is the point at which the retired plan's own design already declared
   `conventional-accounting` "DONE and production-serving."
2. **It emits the first cross-plan ERP-facing signal in this three-plan chain** — unblocking
   `ayokoding-learning-path-18-skills-erp-enterprise-depth`'s
   Stage-B-equivalent capability (inventory-costing, multi-company/consolidation, hire-to-retire/
   payroll, and segregation-of-duties/security). Plan 14 emitted no such signal; plan 16 emits the
   second and final one, for the Sharia-specific stage.
3. **It closes the loop on the architecture-not-construction rule (A6)** — course #19 is the
   conventional spine's own terminal architecture course, replacing the retired single-path design's
   deleted `capstone-build-a-general-ledger-system` capstone with domain knowledge, never a build
   instruction.

## Why this plan's course range (#12–#19) completes `conventional-accounting`

Restated from plan 14's own `brd.md`: the retired plan's original sixteen-course Stage 2
(#4–#19 in its own numbering) splits at course #11 into a **transactional-cycle** half (plan 14) and
an **enterprise-reporting-and-architecture** half (this plan). This plan's eight courses are
precisely that second half:

- **Multi-currency and consolidation** (#12, #13) — the cross-border and multi-entity reporting
  cluster, both **new courses added past the retired plan's original twenty-course single-path
  design** (A9): the original catalog named consolidation but never taught FX translation, which
  consolidation cannot be honestly taught without.
- **IFRS-vs-GAAP and XBRL** (#14, #18) — the cross-standard reporting cluster, both Annotated-concept
  format since their subject is a landscape/judgment framework rather than a mechanism a reader
  executes.
- **Audit/controls and payroll/tax** (#15, #16) — the compliance and operational-control cluster.
- **Treasury** (#17) — depends on plan 14's own AP/AR courses (#6, #7), so it could not land any
  earlier than this plan.
- **General-ledger-system-architecture** (#19) — the terminal architecture course, closing the
  conventional spine.

**This plan's own boundary at #19 is not a new judgment call this split introduces** — it is the
retired plan's own Stage-2/Dangerous-2 boundary, unchanged. What is new to this three-plan split is
only that this boundary now also happens to be **this plan's own** terminal course, rather than the
middle of a single plan's sixteen-course sub-phase.

## Business Impact

**Pain points addressed** (restated, applicable to this plan's slice)

- **`conventional-accounting` was incomplete after plan 14** (11 of 19 courses) — this plan finishes
  it.
- **ERP is blocked with no path forward** — this plan's own Stage-2 signal is the first concrete
  unblock in this three-plan chain.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **A complete, standalone-shippable `conventional-accounting` path** — the first of the two
  accounting paths to reach this state, and (per this plan's own Rule-15 disposition) the first to
  receive its own full live-site retest rather than waiting for the whole chain to finish.
- **The ERP chain's first concrete unblock**, at Stage-2/Dangerous-2 (Stage-B-equivalent capability)
  granularity — plan 18 can now independently verify (via `test -d`) that every course ID its own
  Stage-B-equivalent needs is present on `origin/main`.
- **A materially reduced-risk final architecture course**: `general-ledger-system-architecture`
  extends the `DD-15` license-aware-technology-choices precedent (ledger-cli BSD-3-Clause, Apache
  Fineract Apache-2.0 named as permissive references; GnuCash/hledger/Beancount described
  behaviourally, never quoted) rather than re-deriving a licensing posture from scratch.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears the same six roles plan 14's
`brd.md` names (content strategist, domain researcher, licensing steward, content author, frontend
engineer, content reviewer), now additionally acting as **retest coordinator** for this plan's own
Rule-15 dispatch.

Consuming agents: `apps-ayokoding-www-by-example-maker` (five of this plan's eight courses),
`apps-ayokoding-www-annotated-concept-maker` (the three Annotated-concept courses: #14, #15, #18),
their matching checkers and fixers, `apps-ayokoding-www-general-maker` (landing prose),
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`, `web-researcher`,
`apps-ayokoding-www-deployer`, and — new to this plan — the three live-site testers
`web-exploratory-tester`, `web-usability-tester`, `web-design-tester` for the full Rule-15 retest
[Repo-grounded — each verified present under `.claude/agents/`].

## Business-Level Success Metrics

- **Both manifests grown from 11 to 19 entries** (observable): `conventional-accounting.json` and
  `sharia-accounting.json` each hold exactly 19 IDs, byte-identical, at this plan's end.
- **`conventional-accounting.json` is done growing, verified not merely asserted** (observable): any
  later plan's edit to that file is caught by `git diff --quiet` against this plan's own merge
  point.
- **Eight course bundles resolve** (observable): each of courses #12–#19 resolves to a directory
  under `content/en/learn/courses/`.
- **The silent-failure requirement is met for all eight courses** (observable): every course #12–#19
  carries an explicit "what still balances while being wrong" section.
- **No prerequisite is walked that should be linked** (observable): neither manifest's
  `courseOrder` contains `backend-essentials`.
- **The Stage-2 signal is recorded on the persistent final-delivery branch** (observable): its four
  required fields, including `FINAL_DELIVERY_BRANCH`, are present exactly once before the terminal
  archival PR is opened.
- **`conventional-accounting` passes its full Rule-15 retest** (observable): every EWT/UWT/DWT
  finding against that landing and its 19-course walk is resolved or explicitly deferred with
  recorded permission.
- **No regressions** (observable): `ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **Courses #1–#11 and #20–#24.**
- **Growing `sharia-accounting.json` past 19 entries.**
- **Any ERP content.**
- **Any structural `_index.md` under `paths/`.**
- **Re-authoring `backend-essentials`.**
- **Accountancy certification coverage, tax jurisdiction depth, corporate finance.**
- **An Indonesian mirror of either path.**
- **Building a system, anywhere in the corpus (A6).**
- **A Rule-15 retest for `sharia-accounting`** — that path's incremental delta is retested in
  plan 16, once it too reaches its own terminal state.

## Business Risks and Mitigations

| Risk                                                                                                                            | Mitigation                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A course teaches a plausible, silently wrong model** (multi-currency, consolidation, and audit are especially prone to this). | Every course carries the mandatory silent-failure section, grep-verifiable at its authoring step; the fact-checker runs on every body.                |
| **`conventional-accounting.json` keeps growing past 19**, silently becoming a fork of the Sharia manifest.                      | The Phase 2 gate asserts exactly 19 entries; every later phase re-asserts `git diff --quiet` against this plan's own merge point.                     |
| **The Stage-2 signal is course-number-keyed and goes stale the moment plan 18 renumbers.**                                      | The signal names an ERP capability (Stage-B-equivalent), never an ERP course number — same mechanism the retired plan used, re-pointed to plan 18.    |
| **Deferring `sharia-accounting`'s retest to plan 16 leaves this plan's own retest incomplete-feeling.**                         | Scoped explicitly: this plan's retest covers `conventional-accounting` only, and that scoping is stated, not silent.                                  |
| **Licensing exposure (A8)**, especially XBRL taxonomy version drift and IFRS-vs-GAAP standard citations.                        | The eleven safe-authoring rules bind every course; a Phase 3 reading audit checks volatile facts carry a dated accuracy-note sidebar.                 |
| **Scope creep into courses #20+.**                                                                                              | Each course's overview states its scope boundary; the Phase 2 gate asserts exactly 19 course directories exist across the shared spine, never more.   |
| **The linked prerequisite (`backend-essentials`) gets walked.**                                                                 | Both manifests are asserted to never contain `backend-essentials`; course #19's frontmatter is asserted to declare it.                                |
| **Plan 16 starts before this plan's course bodies and manifests are actually on `origin/main`.**                                | Plan 16's own Phase 0 precondition checks a merge-presence grep for this plan's identifier, matching the pattern plan 15 itself uses against plan 14. |
