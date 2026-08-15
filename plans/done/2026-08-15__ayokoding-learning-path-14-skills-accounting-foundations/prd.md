# Product Requirements — Skills Paths: Accounting Foundations & Transactional Cycles

> **Programme decisions** — the `R*`/`A*` decisions cited below are defined locally in
> [tech-docs.md §Programme decisions](./tech-docs.md#programme-decisions).

## Product Overview

Courses #1–#11 of a twenty-four-course catalog, split across three sequential plans (14 → 15 → 16).
This plan **creates** both manifests — `manifests/skills/conventional-accounting.json` and
`manifests/skills/sharia-accounting.json` — and grows each to **eleven** entries. It **creates**
both path landings — `/en/learn/paths/skills/conventional-accounting` and
`/en/learn/paths/skills/sharia-accounting` — with content stating the arc promise and the
Dangerous-1 boundary.

A **skills path** is a subject-scoped reading arc over the shared course library, addressed as
`skills/<subject>` — two URL segments. The arc segment is absent because every skills path **is**
the `immediately-effective` arc (R8). Both manifests record `arc: immediately-effective`.

What ships in this plan:

- **Two manifests, created here** — both hold the **same** 11 IDs, in the same order, since
  courses #1–#11 are entirely shared-spine courses (no Sharia-specific course exists in this
  plan's range). The two manifest files are byte-identical in their `courseOrder` at the end of this
  plan — the same falsifiable invariant the retired plan asserted at every shared-growth step.
- **Two landing contents, created here** — the arc promise, the Dangerous-1 boundary, and the
  outbound link to `sql-essentials` (the one linked prerequisite reachable within this plan's range;
  `backend-essentials` is linked by course #19, in plan 15, and is not referenced here).
- **Eleven syllabus specs**, each carrying a module/topic breakdown.
- **Eleven course bodies**, all By Example format (no Annotated-concept course falls in this range —
  see [tech-docs.md §The eleven-course catalog slice](./tech-docs.md#the-eleven-course-catalog-slice-courses-111)).

What does not ship: courses #12–#24 (plans 15, 16), any `_index.md` under `paths/` (plan 01's, A3),
any ERP content, any component (plan 03's), any schema (plan 02's), any edit to an existing library
course, any building exercise or capstone (A6), and neither manifest growing past 11 entries.

## The silent-failure constraint (the corpus-shaping fact)

**Accounting's characteristic failure mode is silent, and that is the single most important
pedagogical constraint on this plan's own course range**, restated verbatim from the retired plan
because nothing about the constraint changes with the split.

A trial balance still balances when:

- revenue is recognised in the wrong period;
- a purchase or sale is posted to the wrong period or account;
- a fixed asset is depreciated on a method inconsistent with its actual consumption;
- a lease is classified as an operating cost when it should be capitalised;
- inventory is costed on a method (FIFO/LIFO/weighted-average) inconsistent with how it is actually
  consumed.

**Product consequences, applicable to this plan's own range:**

1. **The ramp slows after course #3 rather than accelerating.** Three courses buy a reader a
   correctly balancing ledger and the three statements — and that competence is exactly what makes
   the next mistakes invisible to them.
2. **Every course from #4 through #11 carries an explicit "what still balances while being wrong"
   section.** Required in all eight of this plan's Stage-1B courses (#4–#11); courses #1–#3 do not
   carry it, matching the retired plan's own Stage-1 exemption.
3. **"Dangerous by here" is stated as much by what a reader _cannot_ do as by what they can**, on
   both landings, at the Dangerous-1 boundary.

Courses #12–#24 (plans 15, 16) extend this same constraint into reporting, consolidation, and
Sharia-specific failure modes — unchanged in kind, carried forward by those sibling plans rather
than restated here.

## Personas

Restated verbatim from the retired plan — the split changes delivery unit size, not who the corpus
serves.

- **The systems builder with no accounting background, conventional-only** (north-star for
  `conventional-accounting`). Ships software, has been handed a ledger, an invoicing feature, or a
  finance integration, has no Sharia requirement. Wants to be useful within three courses. Within
  this plan's own range, becomes able to run a mid-size company's full transactional cycle by
  course #11.
- **The builder of Sharia-compliant financial systems** (north-star for `sharia-accounting`).
  Arrives either cold or after finishing `conventional-accounting`. Within this plan's range, gets
  the same eleven foundation-and-cycle courses `conventional-accounting` gets — the Sharia-specific
  depth (courses #20–#24) does not begin until plan 16.
- **The reader who only needs the first three courses.** The arc must genuinely pay off early, in
  either path.
- **The ERP-path reader arriving from `ayokoding-learning-path-18-skills-erp-enterprise-depth`.**
  Not yet served by this plan's own stage signal (see
  [tech-docs.md §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-18-handoff-stage-granularity)) —
  this persona's needs are met once plan 15 completes, but the persona still benefits from this
  plan's course #3 (the shared record-to-report hard edge) being reachable.
- **The reader who deep-links a single accounting course** from search or a share, with no
  `?path=` context. Must get a coherent standalone view with prerequisites surfaced.
- **Maintainer** (content strategist / domain researcher / licensing steward / content author /
  frontend engineer / reviewer).

## User Stories

- As a **conventional-only systems builder**, I want the first three courses to leave me with a
  working, correctly balancing ledger, so that I get real capability before I invest in depth.
- As a **systems builder**, I want courses #4 through #11 to teach me the full day-to-day
  transactional cycle — journal entries, revenue recognition, AP, AR, managerial/cost accounting,
  fixed assets, inventory, and leases — so that I can model the operational reality of a mid-size
  company's books.
- As a **systems builder**, I want every course past the foundations to name the mistakes that still
  balance, so that I can recognise a plausible wrong answer instead of trusting the totals.
- As a **builder of Sharia-compliant systems entering cold**, I want the same eleven foundation
  courses `conventional-accounting` teaches, so that when I continue into plan 16's Sharia-specific
  content later I am not missing any conventional grounding.
- As a **maintainer**, I want both manifests to share these eleven courses by reference rather than
  by duplication from the very first entry, so that the shared-course pattern is established
  correctly before either manifest grows further in a later plan.
- As a **maintainer**, I want no course in this plan's range to teach a standard's text verbatim, a
  proprietary chart-of-accounts structure, or copyleft reference-implementation code.
- As the **maintainer**, I want no unverified standard number or claim to reach a published course in
  this plan's range.
- As the **maintainer**, I want both manifests published early (at 3 entries) and grown once more
  within this same plan (to 11), so that plan 15 has a concrete, merged starting point to grow from
  rather than an empty or ambiguous one.
- As a **screen-reader or keyboard user**, I want both landings' ramp statements and ordered course
  lists to be fully navigable without a mouse.

## Acceptance Criteria (Gherkin)

Eleven scenarios. Each uses **exactly one** primary `Given`, one `When`, and one `Then`; every extra
precondition, action, or outcome chains with `And`. `Scenario Outline` / `Examples` are used for the
checks that repeat identically per path.

**How these relate to `delivery.md`'s embedded Gherkin** — they are two levels, not two copies,
exactly as in the retired plan: the scenarios below are **requirement-level**; `delivery.md`'s
fenced `Gherkin (binds)` blocks are the **execution-level** bindings copied into `specs/**` at
authoring time.

### The ramp

```gherkin
Scenario: The first ramp boundary is reachable in three courses
  Given both accounting manifests are published with courses 1 through 3 in courseOrder
  When a reader finishes the third course
  Then the reader can build a correctly balancing ledger and produce the three statements for a single entity
  And both landings state that the reader cannot yet safely handle journal-entry mechanics, revenue recognition, procurement, order-to-cash, cost accounting, fixed assets, inventory, or leases
```

```gherkin
Scenario Outline: A path landing states its arc and ramp before the course list
  Given the <path> landing is published
  When a reader opens /en/learn/paths/skills/<path>
  Then the immediately-effective promise and the Dangerous-1 boundary appear before the ordered course list
  And the boundary names both what the reader can do and what the reader cannot yet do
  And the ordered course list is rendered from that path's manifest rather than hand-listed in the landing

  Examples:
    | path                    |
    | conventional-accounting |
    | sharia-accounting       |
```

### Composition

```gherkin
Scenario Outline: A manifest links its software-engineering prerequisite instead of walking it
  Given the <path> manifest is published
  When a reader inspects its courseOrder
  Then sql-essentials does not appear in courseOrder
  And the chart-of-accounts course declares sql-essentials in its prerequisites frontmatter
  And the <path> landing links that prerequisite course at its canonical /en/learn/courses/ URL

  Examples:
    | path                    |
    | conventional-accounting |
    | sharia-accounting       |
```

```gherkin
Scenario Outline: A two-segment skills path ID resolves end to end
  Given the <path> manifest declares its pathId and arc immediately-effective
  When a reader walks the path from its landing
  Then the landing, the prev and next controls, and the breadcrumb all resolve against that two-segment path ID
  And the ?path=<path> context persists across every course in the walk
  And no resolver assumes a three-segment path ID

  Examples:
    | path                           |
    | skills/conventional-accounting |
    | skills/sharia-accounting       |
```

```gherkin
Scenario: Both manifests are created identically and grow together within this plan
  Given neither manifest exists before this plan runs
  When Phase 2 and Phase 3 complete
  Then both manifests hold exactly the same eleven course IDs, in the same order
  And no course file exists at two different paths for the same subject matter
  And neither manifest's courseOrder exceeds eleven entries
```

### Correctness

```gherkin
Scenario: Every course from four through eleven names what still balances while being wrong
  Given a course numbered four through eleven is authored
  When its overview is inspected
  Then it contains an explicit section naming at least one outcome that still balances while being substantively wrong
  And that section names the observable signal, if any, that would reveal the error
```

```gherkin
Scenario: Courses one through three carry no silent-failure section
  Given courses one, two, and three are authored
  When each overview is inspected
  Then none of them is required to carry a silent-failure section
  And each instead states the forward boundary to the next course
```

```gherkin
Scenario: No unverified claim is published as fact
  Given the research seeding this plan's syllabi marked items as Unverified or Needs Verification
  When a syllabus spec or a course body states a claim
  Then the claim carries either a primary-source citation or an explicit confidence marker
  And every item still marked Needs Verification when this plan's Phase 4 gate runs is registered with a reason in verification-log.md
```

```gherkin
Scenario: No standard's text or proprietary structure is reproduced
  Given this plan's eleven courses are authored under the licensing posture in tech-docs.md
  When any course body cites a standard, a chart of accounts, or a reference implementation
  Then the standard is restated in original words with only its number, title, and official link cited
  And every chart of accounts in this plan's courses is originally authored rather than copied from any source
```

### Boundaries

```gherkin
Scenario: This plan's corpus never re-teaches the linked library course
  Given this plan's eleven-course corpus is authored
  When course two's scope is compared with sql-essentials
  Then course two states its scope boundary against sql-essentials explicitly
  And no course in this plan's range teaches relational modelling or query performance as its own subject
```

```gherkin
Scenario: This plan's authored slice builds and validates green
  Given both manifests hold eleven entries and all eleven course bodies are authored
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations for both manifests
```

## Product Scope

### In scope

- Two `PathManifest` JSON manifest data files, **created by this plan**, each grown to 11 entries.
- Each manifest's own co-located unit test.
- One shared Gherkin feature file (Scenario Outline, two Examples rows) and its step-definition file.
- Two path landing bundles, **created by this plan**. **No `courseOrder` in either landing.**
- Eleven syllabus specs under this plan's own `syllabus/courses/`, each with a module/topic
  breakdown.
- Eleven course bodies under `apps/ayokoding-www/content/en/learn/courses/<course-id>/`.
- Manifest integrity, prerequisite-consistency, ownership-boundary, licensing, and ramp
  verification at every phase gate.

### Out of scope

- **Courses #12–#24** — plans 15 and 16.
- **Growing either manifest past 11 entries.**
- **Every `_index.md` under `paths/`** — plan 01's (A3).
- **All ERP content** — plan 18's.
- **Any rendering component, route wiring, or design asset** — plan 03's.
- **The `PathManifest` schema, the `course-paths` core modules, and the integrity functions** —
  plan 02's.
- **The `careers/` manifests and their landings** — plan 05's.
- **Any edit to an existing library course.**
- **Any edit to plan 02's frozen `syllabus/` corpus, or to any sibling plan's own `syllabus/`
  folder.**
- **An Indonesian mirror** of either path.
- **A second skills arc**, a second skills subject, or a `skills/<arc>/<subject>` URL grammar.
- **Certification-syllabus coverage**, tax-jurisdiction depth, and corporate finance.
- **Any building exercise, capstone, or scaffolded codebase (A6).**
- **Reproducing any standard's text, proprietary chart-of-accounts structure, or copyleft
  reference-implementation code (A8).**

### UI-design-funnel disposition

**Exempt — and the exemption is recorded, not silently taken.** This plan adds **no net-new screen
and no net-new component**, for either path. Both skills path landings are rendered by
`path-landing.tsx` and its siblings, all owned by `ayokoding-learning-path-03-navigation-ui`. This
plan ships **content and data into** those screens — the same exemption reasoning the retired plan
recorded, unchanged by the split.

What this plan contributes is a **requirement**, not a design: the **ramp affordance** for the
Dangerous-1 boundary, and (on the Sharia landing) the **path-choice affordance** distinguishing
`conventional-accounting` from `sharia-accounting`. Both are handed to plan 03.

The exemption is scoped to the **design funnel only**. Manual Playwright MCP verification is
mandatory and performed in this plan's Phase 5, and **this plan's own Rule-15 three-tester retest
also runs in Phase 5**, scoped to the two live partial landings as they exist at this plan's end —
see [README.md §Rule-15 disposition](./README.md#rule-15-disposition-for-this-plan--scoped-retest-against-the-eleven-course-slice).

## Product-Level Risks

- **A course teaches something plausible and wrong.** Mitigated by the mandatory "what still
  balances while being wrong" section from #4 onward, the deliberately slow post-#3 ramp, and the
  fact-checker on every body.
- **A shared course drifts because both manifests reference it and only one path's authoring pass
  reviews it.** Mitigated by authoring each course exactly once and by the Phase 5 sweep asserting
  byte-identical `courseOrder` entries across both manifests.
- **Either manifest is silently extended past 11 entries within this plan**, eroding the "plan 15
  grows from exactly 11" contract. Mitigated by a falsifiable clause at every later phase gate.
- **Licensing exposure (A8).** Mitigated by the eleven safe-authoring rules, a Phase 5 reading
  audit, and the explicit flag that no public-domain chart of accounts exists.
- **This plan's Rule-15 retest, scoped to 11 courses, misses a defect that only manifests once
  either manifest grows to 19/24.** Mitigated by plans 15 and 16 each running their own follow-up
  retest scoped to their own incremental delta; see [README.md §Rule-15 disposition](./README.md#rule-15-disposition-for-this-plan--scoped-retest-against-the-eleven-course-slice).
- **Overconfidence at a ramp boundary.**
- **Prerequisite drift.**
- **Scope collision with courses #12+.**
- **Scope collision with the library.**
- **Cross-plan file collision with plan 15/16's own future work on the same two manifest files.**
- **Either landing reads as a syllabus.**
- **Prior-art contamination** from `business/accounting.md`.
