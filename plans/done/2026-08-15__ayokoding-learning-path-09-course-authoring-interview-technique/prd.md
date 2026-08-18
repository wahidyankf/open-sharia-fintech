# Product Requirements — Course Authoring: Interview-Technique Courses (Band 9)

## Product Overview

This plan authors **5 course bodies** — the shared course library's Band 9 — under
`apps/ayokoding-www/content/en/learn/courses/`, each a standalone, path-neutral building block with a
stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track, exactly matching the anatomy every other authored course in the library uses (see
[tech-docs.md §The course page bundle](./tech-docs.md#the-course-page-bundle-consumed-from-plan-04)).

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter. Two `careers/` paths carry this band in their `courseOrder`:

- **`careers/interview-ready/software-engineer`** — the **interview/job-prep-first** arc for an
  experienced engineer re-entering the market. This band is that path's own namesake content.
- **`careers/fundamentally-strong/software-engineer`** — the **university-style,
  fundamentals-first** arc. This band appears there too, as an optional deepening tail.

A third path, **`careers/immediately-effective/software-engineer`**, deliberately **omits** this band
from its `courseOrder` — its reader reaches these 5 courses (if at all) via their canonical course
pages, not via that path's own manifest. See
[README.md §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant--this-band-is-the-special-case).

The library body is **content**, exempt from `specs:behavior:coverage`; the navigation feature that renders it
is app code owned by `ayokoding-learning-path-03-navigation-ui` (already merged). The acceptance
criteria below are **content-level** criteria, verified by the ayokoding content checkers and by
grep-checkable assertions on the authored bodies, not by application tests.

## Personas

- **Experienced engineer re-entering the job market (north-star for
  `careers/interview-ready/software-engineer`)** — recently laid off, returning from a
  gap/sabbatical, or an employed senior wanting to switch. Already owns the editor workflow and deep
  fundamentals; needs to **refresh interview technique fast** at mid/senior/staff level and handle a
  **layoff / employment-gap narrative** — without walking a from-scratch curriculum. This is the
  direct beneficiary of this plan's 5 bodies.
- **A university-style, fundamentals-first learner (north-star for
  `careers/fundamentally-strong/software-engineer`)** — reaches this band as an optional deepening
  tail once fundamentals are established, not as a first-priority arc.
- **A reader who lands on a shared course by deep-link / share** — arrives at `coding-interview` or
  any of the other 4 course URLs without a path context and must get a coherent standalone view (with
  prerequisites surfaced) plus an obvious way to enter a path.
- **Maintainer (content strategist / content author / reviewer)** — authors the 5 bodies via the
  ayokoding maker agents and reviews them through the secret scan, local quality checks, and PR quality-gate verification.

## User Stories

- As an **experienced engineer re-entering the market**, I want real interview-technique modules in a
  **refresh register**, so that I reload technique at my level instead of being taught data structures,
  algorithms, or system design from zero.
- As an **experienced engineer re-entering the market**, I want an explicit module on framing an
  employment gap, a layoff, or a re-entry story, so that I walk into a behavioral round prepared for
  the question every other interview-prep resource treats as an afterthought.
- As a **reader of `system-design-interview`**, I want it to forward-link the depth course
  `system-design` rather than re-teaching architecture from scratch, so that I get the interview
  rubric without a duplicate treatment of material another course owns.
- As a **capstone reader**, I want `capstone-interview-loop` to assemble all 4 interview-technique
  courses into one runnable, gradeable mock loop, so that "done" is a thing I can run and self-score.
- As the **maintainer**, I want every body authored **from** its settled `syllabus/courses/<id>.md`
  spec, so that concept coverage and prerequisite edges are transcribed rather than re-invented.
- As the **downstream manifest author**
  (`ayokoding-learning-path-12-careers-se-manifests`), I want a complete, explicit band-completion
  signal naming exactly the two manifests this band feeds, so that I never grow
  `careers/immediately-effective/software-engineer` by mistake.

## Acceptance Criteria (Gherkin)

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule).

Two of the six scenarios below are reproduced **verbatim** from the parent plan's own `prd.md`
(they were already written and delivery-bound there under Band 9 / Phase 11); the remaining four are
newly authored for this plan's own course-level and plan-level acceptance shape.

```gherkin
Scenario: Interview courses are written in a refresh register
  Given the four new interview-technique courses are authored
  When an experienced engineer reads them
  Then each assumes prior professional experience and focuses on interview technique and breadth refresh
  And none teaches core concepts from zero
```

```gherkin
Scenario: The behavioral course covers the layoff and employment-gap narrative
  Given the behavioral-and-leadership-interviews course is authored
  When an experienced re-entrant reads its learning track
  Then it explicitly covers framing an employment gap, a layoff, or a re-entry story
  And it treats senior/staff/EM leadership rounds as core material
```

```gherkin
Scenario: The system-design-interview course forward-links depth rather than re-teaching it
  Given the system-design-interview course is authored
  When a reader compares its overview against the system-design course
  Then it teaches only the interview rubric and whiteboard flow
  And it forward-links system-design for architecture depth rather than re-teaching it
```

```gherkin
Scenario: The coding-agent capstone assembles the four interview courses into a runnable mock loop
  Given the four interview-technique courses and capstone-interview-loop are authored
  When a reader completes the capstone
  Then they run a coding round, a take-home/live round, a system-design round, and a behavioral round
  And their `_index.md` declares all four interview courses as prerequisites
```

```gherkin
Scenario: The band-completion signal names exactly the two manifests this band feeds
Given all 5 Band-9 bodies are authored on this plan's final-delivery branch
  When the band-completion signal is recorded in delivery.md
  Then GROW_MANIFESTS names exactly careers/interview-ready/software-engineer.json and careers/fundamentally-strong/software-engineer.json
  And it does not name careers/immediately-effective/software-engineer.json
```

```gherkin
Scenario: The authored Band-9 course library builds and validates green
  Given all 5 course bodies this plan authors have landed under the courses bucket
  When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
  Then the build succeeds over the 5 authored course bodies
  And link, heading-hierarchy, and markdownlint validation report no errors across them
```

## Scenario-to-delivery binding

| Scenario                                                                                 | Binds to                                               |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Interview courses are written in a refresh register                                      | Phase 1 · the four interview-technique authoring steps |
| The behavioral course covers the layoff and employment-gap narrative                     | Phase 1 · `behavioral-and-leadership-interviews` step  |
| The system-design-interview course forward-links depth rather than re-teaching it        | Phase 1 · `system-design-interview` step               |
| The coding-agent capstone assembles the four interview courses into a runnable mock loop | Phase 1 · `capstone-interview-loop` step               |
| The band-completion signal names exactly the two manifests this band feeds               | Phase 1 · band-completion signal recording step        |
| The authored Band-9 course library builds and validates green                            | Phase 2 · Section & Tree Verification                  |

## Course Specifications

Full per-course concept/example counts, prerequisites, and format detail live in the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)
(one file per course ID) — the specs below fix each course's purpose, register, and acceptance shape.
The catalog is the source of truth for authoring; these specs are not a substitute for it.

**Register.** All 4 interview-technique courses (not the capstone, which integrates rather than
teaches from a register) use a **refresh register** (assume prior professional experience; reload
technique, do not teach from zero) — DD-10, consumed from the parent plan (see
[tech-docs.md §Design Decisions Consumed](./tech-docs.md#design-decisions-consumed)).

**Principle-first framing (HARD, inherited).** Every course teaches a durable **principle** or
**technique**; any named company's interview format is an **illustrative, dated accuracy-note aside**,
never the subject — company-specific formats drift yearly and must never anchor the stable spine.

**Volume-target bands** (inherited from the parent plan; floor not cap):

| Course shape                                  | Concept floor (`co-NN`) | Worked-example band (`ex-NN`) |
| --------------------------------------------- | ----------------------- | ----------------------------- |
| By Example                                    | ≥ 10                    | 75–85 code examples (target)  |
| Annotated-concept, no-code (refresh register) | ≥ 8                     | 30–60 worked scenarios        |

> **Note on realized counts vs. the target band.** The four interview-technique courses' settled specs
> realize the register-appropriate volume rather than the full By-Example ceiling — see the per-course
> counts below, each `[Repo-grounded]` against its own `syllabus/courses/<id>.md` file. A refresh-register
> course intentionally runs leaner than a first-learn course of the same nominal format, because it is
> reloading technique the reader already has the underlying concepts for, not teaching those concepts
> for the first time.

### `coding-interview` — By Example, Python (patterns language-agnostic)

**[Repo-grounded]** 24 concepts (`co-01`–`co-24`), 56 worked examples (`ex-01`–`ex-56`), settled per
[`syllabus/courses/coding-interview.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/coding-interview.md)
(282 lines). **Prerequisites**: `data-structures-and-algorithms-essentials`, `advanced-algorithms`
(both already re-homed and live). Reload LeetCode-style pattern recognition and time-boxed
problem-solving narration; hosts the interview-loop map. Refresh register — a strong engineer can
still fail this round for reasons unrelated to CS ability (freezing on an unfamiliar framing, silent
problem-solving), so the course drills the **performance skill**, not the underlying data structures
(that is `data-structures-and-algorithms-essentials`) or algorithms (`advanced-algorithms`).

### `take-home-and-live-coding` — By Example, Python

**[Repo-grounded]** 22 concepts (`co-01`–`co-22`), 50 worked examples (`ex-01`–`ex-50`), settled per
[`syllabus/courses/take-home-and-live-coding.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/take-home-and-live-coding.md)
(269 lines). **Prerequisites**: `data-structures-and-algorithms-essentials`. Time-boxed take-home
technique (scope, test, README hygiene) plus observed live/pair technique (thinking aloud, narrated
incremental building).

### `system-design-interview` — Annotated-concept, no code

**[Repo-grounded]** 22 concepts (`co-01`–`co-22`), 44 worked scenarios (`ex-01`–`ex-44`), settled per
[`syllabus/courses/system-design-interview.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/system-design-interview.md)
(263 lines). **Prerequisites**: `backend-essentials`, `networking-essentials`, `sql-essentials` (all
already live). The senior/staff system-design interview rubric and whiteboard flow.
**Forward-links `system-design`** for architecture depth (DD-10) rather than re-teaching it — the
scope-boundary acceptance clause below enforces this.

### `behavioral-and-leadership-interviews` — Annotated-concept, no code

**[Repo-grounded]** 22 concepts (`co-01`–`co-22`), 42 worked scenarios (`ex-01`–`ex-42`), settled per
[`syllabus/courses/behavioral-and-leadership-interviews.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/behavioral-and-leadership-interviews.md)
(256 lines). **Prerequisites**: none (entry point). STAR technique, senior/staff/EM leadership rounds
treated as **core** (not optional) material, and the **employment-gap / layoff / re-entry narrative** —
the module every other interview-prep resource treats as an afterthought.

### `capstone-interview-loop` — Interview milestone, Python + prose

**[Repo-grounded]** integrates the four courses above (no new concepts of its own — "does not
introduce new concepts; it integrates the Phase 1 courses' concepts under realistic loop conditions"),
settled per
[`syllabus/courses/capstone-interview-loop.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/capstone-interview-loop.md)
(98 lines). **Prerequisites**: all 4 interview-technique courses above, plus the interview-facing
fundamentals they in turn depend on (DS&A, advanced algorithms, OOP, OO design, SQL, technical
communication — all already live). Five ordered artefacts: a timed coding round, a take-home + live
round, a system-design walkthrough with a Mermaid diagram, a behavioral mock round (≥ 6 STAR answers
including the layoff/gap probe), and a score sheet diagnosing the weakest round with a concrete
improvement plan. Done bar: every code artefact runs; every non-code round produces its scored
artefact; web-verified.

## Product Scope

**In scope**:

- Authoring all 5 course bodies listed above, each as a full page bundle (`_index.md`, `overview.md`,
  `learning/`, `drilling/`) under `apps/ayokoding-www/content/en/learn/courses/<course-id>/`.
- Running `npm exec nx run ayokoding-www:generate-indexes` after course additions, then `npm exec nx run ayokoding-www:validate-indexes`.
- Adding one Course Library Catalog row per landed course ID (see
  [tech-docs.md §Course Library Catalog (Band 9 rows)](./tech-docs.md#course-library-catalog-band-9-rows)).
- Recording the one band-completion signal for Band 9.
- Manual behavioural verification (Playwright MCP, `en` locale, all 3 breakpoints) of the 5 rendered
  pages.

**Out of scope** (see [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals) for the
business framing of each):

- Any manifest `.json` edit.
- An Indonesian (`id`) mirror of these 5 courses.
- Re-deciding any of the 5 courses' concept coverage, prerequisite chain, or register.
- Any edit to `ayokoding-learning-path-04-course-authoring`'s own files.
- Any application-code or manifest-data change under `apps/ayokoding-www/src/features/course-paths/`.

## Product-Level Risks

- **Scope creep into the parent plan's remaining bands.** Mitigated by this plan's own
  `evidence/authored-body-slugs.txt` register holding exactly these 5 slugs — a sixth slug appearing
  there would be a defect this plan's Phase 0 baseline check would catch.
- **A reader confusion between `system-design-interview` and `system-design`.** Mitigated by the
  explicit forward-link acceptance clause (Phase 1) and the Gherkin scenario above.
- **The capstone's prerequisite declaration silently omitting one of the four interview courses.**
  Mitigated by a grep-checkable acceptance clause enumerating all four by name (Phase 1).
