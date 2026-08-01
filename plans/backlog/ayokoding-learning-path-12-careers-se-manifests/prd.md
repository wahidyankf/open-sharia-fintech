# Product Requirements — Learning Path Manifests (software-engineer-role)

## Product Overview

Three **path manifests** compose the shared course library into three readable
`software-engineer`-role journeys. A manifest is an ordered, prerequisite-consistent list of course
IDs — a **path ID**, a display **title**, a **description**, and a `courseOrder` — stored as a
standalone YAML data file under `apps/ayokoding-www/src/features/course-paths/manifests/careers/`,
nested to mirror each slash path ID. Each manifest gets a thin content **landing anchor** (prose/SEO
only, no `courseOrder`) at `/en/learn/paths/<path-id>`, and a card in the paths hub's `careers/` group
(hub layout owned by `ayokoding-learning-path-03-navigation-ui`).

All three converge on the same software-engineering deep mastery; only the **entry point**, the
**journey ordering**, and the **teaching emphasis** differ:

- **`careers/interview-ready/software-engineer`** — the **interview/job-prep-first** arc: interview
  prep FIRST → production-effective → deeper.
- **`careers/immediately-effective/software-engineer`** — editor/tooling → one language end-to-end →
  **build a real app first** → then deepen.
- **`careers/fundamentally-strong/software-engineer`** — CS foundations / theory first → deeper.

**This product surface is composition only.** No course body is authored here; no rendering component
is built here. What ships is: three YAML manifests, three landing anchors, three hub cards, the
integrity and smoothness verification that keeps them honest, the growth that closes each
smoke-test-scoped manifest as backfill lands, and — at this plan's own final phase, once the sibling
AI-manifest plan has fully merged — the four-manifest completeness check spanning all of `careers/`.

## Personas

- **Experienced engineer re-entering the job market (north-star for `interview-ready`)** — already
  owns the editor workflow and deep fundamentals; needs to refresh breadth fast, relearn interview
  technique, and handle a layoff/employment-gap narrative — without walking a from-scratch curriculum.
- **A builder who wants to be effective fast (north-star for `immediately-effective`)** — wants to set
  up the editor, learn one language end-to-end, ship a real app early, then deepen into CS
  fundamentals, DS&A, algorithms, and systems.
- **A university-style, fundamentals-first learner (north-star for `fundamentally-strong`)** — wants
  the rigorous bottom-up route: CS foundations, computer architecture, paradigms, and DS&A before
  building apps at scale.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view plus an obvious way to enter a path. Once the
  sibling AI-manifest plan has also merged, this reader's "this course is part of" affordance can name
  all four paths, not only this plan's three.
- **Maintainer** — owns the three-manifest architecture and authors landing content via the ayokoding
  maker agents.

## User Stories

- As an **experienced engineer re-entering the market**, I want a published interview-ready manifest
  whose order leads with interview technique, so that the first thing I read is the thing I need
  soonest.
- As a **builder who wants to be effective fast**, I want the immediately-effective manifest to place
  building a real app ahead of every pure-theory course, so that I feel the payoff before I go deep.
- As a **university-style learner**, I want the fundamentally-strong manifest to place CS foundations,
  architecture, paradigms, and DS&A ahead of build-at-scale courses, so that I understand the theory
  before I apply it.
- As a **reader on any of this plan's path landings**, I want the courses listed in the manifest's
  exact order with the path context carried into every link, so that "next" always means the next
  course in the arc I chose.
- As a **reader who deep-links a shared course**, I want to see every published path that includes it
  — once all four `careers/` manifests are live — so that I can enter whichever arc fits me.
- As the **maintainer**, I want each of the three manifests verified prerequisite-consistent at its own
  phase gate, so that an invalid ordering fails at the boundary that introduced it.
- As the **maintainer**, I want the Band-9 interview-technique growth to land in exactly
  `interview-ready` and `fundamentally-strong`, and never in `immediately-effective`, so that the
  deliberate two-of-three design is enforced mechanically, not by memory.
- As the **maintainer**, I want this plan's final phase to run the four-manifest completeness check
  only after the sibling AI-manifest plan has fully merged, so that the check is never a false pass
  against a manifest that does not yet exist.
- As a **screen-reader / keyboard user**, I want each path landing's ordered course list and the hub's
  card grid to be fully navigable without a mouse.

## Acceptance Criteria (Gherkin)

Each scenario uses exactly one primary `Given`, one `When`, and one `Then`; every extra precondition,
action, or outcome chains with `And`.

```gherkin
Scenario: The interview-ready MVP proves the architecture and unblocks the sibling AI-manifest plan
  Given the careers/interview-ready/software-engineer MVP (an architecture smoke test over already-live topics 1-33) is delivered end-to-end
  When its delivery unit is merged to origin/main
  Then the interview-ready MVP's landing page, manifest, and path-aware nav are already live in production
  And the merge of this delivery unit is the recorded start precondition ayokoding-learning-path-13-careers-ai-manifest checks before its own Phase 0 begins
```

```gherkin
Scenario: The immediately-effective path is build-app-first
  Given the careers/immediately-effective/software-engineer path manifest is published
  When a reader walks the path
  Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
  And the reader ships a real deployed app before any pure-theory course
```

```gherkin
Scenario: The fundamentally-strong path is fundamentals-first
  Given the careers/fundamentally-strong/software-engineer path manifest is published
  When a reader walks the path
  Then CS foundations, computer architecture, paradigms, and DS&A precede the build-real-software courses
  And the ordering is a valid topological entry into the prerequisite DAG
```

```gherkin
Scenario: The three software-engineer paths reference a shared course with no body duplication
  Given a course appears in all three of the interview-ready, immediately-effective/software-engineer, and fundamentally-strong/software-engineer manifests
  When the course library is inspected
  Then exactly one canonical path-neutral body exists for that course
  And each manifest references the course by its stable course ID
```

```gherkin
Scenario: Band 9 grows exactly two of the three software-engineer manifests, never the third
  Given the five Band-9 interview-technique course IDs have landed as authored bodies
  When the growth phase appends them to this plan's manifests
  Then interview-ready and fundamentally-strong each carry all five IDs in courseOrder
  And immediately-effective/software-engineer carries none of the five, by design
```

```gherkin
Scenario: A shared course names every published careers/ path that includes it (needs all four manifests)
  Given all four careers/ path manifests are published — this plan's three plus the sibling plan's ai-engineer manifest — and a course appears in more than one of them
  When a reader opens that course's canonical URL with no path context
  Then the "this course is part of" affordance lists every published path whose manifest includes the course
  And each listed path links to its own path landing page
```

```gherkin
Scenario: This plan's software-engineer manifest layer builds and validates green
  Given this plan's three path manifests and their landing anchors are published
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations across this plan's three manifests
```

## Product Scope

### In scope

- Three `PathManifest` YAML data files under
  `apps/ayokoding-www/src/features/course-paths/manifests/careers/`.
- Three thin landing anchors under
  `apps/ayokoding-www/content/en/learn/paths/careers/<arc>/software-engineer/_index.md`.
- This plan's three-card slice of the paths-hub population.
- Manifest integrity, prerequisite-consistency, and no-forked-body verification at every phase gate.
- Per-path progression-smoothness audits, including the interview-ready refresh-register lever.
- All growth of these three manifests as the seven course-authoring successor plans' bands land.
- The four-manifest "names every path" completeness check and the terminal 127-course catalog
  assertion, both at this plan's own final phase (after the sibling plan is fully merged).

### Out of scope

- The `careers/immediately-effective/ai-engineer` manifest, landing, and hub card — the sibling plan's
  own deliverable.
- Any course body, rendering component, schema, URL/redirect work, or `skills/` category manifest —
  see [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals).

### UI-design-funnel disposition

This plan adds **no net-new screen and no net-new component** — same disposition as the plan it
succeeds. It publishes content and data into two screens whose design funnels are already complete and
owned by `ayokoding-learning-path-03-navigation-ui`. Full exemption record in
[tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-recorded-explicitly).
The exemption is scoped to the design funnel only — the **Rule-15 three-tester retest remains
mandatory**, scoped to this plan's own three landings plus its slice of the hub, and runs in
[Phase 6](./delivery.md#phase-6-manual-ui-verification-and-rule-15-three-tester-retest).

## Product-Level Risks

- **Order/manifest drift**: mitigated by manifest-integrity + prerequisite-consistency checks at every
  gate and stable course-ID slugs.
- **Silent truncation**: mitigated by falsifiable before/after checks at publication time, a dedicated
  growth phase, and terminal gates asserting the full arcs.
- **Band-9 misrouting** (landing in the wrong subset of manifests): mitigated by a same-step,
  both-directions acceptance clause — present in two named manifests, absent in the third.
- **Duplication creep**: mitigated by callout-only framing and a no-forked-body check at every gate.
- **Ownership erosion** across the two-plan split: mitigated by the invariant stated in both plans'
  docs and this plan's own boundary-check phase.
- **Coupling misread as circular**: mitigated by the explicit sequence diagram and distinct-node
  framing in both READMEs.
- **Four-manifest check running early / false pass**: mitigated by a literal merged-PR check as the
  phase's start condition, not an assumption.
- **Hub incoherence mid-flight**: mitigated by populating exactly one card per shipped manifest, using
  per-href presence checks rather than a whole-file count (since the sibling plan edits the same shared
  hub file concurrently).
- **Deep-link affordance goes stale before the sibling plan ships**: recorded as an accepted, temporary
  state — the affordance genuinely cannot name a path that does not exist yet — and closed at this
  plan's final phase once all four manifests are live.
