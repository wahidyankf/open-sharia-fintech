# Product Requirements — Learning Path Manifests

## Product Overview

Four **path manifests** compose the shared course library into four readable journeys. A manifest is
an ordered, prerequisite-consistent list of course IDs — a **path ID**, a display **title**, a
**description**, and a `courseOrder` — stored as a standalone YAML data file under
`apps/ayokoding-www/src/features/course-paths/manifests/`, nested to mirror each slash path ID.
Each manifest gets a thin content **landing anchor** (prose/SEO only, no `courseOrder`) at
`/en/learn/paths/<path-id>`, and a card in the paths hub's `careers/` group — the hub is
category-grouped, not a flat 2×2 grid, now that it also serves the sibling `skills/` category (see
[tech-docs.md DD-34](./tech-docs.md#design-decisions); hub layout owned by
`ayokoding-learning-path-03-navigation-ui`).

The three `software-engineer` paths converge on the same software-engineering deep mastery; the
fourth path converges on a distinct AI-engineering deep mastery — convergence is a **per-role**
property, not a library-wide axiom (see [tech-docs.md DD-22](./tech-docs.md#design-decisions)):

- **`careers/interview-ready/software-engineer`** — the **interview/job-prep-first** arc for an experienced
  engineer re-entering the market: interview prep FIRST → production-effective → deeper.
- **`careers/immediately-effective/software-engineer`** — the **immediately-effective** arc: editor/tooling →
  one language end-to-end → **build a real app first** → then deepen.
- **`careers/fundamentally-strong/software-engineer`** — the **university-style, fundamentals-first** arc:
  CS foundations / theory first → deeper.
- **`careers/immediately-effective/ai-engineer`** — a **from-scratch** AI-engineering arc (renamed
  and re-scoped 2026-07-21, DD-35 — no longer a role transition): assumes **no** prior
  software-engineering competence; SWE-fundamentals prerequisite courses are **included** at the head
  of `courseOrder`, not linked out, so a reader with zero programming background can start at
  `courseOrder[0]` and finish; teaches **building** AI systems (models, agents, evals, inference
  serving), not driving them (`agentic-coding` stays a separate, unrelated axis). Its `courseOrder`
  also **walks** the nine-course AI/harness cluster directly (DD-33).

**This product surface is composition only.** No course body is authored here; no rendering component
is built here. What ships is: four YAML manifests, four landing anchors, four hub cards, the
integrity and smoothness verification that keeps them honest, and the growth that closes each
smoke-test-scoped manifest as backfill lands.

## Personas

Reproduced verbatim from the source plan. All four path personas are carried, not only the ones whose
manifest ships first — every path landing this plan publishes is reached by readers of all four
paths, and a reviewer cannot assess fit-for-purpose against a subset.

- **Experienced engineer re-entering the job market (north-star for the
  `careers/interview-ready/software-engineer` path)** — recently laid off, returning from a gap/sabbatical, or
  an employed senior wanting to switch. Already owns the editor workflow and deep fundamentals; needs
  to **refresh breadth fast, relearn interview technique** at mid/senior/staff level, and handle a
  **layoff / employment-gap narrative** — without walking a from-scratch curriculum. Interview/job prep
  FIRST.
- **A builder who wants to be effective fast (north-star for the
  `careers/immediately-effective/software-engineer` path)** — wants "immediately effective" SWE: set up the
  editor, learn one language end-to-end, **ship a real app early**, then deepen into CS fundamentals,
  DS&A, algorithms, and systems. Serves both a from-scratch learner and a mid-career switcher.
- **A university-style, fundamentals-first learner (north-star for the
  `careers/fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route: CS
  foundations, computer architecture, paradigms, and data structures & algorithms **before** building
  apps at scale. Prefers to understand the machine and the theory first, then apply it.
- **A reader with no assumed prior software-engineering competence, aiming straight at AI
  engineering (north-star for the `careers/immediately-effective/ai-engineer` path, added
  2026-07-20, corrected 2026-07-21 — no longer a transition path)** — owns none of the SWE
  fundamentals the other three paths teach; wants to become immediately effective at **building**
  AI systems (models, agents, evals, inference serving), not at driving coding agents. Its
  foundational SWE prerequisites are **included at the head of `courseOrder`**, not linked out —
  a reader with zero programming background can start at `courseOrder[0]` and finish. Those
  included prerequisites are existing library courses (see
  [tech-docs.md DD-35](./tech-docs.md#design-decisions)); no new course body is authored for
  them. Converges on a distinct AI-engineering endpoint, not the other three paths' shared
  software-engineering endpoint.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced) plus an
  obvious way to enter a path.
- **Maintainer (content strategist / frontend engineer / content author / reviewer)** — owns the
  four-path architecture, builds the navigation feature, and authors the NEW courses via the ayokoding
  maker agents.

## User Stories

- As an **experienced engineer re-entering the market**, I want a published interview-ready manifest
  whose order leads with interview technique, so that the first thing I read is the thing I need
  soonest.
- As a **reader with no software-engineering background**, I want the AI-engineering path's
  manifest to **include** its SWE-fundamentals prerequisites at the head of `courseOrder` rather
  than link out to them, so that I can start at `courseOrder[0]` with zero prior programming
  knowledge and finish the whole path from one manifest.
- As a **reader walking the AI-engineering path**, I want `courseOrder` to actually **walk** the
  agent-building courses after the included SWE fundamentals, so that the path teaches what its
  own scope promises once the foundation is laid.
- As a **builder who wants to be effective fast**, I want the immediately-effective manifest to place
  building a real app ahead of every pure-theory course, so that I feel the payoff before I go deep.
- As a **university-style learner**, I want the fundamentally-strong manifest to place CS foundations,
  architecture, paradigms, and DS&A ahead of build-at-scale courses, so that I understand the theory
  before I apply it.
- As a **reader on any path landing**, I want the courses listed in the manifest's exact order with
  the path context carried into every link, so that "next" always means the next course in the arc I
  chose.
- As a **reader who deep-links a shared course**, I want to see every path that includes it, so that I
  can enter whichever arc fits me from wherever I landed.
- As a **reader who bookmarked a legacy section-index entry**, I want the old browse and a new path
  landing to reach the same single canonical body, so that neither route serves me a stale copy.
- As the **maintainer**, I want each manifest verified prerequisite-consistent at its own phase gate,
  so that an invalid ordering fails at the boundary that introduced it rather than months later.
- As the **maintainer**, I want a manifest published early over partial content to carry a falsifiable
  before/after check for the courses it deliberately defers, so that a truncated path cannot pass as
  complete.
- As the **maintainer**, I want every manifest mutation to live in exactly one plan, so that manifest
  growth is never skipped by both plans nor duplicated by two.
- As the **maintainer**, I want the paths hub to render a card per published path as each ships, so
  that the hub is coherent at every intermediate state, not only at the end.
- As a **screen-reader / keyboard user**, I want each path landing's ordered course list and the hub's
  card grid to be fully navigable without a mouse, so that path selection works without pointing.

## Acceptance Criteria (Gherkin)

Nine scenarios: **six inherited** from the source plan (routed to this plan by the split's scenario
map) and **three new** ones the split required.

Each scenario uses exactly one primary `Given`, one `When`, and one `Then`; every extra precondition,
action, or outcome chains with `And`. Provenance is noted above each scenario.

### Inherited scenarios

_Source: `prd.md` scenario at line 1612 — routed whole to this plan._

```gherkin
Scenario: The interview-ready MVP proves the architecture before other path work begins
  Given the careers/interview-ready/software-engineer MVP (an architecture smoke test over already-live topics 1-33) is delivered end-to-end
  When the careers/immediately-effective/ai-engineer path's authoring begins
  Then the interview-ready MVP's landing page, manifest, and path-aware nav are already live in production
  And the interview cluster's remaining NEW courses are not required for that MVP to be considered shipped
```

_Source: `prd.md` scenario at line 1620 — routed whole to this plan. **Not harness-executable**: this
is a build-order assertion about this plan's own phase sequence, verified by reading the delivery
checklist. Kept deliberately; see [README §JC-1](./README.md#jc-1-the-build-order-scenario-is-kept-not-deleted)._

```gherkin
Scenario: The AI path is authored before the other two manifests are composed
  Given the interview-ready MVP has shipped
  When authoring effort is allocated across the remaining paths
  Then the careers/immediately-effective/ai-engineer path's six net-new AI-engineer-role courses (DD-28) and manifest are authored first
  And the careers/immediately-effective/software-engineer and careers/fundamentally-strong/software-engineer manifests are composed only afterward
```

_Source: `prd.md` scenario at line 1644 — routed whole to this plan._

```gherkin
Scenario: The AI-engineer path includes its software-engineering prerequisites instead of linking them (inverted 2026-07-21, see tech-docs.md DD-35)
  Given the careers/immediately-effective/ai-engineer path manifest is published
  When a reader with no prior software-engineering competence inspects its courseOrder
  Then the shared software-engineering-fundamentals courses this path's AI-specific spine depends on are present at the head of courseOrder, ordered prerequisite-consistently
  And that reader can start at courseOrder[0] and finish the whole path from this one manifest, with no external prerequisite link required
```

_Source: `prd.md` scenario at line 1628 — routed whole to this plan._

```gherkin
Scenario: The immediately-effective path is build-app-first
  Given the careers/immediately-effective/software-engineer path manifest is published
  When a reader walks the path
  Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
  And the reader ships a real deployed app before any pure-theory course
```

_Source: `prd.md` scenario at line 1636 — routed whole to this plan._

```gherkin
Scenario: The fundamentally-strong path is fundamentals-first
  Given the careers/fundamentally-strong/software-engineer path manifest is published
  When a reader walks the path
  Then CS foundations, computer architecture, paradigms, and DS&A precede the build-real-software courses
  And the ordering is a valid topological entry into the prerequisite DAG
```

_Source: `prd.md` scenario at line 1604 — routed whole to this plan (straddle S6). Its `Given` requires
all three software-engineer manifests to exist, which is first true at this plan's fourth-manifest
gate. `ayokoding-learning-path-03-navigation-ui` keeps a fixture-level substitute as a checklist
acceptance clause, not as Gherkin._

```gherkin
Scenario: The three software-engineer paths reference a shared course with no body duplication
  Given a course appears in all three of the interview-ready, careers/immediately-effective/software-engineer, and careers/fundamentally-strong/software-engineer manifests
  When the course library is inspected
  Then exactly one canonical path-neutral body exists for that course
  And each manifest references the course by its stable course ID
```

### New scenarios introduced by the split

_New (straddle S3). The source scenario "Old-way and new-way navigation coexist" spanned all three
waves: its legacy-browse half is `ayokoding-learning-path-01-url-restructure`'s narrowed scenario,
and this is its path-landing half, first satisfiable at this plan's first-manifest gate._

```gherkin
Scenario: A path landing and the legacy browse resolve to the same canonical body
  Given a course lives at its canonical /en/learn/courses/<course-id> URL and appears in a published path manifest
  When a reader reaches that course from the path landing at /en/learn/paths/<path-id>
  And another reader reaches it through the legacy section-index browse
  Then both routes resolve to the same single canonical course body
  And neither route serves a duplicated or forked copy of that body
```

_New (straddle S7). The "this course is part of" affordance is rendered by
`ayokoding-learning-path-03-navigation-ui`'s `PathCourseLinks`, but its **content** enumerates every
published manifest, which is this plan's data. The navigation plan keeps its fixture-backed scenario;
this one asserts the real, all-four-manifests behaviour._

```gherkin
Scenario: A shared course names every path that includes it
  Given all four path manifests are published and a course appears in more than one of them
  When a reader opens that course's canonical URL with no path context
  Then the "this course is part of" affordance lists every published path whose manifest includes the course
  And each listed path links to its own path landing page
```

_New (straddle S8 decomposition). The source scenario "The app builds and validates green" conjoined
the navigation feature and the interview-ready path in its `Given`, spanning two plans by
construction, and bound no delivery step. Each of the five split plans writes its own scoped
replacement naming its own surface; this is this plan's. See
[README §JC-2](./README.md#jc-2-the-composite-build-green-scenario-is-decomposed-not-inherited)._

```gherkin
Scenario: The manifest layer builds and validates green
  Given all four path manifests and their landing anchors are published
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations across all four manifests
```

## Product Scope

### In scope

- Four `PathManifest` YAML data files under `apps/ayokoding-www/src/features/course-paths/manifests/`,
  nested to mirror each slash path ID.
- Four thin landing anchors under `apps/ayokoding-www/content/en/learn/paths/<path-id>/_index.md` —
  prose and SEO metadata, plus fast-path affordance. **No `courseOrder` in any landing.** The AI
  path's included SWE-fundamentals prerequisites live in its manifest's `courseOrder`, not as
  outbound landing links (see [tech-docs.md DD-35](./tech-docs.md#design-decisions)).
- Population of the `careers/` group of the paths-hub cards: one card per published `careers/`
  manifest, added as each manifest ships, so the hub is coherent at every intermediate state. The hub
  is category-grouped, not a flat 2×2 grid, owned by `ayokoding-learning-path-03-navigation-ui`.
- Manifest integrity, prerequisite-consistency, and no-forked-body verification at every phase gate.
- Per-path progression-smoothness audits, including the interview-ready refresh-register lever that
  the smoke-test phase deliberately deferred.
- All manifest growth as backfill lands: Bands 1–8 into the three software-engineer manifests, Band 9
  into interview-ready and fundamentally-strong only, and the AI path's growth from its
  smoke-test-scoped starting composition to its full, prerequisite-consistent composition (an open
  course count, not a fixed "6 → 15" figure — see [tech-docs.md DD-35](./tech-docs.md#design-decisions)).
- The four-path blast-radius statement for every course surgery that touches a manifest this plan
  owns.

### Out of scope

- **Any course body.** Owned by `ayokoding-learning-path-04-course-authoring`.
- **Any rendering component or route wiring.** Owned by `ayokoding-learning-path-03-navigation-ui`.
- **The `PathManifest` zod schema, the pure core modules, the `<MANIFESTS>` directory scaffold, and
  the `syllabus/` detail layer.** Owned by `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- **URLs, redirects, the flat `courses/` namespace, the `legacy/` bucket, and the learn-section IA.**
  Owned by `ayokoding-learning-path-01-url-restructure`.
- **A fifth `careers/` path.** The four-path `careers/` composition is locked; a fifth would be its
  own plan. (The sibling `skills/` category's two paths, owned end-to-end by
  `ayokoding-learning-path-06-skills-paths`, are a separate category, not a fifth `careers/` path.)
- **An Indonesian mirror of the path content** — deferred; `id/belajar/` has zero courses and zero
  paths, so a manifest over it would compose nothing.
- **Path-level progress persistence, accounts, or bookmarking.**
- **Speculative course variants.**

### UI-design-funnel disposition

This plan adds **no net-new screen and no net-new component**. It publishes content and data into two
screens whose design funnels are complete and owned by
`ayokoding-learning-path-03-navigation-ui` — Screen 1 (paths hub) and Screen 2 (path landing) — each
already carrying its low-fi alternatives, hi-fi finalists, named selection, rationale, and responsive
record. The full exemption record, with the reasoning and the cross-plan pointers, is in
[tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-recorded-explicitly).

The exemption is scoped to the **design funnel only**. Because this plan does ship user-visible
surfaces (four path landings plus the hub), the **Rule-15 three-tester retest remains mandatory** and
runs in [Phase 7](./delivery.md#phase-7-manual-ui-verification-and-rule-15-three-tester-retest).

## Product-Level Risks

- **Order/manifest drift**: a manifest references a missing or renamed course ID, or orders a course
  before its prerequisite → broken nav / invalid DAG entry. Mitigated by a manifest-integrity check
  (gate + unit test) validating both ID resolution and topological consistency, plus stable course-ID
  slugs.
- **Silent truncation**: a manifest published over partial content is narrowed to whatever exists,
  passes integrity, and is never grown — leaving a path that looks correct and is permanently short.
  Mitigated by writing a falsifiable before/after check at publication time for every deliberately
  deferred course ID, by a dedicated growth phase, and by a terminal gate asserting the full arcs.
- **Growth applied to the wrong manifest**: Band 9's interview-technique courses are appended to
  `careers/immediately-effective/software-engineer`, which omits that band by design. Mitigated by an
  acceptance clause that asserts presence in the two growing manifests **and** continued absence in
  the third, in the same step.
- **Duplication creep**: a path forks a body for its framing. Mitigated by callout-only framing (DD-7 /
  DL-5), a distinct course variant for genuine pedagogy differences, and a no-forked-body check at
  every manifest gate.
- **Ownership erosion**: a step in the course-authoring plan appends a course ID to a `.yaml`, or a
  step here edits a body. Mitigated by the ownership invariant being stated in both plans and by this
  plan's Phase 6 boundary check; any manifest mutation outside this plan is a violation by definition.
- **Per-role convergence confusion**: a reader or future author assumes the fourth path converges with
  the other three, because the plan previously asserted one global endpoint. Mitigated by the explicit
  DD-22 amendment record, cross-referenced from every prose and diagram site that made the original
  single-endpoint claim.
- **Split amendment fragmentation**: DD-7 lands here while its amendment DD-28 lands in
  `ayokoding-learning-path-04-course-authoring`, so a reader of either plan alone inherits a stale
  claim. Mitigated by carrying the amendment sentence verbatim in this plan's DD-7 plus a working
  cross-plan link, with the reciprocal link in the other plan.
- **Course-surgery blast radius**: a surgery on a shared course silently breaks another path's manifest
  or prerequisite chain. Mitigated by DD-28's binding rule — every surgery states its blast radius
  across all four manifests before it is applied, and every affected manifest is re-verified afterward.
- **Landing/manifest divergence**: a landing anchor hand-lists courses and drifts from the manifest it
  is supposed to render. Mitigated by the hard rule that no landing carries a `courseOrder` — the
  ordered list renders from the loaded manifest only — asserted at each landing's authoring step.
- **Hub incoherence mid-flight**: the hub's `careers/` group shows empty or placeholder cards between
  manifest phases. Mitigated by populating exactly one card per shipped `careers/` path at each phase
  and asserting the populated count at that phase's gate.
- **Smoothness regression fixed by reordering**: an audit finding is "fixed" by re-ordering a manifest,
  which can silently break prerequisite-consistency. Mitigated by the audit rule that a regression is
  fixed by softening or bridging **in place, never by reordering**, with the integrity gate re-run
  after any change.
- **Deep-link affordance goes stale**: the "this course is part of" list omits a path added later.
  Mitigated by the affordance enumerating published manifests at build time rather than a hand-written
  list, asserted by the new S7 scenario at the fourth-manifest gate.
