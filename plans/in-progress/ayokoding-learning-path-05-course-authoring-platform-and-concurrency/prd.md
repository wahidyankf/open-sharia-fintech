# Product Requirements — Course Authoring: Platform & Concurrency Languages

## Product Overview

This plan authors **14 course bodies** of the shared course library — page bundles under
`apps/ayokoding-www/content/en/learn/courses/`, each a standalone, path-neutral building block with a
stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track.

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter. The three **software-engineer**-role `careers/` paths — reused
verbatim from plan04, since this plan serves the same readers:

- **`careers/interview-ready/software-engineer`** — the interview/job-prep-first arc for an
  experienced engineer re-entering the market.
- **`careers/immediately-effective/software-engineer`** — the immediately-effective arc: editor/tooling
  → one language end-to-end → build a real app first → then deepen.
- **`careers/fundamentally-strong/software-engineer`** — the university-style, fundamentals-first arc.

— will each eventually reference some subset of these 14 courses (per plan04's routing table, Bands 3
and 4 grow exactly these three manifests, never the fourth `ai-engineer` path). The library body is
**content**, exempt from `specs:coverage`; the acceptance criteria below are content-level, verified
by the ayokoding content checkers and by grep-checkable assertions on the authored bodies.

## Personas

Reused verbatim from plan04's `prd.md`, since this plan's 14 bodies are reachable by readers of all
three software-engineer paths, exactly as plan04's other bodies are:

- **A builder who wants to be effective fast (north-star for the
  `careers/immediately-effective/software-engineer` path)** — wants "immediately effective" SWE: set
  up the editor, learn one language end-to-end, **ship a real app early**, then deepen. This persona is
  this plan's most direct beneficiary: every one of the 10 Band-3 courses is exactly the kind of
  "ship a real app" material this path prioritizes.
- **Experienced engineer re-entering the job market (north-star for the
  `careers/interview-ready/software-engineer` path)** — already owns deep fundamentals; needs breadth
  refreshed fast. A platform course here (e.g. `android-app-development`) may be an optional breadth
  item on this path's manifest rather than a core spine course.
- **A university-style, fundamentals-first learner (north-star for the
  `careers/fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route. The
  two concurrency-paradigm courses (`csp-style-concurrency`, `actor-model-concurrency`) are exactly the
  kind of depth-after-fundamentals material this path prioritizes, sitting downstream of
  `concurrency-and-parallelism`.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced) plus an
  obvious way to enter a path.
- **Maintainer (content strategist / content author / reviewer)** — authors the 14 bodies via the
  ayokoding maker agents and reviews them via the matching checkers.

> The end-to-end **Learner Journey** walk-through is not duplicated here. It belongs to the plans that
> build and populate that journey — see plan04's
> [navigation-UI plan reference](../../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/prd.md)
> and the [manifest plan — careers-se-manifests](../../backlog/ayokoding-learning-path-12-careers-se-manifests/prd.md).

## User Stories

Scoped to this plan's surface — the 14 course bodies themselves.

- As a **builder who wants to ship a real app fast**, I want a `just-enough-<language>` primer that
  teaches exactly enough of Kotlin, Swift, Dart, or C# to start its paired platform course, so that I
  do not have to learn a whole language before building anything.
- As a **reader who wants to build for Android**, I want `android-app-development` to declare
  `just-enough-kotlin` as its prerequisite and use it, so that the primer and the platform course read
  as one coherent on-ramp rather than two disconnected pieces.
- As a **reader who wants to build for iOS**, I want the equivalent `just-enough-swift` →
  `ios-app-development` pairing.
- As a **reader who wants one codebase across platforms**, I want `just-enough-dart` →
  `hybrid-app-development` to teach Flutter idioms and cross-platform packaging from one Dart
  codebase.
- As a **reader who wants native Windows desktop development**, I want `just-enough-csharp` →
  `windows-app-development` to cover C# syntax, LINQ, async, and .NET, then apply it to a native
  Windows app.
- As a **reader who already knows Python**, I want `linux-app-development` to build directly on
  `just-enough-python` without re-teaching the language, so that I get straight to native Linux
  desktop development and packaging.
- As a **reader who wants to ship a distributable CLI tool**, I want `building-production-cli-tools`
  to build on both `just-enough-go` and `just-enough-rust` and teach the concrete packaging/
  distribution concerns neither language primer covers alone.
- As a **fundamentals-first reader who has completed `concurrency-and-parallelism`**, I want a named
  concurrency-paradigm course in Go (CSP-style channels) and one in Elixir (the actor model with
  supervision trees), so that I can go deep on a named paradigm rather than stopping at the
  language-agnostic foundation.
- As the **maintainer**, I want every body authored **from** its settled spec file, so that concept
  coverage and prerequisite edges are transcribed rather than re-invented.
- As the **downstream manifest-growth plan**, I want a complete, explicit band-completion signal
  naming every manifest I must grow, so that I never have to guess which paths a landed band affects.
- As the **downstream `ayokoding-learning-path-10-...`**, I want `just-enough-go` fully authored and
  structurally complete, so that `build-your-own-raft`'s declared prerequisite resolves to a real body
  rather than a dangling ID. (This story is corrected from an earlier draft that named
  `csp-style-concurrency`/`actor-model-concurrency` — plan04's own catalog row for `build-your-own-raft`
  lists `just-enough-go` and `distributed-systems` as its only prerequisites, confirmed independently by
  `ayokoding-learning-path-10-...`'s own dependency research.)

## Acceptance Criteria (Gherkin)

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And` / `But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria.md#step-keyword-cardinality-hard-rule).

### Primer/platform pairing scenarios

```gherkin
Scenario: Each just-enough primer correctly unlocks its paired platform course
  Given a just-enough-<language> primer and its paired platform course are both authored
  When a reader completes the primer and starts the platform course
  Then the platform course's own _index.md declares the primer's exact course-id as a prerequisite
  And the platform course does not re-teach the language syntax its paired primer already covers
```

```gherkin
Scenario Outline: Every primer/platform pair resolves its declared prerequisite
  Given the platform course "<platform>" is authored
  When its _index.md prerequisites list is inspected
  Then it declares "<primer>" as a prerequisite

  Examples:
    | platform                  | primer              |
    | android-app-development    | just-enough-kotlin  |
    | ios-app-development        | just-enough-swift   |
    | hybrid-app-development     | just-enough-dart    |
    | windows-app-development    | just-enough-csharp  |
    | csp-style-concurrency      | just-enough-go      |
    | actor-model-concurrency    | just-enough-elixir  |
```

### Standalone platform courses

```gherkin
Scenario: linux-app-development builds on the existing Python primer without re-teaching it
  Given linux-app-development is authored
  When a reader who already completed just-enough-python starts it
  Then it declares just-enough-python as its prerequisite
  And it teaches native Linux desktop development and packaging without repeating Python syntax
```

```gherkin
Scenario: building-production-cli-tools builds on both Go and Rust primers
  Given building-production-cli-tools is authored
  When a reader inspects its prerequisites and its worked examples
  Then it declares both just-enough-go and just-enough-rust as prerequisites
  And its worked examples cover distributable CLI packaging concerns neither primer alone teaches
```

### Concurrency-paradigm depth scenarios

```gherkin
Scenario: The two concurrency-paradigm courses each build on the shared foundation, not on each other
  Given csp-style-concurrency and actor-model-concurrency are both authored
  When a reader compares their prerequisite chains
  Then each declares concurrency-and-parallelism as a shared prerequisite
  And neither declares the other as a prerequisite, since they teach independent paradigms
```

```gherkin
Scenario: just-enough-go is ready as build-your-own-raft's declared prerequisite
  Given just-enough-go is authored and merged to origin/main
  When ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own's build-your-own-raft authoring begins
  Then the just-enough-go course body resolves under the courses bucket
  And the terminal delivery record will name just-enough-go among the Band-4 IDs after the sole PR merges
```

### Scoped build-green (this plan's own surface)

```gherkin
Scenario: The authored platform-and-concurrency course library builds and validates green
  Given all 14 course bodies this plan authors have landed under the courses bucket
  When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
  Then the build succeeds over the authored tree
  And link, heading-hierarchy, and markdownlint validation report no errors across the 14 course bodies
```

## Scenario-to-delivery binding

| Scenario                                                                                    | Binds to                                                            |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Each just-enough primer correctly unlocks its paired platform course                        | Phase 1 · each primer/platform pair's authoring step                |
| Every primer/platform pair resolves its declared prerequisite (Scenario Outline)            | Phase 1 Gate + Phase 2 Gate · pairing check                         |
| linux-app-development builds on the existing Python primer without re-teaching it           | Phase 1 · `linux-app-development` authoring step                    |
| building-production-cli-tools builds on both Go and Rust primers                            | Phase 1 · `building-production-cli-tools` authoring step            |
| The two concurrency-paradigm courses each build on the shared foundation, not on each other | Phase 2 · `csp-style-concurrency` / `actor-model-concurrency` steps |
| just-enough-go is ready as build-your-own-raft's declared prerequisite                      | Phase 2 Gate · band-completion signal                               |
| The authored platform-and-concurrency course library builds and validates green             | Phase 3 · Section & Authored-Tree Verification                      |

## Course & Format Specifications

Each course is a full page-bundle (learning track + drilling track), matching plan04's per-course
anatomy and inheriting its cross-cutting authoring guarantees verbatim: accuracy-verified via
`web-researcher` before authoring; follow-along-complete; colocated runnable `code/` where
code-bearing; exhaustive `co-NN`/`ex-NN` enumeration; `prerequisites` metadata plus navigation. Every
course declares its `prerequisites` so it takes its place in the library's prerequisite DAG.

**Full per-course concept / example detail lives in the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)**
(one file per course ID) — the summary below (drawn from plan04's own catalog table) fixes each
course's format, language, and prerequisites; the catalog remains the source of truth for authoring.

**Volume-target bands** (inherited from plan04; floor, not cap):

| Course shape             | Concept floor (`co-NN`) | Worked-example band (`ex-NN`)         |
| ------------------------ | ----------------------- | ------------------------------------- |
| By Example               | ≥ 10                    | 75–85 code examples                   |
| Primer (_Just Enough X_) | ≥ 8                     | 75–85 code examples (By-Example pace) |

### Mobile & desktop platforms (Band 3, 10 courses)

- **`just-enough-kotlin`** (Primer · Kotlin) — Kotlin syntax, null-safety, coroutines.
- **`android-app-development`** (By Example · Kotlin) — native Android with the SDK; prereq
  `just-enough-kotlin`.
- **`just-enough-swift`** (Primer · Swift) — Swift syntax, optionals.
- **`ios-app-development`** (By Example · Swift) — native iOS with the SDK; prereq
  `just-enough-swift`.
- **`just-enough-dart`** (Primer · Dart) — Dart syntax, async, Flutter idioms.
- **`hybrid-app-development`** (By Example · Dart) — cross-platform from one Dart codebase; prereq
  `just-enough-dart`.
- **`just-enough-csharp`** (Primer · C#) — C# syntax, LINQ, async, .NET.
- **`windows-app-development`** (By Example · C#) — native Windows desktop; prereq
  `just-enough-csharp`.
- **`linux-app-development`** (By Example · Python) — native Linux desktop, packaging; prereq
  `just-enough-python` (library course, authored elsewhere).
- **`building-production-cli-tools`** (By Example · Go + Rust) — distributable CLI tools; prereqs
  `just-enough-go`, `just-enough-rust` (both library courses; `just-enough-go` is also authored in
  this plan's Band 4).

### Concurrency languages (Band 4, 4 courses)

- **`just-enough-go`** (Primer · Go) — Go syntax, goroutines.
- **`csp-style-concurrency`** (By Example · Go) — channels, CSP concurrency; prereqs
  `just-enough-go`, `concurrency-and-parallelism` (library course, authored elsewhere).
- **`just-enough-elixir`** (Primer · Elixir) — Elixir syntax, pattern matching.
- **`actor-model-concurrency`** (By Example · Elixir) — actors, supervision trees; prereqs
  `just-enough-elixir`, `concurrency-and-parallelism`.

## Product Scope

**In-scope**:

- Authoring **14 course page bundles** under
  `apps/ayokoding-www/content/en/learn/courses/<course-id>/`, each with `_index.md` (declaring
  `prerequisites`), `overview.md`, a `learning/` track (concepts, worked examples, colocated runnable
  `code/`, and `learning/capstone/`), and a `drilling/` track in the fixed five-section order.
- Declaring each body's `prerequisites` in the contracted frontmatter shape, transcribed from its
  settled spec.
- Stating each body's **scope boundary** against any sibling course it could be confused with (e.g.
  `linux-app-development` against `just-enough-python`'s own scope).
- Adding this plan's authored courses to the tracked
  [Course Library Catalog](./tech-docs.md#course-library-catalog) as real rows.
- Updating `<COURSES>_index.md` to list every authored course.
- Emitting one complete **band-completion signal** per band (2 total).
- Manual behavioural verification of a sample of authored course pages via Playwright MCP, with
  committed screenshot evidence in `evidence/`.

**Out of scope**:

- **Any manifest file** under `<MANIFESTS>` — creating, appending to, reordering, or re-verifying.
  Owned by the manifest-growth plan. Binding invariant.
- **Any path landing anchor** under `<PATHS>` and the paths hub.
- **Any `course-paths` feature code** (`core/` or `shell/`).
- **Any redirect module or rule.**
- **Any course outside the named 14** — no Band 1, 2, 5, 6, 7, 8, or 9 course, no new capstone.
- **The `prerequisites` frontmatter contract's definition** — consumed here, owned by the schema plan.
- **The `syllabus/` folder** — read-only from this plan; never copied.
- **Any Indonesian (`id`) course content** — explicitly deferred.
- **The UI design funnel** — this plan is not UI-bearing.
- **The rule-15 three-tester retest** — exemption recorded with reasons in
  [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded).

## Product-Level Risks

- **A body authored from judgment rather than its spec.** Concept coverage silently drops and
  prerequisite edges get invented. Mitigated by naming the exact cross-plan spec path in every
  authoring step and making "authored from that spec" an explicit acceptance criterion.
- **A primer/platform pair authored in the wrong order or with a missing prerequisite declaration.**
  Mitigated by authoring each pair inside the same phase and asserting the exact prerequisite slug via
  a grep-checkable clause in each phase's gate (see the Scenario Outline above).
- **A prerequisite edge invented at authoring time.** The failure does not surface here — it surfaces
  in the manifest-growth plan as an integrity failure with no trace back. Mitigated by transcribing the
  declared chain rather than re-deriving it.
- **A natively-authored slug colliding with an already-shipped or already-landed slug.** Mitigated by
  running the 14-slug collision check against a populated namespace — which is why
  `ayokoding-learning-path-01-url-restructure` and `ayokoding-learning-path-04-course-authoring` are
  both hard prerequisites.
- **A manifest-mutating step reintroduced into this plan.** Makes the split unschedulable. Mitigated
  by the invariant being stated in three documents plus a phase-gate check that the plan's diff
  touches zero `<MANIFESTS>` paths.
- **A vague band-completion signal.** The manifest-growth plan cannot act on it. Mitigated by the
  five-field signal contract, with an explicit rejection rule for incomplete signals.
- **`ayokoding-learning-path-10-...`'s downstream work stalls because Band 4 lands incompletely.**
  Mitigated by Band 4 being its own phase with its own delivery boundary, its own band-completion
  signal, and an explicit downstream-readiness Gherkin scenario bound to that phase's gate.
- **This plan lands against a still-dynamic, still-middlewared `ayokoding-www`.** Mitigated by the
  hard `blockedBy` on `vercel-function-cost-reduction` with a concrete, checkable precondition gated
  in Phase 0.
