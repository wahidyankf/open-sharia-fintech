# Product Requirements — Skills Path: Accounting

## Product Overview

One path, one manifest, twenty courses, served at `/en/learn/paths/skills/accounting`.

A **skills path** is a subject-scoped reading arc over the shared course library, addressed as
`skills/<subject>` — two URL segments, not the three that `careers/<arc>/<role>` uses. The arc
segment is absent because every skills path **is** the `immediately-effective` arc (R8): get up and
running and become dangerous as fast as possible, then go deeper and deeper, on solid ground. The arc
is constant, so naming it in every URL would be noise — but it is still recorded as `arc:
immediately-effective` in the manifest data, which is what keeps a future `skills/<arc>/<subject>`
grammar purely additive.

What ships:

- **The manifest** — `manifests/skills/accounting.yaml`: `pathId: skills/accounting`, `arc:
immediately-effective`, a title, a description, and a 20-entry `courseOrder`.
- **The landing content** — the copy at `content/en/learn/paths/skills/accounting/_index.md`: the arc
  promise, the three ramp boundaries, and the outbound links to the two linked prerequisites. The
  ordered course list renders from the manifest; the landing never hand-lists it. _(The landing's
  visual design belongs to `ayokoding-learning-path-03-navigation-ui`; this plan supplies content and
  states requirements, and ships no mockup or render.)_
- **Twenty syllabus specs** — the per-course contract layer, in this plan's own `syllabus/courses/`.
- **Twenty course bodies** — full page bundles under `content/en/learn/courses/<course-id>/`.

What does not ship: any `_index.md` under `paths/` (plan 01's, per A3), any ERP content (plan 07's),
any component (plan 03's), any schema (plan 02's), and any edit to an existing library course.

## The silent-failure constraint (the corpus-shaping fact)

**Accounting's characteristic failure mode is silent, and that is the single most important
pedagogical constraint on this corpus.**

A trial balance still balances when:

- revenue is recognised in the wrong period;
- a lease is classified as an operating cost when it should be capitalised;
- inventory is costed on a method inconsistent with how it is actually consumed;
- intercompany balances are consolidated without elimination;
- a **murabaha markup is booked as interest income**.

In most software domains a wrong abstraction fails loudly — it does not compile, a test goes red, a
request 500s, a queue backs up. Here, nothing goes red. Every total foots. Every report renders.
The numbers are plausible and substantively wrong, and they stay wrong until an auditor, a regulator,
or a restatement finds them.

**Four product consequences follow directly, and none of them is optional:**

1. **The ramp slows after course #3 rather than accelerating.** A reader who has finished #1–#3 owns
   a correctly balancing ledger — and that competence is precisely what makes the next class of
   mistakes invisible to them. They now have a tool that will happily produce a confident wrong
   answer. Accelerating here would be the single most dangerous thing this corpus could do.
2. **Every course from #4 onward carries an explicit "what still balances while being wrong"
   section.** Not a footnote, not a callout at the author's discretion: a required section in the
   course's `overview.md`, verified by a grep-checkable acceptance clause at its authoring step
   ([tech-docs DD-609](./tech-docs.md#design-decisions)). If a course cannot name a plausible-but-wrong
   outcome in its own subject, it has not identified what it is actually teaching.
3. **The Sharia stage sits at the end, not sprinkled through.** Applying conventional
   accrual-and-interest models to murabaha, ijara, mudaraba or musharaka is the exact silent mistake
   AAOIFI and PSAK Syariah exist to prevent — a murabaha receivable schedule and a conventional
   amortising loan schedule can look numerically similar and must be modelled completely differently.
   Teaching that contrast requires the conventional model to already be solid. A reader who meets
   both at once learns neither.
4. **"Dangerous by here" is stated as much by what a reader _cannot_ do as by what they can.** Every
   boundary in the ramp names its own ceiling. A boundary that only advertises new capability trains
   exactly the overconfidence this domain punishes.

## Personas

- **The systems builder with no accounting background** (north-star). Ships software, has been handed
  a ledger, an invoicing feature, a revenue report, or a finance integration, and has no idea which
  of their instincts are wrong. Owns SQL and backend fundamentals or can pick them up from the linked
  library courses. Wants to be useful within three courses and correct by the end. **Does not want a
  certification syllabus.**
- **The reader who only needs the first three courses.** Designing a chart of accounts as a schema,
  or getting a hand-rolled ledger to balance, is the whole of their need. The arc must genuinely pay
  off for them and must tell them plainly where their competence stops.
- **The builder of Sharia-compliant financial systems.** Arrives specifically for #17–#20. Needs
  three jurisdictional models rather than one, because they may be building for Bahrain, Indonesia or
  Malaysia and the three are structurally different. Needs murabaha modelled as a trade, not as a
  loan with different vocabulary.
- **The ERP-path reader arriving from plan 07.** Hits ERP #7 and is sent here for
  `financial-statements-and-close-cycle`. Wants the shortest correct route in and a clear route back
  — not to be enrolled in a second full path.
- **The reader who deep-links a single accounting course** from search or a share, with no `?path=`
  context. Must get a coherent standalone view with its prerequisites surfaced, including the linked
  library prerequisites, plus an obvious way into the path.
- **Maintainer** (content strategist / domain researcher / content author / frontend engineer /
  reviewer) — owns the ramp, the verification debt, the corpus, the manifest, and the review loop.

## User Stories

- As a **systems builder with no accounting background**, I want the first three courses to leave me
  with a working, correctly balancing ledger, so that I get real capability before I invest in depth.
- As a **systems builder**, I want the landing to tell me exactly what I still cannot safely do at
  each ramp boundary, so that I do not mistake early competence for coverage.
- As a **systems builder**, I want every course past the foundations to name the mistakes that still
  balance, so that I can recognise a plausible wrong answer instead of trusting the totals.
- As a **reader who only needs a ledger schema**, I want courses #1 and #2 to be standalone-useful,
  so that I can stop after two courses without having learned half of something.
- As a **builder of Sharia-compliant systems**, I want the standards courses to present AAOIFI, PSAK
  Syariah and MFRS-plus-BNM as three coexisting models, so that I am not confidently wrong in two of
  the three jurisdictions I might build for.
- As a **builder of Sharia-compliant systems**, I want murabaha modelled as a trading transaction
  with a disclosed markup rather than as accrued interest, so that my receivable schedule and my
  revenue recognition are both right.
- As an **ERP-path reader**, I want the accounting courses my ERP course depends on to be reachable
  and finishable on their own, so that a cross-domain prerequisite is a detour and not a second
  curriculum.
- As a **reader who deep-links one accounting course**, I want its prerequisites surfaced — including
  the linked software-engineering ones — so that I can tell whether I am ready for it.
- As a **reader who already knows SQL**, I want the path not to re-teach `sql-essentials`, so that a
  subject path stays a subject path.
- As the **maintainer**, I want no unverified standard number or doctrinal claim to reach a published
  course, so that the corpus is trustworthy in exactly the places where being wrong is expensive.
- As the **maintainer**, I want the manifest to be published early and grown in recorded stages, so
  that a truncated path cannot pass as complete and plan 07 is unblocked at the earliest safe moment.
- As the **maintainer of plan 07**, I want a complete, five-field stage signal for each stage, so that
  I can start ERP work against a verified prerequisite rather than a guess.
- As a **screen-reader or keyboard user**, I want the landing's ramp statement and the ordered course
  list to be fully navigable without a mouse, so that path selection works without pointing.

## Acceptance Criteria (Gherkin)

Eleven scenarios. Each uses **exactly one** primary `Given`, one `When`, and one `Then`; every extra
precondition, action, or outcome chains with `And`. Each is bound to a delivery step in
[delivery.md](./delivery.md).

### The ramp

```gherkin
Scenario: The first ramp boundary is reachable in three courses
  Given the accounting path manifest is published with courses 1 through 3 in courseOrder
  When a reader finishes the third course
  Then the reader can build a correctly balancing ledger and produce the three statements for a single entity
  And the landing states that the reader cannot yet safely handle revenue recognition, inventory costing, leases, consolidation, or dual IFRS-and-GAAP reporting
```

```gherkin
Scenario: The landing states the arc and the ramp before the course list
  Given the accounting path landing is published
  When a reader opens /en/learn/paths/skills/accounting
  Then the immediately-effective promise and all three dangerous-by-here boundaries appear before the ordered course list
  And each boundary names both what the reader can do and what the reader cannot yet do
  And the ordered course list is rendered from the manifest rather than hand-listed in the landing
```

### Composition

```gherkin
Scenario: The accounting manifest links its software-engineering prerequisites instead of walking them
  Given the accounting path manifest is published
  When a reader inspects its courseOrder
  Then neither sql-essentials nor backend-essentials appears in courseOrder
  And the chart-of-accounts course declares sql-essentials in its prerequisites frontmatter
  And the general-ledger capstone declares backend-essentials in its prerequisites frontmatter
  And the landing links both prerequisite courses at their canonical /en/learn/courses/ URLs
```

```gherkin
Scenario: A two-segment skills path ID resolves end to end
  Given the manifest declares pathId skills/accounting and arc immediately-effective
  When a reader walks the path from its landing
  Then the landing, the prev and next controls, and the breadcrumb all resolve against the two-segment path ID
  And the ?path=skills/accounting context persists across every course in the walk
  And no resolver assumes a three-segment path ID
```

```gherkin
Scenario: The manifest grows in recorded stages rather than shipping truncated
  Given the manifest is first published with only the three Stage 1 courses
  When each later authoring stage completes
  Then the manifest grows to sixteen and then to twenty course IDs
  And every deferred course ID is recorded as absent at publication and asserted present after its growth step
```

### Correctness

```gherkin
Scenario: Every post-foundations course names what still balances while being wrong
  Given a course from number four onward is authored
  When its overview is inspected
  Then it contains an explicit section naming at least one outcome that still balances while being substantively wrong
  And that section names the observable signal, if any, that would reveal the error
```

```gherkin
Scenario: The Sharia stage presents three jurisdictional models
  Given the Sharia-standards, contract-modelling, and Sharia-ledger courses are authored
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
Scenario: No unverified claim is published as fact
  Given the research seeding this plan marked items as Unverified or Needs Verification
  When a syllabus spec or a course body states a standard number or a doctrinal position
  Then the claim carries either a primary-source citation or an explicit confidence marker
  And no item marked Needs Verification remains open when the Sharia stage begins
```

### Boundaries

```gherkin
Scenario: The accounting corpus never re-teaches a linked library course
  Given the accounting corpus is authored
  When a course's scope is compared with the library course it links as a prerequisite
  Then the course states its scope boundary against that library course explicitly
  And no accounting course teaches relational modelling, query performance, or HTTP service construction as its own subject
```

```gherkin
Scenario: The accounting path builds and validates green
  Given the manifest is at its full twenty-course composition and every body is authored
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations for the accounting manifest
  And the manifests directory contains exactly one file this plan owns
```

## Product Scope

### In scope

- One `PathManifest` YAML data file at
  `apps/ayokoding-www/src/features/course-paths/manifests/skills/accounting.yaml`, carrying
  `pathId: skills/accounting` and `arc: immediately-effective`.
- One path landing bundle at `apps/ayokoding-www/content/en/learn/paths/skills/accounting/_index.md`
  — prose, SEO metadata, the arc statement, the three-boundary ramp, and the outbound links to the
  two linked prerequisites. **No `courseOrder` in the landing.**
- Twenty syllabus specs under this plan's own `syllabus/courses/`, one per course ID.
- Twenty course bodies under `apps/ayokoding-www/content/en/learn/courses/<course-id>/`, each a full
  page bundle in the established anatomy.
- Population of this path's card in the paths-hub / skills-category surfaces that plans 01 and 03
  own, as content only.
- Three stage-completion signals recorded in `delivery.md` for plan 07's consumption.
- Manifest integrity, prerequisite-consistency, ownership-boundary and ramp verification at every
  phase gate.

### Out of scope

- **Every `_index.md` under `paths/`**, including `paths/skills/_index.md` — plan 01's (A3).
- **All ERP content** — plan 07's.
- **Any rendering component, route wiring, or design asset** — plan 03's. This plan carries no
  `assets/` folder and produces no mockup or render.
- **The `PathManifest` schema, the `course-paths` core modules, and the integrity functions** —
  plan 02's. This plan runs them; it does not author them.
- **The `careers/` manifests and their landings** — plan 05's.
- **Any edit to an existing library course**, including adding an accounting section to
  `sql-essentials` or `backend-essentials`.
- **Any edit to plan 02's frozen `syllabus/` corpus.** This plan's specs live in this plan's folder
  ([tech-docs DD-601](./tech-docs.md#design-decisions)).
- **An Indonesian mirror** of the path or the corpus.
- **A second skills arc**, a second skills subject, or a `skills/<arc>/<subject>` URL grammar.
- **Certification-syllabus coverage**, tax-jurisdiction depth, and corporate finance.

### UI-design-funnel disposition

**Exempt — and the exemption is recorded, not silently taken.**

This plan adds **no net-new screen and no net-new component**. The skills path landing is rendered by
`path-landing.tsx` and its siblings, all owned by `ayokoding-learning-path-03-navigation-ui`, which
holds the whole `assets/` and `assets/src/` set for this programme and is extending it to cover
skills-path landings. This plan ships **content and data into** that screen.

What this plan does contribute is a **requirement**, not a design: the **ramp affordance**. A skills
path must tell a reader _how far in they become useful_, and that concept has no careers-path
equivalent — a careers path converges on a role, a skills path converges on a capability with named
intermediate landings. The full statement of what the landing must convey is in
[tech-docs §Landing content contract](./tech-docs.md#landing-content-contract--what-it-must-convey),
handed to plan 03 as the distinguishing requirement for skills-path landings.

The exemption is scoped to the **design funnel only**. Because this plan ships a user-visible
surface, the **Rule-15 three-tester retest remains mandatory** and runs in
[Phase 7](./delivery.md#phase-7-manual-ui-verification-and-rule-15-three-tester-retest).

## Product-Level Risks

- **A course teaches something plausible and wrong.** The domain's own failure mode, reproduced by
  the material. Mitigated by the mandatory "what still balances while being wrong" section from #4
  onward, the deliberately slow post-#3 ramp, and the fact-checker on every body.
- **Overconfidence at a ramp boundary.** A reader finishes #3, believes they are done, and ships a
  revenue model. Mitigated by every boundary stating its ceiling as prominently as its capability,
  asserted in both the landing scenario and the ramp scenario.
- **Sharia content flattened to one standard.** Mitigated by the three-model invariant asserted per
  course at #17, #18 and #20, including the two specific facts that are easiest to get wrong —
  Malaysia's absence from the mandatory-adoption list, and Indonesia's use of AAOIFI as a basis
  rather than an adoption.
- **Verification laundering.** An `[Unverified]` research line becomes a confident sentence in a
  published course. Mitigated by Phase 4 gating the Sharia stage, per-claim confidence markers, and a
  gate asserting zero open `[Needs Verification]` items.
- **Silent truncation.** The 3-course manifest passes integrity and is never grown. Mitigated by
  falsifiable before/after deferred-ID checks at publication and at each growth step, plus a terminal
  20-ID assertion.
- **Prerequisite drift.** The linked prerequisites get walked (turning the path into a
  software-engineering path) or get forgotten (leaving course #2 unreachable). Mitigated by asserting
  **both** halves: absent from `courseOrder`, present in the frontmatter.
- **Scope collision with ERP.** Shared vocabulary pulls an accounting course into module design.
  Mitigated by explicit, grep-checkable scope-boundary statements in the affected bodies, and by the
  clean one-directional dependency: no accounting course cites an ERP course.
- **Scope collision with the library.** `chart-of-accounts-and-data-modeling` drifts into teaching
  SQL; `capstone-build-a-general-ledger-system` drifts into teaching HTTP services. Mitigated by the
  same boundary-statement rule, applied against the linked library course.
- **Cross-plan file collision.** Two skills plans, one manifests directory, one structural index.
  Mitigated by one manifest file per plan and by A3 assigning every `_index.md` under `paths/` to
  plan 01; asserted by the Phase 6 ownership-footprint check.
- **The landing reads as a syllabus.** Mitigated by the landing content contract ordering the arc and
  ramp ahead of the list, by the list rendering from the manifest, and by the Rule-15 usability
  tester exercising the live page.
- **Prior-art contamination.** `business/accounting.md` is transplanted rather than mined, importing
  a small-business-owner register into a systems-builder course. Mitigated by DD-606's explicit rule
  — harvest the running example and the sequencing, discard the register, and leave the data-modelling
  layer to course #2 — plus a checker pass on the authored body.
