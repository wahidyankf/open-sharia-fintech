# Product Requirements — Learning Path Course Authoring: Capstones (Band 8)

## Product Overview

This plan authors **8 capstone course bundles** — `capstone-build-your-own-coding-agent`,
`capstone-build-your-own-pentest-engine`, `capstone-real-world-delivery`, `capstone-secure-service`,
`capstone-data-pipeline`, `capstone-concurrency-and-systems`, `capstone-concurrency-showdown`, and
`capstone-lead-at-altitude` — each a full page bundle at `<COURSES><course-id>/` following the fixed
anatomy (`_index.md` with `prerequisites: [...]`, `overview.md`, `learning/`, `drilling/`) that every
other course-authoring successor plan uses, landing under
`apps/ayokoding-www/content/en/learn/courses/`. Unlike a normal course, a capstone's `learning/`
content is an **assembly project**: it integrates concepts from multiple prior courses into one
runnable artefact (a coding agent, a pentest engine, a service, a pipeline, a deployed system, or a
comparison/synthesis document) rather than introducing new `co-NN` concepts of its own.

Every body is authored **from** its `syllabus/courses/<course-id>.md` spec — six of the eight are
embedded inter-topic capstone specs inside `defensive-security.md`, `compilers-parsers-and-transpilers.md`,
and `site-reliability-engineering.md`; the remaining two have their own dedicated spec files. See
[tech-docs.md §Course Library Catalog](./tech-docs.md#course-library-catalog) for the exact citation
per course.

## Personas

Solo-maintainer framing: these are hats the maintainer wears, plus the AI agents that consume this
plan's artefacts — not external stakeholder roles.

- **The near-completion learner.** A self-paced learner who has worked through most of a `careers/`
  path and reaches one of these eight capstones as the milestone that proves the preceding courses'
  content actually composes into something real. Cares that the capstone's prerequisites are courses
  they have actually already studied, that the "done bar" is concrete and checkable, and that the
  capstone does not silently re-teach material a prior course already owns.
- **The manifest-growth agent** (the executor behind `ayokoding-learning-path-12-careers-se-manifests`
  and `ayokoding-learning-path-13-careers-ai-manifest`). Consumes this plan's band-completion signal
  as a machine-readable handoff: it needs `LANDED_COURSE_IDS` to resolve under `<COURSES>` and
  `GROW_MANIFESTS` to name exactly which `.json` files to grow — nothing looser is actionable.
  Cares that this plan never touches a manifest file itself.
- **The course-authoring executor** (`apps-ayokoding-www-by-example-maker`,
  `apps-ayokoding-www-annotated-concept-maker`, their checkers/fixers, `web-researcher`). Cares that
  each capstone's own spec file is read in full before authoring, that the fixed page-bundle anatomy
  is followed exactly, and that every content checker returns zero CRITICAL/HIGH/MEDIUM before merge.
- **The maintainer**, reviewing the content-quality findings and the merge outcome.

## User Stories

- **As** the near-completion learner, **I want** `capstone-lead-at-altitude` to build on the two prior
  capstones it names as prerequisites (`capstone-concurrency-and-systems`,
  `capstone-real-world-delivery`) rather than starting from nothing, **so that** the whole-journey
  synthesis genuinely reflects the systems I already built.
- **As** the near-completion learner reaching `capstone-build-your-own-pentest-engine`, **I want** the
  capstone to hard-enforce that every exercise runs only against a lab target I control, **so that** I
  never risk running an offensive-security exercise against a real, unauthorized system.
- **As** the manifest-growth agent for `ayokoding-learning-path-13-careers-ai-manifest`, **I want**
  the band-completion signal to explicitly name the `ai-engineer` manifest among `GROW_MANIFESTS`,
  **so that** I do not have to infer from the course content alone that this band is one of the two
  that grows it.
- **As** the course-authoring executor, **I want** each capstone's `overview.md` to state its scope
  boundary against the courses it assembles, **so that** the capstone is legible as an integration
  project rather than read as introducing new, undocumented concepts.
- **As** the maintainer, **I want** every capstone's own accuracy-sensitive claims (version-pinned
  dependencies, benchmark citations, contested-vocabulary framing) confined to dated accuracy-note
  sidebars rather than the stable spine, **so that** the capstone's core teaching content does not age
  out with the next model or library release.

## Acceptance Criteria (Gherkin)

**Scenario Outline (binds) →** "Every capstone bundle is authored with the fixed anatomy and declares
its prerequisites"

```gherkin
Scenario Outline: Every capstone bundle is authored with the fixed anatomy and declares its prerequisites
  Given the syllabus spec for "<course-id>" has been read in full
  When the capstone bundle is authored at "apps/ayokoding-www/content/en/learn/courses/<course-id>/"
  Then "_index.md", "overview.md", "learning/_index.md", and "drilling/_index.md" all exist
  And "_index.md" declares a "prerequisites:" field transcribed verbatim from the spec

  Examples:
    | course-id                                |
    | capstone-build-your-own-coding-agent      |
    | capstone-build-your-own-pentest-engine    |
    | capstone-secure-service                   |
    | capstone-data-pipeline                    |
    | capstone-concurrency-showdown              |
    | capstone-concurrency-and-systems          |
    | capstone-real-world-delivery              |
    | capstone-lead-at-altitude                 |
```

**Scenario (binds) →** "`capstone-lead-at-altitude` is authored only after its intra-band candidate
prerequisites land"

```gherkin
Scenario: capstone-lead-at-altitude is authored only after its intra-band candidate prerequisites land
  Given this plan's own Cohort B ordering places capstone-concurrency-and-systems and capstone-real-world-delivery before capstone-lead-at-altitude
  When capstone-lead-at-altitude's own authoring step begins
  Then both "apps/ayokoding-www/content/en/learn/courses/capstone-concurrency-and-systems/" and "apps/ayokoding-www/content/en/learn/courses/capstone-real-world-delivery/" already exist
  And capstone-lead-at-altitude's own _index.md prerequisites field names at least one of the two course IDs, per the spec's disjunctive "one of ... or ..." framing
```

**Scenario (binds) →** "`capstone-build-your-own-pentest-engine` hard-enforces authorized-lab-only
scope"

```gherkin
Scenario: capstone-build-your-own-pentest-engine hard-enforces authorized-lab-only scope
  Given the capstone-build-your-own-pentest-engine spec's non-negotiable authorization-and-scope rule
  When the course body's overview.md and learning content are authored
  Then the body restates the authorized-lab-target-only rule as a hard, non-tunable requirement
  And no worked example or exercise references any target other than a reader-controlled isolated lab
```

**Scenario (binds) →** "`capstone-build-your-own-coding-agent` is recorded as the ninth AI-cluster
course in the band-completion signal"

```gherkin
Scenario: capstone-build-your-own-coding-agent is recorded as the ninth AI-cluster course in the band-completion signal
  Given capstone-build-your-own-coding-agent assembles the five-course harness cluster authored by ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness
  When this band's completion signal is recorded in delivery.md
  Then GROW_MANIFESTS names apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/ai-engineer.json in addition to the three software-engineer-role manifests
```

**Scenario (binds) →** "This plan never edits a manifest file"

```gherkin
Scenario: This plan never edits a manifest file
  Given this plan's own delivery boundary branch, diffed against origin/main
  When the diff is filtered to paths under apps/ayokoding-www/src/features/course-paths/manifests/
  Then the filtered diff is empty
```

**Scenario (binds) →** "The rendering repository baseline is recorded"

```gherkin
Scenario: The rendering repository baseline is recorded
  Given the concrete checkable signal from vercel-function-cost-reduction's Phase 1-4 changes
  When Phase 0 evaluates apps/ayokoding-www/src/app/layout.tsx, apps/ayokoding-www/src/middleware.ts, and any remaining server-side searchParams read
  Then the observed rendering state is recorded as implementation context and does not add a plan-start gate
```

**Scenario (binds) →** "The eight-capstone catalog builds green"

```gherkin
Scenario: The eight-capstone catalog builds green
  Given all eight capstone bundles are authored and merged to origin/main
  When "npm exec nx run ayokoding-www:build" is run
  Then the build exits 0 and every one of the eight capstone slugs renders a page
```

## Product Scope

**In scope:**

- Authoring all 8 capstone course bundles listed above, from their syllabus specs, following the
  fixed page-bundle anatomy.
- Recording the eight rows in this plan's own `tech-docs.md` Course Library Catalog.
- Recording one band-completion signal (four manifests) at the close of Cohort B.
- A bounded, per-course accuracy pre-verify (`web-researcher`) for version-pinned or benchmark claims,
  confined to dated accuracy-note sidebars.
- Manual Playwright MCP verification of a sample of the eight pages at three breakpoints, `en` only.

**Out of scope:**

- Any manifest edit (owned by `ayokoding-learning-path-12-careers-se-manifests` and
  `ayokoding-learning-path-13-careers-ai-manifest`).
- Any change to any other band's course content, or to any other plan's folder.
- Any Indonesian-locale content.
- Any new route, component, or redirect — this plan ships markdown only.
- Re-deciding the eight-course list itself (fixed by plan 04's DD-20 ruling and this plan's own
  authoring brief).

## Product-Level Risks

- **A capstone's `overview.md` fails to state its scope boundary against the courses it assembles**,
  reading as though it introduces new, undocumented concepts rather than an integration project.
  Mitigated by the per-course authoring convention's explicit scope-boundary acceptance clause (see
  [delivery.md](./delivery.md)).
- **A learner reaching a capstone whose prerequisite course does not yet exist** (if this plan's own
  Phase 0 preconditions were skipped) would hit a dead cross-reference. Mitigated by per-course
  precondition checks against the confirmed prerequisite list in
  [tech-docs.md](./tech-docs.md#confirmed-per-capstone-dependency-map), not only the plan-level
  precondition.
- **Two cross-plan documentation discrepancies** (see [tech-docs.md](./tech-docs.md#confirmed-per-capstone-dependency-map))
  could have misled a future reader of the sibling plans about this plan's true dependency surface;
  flagged rather than silently propagated, and both are now reconciled in the sibling plans' own
  folders.
