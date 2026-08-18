# Product Requirements — Course Authoring: Low-Level Systems & Native Languages

## Product Overview

This plan authors **7 course bodies** — page bundles under
`apps/ayokoding-www/content/en/learn/courses/` — each a standalone, path-neutral building block with
a stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track. It is one half of a two-way split of
`ayokoding-learning-path-04-course-authoring`'s original Band 6; the other half
(`just-enough-java`, `enterprise-java-and-the-jvm`, `lisp`, `just-enough-fsharp`, `type-systems`,
`compilers-parsers-and-transpilers`, `build-your-own-git`, `build-your-own-database`,
`build-your-own-raft`) is authored by
[`ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`](../../backlog/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/README.md)
(sibling, not created here).

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter. All three `careers/`-role software-engineer paths
(`interview-ready`, `immediately-effective`, `fundamentally-strong`) may reference these 7 courses
once `ayokoding-learning-path-12-careers-se-manifests` grows them in; the fourth path
(`careers/immediately-effective/ai-engineer`) does not, since none of these 7 courses is an
AI-engineering course.

The library body is **content**, exempt from `specs:coverage`. The acceptance criteria below are
**content-level**, verified by the ayokoding content checkers and by grep-checkable assertions on the
authored bodies, not by application tests.

## Personas

Reproduced from `ayokoding-learning-path-04-course-authoring`'s persona set, scoped to the two
personas most directly served by this plan's 7 courses — every authored course remains reachable by
readers of all three `software-engineer`-role paths, so all three are carried:

- **A university-style, fundamentals-first learner (north-star for the
  `careers/fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route:
  computer architecture, close-to-metal systems programming, and language internals before building
  apps at scale. This plan's 7 courses are exactly this persona's systems-depth material.
- **An experienced engineer re-entering the job market (north-star for the
  `careers/interview-ready/software-engineer` path)** — already owns editor workflow and deep
  fundamentals; may need to refresh systems-level breadth (OS internals, memory management) for a
  senior/staff systems-adjacent interview loop.
- **A builder who wants to be effective fast (north-star for the
  `careers/immediately-effective/software-engineer` path)** — reaches these courses later in the
  journey, once deepening into systems fundamentals.
- **A reader who lands on a shared course by deep-link / share** — arrives at, e.g.,
  `/en/learn/courses/system-programming` without a path context and must get a coherent standalone
  view (with its prerequisites surfaced) plus an obvious way to enter a path.
- **Maintainer (content strategist / content author / reviewer)** — authors the 7 bodies via the
  ayokoding primer and by-example maker agents.

## User Stories

Scoped to this plan's 7-course surface.

- As a **fundamentals-first learner**, I want a dedicated C++ on-ramp (`just-enough-cpp`) that
  declares `just-enough-c` as its prerequisite, so that I progress from C to C++ in the order the
  library's DAG expects rather than reading them as unrelated primers.
- As a **reader comparing operating systems**, I want `linux-os` and `windows-os` each to state its
  own OS-family scope boundary explicitly, so that I know which course teaches which internals rather
  than reading one as a subset or superset of the other.
- As a **reader comparing systems-programming languages**, I want `system-programming` (C) and
  `modern-system-programming` (Rust) each to name the other as its same-depth counterpart, so that I
  understand they teach the identical close-to-metal principles in a different language's idiom
  rather than duplicating each other.
- As a **reader following the C-family chain**, I want `system-programming` to declare both
  `just-enough-c` and `linux-os` as prerequisites, so that I arrive with the OS-internals knowledge
  the course's syscall-level material assumes.
- As the **maintainer**, I want every body authored **from** its settled `syllabus/courses/<id>.md`
  spec, so that concept coverage and prerequisite edges are transcribed rather than re-invented.
- As the **downstream manifest author**, I want a complete, explicit band-completion signal naming
  every manifest to grow, so that I never have to guess which paths this band affects.
- As a **reader of either half of the original Band 6**, I want this plan's 7 courses to carry zero
  dependency on the sibling plan's 9 courses, so that I can read this plan's sub-arc to completion
  without waiting on unrelated JVM/build-your-own material.

## Acceptance Criteria (Gherkin)

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule).

### C-family on-ramp chain

```gherkin
Scenario: just-enough-cpp declares its C on-ramp prerequisite
  Given the just-enough-cpp course is authored
  When a reader inspects its declared prerequisites
  Then it names just-enough-c as a prerequisite
  And its overview states the C-to-C++ progression rationale (DD-14's dedicated on-ramp)
```

### OS-internals courses

```gherkin
Scenario: linux-os and windows-os state distinct OS-family scope boundaries
  Given linux-os and windows-os are both authored
  When a reader compares their overviews
  Then each explicitly scopes to its own OS family (Linux syscalls/filesystems vs. Windows internals/the API)
  And neither overview presents the other's OS family as in scope
```

### C/Rust systems-programming counterparts

```gherkin
Scenario: system-programming and modern-system-programming state their counterpart relationship
  Given system-programming (C) and modern-system-programming (Rust) are both authored
  When a reader compares their overviews
  Then modern-system-programming's overview names system-programming as its C counterpart
  And each teaches the same close-to-metal principles in its own language's idiom without reproducing the other's worked examples
```

### The one non-trivial DAG chain in this plan's scope

```gherkin
Scenario: The C-family prerequisite chain resolves in declaration order
  Given just-enough-c, linux-os, and system-programming are all authored
  When the library's prerequisite DAG is read for these three IDs
  Then linux-os declares just-enough-c and just-enough-bash as prerequisites
  And system-programming declares just-enough-c and linux-os as prerequisites
```

### Scoped build-green (this plan's own surface)

```gherkin
Scenario: The authored low-level-systems course bodies build and validate green
  Given all seven course bodies this plan authors have landed under the courses bucket
  When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
  Then the build succeeds over the authored tree
  And link, heading-hierarchy, and markdownlint validation report no errors across the authored course bodies
```

## Scenario-to-delivery binding

| Scenario                                                                              | Binds to                                                                                 |
| ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| just-enough-cpp declares its C on-ramp prerequisite                                   | Phase 1 · `just-enough-cpp` authoring step                                               |
| linux-os and windows-os state distinct OS-family scope boundaries                     | Phase 1 · `linux-os` and `windows-os` authoring steps                                    |
| system-programming and modern-system-programming state their counterpart relationship | Phase 1 (`system-programming`) and Phase 2 (`modern-system-programming`) authoring steps |
| The C-family prerequisite chain resolves in declaration order                         | Phase 1 · `linux-os` and `system-programming` authoring steps                            |
| The authored low-level-systems course bodies build and validate green                 | Phase 3 · Section & Authored-Tree Verification                                           |

## NEW Course & Transferred-Topic Specifications

Six of the seven courses are **transferred FS-SE topics** (native-authored, no legacy home); one
(`just-enough-cpp`) is genuinely **NEW**. Every course is a full page-bundle (learning track +
drilling track) inheriting the same cross-cutting authoring guarantees as every course in this
programme: accuracy-verified via `web-researcher` before authoring; follow-along-complete; colocated
runnable `code/`; exhaustive `co-NN`/`ex-NN` enumeration; `prerequisites` metadata plus navigation.

**Full per-course concept / example / prerequisite / capstone detail lives in the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)**
(one file per course ID). The table below is copied verbatim from
`ayokoding-learning-path-04-course-authoring`'s own catalog row set for these 7 IDs — see
[tech-docs.md §Course Library Catalog](./tech-docs.md#course-library-catalog) for the reproduced
table with origin codes.

- **`just-enough-c`** (Primer · C, transferred topic 78) — minimal C for the OS/systems topics that
  follow. Entry point, no prerequisite.
- **`just-enough-cpp`** (Primer · C++, **NEW**) — RAII, templates, STL, smart pointers. Prerequisite:
  `just-enough-c` (DD-14's dedicated on-ramp — the library had no C++ course before this).
- **`linux-os`** (By Example · C + shell, transferred topic 79) — processes, syscalls, filesystems.
  Prerequisites: `just-enough-c`, `just-enough-bash`.
- **`windows-os`** (By Example · C + PowerShell, transferred topic 80) — Windows internals, the API.
  Prerequisite: `just-enough-c`.
- **`system-programming`** (By Example · C, transferred topic 81) — close-to-metal C: memory model,
  manual resource management. Prerequisites: `just-enough-c`, `linux-os`.
- **`just-enough-rust`** (Primer · Rust, transferred topic 82) — ownership, borrowing, the type
  system. Entry point, no prerequisite.
- **`modern-system-programming`** (By Example · Rust, transferred topic 83) — safe systems
  programming; the Rust counterpart of `system-programming` (81). Prerequisite: `just-enough-rust`.

**Principle-first framing (HARD, inherited).** Every course teaches a durable **principle**; any
target codebase used as a worked-example illustration is illustrative, never the subject.

**Volume-target bands** (inherited from the source plan; floor not cap):

| Course shape             | Concept floor (`co-NN`) | Worked-example band (`ex-NN`)         |
| ------------------------ | ----------------------- | ------------------------------------- |
| By Example               | ≥ 10                    | 75–85 code examples                   |
| Primer (_Just Enough X_) | ≥ 8                     | 75–85 code examples (By-Example pace) |

## Product Scope

**In-scope**:

- Authoring **7 course page bundles** under
  `apps/ayokoding-www/content/en/learn/courses/<course-id>/`, each with `_index.md` (declaring
  `prerequisites`), `overview.md`, a `learning/` track (concepts, worked examples, colocated runnable
  `code/`, and `learning/capstone/` where the spec calls for one), and a `drilling/` track in the
  fixed five-section order.
- Declaring each body's `prerequisites` in the contracted frontmatter shape, transcribed from its
  settled spec.
- Stating each body's **scope boundary** against the sibling course it could be confused with
  (`linux-os` vs. `windows-os`; `system-programming` vs. `modern-system-programming`).
- Adding this plan's 7 authored courses to the tracked
  [Course Library Catalog](./tech-docs.md#course-library-catalog) as real rows.
- Updating `<COURSES>_index.md` to list the 7 newly authored courses.
- Emitting **one** complete band-completion signal.
- Manual behavioural verification of a sample of the 7 authored course pages via Playwright MCP, with
  committed screenshot evidence.

**Out of scope**:

- **Any manifest file** under `<MANIFESTS>` — owned by `ayokoding-learning-path-12-careers-se-manifests`.
  Binding invariant.
- **The sibling plan's 9 courses** — owned by
  `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`.
- **Any path landing anchor**, **any `course-paths` feature code**, **any redirect module or rule** —
  owned elsewhere, same as every plan in this programme.
- **The `prerequisites` frontmatter contract's definition** — consumed here, owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- **The `syllabus/` folder** — read-only from this plan; never copied.
- **Any Indonesian (`id`) course content** — explicitly deferred.
- **The UI design funnel** — this plan is not UI-bearing.
- **The rule-15 three-tester retest** — exemption recorded with reasons in
  [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded).
- **Any change to `ayokoding-learning-path-04-course-authoring`'s remaining scope** (its 6 AI courses,
  its already-merged Band 1, or its own Band 6 trim) — read-only precondition, never edited here.

## Product-Level Risks

- **A body authored from judgment rather than its spec.** Mitigated by naming the exact
  `syllabus/courses/<id>.md` path in every authoring step and making "authored from that spec" an
  explicit acceptance criterion.
- **A prerequisite edge invented or dropped on the plan's one non-trivial DAG chain
  (`just-enough-c` → `linux-os` → `system-programming`; `just-enough-c` → `just-enough-cpp`;
  `just-enough-rust` → `modern-system-programming`).** The failure would surface downstream in the
  manifest plan as an integrity failure with no trace back. Mitigated by transcribing the declared
  chain rather than re-deriving it, with a grep-checkable acceptance clause per edge.
- **`system-programming` / `modern-system-programming` or `linux-os` / `windows-os` read as
  duplicates.** Mitigated by an explicit counterpart/scope-boundary statement in each course's own
  `overview.md`.
- **A false assumption of a dependency edge on the sibling plan's courses**, causing this plan to
  stall waiting on unrelated JVM/build-your-own work. Mitigated by the dependency-edge investigation
  in `tech-docs.md`, which checks all 9 of the sibling's courses' prerequisites against this plan's 7
  IDs and finds none.
- **A manifest-mutating step introduced into this plan.** Mitigated by the invariant stated in three
  documents plus a phase-gate check that the plan's diff touches zero `<MANIFESTS>` paths.
- **A vague band-completion signal.** Mitigated by the five-field signal contract, with an explicit
  rejection rule for incomplete signals.
- **Proceeding without verifying the current rendering baseline.** Mitigated by a hard Phase 0 gate on
  that plan's concrete file-based signal.
