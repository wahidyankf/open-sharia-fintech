# Product Requirements — Course Authoring: JVM, Advanced Languages & Build-Your-Own Internals

## Product Overview

This plan authors **9 course bodies** of the shared course library — page bundles under
`apps/ayokoding-www/content/en/learn/courses/`, each a standalone, path-neutral building block with a
stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track, per the shape
[`ayokoding-learning-path-04-course-authoring/tech-docs.md`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/tech-docs.md#the-course-page-bundle)
defines and this plan inherits verbatim.

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter — the four `careers/` paths (three `software-engineer`-role manifests
owned by `ayokoding-learning-path-12-careers-se-manifests`, plus the one `ai-engineer` manifest owned
by `ayokoding-learning-path-13-careers-ai-manifest`, successors to the retired
`ayokoding-learning-path-05-manifests`) will eventually compose these 9 bodies alongside the other 118
in the 127-course catalog.

The library body is **content**, exempt from `specs:coverage`; the navigation feature that renders it
is app code already shipped by the (done) `ayokoding-learning-path-03-navigation-ui` plan. The
acceptance criteria below are **content-level**, verified by the ayokoding content checkers and by
grep-checkable assertions on the authored bodies, not by application tests.

## Personas

Scoped to this plan's 9-course slice; the full four-path persona set is reproduced verbatim in
`ayokoding-learning-path-04-course-authoring/prd.md` and is not re-derived here.

- **A builder who wants to be effective fast** — reaches `just-enough-java`,
  `enterprise-java-and-the-jvm`, `just-enough-fsharp`, or the build-your-own trio while deepening past
  their first working app; wants a fast, honest on-ramp rather than exhaustive language coverage.
- **A university-style, fundamentals-first learner** — reaches `type-systems`,
  `compilers-parsers-and-transpilers`, and `lisp` for CS-theory depth (algebraic types, parsing, macro
  systems) before or alongside building apps at scale.
- **An experienced engineer re-entering the market** — reaches the build-your-own trio as
  senior/staff-level proof-of-transfer material: a runnable Git plumbing layer, a small transactional
  database, and a Raft-replicated KV store are exactly the kind of artefact that answers "what have you
  actually built" in a loop.
- **A reader who lands on a shared course by deep-link / share** — arrives at, say,
  `build-your-own-raft` without a path context and must see its prerequisites (`just-enough-go`,
  `distributed-systems`) surfaced, plus an obvious way to enter a path.
- **Maintainer (content strategist / content author / reviewer)** — owns each course's scope boundary,
  authors the 9 bodies via the ayokoding maker agents, and records the band-completion signal.

## User Stories

- As a **builder wanting JVM depth**, I want `just-enough-java` to teach syntax, the JVM, and
  collections without comprehensive Java coverage, and `enterprise-java-and-the-jvm` to build on it
  with Spring and the JVM ecosystem, so that I get a fast, honest on-ramp rather than a textbook.
- As a **reader curious about homoiconicity**, I want `lisp` to teach macros and homoiconicity through
  Scheme and Clojure, so that I understand code-as-data without needing either language for anything
  else in the library.
- As a **functional-programming-curious reader**, I want `just-enough-fsharp` as a fast on-ramp and
  `type-systems` to build on the already-shipped `functional-programming` and `programming-paradigms`
  (plus a first taste of static types from the already-shipped `just-enough-typescript`) with
  algebraic types and inference across OCaml, Haskell, and F#, so that I see the same ideas across
  three type systems rather than one.
- As a **reader wanting compiler depth**, I want `compilers-parsers-and-transpilers` to teach lexers,
  parsers, and ASTs in F#, building on `just-enough-fsharp`, `type-systems`, and the already-shipped
  `computer-science-foundations`, so that I understand how source text becomes a program.
- As a **reader wanting a concrete Git-internals artefact**, I want `build-your-own-git` to build the
  Git object model and plumbing in Python from `just-enough-python` and `version-control-and-git`, so
  that I finish with a runnable, if minimal, Git implementation.
- As a **reader wanting a concrete database-internals artefact**, I want `build-your-own-database` to
  build storage, indexing, and transactions in Python from `database-internals-and-storage-engines`
  and the already-shipped `sql-essentials`, so that I understand what a database actually does under
  its query language.
- As a **reader wanting a concrete consensus artefact**, I want `build-your-own-raft` to build Raft
  consensus and a replicated key-value store in Go from `just-enough-go` and `distributed-systems`, so
  that I finish having implemented the algorithm most distributed-systems courses only describe.
- As the **maintainer**, I want every body authored **from** its settled
  `syllabus/courses/<course-id>.md` spec, so that concept coverage and prerequisite edges are
  transcribed rather than re-invented.
- As the **downstream manifest author**, I want a complete, explicit band-completion signal naming
  every manifest to grow and every course ID landed, so that I never have to guess which paths this
  plan's bodies affect.
- As the **maintainer sequencing cross-plan work**, I want the `build-your-own-*` trio authored last
  within this plan, so that the two sibling plans supplying `just-enough-go` and `distributed-systems`
  have the maximum possible window to land before their bodies are actually needed.

## Acceptance Criteria (Gherkin)

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And`/`But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule).

### Course bodies and their prerequisite chains

```gherkin
Scenario: enterprise-java-and-the-jvm declares just-enough-java and software-architecture as its prerequisites
  Given the just-enough-java course is authored and software-architecture is confirmed present
  When a reader opens enterprise-java-and-the-jvm's frontmatter
  Then it declares just-enough-java in its prerequisites list
  And it also declares software-architecture in its prerequisites list
```

```gherkin
Scenario: type-systems declares functional-programming, programming-paradigms, and just-enough-typescript as its prerequisites
  Given the type-systems course is authored
  When a reader opens type-systems's frontmatter
  Then it declares the already-shipped functional-programming course in its prerequisites list
  And it also declares the already-shipped programming-paradigms and just-enough-typescript courses
```

```gherkin
Scenario: compilers-parsers-and-transpilers declares its three prerequisites
  Given the compilers-parsers-and-transpilers and type-systems courses are authored
  When a reader opens compilers-parsers-and-transpilers's frontmatter
  Then it declares just-enough-fsharp and type-systems in its prerequisites list
  And it declares the already-shipped computer-science-foundations course
```

```gherkin
Scenario: build-your-own-git declares its two prerequisites
  Given the build-your-own-git course is authored
  When a reader opens its frontmatter
  Then it declares just-enough-python in its prerequisites list
  And it declares the already-shipped version-control-and-git course
```

```gherkin
Scenario: build-your-own-database's prerequisite body is confirmed present before authoring
  Given database-internals-and-storage-engines already exists under the courses namespace (Band 1, plan04)
  When build-your-own-database's own authoring sub-phase begins
  Then a repo-grounded check confirms the course directory exists before the body is written
  And build-your-own-database's frontmatter declares it as a prerequisite
```

```gherkin
Scenario: build-your-own-raft's two external prerequisite bodies are confirmed present before authoring
  Given just-enough-go and distributed-systems are each declared prerequisites of build-your-own-raft
  When build-your-own-raft's own authoring sub-phase begins
  Then a repo-grounded check confirms both course directories exist under the courses namespace
  And the check blocks authoring until both directories are present
```

### Cross-plan independence

```gherkin
Scenario: This plan's courses declare no prerequisite on any of plan 07's 7 low-level courses
  Given the 9 course catalog rows this plan authors
  When each row's prerequisites list is checked against plan 07's 7 course IDs
  Then zero matches are found
  And this plan and plan 07 are confirmed independent, running in parallel
```

### Cost-reduction precondition

```gherkin
Scenario: This plan's first deploy waits for prerendering to be restored
  Given apps/ayokoding-www/.next/prerender-manifest.json currently reports 4 routes
  When this plan's Phase 0 precondition check runs before the first delivery-boundary deploy
  Then the recorded route count from vercel-function-cost-reduction's own merge is at least 2000
  And the deploy proceeds only after that count is confirmed
```

### Manifest isolation

```gherkin
Scenario: No manifest file is ever touched by this plan's diff
  Given any delivery-boundary branch in this plan
  When its diff against origin/main is checked for the manifests directory
  Then zero files under apps/ayokoding-www/src/features/course-paths/manifests/ appear in the diff
  And the phase gate fails if any manifest file is touched
```

### Scoped build-green scenario

```gherkin
Scenario: The 9 authored course bodies build and validate green
  Given all 9 course bodies in this plan's catalog are authored and merged to origin/main
  When ayokoding-www's build and content checkers run against the merged tree
  Then npm exec nx run ayokoding-www:build exits 0
  And every one of the 9 bodies passes its matching content checker with zero CRITICAL/HIGH/MEDIUM findings
```

## Product Scope

**In scope**:

- Authoring all 9 course bodies listed in [tech-docs.md's Course Library Catalog](./tech-docs.md#course-library-catalog).
- Declaring each course's `prerequisites` frontmatter exactly as transcribed from its settled
  `syllabus/courses/<course-id>.md` spec.
- Adding each course's row to this plan's own tech-docs.md catalog (the plan-local mirror of the
  shared catalog).
- Recording the partial band-completion signal at the end of this plan's authoring phases.
- A sample Playwright MCP manual-verification pass over the 9 authored pages (Rule-15 triad exempt,
  per [README.md](./README.md#rule-15-three-tester-retest--exemption-recorded)).

**Out of scope** (each with a recorded rationale):

- Authoring any of the other 7 Band-6 courses — belongs to
  `ayokoding-learning-path-07-course-authoring-low-level-systems`.
- Any manifest file edit or manifest integrity/prerequisite-consistency re-verification — belongs to
  `ayokoding-learning-path-12-careers-se-manifests` (successor to the retired
  `ayokoding-learning-path-05-manifests`).
- Any Indonesian (`id`) translation of the 9 bodies — deferred per the source plan's Business-Scope
  Non-Goals.
- Resolving the `-05-`/`-06-` folder-prefix naming collision — observed and reported, not fixed here.
- Any change to `apps/ayokoding-www`'s rendering, caching, or Vercel-cost-reduction code — that is
  `vercel-function-cost-reduction`'s own historical scope; this plan only records the current
  rendering state as repository context.

## Product-Level Risks

- **UX risk**: a reader who deep-links to `build-your-own-raft` before its prerequisite courses exist
  in any path manifest sees a course with no path context — mitigated by the existing navigation
  feature's standalone-course view (already shipped by plan 03), not by anything this plan builds.
- **Feature-interaction risk**: if this plan's cohort-2 sub-phase for `build-your-own-raft` runs before
  plan 05/06 actually merge `just-enough-go`/`distributed-systems`, the frontmatter prerequisite would
  point at a non-existent course ID — mitigated by the explicit pre-authoring existence check in the
  Gherkin scenario above and in [delivery.md](./delivery.md)'s cohort-2 gate.
