# Product Requirements — Learning Path Schema and Prerequisite DAG

## Product Overview

This plan delivers the **data layer** of the shared-course-library product: the machine-readable
description of what a path is, what a course declares, and the pure functions that answer questions
about both.

Concretely, it ships five things:

1. A **course-prerequisite frontmatter contract** — `prerequisites: [course-id, ...]` declared in
   each course's canonical `_index.md`. This plan is its canonical owner.
2. A **`PathManifest` zod schema** — `pathId` (variable-depth: `careers/<arc>/<role>` or, for the
   sibling `skills/` category this plan does not own, `skills/<subject>` — R2), `arc` (always
   required, independent of the URL grammar — R8), `title`, `description`, `courseOrder[]`, optional
   per-course `framing` — describing the standalone YAML data file that is a path's single
   machine-consumed source of truth.
3. The **`<MANIFESTS>` directory** and its `README.md`, the home those YAML files land in later.
4. A **pure functional core** — `resolvePathNav`, `parsePathContext`, `resolvePrerequisites`,
   `checkPrerequisiteConsistency`, `checkManifestIntegrity`, plus course-ref normalization — IO-free
   and unit-tested without a browser or a server.
5. The **`course-paths` Gherkin companion** under
   `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`, authored RED.

It also extends `content-url.ts` with the optional `pathId` param and the canonical
`/en/learn/courses/<course-id>` URL shape, because path context has to be expressible in a link
before any component can render one.

**Nothing user-facing ships here.** No component, no route, no rendered page, no manifest data file,
no course body. Each of those has a named owner listed in
[README.md §What this plan owns](./README.md#what-this-plan-owns).

**UI-design-funnel applicability**: this plan is **exempt** — it adds no user-facing screen or
component. The exemption is stated with its reasoning in
[tech-docs.md §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption).

## Personas (one per path)

Reproduced **verbatim** from the source plan, except the fourth persona, which is **corrected
2026-07-21 (R3, custody exception)** — its original framing became factually wrong once the ruling
landed, so it is updated in place rather than left as a known-incorrect quotation (same reasoning as
the `syllabus/` custody exception; see
[tech-docs.md §Custody rules](./tech-docs.md#custody-rules-binding)). All four path personas are
carried, not just the ones this plan's surface most directly serves: the resolvers and the DAG
underpin every path, and a reviewer cannot assess fit-for-purpose against a persona living in a
sibling folder. **This plan is careers-only (R4)** — all four paths below sit under the `careers/`
URL category; see [tech-docs.md §Ownership split](./tech-docs.md#ownership-split-careers-vs-skills--r4).

- **Experienced engineer re-entering the job market (north-star for the
  `careers/interview-ready/software-engineer` path)** — recently laid off, returning from a
  gap/sabbatical, or an employed senior wanting to switch. Already owns the editor workflow and deep
  fundamentals; needs to **refresh breadth fast, relearn interview technique** at mid/senior/staff
  level, and handle a **layoff / employment-gap narrative** — without walking a from-scratch
  curriculum. Interview/job prep FIRST.
- **A builder who wants to be effective fast (north-star for the
  `careers/immediately-effective/software-engineer` path)** — wants "immediately effective" SWE: set
  up the editor, learn one language end-to-end, **ship a real app early**, then deepen into CS
  fundamentals, DS&A, algorithms, and systems. Serves both a from-scratch learner and a mid-career
  switcher.
- **A university-style, fundamentals-first learner (north-star for the
  `careers/fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route: CS
  foundations, computer architecture, paradigms, and data structures & algorithms **before** building
  apps at scale. Prefers to understand the machine and the theory first, then apply it.
- **A reader with no assumed prior software-engineering competence, specializing directly into AI
  (north-star for the `careers/immediately-effective/ai-engineer` path, added 2026-07-20, corrected
  2026-07-21 per R3)** — wants to become immediately effective at **building** AI systems (models,
  agents, evals, inference serving), not at driving coding agents, starting from scratch. Its
  software-engineering prerequisites (the courses an already-working engineer would already own) are
  **included in `courseOrder`, not linked** — a correction from the original framing, which wrongly
  assumed an already-working software engineer and linked rather than included them. No new course
  body is authored for this correction; every included prerequisite is an existing library course.
  Converges on a distinct AI-engineering endpoint, not the other three paths' shared
  software-engineering endpoint.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced) plus an
  obvious way to enter a path.
- **Maintainer (content strategist / frontend engineer / content author / reviewer)** — owns the
  four-path architecture, builds the navigation feature, and authors the NEW courses via the ayokoding
  maker agents.

The **end-to-end learner journey** that these personas walk is not reproduced here — it is the
navigation and manifest plans' surface. See
[`shared-course-library-and-learning-paths/prd.md` §Learner Journey](../../done/2026-07-21__shared-course-library-and-learning-paths/prd.md#learner-journey-end-to-end)
until `ayokoding-learning-path-03-navigation-ui` carries its own copy.

## User Stories

Scoped to this plan's surface. Stories about rendering, authoring, or publishing belong to the
downstream plans.

- As the **maintainer**, I want each course to declare its prerequisites in one canonical field, so
  that the library forms a single dependency graph instead of a set of unstated assumptions.
- As the **maintainer**, I want a path's order to live in a standalone data file rather than in any
  course body, so that one canonical body can appear in four different orders with zero duplication.
- As the **maintainer**, I want a machine check that no path presents a course before its declared
  prerequisites, so that "does this path read smoothly?" stops being an opinion I re-argue on every
  manifest change.
- As the **maintainer**, I want a machine check that every `courseOrder` entry resolves to a real
  course and appears at most once, so that a renamed or not-yet-authored course ID fails the build
  instead of shipping a dead entry.
- As the **maintainer**, I want the ordering and prerequisite logic to be pure and IO-free, so that I
  can unit-test the hardest part of the product without a browser, a server, or a fixture site.
- As a **downstream plan author** (`ayokoding-learning-path-03-navigation-ui`), I want the five
  `core/` modules merged and typechecking before I start, so that my RED steps fail on the behaviour
  under test rather than on an unresolved import.
- As a **downstream plan author** (`ayokoding-learning-path-04-course-authoring`), I want the
  `prerequisites:` frontmatter contract settled and canonical, so that every body I author declares
  the field in a shape the resolver actually parses.
- As a **reader who shares or deep-links a course**, I want an absent or unknown `?path=` value to
  resolve to "no path context" rather than to an error, so that a shared link never breaks — the
  fallback begins in `parsePathContext`, before any component is involved.
- As the **maintainer**, I want a link to a course to be able to carry path context, so that a reader
  walking a path stays in that path as they follow prev/next and breadcrumb links.
- As a **manifest-owning plan author** (careers or skills), I want to link out to a prerequisite my
  path's audience already has, without being forced to either walk it or drop the course that needs
  it, so that curation stays possible for an audience with partial, non-standard prior knowledge
  (OI-4, 2026-07-21).

## Acceptance Criteria (Gherkin)

Each scenario uses exactly one primary `Given`, one `When`, and one `Then`; every extra clause chains
with `And`.

Two scenarios below are carried **verbatim** from the source plan and are this plan's own (they
describe the pure integrity gates, whose entire implementation lives here). The third is this plan's
scoped share of the decomposed build-green scenario — see the provenance note that follows it. The
fourth is new, added 2026-07-21 to resolve **OI-4** (see
[tech-docs.md §Link-don't-walk](./tech-docs.md#link-dont-walk-prerequisite-omission-is-permitted-oi-4-ruling-2026-07-21)).

```gherkin
Scenario: A path manifest is a valid topological entry into the prerequisite DAG
  Given a path manifest lists a courseOrder of course IDs
  When the manifest-integrity check runs
  Then no course appears before any of its declared prerequisites that are also in the manifest
  And every listed course ID resolves to an existing course in the library
```

```gherkin
Scenario: Every manifest course reference resolves to a real course
  Given a path manifest lists a courseOrder of course IDs
  When the manifest-integrity check runs
  Then every listed course ID resolves to an existing course in the library
  And no course ID appears more than once in the manifest
```

```gherkin
Scenario: A path may link a prerequisite it does not include, without failing integrity
  Given a path manifest includes a course whose declared prerequisite is absent from that manifest
  When the manifest-integrity check runs
  Then the absent prerequisite is not reported as a violation
  And the absent prerequisite appears in the check's informational linkedPrerequisites list
```

```gherkin
Scenario: The schema and prerequisite-DAG surface builds and validates green
  Given the course-paths pure core and the PathManifest schema are complete
  When nx run ayokoding-www:build, the affected test tiers, and the link and heading validators run
  Then the build and all affected tiers succeed
  And link, heading-hierarchy, and markdownlint validation report no errors
```

### Provenance note — the decomposed build-green scenario

The source plan carried one scenario, _"The app builds and validates green"_, whose `Given`
conjoined the navigation feature **and** the interview-ready path. That conjunction spans two of the
five split plans by construction, so it has no single receiving plan and it bound no delivery step.

It was therefore **decomposed rather than routed**: each of the five plans writes its own scoped
build-green scenario naming its own surface. The scenario immediately above is this plan's share.
The composite original is not carried by any plan.

### Scenarios owned by downstream plans that this plan's resolvers underpin

The pure resolvers built here are the mechanism behind several scenarios whose observable behaviour
is rendered by `ayokoding-learning-path-03-navigation-ui`. Those scenarios are **owned by that
plan's `prd.md`**, not by this one, and are not duplicated into this section. This plan's
`delivery.md` reproduces them inside `**Gherkin (underpins) →**` markers on the RED steps that build
their mechanism, so that the RED signal names the behaviour it is ultimately serving.

The affected scenarios, by title:

- _Prev and next follow the active path's order_ — underpinned by `resolvePathNav`.
- _A course omitted from a path shows no path nav for that path_ — underpinned by `resolvePathNav`.
- _A course deep-linked without path context renders the canonical view_ — underpinned by
  `parsePathContext`.
- _An invalid path context falls back to the canonical view_ — underpinned by `parsePathContext`.
- _The path rail shows the whole ordered arc beside a course at desktop width_ — underpinned by
  `resolvePathNav`.
- _The path rail collapses into the existing navigation drawer on a phone_ — underpinned by
  `resolvePathNav`.
- _A course opened without path context renders the generic sidebar unchanged_ — underpinned by
  `parsePathContext`.
- _A path landing page lists its courses in manifest order_ — underpinned by the `PathManifest`
  schema and `contentUrl(pathId)`.
- _The breadcrumb reflects the active path_ — underpinned by `contentUrl(pathId)`.
- _A course page surfaces its declared prerequisites_ — underpinned by `resolvePrerequisites`.
- _A legacy fundamentally-strong URL redirects to the canonical course URL_ — underpinned by
  `contentUrl`'s canonical `/en/learn/courses/<course-id>` shape. **Owned by
  `ayokoding-learning-path-01-url-restructure`**, not by the navigation plan.

## Product Scope

**In-scope features:**

- The course-prerequisite frontmatter contract `prerequisites: [course-id, ...]` — **canonical
  here**, documented in `tech-docs.md`, and reproduced verbatim in
  `ayokoding-learning-path-01-url-restructure`'s `tech-docs.md` as the Wave-1 parallel-safe shared
  contract.
- The `PathManifest` zod schema in `apps/ayokoding-www/src/features/course-paths/core/schemas.ts`.
- The `<MANIFESTS>` directory (`apps/ayokoding-www/src/features/course-paths/manifests/`) plus its
  `README.md`, empty of `.yaml` files.
- The pure `course-paths` functional core: `manifest.ts` (course-ref normalization), `path-nav.ts`
  (`resolvePathNav`), `path-context.ts` (`parsePathContext`), `prerequisites.ts`
  (`resolvePrerequisites`, `checkPrerequisiteConsistency`), `manifest-integrity.ts`
  (`checkManifestIntegrity`) — each built RED → GREEN → REFACTOR.
- The `content-url.ts` extension: an optional `pathId` param appending `?path=<path-id>`, and the
  canonical `/en/learn/courses/<course-id>` shape.
- The `course-paths` Gherkin companion under
  `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/` plus its `README.md`, authored
  RED (step bindings land in `ayokoding-learning-path-03-navigation-ui`).
- Custody of the `syllabus/` detail layer (128 files), including the archival repoint of 34
  cross-plan inbound links.

**Out-of-scope features:**

- Any **careers** `.yaml` manifest data file — owned by `ayokoding-learning-path-05-manifests`
  (4 manifests, not 6 — R4).
- The entire `skills/` URL category — both path landings, both manifests
  (`skills/enterprise-resource-planning`, `skills/accounting`), and its course corpus — owned
  end-to-end by a separate, not-yet-created plan (R4). See
  [tech-docs.md §Ownership split](./tech-docs.md#ownership-split-careers-vs-skills--r4).
- Any `shell/` component, the `?path=` route wiring, the path rail, the path banner, the paths hub,
  and every mockup render — owned by `ayokoding-learning-path-03-navigation-ui`.
- Any course body, and any edit to a file under `syllabus/` — owned by
  `ayokoding-learning-path-04-course-authoring` (bodies) and by nobody (the corpus is frozen).
- The `<COURSES>_index.md` and `<PATHS>_index.md` content homes, the `legacy/` bucket, and every
  redirect module — owned by `ayokoding-learning-path-01-url-restructure`.
- Writing the actual `prerequisites:` values into the 37 re-homed course bundles — this plan defines
  the shape; `ayokoding-learning-path-01-url-restructure` writes the values.
- Path progress persistence, accounts, or bookmarking — the path context is URL/client state only.
- Any Indonesian content mirror. The code is locale-neutral and is **verified** against both
  supported locales, but no `id` content is authored.

## Sections that route to sibling plans

The `syllabus/` corpus custodied by this plan back-references one section of this document that the
five-way split routed elsewhere. The corpus is frozen, so the anchor is kept resolvable from this
side. The heading below exists only to keep that inbound anchor alive and to name the owning plan; it
duplicates no content. The full accounting of all 12 such targets is in
[tech-docs.md §Sections that route to sibling plans](./tech-docs.md#sections-that-route-to-sibling-plans).

### NEW Course & Capstone Specifications

Moved to **`ayokoding-learning-path-04-course-authoring`**, which owns every course body and every
net-new course and capstone specification. The authoritative per-course spec is
[`syllabus/courses/<course-id>.md`](./syllabus/courses/README.md), custodied here — each body is
authored **from** its spec file, never from a fresh judgment call.

## Product-Level Risks

- **Contract drift between the two Wave-1 plans** — `ayokoding-learning-path-01-url-restructure`
  writes `prerequisites:` frontmatter in a shape `resolvePrerequisites` does not parse. Because the
  field is inert until a Wave-2 consumer reads it, **nothing fails in Wave 1**: the build stays green
  and 37 empty prerequisite lists surface only inside
  `ayokoding-learning-path-03-navigation-ui`. Mitigated by reproducing the contract verbatim in both
  plans with this plan named canonical, and by a Phase 1 acceptance clause that quotes the exact
  three-line frontmatter shape.
- **Order/manifest drift** — a manifest references a missing or renamed course ID, or orders a course
  before its prerequisite. Mitigated by `checkManifestIntegrity` and `checkPrerequisiteConsistency`,
  each with a passing **and** a deliberately-violating unit fixture so the check is falsifiable in
  both directions.
- **Deep-link fallback gap** — a course reached without path context resolves to an error rather than
  a canonical view. Mitigated in the core: `parsePathContext` returns `null` for unknown and absent
  path IDs and never throws; the rendered half is the navigation plan's.
- **`content-url.ts` regression** — the new canonical `/en/learn/courses/<course-id>` shape changes
  link generation for pages this plan does not otherwise touch. Mitigated by keeping the `pathId`
  param optional, by updating the existing `content-url` tests in the same commit, and by a Phase 4
  live no-regression sweep across both supported locales at three breakpoints with committed
  screenshot evidence.
- **The pure core acquires IO** — a later convenience import of `fs` or React inside `core/` destroys
  the property that makes this layer cheap to test. Mitigated by an explicit REFACTOR step asserting
  no `fs` and no React import under `core/`, and by DD-9's stated functional-core boundary.
- **Specs coverage delta is untraceable** — the `course-paths` Gherkin lands with no step bindings
  (they are the navigation plan's), so `specs:behavior:coverage` reports a delta. Mitigated by
  recording the delta explicitly at the Phase 2 gate and naming
  `ayokoding-learning-path-03-navigation-ui` as the plan that closes it, so the delta has a named
  owner rather than being an anonymous regression.
- **The `syllabus/` corpus is copied rather than linked** — forking the source of truth for 121
  course specs and four manifest orderings, so a later spec correction lands in one copy only.
  Mitigated by the custody rule stated in this plan's `README.md` and restated as a
  `> **Cross-plan source of truth**` blockquote in each of the other four plans' READMEs.
- **The archival move breaks four sibling plans** — this plan is Wave 1 and archives long before
  `ayokoding-learning-path-05-manifests` and `ayokoding-learning-path-04-course-authoring` finish;
  its `git mv` relocates the target of 34 inbound cross-plan links. Mitigated by the reciprocal
  repoint step in the same commit as the move, plus the pre-push-hook form of `md links validate` as
  its acceptance.
- **The DD-34 / DD-35 / DD-39 numbering gap is "fixed"** — a future reader closes the apparent gap
  and rewrites 276 in-corpus tokens whose meanings belong to a different, closed plan. Mitigated by
  restating the source plan's explanatory passage verbatim in both `README.md` and `tech-docs.md`,
  with an explicit "never renumber" instruction.
