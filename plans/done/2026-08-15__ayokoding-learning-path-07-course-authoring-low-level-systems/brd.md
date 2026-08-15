# Business Requirements — Course Authoring: Low-Level Systems & Native Languages

## Business Goal

Fill **7 of the 16 course slots** in the shared course library's original "Low-level systems, JVM &
languages, internals builds" band with real, authored bodies: `just-enough-c`, `just-enough-cpp`,
`linux-os`, `windows-os`, `system-programming`, `just-enough-rust`, and `modern-system-programming`.
A path manifest is an ordered list of course IDs; an ID with no resolving body is an integrity
failure, not a path. **This plan is one of two that finish the job the original band started but
could not complete inside a single 5–15-course-per-plan-sized plan.**

Concretely, it authors:

- **Two systems-language on-ramps**: `just-enough-c` (transferred FS-SE topic 78) and
  `just-enough-cpp` (net-new — the library had no dedicated C++ course before this).
- **Two OS-internals courses**: `linux-os` (topic 79) and `windows-os` (topic 80) — the two dominant
  production operating systems, taught by-example against real syscalls/API surfaces.
- **A C systems-programming course**: `system-programming` (topic 81) — close-to-metal memory
  management, the counterpart every reader eventually compares against a memory-safe language.
- **A Rust on-ramp and its systems-programming counterpart**: `just-enough-rust` (topic 82) and
  `modern-system-programming` (topic 83) — the safe-systems-programming answer to `system-programming`.

The business change here is **content, not architecture**: no schema, no route, no component, no
redirect, and — by binding invariant — **no manifest**. This mirrors
`ayokoding-learning-path-04-course-authoring`'s own framing exactly; this plan differs only in scope
(7 bodies, not 90) and in being one of a two-way split rather than the whole band.

## Why the split, and why this half specifically

The original Band 6 held 16 courses — outside the repo's 5–15-course-per-plan sizing rule for a
single delivery plan. Splitting along the **C-family/OS vs. JVM/advanced-languages** seam (rather
than, say, an arbitrary alphabetical half) keeps each half's courses **mutually more related to each
other than to the other half**: the 7 courses here share a native-systems-programming throughline
(C → C++, C → Linux/Windows internals, C → close-to-metal C, Rust as the safe-systems answer to all
of it), while the sibling's 9 courses share a managed-runtime/PL-theory/build-your-own throughline
(JVM, Lisp, F#/type theory, compilers, and three build-your-own-X capstones). A reader following
either half in sequence gets a coherent sub-arc rather than an arbitrary fragment.

## Why the bodies must be authored from the settled spec, not generated ad hoc

Identical reasoning to `ayokoding-learning-path-04-course-authoring` [inherited, not re-derived]: each
of these 7 courses already has a settled spec file
(`syllabus/courses/<course-id>.md`) with an enumerated `co-NN` concept list, an `ex-NN`
worked-example inventory, and a declared prerequisite chain. Authoring "from a fresh judgment call"
risks the same three failure modes that plan names explicitly:

- **Concept coverage drifts** against the settled enumeration.
- **Prerequisite edges get invented**, breaking the library's DAG in a way that surfaces far
  downstream in `ayokoding-learning-path-12-careers-se-manifests` as an integrity failure with no
  traceable link back to the authoring decision that caused it. This risk is concrete here: `just-enough-cpp` MUST
  declare `just-enough-c` (DD-14's dedicated on-ramp, cited by
  `ayokoding-learning-path-04-course-authoring`'s tech-docs.md), and `system-programming` MUST declare
  both `just-enough-c` and `linux-os` — an invented or dropped edge among these four courses breaks
  the one non-trivial DAG chain inside this plan's own 7-course scope.
- **Scope boundaries collapse** — specifically the risk that `system-programming` (C) and
  `modern-system-programming` (Rust) drift into being read as duplicates rather than deliberate
  same-depth counterparts in different languages, or that `linux-os` and `windows-os` blur into one
  undifferentiated "operating systems" course.

## Business Impact

**Pain points addressed**:

- Without this plan (and its sibling), the library's `careers/fundamentally-strong/software-engineer`
  and `careers/interview-ready/software-engineer` manifests cannot reference any of these 7 course
  IDs — a reader following either path toward systems depth hits a dead link.
- The library had **no C++ course at all** before `just-enough-cpp` — a genuine gap DD-14 identified
  (dedicated on-ramp, prerequisite `just-enough-c`), not a re-teach of existing material.
- A reader comparing "how does this look in a memory-safe systems language" had no Rust
  systems-programming counterpart to `system-programming` before `modern-system-programming` exists.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- **One authoring investment, four products** — each body is authored once, path-neutral, at one
  canonical URL, exactly as `ayokoding-learning-path-04-course-authoring`'s own reasoning states.
- **A curriculum that can be audited** — every body traces to its settled
  `syllabus/courses/<course-id>.md` spec, so "is this course complete?" is answerable by comparison
  against the spec's `co-NN`/`ex-NN` enumeration.
- **A coherent native-systems sub-arc ships as one unit** — a reader working this band in order gets
  C → C++ → OS internals (both families) → close-to-metal C → Rust → safe systems programming, without
  waiting on the unrelated JVM/build-your-own half to land first (the two halves have no dependency
  edge in either direction — see `tech-docs.md`).

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears the same roles
`ayokoding-learning-path-04-course-authoring` names:

- **Content strategist** — owns each of these 7 courses' scope boundary against its siblings
  (`system-programming` vs. `modern-system-programming`; `linux-os` vs. `windows-os`).
- **Content author** (via `apps-ayokoding-www-primer-maker` and `apps-ayokoding-www-by-example-maker`)
  — writes the 7 bodies.
- **Content reviewer** (via the matching checkers plus `apps-ayokoding-www-facts-checker` and
  `apps-ayokoding-www-link-checker`) — validates every body before its PR merges.

**Roles explicitly NOT worn by this plan**: frontend engineer, data/schema author, path composer, and
IA/URL owner — identical exclusions to `ayokoding-learning-path-04-course-authoring`, all owned by
that programme's other split plans.

## Business-Level Success Metrics

Each metric below is an **observable check**.

- **7 authored bodies exist** (observable): every slug in `evidence/authored-body-slugs.txt`
  resolves to a directory under `<COURSES>`. Falsifiable both ways: all 7 absent at the Phase-0
  baseline; none absent after Phase 2.
- **Every body traces to its spec** (observable): each course's scope, concept coverage, and declared
  prerequisites match its `syllabus/courses/<course-id>.md` spec's `co-NN`/`ex-NN`/prerequisite-chain
  enumeration. Verified per-course by its checker pass.
- **The one non-trivial DAG chain inside this plan's own scope holds** (observable): `just-enough-cpp`
  declares `just-enough-c`; `linux-os` declares `just-enough-c` and `just-enough-bash`; `windows-os`
  declares `just-enough-c`; `system-programming` declares `just-enough-c` and `linux-os`;
  `modern-system-programming` declares `just-enough-rust`. Each is a grep-checkable assertion on the
  course's own `_index.md`.
- **`system-programming` and `modern-system-programming` state their counterpart relationship**
  (observable): each overview names the other as its same-depth counterpart in the other language.
- **Every body passes its content checkers** (observable): zero CRITICAL / HIGH / MEDIUM findings
  from the matching maker's checker, `apps-ayokoding-www-facts-checker`, and
  `apps-ayokoding-www-link-checker`.
- **No manifest file changed in this plan's commits** (observable): the plan's own diff across all
  merged PRs touches zero paths under `<MANIFESTS>`.
- **One complete band-completion signal is emitted** (observable): the five-field signal names all
  three `software-engineer` manifests by full path and carries a resolvable merge commit SHA.
- **No regressions** (observable): `npm exec nx run ayokoding-www:build` renders green; markdownlint, link
  validation, and heading-hierarchy validation pass across the authored tree.

## Business-Scope Non-Goals

- **Editing any manifest file** — owned by `ayokoding-learning-path-12-careers-se-manifests`. A
  correctness requirement, not a scope preference.
- **Authoring any of the sibling plan's 9 courses** (`just-enough-java`,
  `enterprise-java-and-the-jvm`, `lisp`, `just-enough-fsharp`, `type-systems`,
  `compilers-parsers-and-transpilers`, `build-your-own-git`, `build-your-own-database`,
  `build-your-own-raft`) — owned by
  `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`.
- **Building any part of the navigation UI** — owned by `ayokoding-learning-path-03-navigation-ui`
  (already done).
- **Defining the `prerequisites` frontmatter contract** — consumed here, owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- **Adding an Indonesian mirror of the course content** — deferred, recorded as a decision. Every
  course body in this plan is `en`-only.
- **Rewriting the pedagogy or depth of any of the 6 transferred topics** (all but `just-enough-cpp`)
  — authored native from their settled specs, not re-conceived.
- **Fixing anything in `ayokoding-learning-path-04-course-authoring`'s own remaining scope** (its
  6 AI-engineering courses, Band 1's already-merged 5 bodies, or whatever else its own concurrent trim
  leaves it with) — this plan reads that plan's trimmed baseline; it does not edit it.
- **Fixing the Vercel cost/rendering issues itself** — this plan depends on
  `vercel-function-cost-reduction` being merged; it does not perform any of that plan's work.

## Business Risks and Mitigations

| Risk                                                                                                                                                                                      | Mitigation                                                                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A body is authored from a fresh judgment call instead of its settled spec, so concept coverage drifts.                                                                                    | Every authoring step names the exact `syllabus/courses/<course-id>.md` path; the checker pass compares the body against the spec's `co-NN`/`ex-NN` enumeration.                                                                                                                     |
| A step in this plan mutates a manifest, making the two-plan-plus-manifest schedule unschedulable.                                                                                         | The manifest ownership invariant is stated in `README.md`, `tech-docs.md`, and `delivery.md`; a phase gate asserts the plan's diff touches zero paths under `<MANIFESTS>`.                                                                                                          |
| This plan and its sibling (`10`) race to author the same course ID, or one assumes a dependency edge on the other that does not exist.                                                    | The dependency-edge investigation in `tech-docs.md` checks all 9 of the sibling's declared prerequisite lists against this plan's 7 IDs and finds none; this plan's own 7-slug collision check in Phase 0 catches any overlap.                                                      |
| A natively-authored slug collides with a not-yet-moved re-home slug or a slug the trimmed `04` plan still claims.                                                                         | Phase 0's collision check runs against both the populated `<COURSES>` namespace and `04`'s (trimmed) `evidence/authored-body-slugs.txt`.                                                                                                                                            |
| Invented prerequisite edges break the DAG, surfacing far downstream with no traceable cause.                                                                                              | Each body's `prerequisites` are transcribed from its spec's declared chain, never re-derived; declaration is an explicit per-course acceptance criterion at authoring time.                                                                                                         |
| `system-programming` and `modern-system-programming` are read as duplicates rather than deliberate C/Rust counterparts.                                                                   | Each course's `overview.md` explicitly names the other as its counterpart in the sibling language — a grep-checkable acceptance criterion.                                                                                                                                          |
| `linux-os` and `windows-os` blur into one undifferentiated "operating systems" course.                                                                                                    | Each course's `overview.md` states its explicit OS-family scope boundary against the other.                                                                                                                                                                                         |
| A course body reproduces copyrighted material (vendor API reference prose, a lifted figure, Stack-Overflow-licensed code) — programme `A8`.                                               | Six concrete hazards mapped to the authoring pipeline (see `tech-docs.md`): code authored originally, docs prose restated with citation, figures authored in Mermaid, structure from the spec's own `co-NN` order, trademarks used nominatively only, datasets authored not lifted. |
| Proceeding without verifying the current rendering baseline compounds the site's dynamic-render cost problem with 7 more pages, or collides with its in-flight layout/middleware rewrite. | Phase 0 checks the current concrete file state (root layout `headers()` call removed; `middleware.ts` deleted) before any authoring begins.                                                                                                                                         |
| A band lands but the manifest plan never grows its manifests, leaving paths permanently truncated.                                                                                        | The band's gate requires a complete five-field signal naming every affected manifest by full path plus the merge commit SHA; an incomplete signal is rejected rather than guessed at.                                                                                               |
