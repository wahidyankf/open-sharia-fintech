# Product Requirements — Skills Paths: Accounting Sharia Extension

> **Programme decisions** — the `R*`/`A*` decisions cited below are defined locally in
> [tech-docs.md §Programme decisions](./tech-docs.md#programme-decisions).

## Product Overview

Courses #20–#24 of the twenty-four-course catalog — the five Sharia-specific courses. This plan
grows **`sharia-accounting.yaml` alone** (created by plan 14, grown by plan 15) from **19 to 24
entries**, its terminal size. `conventional-accounting.yaml` is **never touched** by this plan. The
`sharia-accounting` landing (created by plan 14, updated by plan 15) is **updated** here to state
full completeness at 24 courses.

What ships in this plan:

- **`sharia-accounting.yaml` grown to 24** — the last five entries are Sharia-specific, exclusive
  to this manifest.
- **`sharia-accounting`'s landing content, updated** — states the Dangerous-3 boundary and full
  path completeness.
- **Five syllabus specs**, two Annotated-concept (#20, #23) and three By Example (#21, #22, #24).
- **Five course bodies.**
- **Resolution of the carried verification debt** (OI-1 through OI-4).
- **The full Rule-15 retest**, for `sharia-accounting` only.

What does not ship: courses #1–#19 (plans 14, 15), any edit to `conventional-accounting.yaml` or
its landing, any `_index.md` under `paths/`, any ERP content, any component, any schema, any edit
to an existing library course, any building exercise (A6).

## The silent-failure constraint (continued, at its most consequential)

Restated verbatim from plan 14 and continued from plan 15. All five of this plan's courses carry
the mandatory "what still balances while being wrong" section (DD-609). This is where the
constraint is most consequential: **a murabaha markup booked as interest income still produces a
balancing trial balance**, and **Zakah computed on the wrong base, or folded into income tax, still
ties out**. This is precisely the silent mistake AAOIFI and PSAK Syariah exist to prevent, and
precisely why the Sharia stage sits at the corpus's end rather than sprinkled through — a reader
who has not yet internalised the conventional model's own mistakes (plans 14, 15) cannot yet
recognise the Sharia-specific variant of the same mistake.

## Personas

Restated verbatim from plan 14 — the split changes delivery unit size, not who the corpus serves.
This plan's own range is where the **builder of Sharia-compliant financial systems** persona
reaches full competence — the north-star persona for `sharia-accounting`, served in full for the
first time at this plan's end.

## User Stories

- As a **builder of Sharia-compliant systems**, I want the standards courses to present AAOIFI,
  PSAK Syariah and MFRS-plus-BNM as three coexisting models, so that I am not confidently wrong in
  two of the three jurisdictions I might build for.
- As a **builder of Sharia-compliant systems**, I want murabaha modelled as a trading transaction
  with a disclosed markup rather than as accrued interest, so that my receivable schedule and my
  revenue recognition are both right.
- As a **builder of Sharia-compliant systems**, I want Zakah computation treated as its own subject
  rather than folded into payroll-and-tax essentials, so that I do not conflate a religious levy
  with an income tax.
- As a **builder of Sharia-compliant systems**, I want Sukuk accounting treated as its own subject,
  distinct from conventional bond accounting.
- As a **builder of Sharia-compliant systems continuing from plan 15**, I want
  `sharia-ledger-system-architecture` to teach me how to architect (never build) a Sharia-compliant
  ledger, closing my competence at the same depth `conventional-accounting`'s own architecture
  course closes conventional competence.
- As a **maintainer**, I want `sharia-accounting.yaml` to be the only manifest this plan ever
  touches, so that `conventional-accounting`'s own terminal state (established in plan 15) is
  provably preserved.
- As the **maintainer**, I want no unverified standard number or doctrinal claim (especially the
  riba doctrinal basis) to reach a published course in this plan's range.
- As an **ERP-path reader** (via plan 18), I want this plan's completion to unblock ERP's
  Sharia-specific courses concretely.
- As the **maintainer**, I want `sharia-accounting`'s landing and full 24-course walk verified by
  the live-site testing triad once, at the point it becomes production-complete.
- As a **screen-reader or keyboard user**, I want the updated landing's ramp statements to remain
  fully navigable without a mouse.

## Acceptance Criteria (Gherkin)

Nine scenarios. Each uses **exactly one** primary `Given`, one `When`, and one `Then`.

### The ramp

```gherkin
Scenario: Sharia-accounting reaches its terminal, complete state at course twenty-four
  Given sharia-accounting.yaml has grown to include all twenty-four courses
  When a reader reaches the end of the sharia-accounting courseOrder
  Then the path landing states the path is complete
  And no further course is ever appended to sharia-accounting.yaml at any later phase or plan
  And conventional-accounting.yaml remains exactly as it was at the end of plan 15
```

```gherkin
Scenario: The sharia-accounting landing states all three Dangerous boundaries
  Given the sharia-accounting landing is updated with all twenty-four courses
  When a reader opens /en/learn/paths/skills/sharia-accounting
  Then the Dangerous-1, Dangerous-2, and Dangerous-3 boundaries all appear before the ordered course list
  And each boundary names both what the reader can do and what the reader cannot yet do
  And the landing states the path is complete
```

### Correctness

```gherkin
Scenario: The Sharia stage presents three jurisdictional models
  Given the Sharia-standards, contract-modelling, and Sharia-ledger-architecture courses are authored
  When a reader compares their treatment of standards
  Then each names AAOIFI, PSAK Syariah, and MFRS with the Bank Negara Malaysia Shariah Governance Policy as three structurally different coexisting models
  And none of them describes AAOIFI as the single Sharia accounting standard
  And each states that Malaysia is not on AAOIFI's mandatory-adoption list
  And each states that Indonesia uses AAOIFI as a basis rather than adopting it
```

```gherkin
Scenario: A murabaha is modelled as a trade rather than as a loan
  Given the Islamic contract modelling course is authored
  When a reader compares a murabaha receivable schedule with a conventional amortising loan schedule
  Then the course shows the two schedules can look numerically similar and must be modelled differently
  And the markup is presented as fixed and disclosed at the point of sale in a trade with an underlying asset
  And the recognition is presented as a receivable and revenue from a sale rather than interest income
```

```gherkin
Scenario: Zakah is computed and reported as its own obligation, not folded into tax
  Given the Zakah computation and reporting course is authored
  When a reader compares its treatment with the conventional payroll-and-tax course from plan 15
  Then Zakah is presented as a distinct religious levy computed on a defined asset base under AAOIFI FAS 9
  And the course states explicitly that Zakah is not income tax and is not computed on the same base
  And no course folds a Zakah obligation into a payroll-and-tax course's scope
```

```gherkin
Scenario: No unverified claim is published as fact, and the riba doctrinal basis stays open
  Given the research seeding this plan marked the riba doctrinal basis as an open item
  When course twenty states any doctrinal position on profit and risk
  Then the practical consequence is stated (profit must arise from trade, leasing, partnership or service risk)
  And the specific doctrinal derivation is never asserted as settled fact
  And every item still marked Needs Verification when this plan's Phase 2 gate runs is registered with a reason
```

```gherkin
Scenario: No standard's text or proprietary structure is reproduced
  Given this plan's five courses are authored under the licensing posture in tech-docs.md
  When any course body cites AAOIFI, PSAK Syariah, or MFRS
  Then the standard is restated in original words with only its number, title, and official link cited
  And every chart of accounts in this plan's courses is originally authored
```

### Boundaries and retest

```gherkin
Scenario: This plan's authored slice builds and validates green
  Given sharia-accounting.yaml holds twenty-four entries and all five of this plan's course bodies are authored
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations
  And conventional-accounting.yaml is provably unchanged since plan 15's own merge
```

```gherkin
Scenario: Sharia-accounting passes its full live-site retest
  Given sharia-accounting is complete at twenty-four courses and deployed to production
  When the web-exploratory-tester, web-usability-tester, and web-design-tester triad runs against it
  Then every finding is folded in as an individually tickable, source-attributed checkbox
  And every defect finding is resolved or explicitly deferred with recorded permission before archival
```

## Product Scope

### In scope

- Growth of one existing `PathManifest` YAML data file (`sharia-accounting.yaml`) from 19 to 24
  entries.
- Extension of `sharia-accounting.yaml`'s existing co-located unit test.
- Extension of the shared Gherkin feature file's step definitions to the full 24-course
  `sharia-accounting` walk.
- Content update to the existing `sharia-accounting` landing bundle.
- Five syllabus specs under this plan's own `syllabus/courses/`.
- This plan's own slice of the `sharia-accounting` path mirror (5 rows).
- Five course bodies.
- Resolution of the carried verification debt (OI-1 through OI-4).
- The Stage-3 stage-completion signal.
- **The full Rule-15 three-tester retest, for `sharia-accounting` only.**
- Manifest integrity, prerequisite-consistency, ownership-boundary, licensing, and ramp
  verification at every phase gate.

### Out of scope

- **Courses #1–#19.**
- **Any edit to `conventional-accounting.yaml`, its landing, or its unit test.**
- **Every `_index.md` under `paths/`.**
- **All ERP content.**
- **Any rendering component, route wiring, or design asset.**
- **The `PathManifest` schema, the `course-paths` core modules, and the integrity functions.**
- **The `careers/` manifests and their landings.**
- **Any edit to an existing library course.**
- **Any edit to plan 02's, plan 14's, or plan 15's own `syllabus/` folder.**
- **An Indonesian mirror.**
- **Certification-syllabus coverage**, tax-jurisdiction depth, and corporate finance.
- **Any building exercise, capstone, or scaffolded codebase (A6).**
- **Reproducing any standard's text, proprietary chart-of-accounts structure, or copyleft
  reference-implementation code (A8).**
- **A Rule-15 retest for `conventional-accounting`** — already run, in plan 15.
- **Resolving OI-2 (the riba doctrinal basis) as settled fact.**

### UI-design-funnel disposition

**Exempt — and the exemption is recorded, not silently taken.** This plan adds **no net-new screen
and no net-new component**, restated from plan 14. This plan ships **content and data into** the
existing `sharia-accounting` landing screen, plus growth of one existing manifest data file.

## Product-Level Risks

- **AAOIFI is presented as "the" Sharia accounting standard.** Mitigated by the three-jurisdictional-model
  invariant, re-asserted at the Phase 4 gate.
- **A course teaches a plausible, silently wrong model** (murabaha-as-interest, Zakah-folded-into-tax).
  Mitigated by the mandatory silent-failure section and the explicit contrast scenarios above.
- **An `[Unverified]` research claim (especially OI-2) is restated as fact.** Mitigated by this
  plan's own Phase 2 gate, checked again at every later gate.
- **`conventional-accounting.yaml` is accidentally touched.** Mitigated by a falsifiable
  `git diff --quiet` clause at every phase gate from Phase 3 onward.
- **Licensing exposure (A8)**, at its strictest posture (IAI, AAOIFI). Mitigated by the eleven
  safe-authoring rules and a dedicated Phase 4 reading audit.
- **Prerequisite drift**, especially the cross-plan-boundary edges into plans 14 and 15.
- **Scope collision with the library.**
- **Cross-plan file collision** — accidentally writing to a file plan 14 or plan 15 owns.
- **The landing reads as a syllabus.**
- **The Rule-15 retest for `sharia-accounting` surfaces defects that block this plan's own
  archival** — mitigated by treating every EWT/UWT/DWT defect finding as mandatory-fix, per
  governance, with deferral only by explicit recorded permission.
