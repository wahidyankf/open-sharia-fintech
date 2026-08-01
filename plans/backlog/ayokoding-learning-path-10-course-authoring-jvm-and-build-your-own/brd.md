# Business Requirements — Course Authoring: JVM, Advanced Languages & Build-Your-Own Internals

## Business Goal

Fill the shared course library with **9 course bodies** — the JVM/advanced-language/build-your-own half
of Band 6 — so the four `careers/` path manifests can eventually reference a complete Band 6 without a
truncated `courseOrder`. A path manifest is an ordered list of course IDs; an ID with no resolving body
is an integrity failure, not a path — the same reasoning
[`ayokoding-learning-path-04-course-authoring/brd.md`](../../in-progress/ayokoding-learning-path-04-course-authoring/brd.md)
states for the library as a whole, scoped here to this plan's 9-course slice.

Concretely it authors:

- **Two JVM-track bodies** — `just-enough-java` (Primer) and `enterprise-java-and-the-jvm`
  (By Example), giving the library its first JVM on-ramp and its enterprise/Spring depth course.
- **One Lisp body** — `lisp` (By Example, Scheme + Clojure), the library's only homoiconicity/macro
  treatment.
- **Two functional/type-theory bodies** — `just-enough-fsharp` (Primer) and `type-systems`
  (By Example, OCaml + Haskell + F#), the library's algebraic-type and type-inference depth.
- **One compilers body** — `compilers-parsers-and-transpilers` (By Example, F#), lexers/parsers/ASTs.
- **Three build-your-own internals capstone-adjacent bodies** — `build-your-own-git`,
  `build-your-own-database`, `build-your-own-raft` — each a from-scratch systems-building course whose
  prerequisite depth lives partly in this plan's own family and partly in two sibling plans still in
  flight.

The business change here is **content**, not architecture: no schema, no route, no component, no
redirect, and — by binding invariant — **no manifest**.

## Why this plan exists as a separate folder, not inside plan04

`ayokoding-learning-path-04-course-authoring`'s own Band 6 held 16 courses — above the repo's 5–15
course-per-plan sizing convention that governs this whole family of course-authoring splits. Splitting
along the low-level/JVM content seam produces two independently-deliverable halves that share no
content prerequisite in either direction (verified — see
[tech-docs.md §Independence from plan 07](./tech-docs.md#independence-from-plan-07-verified)), so
splitting costs nothing in coordination overhead while halving each plan's authoring surface and PR
review burden.

## Why this is the most dependency-heavy of the new sibling plans

Unlike a course-authoring band that only needs the two Wave-1 architecture plans (`01`, `02`) plus its
own baseline (`04`), this plan's `build-your-own-raft` course carries two genuine external content
prerequisites — `just-enough-go` (Band 4) and `distributed-systems` (Band 5) — and
`enterprise-java-and-the-jvm` carries a third, `software-architecture` (also Band 5, and previously
undeclared in this plan's own catalog — see
[tech-docs.md's Course Library Catalog](./tech-docs.md#course-library-catalog)). All three now live in
two sibling plans, `05` and `06` respectively, both of which **exist on disk** under `plans/backlog/`
with a full five-file plan structure `[Repo-grounded — confirmed via directory listing and direct file
read]` — an earlier version of this section treated them as not-yet-on-disk presumptions; both are now
directly readable, and reading `06` directly is what surfaced the previously-missed
`software-architecture` edge. This plan also inherits a new, non-content dependency:
`vercel-function-cost-reduction`, because every delivery boundary in this plan's `worktree-to-pr` mode
deploys to production, and deploying before that plan's prerendering fix lands would compound the
exact cost defect it exists to resolve. Six hard `blockedBy` **plans** in total (`01`, `02`, `04`,
`05`, `06`, plus `vercel-function-cost-reduction`) — more than any other sibling plan in this further
split is known to carry `[Judgment call]` (this plan cannot read the other new sibling plans' own
dependency counts, since they are being authored concurrently; the claim is scoped to what this plan
itself can observe: this count is more than the baseline two-plus-one that governs a
dependency-light band).

## Business Impact

**Pain points addressed**:

- Without this plan, the library has no JVM on-ramp, no Lisp/homoiconicity treatment, no
  algebraic-type-systems depth, no compilers course, and three of its most concrete
  proof-of-transfer capstones (`build-your-own-git`, `build-your-own-database`, `build-your-own-raft`)
  are missing entirely.
- `build-your-own-database` and `build-your-own-raft` are exactly the kind of "productive in target
  codebases" proof-of-transfer anchor
  [`ayokoding-learning-path-04-course-authoring`'s DD-18](../../in-progress/ayokoding-learning-path-04-course-authoring/tech-docs.md#owned-by-this-plan)
  names as the library's outcome anchor — durable principles (storage engines, consensus) evidenced by
  a runnable artefact, not subject matter for its own sake.
- Splitting Band 6 unblocks parallel authoring: this plan and its low-level-systems sibling (`07`) can
  proceed independently once their shared upstream preconditions hold, rather than one 16-course band
  serializing all authoring effort into a single PR-review pipeline.

**Expected benefits** (qualitative reasoning; no fabricated metrics) `[Judgment call]`:

- **One authoring investment, four products** — each of these 9 bodies is authored once, path-neutral,
  and every `careers/` path manifest that references it benefits from every later fix at zero marginal
  cost, exactly as plan04's brd.md states for the library as a whole.
- **A curriculum that can be audited** — every body traces to a settled `syllabus/courses/<id>.md`
  spec with an enumerated `co-NN` concept list and `ex-NN` worked-example inventory (see
  [tech-docs.md](./tech-docs.md#course-library-catalog) for the confirmed per-course counts), so "is
  this course complete?" is answerable by comparison, not impression.
- **Deferred-external-dependency courses authored last** — sequencing the `build-your-own-*` trio at
  the end of this plan's own delivery gives the two upstream sibling plans (`05`, `06`) the maximum
  possible window to land before their bodies are actually needed, reducing the odds this plan stalls
  mid-cohort waiting on a cross-plan merge.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns each course's scope boundary against its siblings (e.g.
  `build-your-own-database` vs `database-internals-and-storage-engines`, whose depth it consumes
  rather than re-teaches) and the cross-plan dependency-timing decisions.
- **Content author** (via the `apps-ayokoding-www-primer-maker` and `apps-ayokoding-www-by-example-maker`
  agents — this plan's 9 courses use only these two formats).
- **Content reviewer** (via the matching checkers plus `apps-ayokoding-www-facts-checker` and
  `apps-ayokoding-www-link-checker`) — validates every body before its PR merges.

Consuming agents `[Repo-grounded]`: `apps-ayokoding-www-primer-maker`, `apps-ayokoding-www-by-example-maker`,
and their matching checkers/fixers, plus `apps-ayokoding-www-facts-checker`,
`apps-ayokoding-www-link-checker`, and `web-researcher` for the accuracy pre-verification pass.

## Business-Scope Non-Goals

- **No manifest edits, ever** — the manifest ownership invariant (see [README.md](./README.md)) is
  absolute; this plan's only outbound artefact toward manifest composition is its band-completion
  signal.
- **No authoring of the other 7 Band-6 courses** — `just-enough-c`, `just-enough-cpp`, `linux-os`,
  `windows-os`, `system-programming`, `just-enough-rust`, `modern-system-programming` belong to
  `ayokoding-learning-path-07-course-authoring-low-level-systems`, a different agent's plan.
- **No Indonesian (`id`) mirror** — this plan's content is `en`-only, per the source plan's
  Business-Scope Non-Goals; the deferral is a recorded decision, not an omission.
- **No resolution of the `-05-`/`-06-` folder-prefix naming collision** noted in
  [README.md](./README.md#naming-note--a-real--05--06--prefix-collision-observed-not-fixed-here) — this
  plan observes and reports it but does not rename any other plan's folder.
- **No re-verification of manifest integrity or prerequisite consistency** — that gate belongs to
  `ayokoding-learning-path-12-careers-se-manifests` (successor to the retired
  `ayokoding-learning-path-05-manifests`), which re-runs it over its own composed artefacts.

## Business Risks and Mitigations

| Risk                                                                                                                                                      | Likelihood | Impact | Mitigation                                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `build-your-own-raft` is authored before `just-enough-go` or `distributed-systems` actually exist on disk, leaving a dangling prerequisite edge           | Medium     | High   | Phase 0 records the two upstream plans' merge state as a precondition; the raft sub-phase inside cohort 2 re-checks both bodies exist on `<COURSES>` immediately before authoring begins, not only at plan start.    |
| The `-05-`/`-06-` naming collision causes a human to conflate this plan's sibling dependencies with the existing manifest/skills plans of the same prefix | Low        | Medium | Recorded explicitly in README.md and brd.md as an observed, unresolved naming collision, so a reader is warned rather than silently misled.                                                                          |
| Deploying this plan's sole PR before `vercel-function-cost-reduction` lands compounds that plan's cost defect                                             | Medium     | Medium | Phase 0's precondition check reads `apps/ayokoding-www/.next/prerender-manifest.json`'s route count before the final deploy; the check is re-run at closeout, not only once at plan start.                           |
| The cohort-2 build-your-own trio stalls the whole plan if either sibling plan (05/06) is delayed                                                          | Medium     | Medium | Cohort 1 (5 courses) has zero external blockers beyond the four already-discussed plans and can complete independently; only the trio's own sub-phases wait on 05/06, so most of this plan's value ships regardless. |
