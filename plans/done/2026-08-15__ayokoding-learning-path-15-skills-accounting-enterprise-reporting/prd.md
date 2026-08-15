# Product Requirements — Skills Paths: Accounting Enterprise Reporting & Architecture

> **Programme decisions** — the `R*`/`A*` decisions cited below are defined locally in
> [tech-docs.md §Programme decisions](./tech-docs.md#programme-decisions).

## Product Overview

Courses #12–#19 of the twenty-four-course catalog. This plan **grows both existing manifests**
(created by plan 14) from **11 to 19 entries**. `conventional-accounting.json` reaches its
**terminal** size here and never grows again; `sharia-accounting.json` also reaches 19, continuing
in plan 16. Both landings (created by plan 14) are **updated**, not created, here —
`conventional-accounting`'s landing states path completeness for the first time.

What ships in this plan:

- **Both manifests grown to 19** — still byte-identical at every entry, since all eight of this
  plan's courses are shared-spine, not Sharia-specific.
- **Both landing contents, updated** — `conventional-accounting` states completeness; both state the
  Dangerous-2 boundary.
- **Eight syllabus specs**, three Annotated-concept (#14, #15, #18) and five By Example (#12, #13,
  #16, #17, #19).
- **Eight course bodies.**
- **The full Rule-15 retest**, for `conventional-accounting` only (see
  [README.md §Rule-15 disposition](./README.md#rule-15-disposition-for-this-plan)).

What does not ship: courses #1–#11 (plan 14) or #20–#24 (plan 16), any `_index.md` under `paths/`,
any ERP content, any component, any schema, any edit to an existing library course, any building
exercise (A6), and `sharia-accounting.json` growing past 19 entries.

## The silent-failure constraint (continued)

Restated verbatim from plan 14, unchanged by the split. All eight of this plan's courses carry the
mandatory "what still balances while being wrong" section (DD-609) — the constraint plan 14
established starting at course #4 continues unbroken through this plan's own range.

Domain-specific silent failures this plan's own courses guard against:

- a foreign-currency balance translated with the wrong method (current-rate vs. temporal) still
  produces a balancing trial balance;
- intercompany balances consolidated without elimination still foot;
- a control weakness in segregation of duties leaves every individual posting looking correct;
- a payroll tax miscalculation can balance against the wrong liability account and still tie out.

## Personas

Restated verbatim from plan 14 — the split changes delivery unit size, not who the corpus serves.
This plan's own range is where the **conventional-only systems builder** persona reaches full
competence, and where the **ERP-path reader** persona's needs are first concretely met (via this
plan's own Stage-2 signal).

## User Stories

- As a **conventional-only systems builder**, I want courses #12 through #19 to teach me
  multi-currency translation, consolidation, cross-standard reporting, audit controls, payroll/tax,
  treasury, and how to architect a general-ledger system, so that `conventional-accounting` leaves
  me with complete, production-grade competence.
- As a **conventional-only systems builder**, I want `conventional-accounting` to state clearly that
  the path is **complete** at course #19, so that I know I am not missing content that exists
  elsewhere.
- As a **builder of Sharia-compliant systems continuing from plan 14**, I want the same eight
  courses `conventional-accounting` gets, so that when I continue into plan 16's Sharia-specific
  content later I have the full conventional grounding first.
- As a **maintainer**, I want `conventional-accounting.json` to stop growing the moment it reaches
  19 entries, and for that stoppage to be mechanically verifiable, not merely documented.
- As an **ERP-path reader** (via `ayokoding-learning-path-18-skills-erp-enterprise-depth`),
  I want this plan's completion to unblock ERP's Stage-B-equivalent capability concretely, so that
  I am not blocked on accounting content that has not actually landed.
- As the **maintainer**, I want `conventional-accounting`'s landing and full 19-course walk verified
  by the live-site testing triad once, at the point it becomes production-complete, rather than
  deferred to a later plan that ships different content.
- As a **screen-reader or keyboard user**, I want both landings' updated ramp statements to remain
  fully navigable without a mouse.

## Acceptance Criteria (Gherkin)

Nine scenarios. Each uses **exactly one** primary `Given`, one `When`, and one `Then`.

### The ramp

```gherkin
Scenario: Conventional-accounting reaches its terminal, complete state at course nineteen
  Given both manifests have grown to include the full nineteen-course shared spine
  When a reader reaches the end of the conventional-accounting courseOrder
  Then the path landing states the path is complete
  And no further course is ever appended to conventional-accounting.json at any later phase or plan
  But the sharia-accounting manifest's courseOrder is left ready to continue past entry nineteen
```

```gherkin
Scenario Outline: A path landing states its arc and ramp before the course list
  Given the <path> landing is updated with the Dangerous-2 boundary
  When a reader opens /en/learn/paths/skills/<path>
  Then the Dangerous-2 boundary appears before the ordered course list
  And the boundary names both what the reader can do and what the reader cannot yet do
  And conventional-accounting's landing additionally states the path is complete

  Examples:
    | path                    |
    | conventional-accounting |
    | sharia-accounting       |
```

### Composition

```gherkin
Scenario Outline: A manifest links its software-engineering prerequisite instead of walking it
  Given the <path> manifest is grown to include general-ledger-system-architecture
  When a reader inspects its courseOrder
  Then backend-essentials does not appear in courseOrder
  And the general-ledger-system-architecture course declares backend-essentials in its prerequisites frontmatter
  And the <path> landing links that prerequisite course at its canonical /en/learn/courses/ URL

  Examples:
    | path                    |
    | conventional-accounting |
    | sharia-accounting       |
```

```gherkin
Scenario Outline: A two-segment skills path ID resolves end to end across nineteen courses
  Given the <path> manifest declares its pathId and holds nineteen courses
  When a reader walks the path from its landing
  Then the landing, the prev and next controls, and the breadcrumb all resolve against that two-segment path ID for all nineteen courses
  And the ?path=<path> context persists across every course in the walk

  Examples:
    | path                           |
    | skills/conventional-accounting |
    | skills/sharia-accounting       |
```

### Correctness

```gherkin
Scenario: Every course from twelve through nineteen names what still balances while being wrong
  Given a course numbered twelve through nineteen is authored
  When its overview is inspected
  Then it contains an explicit section naming at least one outcome that still balances while being substantively wrong
  And that section names the observable signal, if any, that would reveal the error
```

```gherkin
Scenario: No unverified claim is published as fact
  Given the research seeding this plan's syllabi marked items as Unverified or Needs Verification
  When a syllabus spec or a course body states a claim, including any XBRL taxonomy version or standard citation
  Then the claim carries either a primary-source citation or an explicit confidence marker
  And every item still marked Needs Verification when this plan's own gate runs is registered with a reason
```

```gherkin
Scenario: No standard's text or proprietary structure is reproduced
  Given this plan's eight courses are authored under the licensing posture in tech-docs.md
  When any course body cites a standard, a chart of accounts, or a reference implementation
  Then the standard is restated in original words with only its number, title, and official link cited
  And every chart of accounts in this plan's courses is originally authored
```

### Boundaries and retest

```gherkin
Scenario: This plan's authored slice builds and validates green
  Given both manifests hold nineteen entries and all eight of this plan's course bodies are authored
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations for both manifests
```

```gherkin
Scenario: Conventional-accounting passes its full live-site retest
  Given conventional-accounting is complete at nineteen courses and deployed to production
  When the web-exploratory-tester, web-usability-tester, and web-design-tester triad runs against it
  Then every finding is folded in as an individually tickable, source-attributed checkbox
  And every defect finding is resolved or explicitly deferred with recorded permission before archival
```

## Product Scope

### In scope

- Growth of two existing `PathManifest` JSON manifest data files (created by plan 14) from 11 to 19 entries.
- Extension of each manifest's existing co-located unit test.
- Extension of the shared Gherkin feature file's step definitions to the full 19-course walk.
- Content updates to both existing path landing bundles — `conventional-accounting`'s landing states
  path completeness for the first time.
- Eight syllabus specs under this plan's own `syllabus/courses/`.
- This plan's own slice of both path mirrors (rows for courses #12–#19).
- Eight course bodies under `apps/ayokoding-www/content/en/learn/courses/<course-id>/`.
- The Stage-2 stage-completion signal, recorded in `delivery.md`, at ERP-capability granularity.
- **The full Rule-15 three-tester retest, for `conventional-accounting` only.**
- Manifest integrity, prerequisite-consistency, ownership-boundary, licensing, and ramp
  verification at every phase gate.

### Out of scope

- **Courses #1–#11 and #20–#24.**
- **Growing `sharia-accounting.json` past 19 entries.**
- **Every `_index.md` under `paths/`.**
- **All ERP content.**
- **Any rendering component, route wiring, or design asset.**
- **The `PathManifest` schema, the `course-paths` core modules, and the integrity functions.**
- **The `careers/` manifests and their landings.**
- **Any edit to an existing library course.**
- **Any edit to plan 02's frozen `syllabus/` corpus, plan 14's own `syllabus/` folder, or plan 16's
  (once it exists).**
- **An Indonesian mirror** of either path.
- **A second skills arc.**
- **Certification-syllabus coverage**, tax-jurisdiction depth, and corporate finance.
- **Any building exercise, capstone, or scaffolded codebase (A6).**
- **Reproducing any standard's text, proprietary chart-of-accounts structure, or copyleft
  reference-implementation code (A8).**
- **A Rule-15 retest for `sharia-accounting`** — deferred to plan 16.

### UI-design-funnel disposition

**Exempt — and the exemption is recorded, not silently taken.** This plan adds **no net-new screen
and no net-new component**, restated from plan 14. This plan ships **content and data into** the
existing two landing screens, plus growth of two existing manifest data files.

## Product-Level Risks

- **A course teaches something plausible and wrong** (especially multi-currency and consolidation).
  Mitigated by the mandatory silent-failure section and the fact-checker on every body.
- **`conventional-accounting.json` is silently extended past 19**, eroding the "the whole path is
  done at #19" promise. Mitigated by a falsifiable `git diff --quiet` clause at every later phase
  gate, including plan 16's own gates.
- **Licensing exposure (A8)**, especially XBRL taxonomy version drift. Mitigated by the eleven
  safe-authoring rules and the "fast-moving facts, re-verify at authoring" rule for volatile
  citations.
- **The Stage-2 signal is misread as a course-number reference** rather than a capability
  description. Mitigated by the field's own name (`UNBLOCKS_ERP_CAPABILITY`) and explicit
  reasoning in tech-docs.md.
- **Prerequisite drift.**
- **Scope collision with courses #20+.**
- **Scope collision with the library.**
- **Cross-plan file collision with plan 16's own future growth of `sharia-accounting.json`.**
- **Either landing reads as a syllabus.**
- **The Rule-15 retest for `conventional-accounting` surfaces defects that block this plan's own
  archival** — mitigated by treating every EWT/UWT/DWT defect finding as mandatory-fix, per
  governance, with deferral only by explicit recorded permission.
