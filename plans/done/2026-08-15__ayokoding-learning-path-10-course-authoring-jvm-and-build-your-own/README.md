# Learning Path — Course Authoring: JVM, Advanced Languages & Build-Your-Own Internals

## Delivery amendment — one final PR

All 9 courses remain within one plan branch and one delivery unit. The sole draft PR opens only in
Phase 7, after verification and Knowledge Capture, and carries the archival move, CI,
merge, and deploy. Earlier cohort or delivery-boundary PR wording is superseded.

Author **9 course bodies** — the JVM/advanced-language half of the original Band 6 — into
`apps/ayokoding-www/content/en/learn/courses/`: `just-enough-java`, `enterprise-java-and-the-jvm`,
`lisp`, `just-enough-fsharp`, `type-systems`, `compilers-parsers-and-transpilers`,
`build-your-own-git`, `build-your-own-database`, `build-your-own-raft`.

This plan is a **further split** of
[`ayokoding-learning-path-04-course-authoring`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md)'s
own **Band 6 — "Low-level systems, JVM & languages, internals builds"** (16 bodies), which is itself
too large for the 5–15-course-per-plan sizing rule. Band 6 splits along a natural content seam into
two sibling plans:

- **`ayokoding-learning-path-07-course-authoring-low-level-systems`** — "Low-Level Systems & Native
  Languages" (7 courses: `just-enough-c`, `just-enough-cpp`, `linux-os`, `windows-os`,
  `system-programming`, `just-enough-rust`, `modern-system-programming`). Authored by a different
  agent; **not created by this plan**.
- **This plan** — "JVM, Advanced Languages & Build-Your-Own Internals" (9 courses, listed above).

7 + 9 = 16, matching Band 6's full course count in
[`ayokoding-learning-path-04-course-authoring/tech-docs.md`'s Course Library Catalog](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/tech-docs.md#course-library-catalog)
`[Repo-grounded]`.

It owns no schema, no route, no component, no redirect — and, per the invariant every course-authoring
split plan carries, **no manifest**.

## The manifest ownership invariant (binding — read before anything else)

> **This plan never edits a manifest file.** Every file under
> `apps/ayokoding-www/src/features/course-paths/manifests/` is owned by
> [`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md) —
> the successor to the retired `ayokoding-learning-path-05-manifests`, which composes `courseOrder`
> entries from every course-authoring plan's landed bodies, this one included, into the three
> `software-engineer`-role `careers/` manifests. A step in this plan that creates, appends to,
> reorders, or re-verifies a `.json` manifest is a **boundary violation**, not a
> convenience — see
> [`ayokoding-learning-path-04-course-authoring/README.md`'s own statement of this invariant](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md#the-manifest-ownership-invariant-binding--read-before-anything-else),
> which this plan inherits verbatim.

When this plan's 9 bodies land, it records a **band-completion signal** (see
[Band-completion signal](#band-completion-signal-partial-band-6) below) in its own
[`delivery.md`](./delivery.md), and the manifest plan performs the growth. This plan never asserts the
127-course catalog total — that is the manifest plan's terminal assertion.

## Naming note — a real `-05-`/`-06-` prefix collision (observed, not fixed here)

**Updated — the manifest plan named `ayokoding-learning-path-05-manifests` no longer exists.** It was
retired and split into
[`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md)
(the three `software-engineer`-role manifests this plan's courses feed) and
[`ayokoding-learning-path-13-careers-ai-manifest`](../../backlog/ayokoding-learning-path-13-careers-ai-manifest/README.md)
(the one `ai-engineer` manifest, which does not consume this plan's Band-6 courses), mirroring
`ayokoding-learning-path-04-course-authoring/README.md`'s own corrected naming note. The `-05-`/`-06-`
prefix numerals were freed by that retirement and are now occupied by an unrelated, second numbering
track: `ayokoding-learning-path-05-course-authoring-platform-and-concurrency` and
`ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` — the further split of Band 6
(and, presumably, other oversized bands) out of `ayokoding-learning-path-04-course-authoring`. This is
the collision that genuinely remains: `05` and `06` are each in use by exactly one plan today (these two
course-authoring siblings), not by two plans apiece. This plan does not rename anything — it only
creates its own folder — but the collision is worth a human's attention before all these sibling plans
are promoted to `in-progress/`. `ayokoding-learning-path-05-course-authoring-platform-and-concurrency`
is archived under `plans/done/2026-08-04__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`;
`ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` is archived under
`plans/done/2026-08-15__ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness/`.
Both retain their full five-file plan structure (README/brd/prd/tech-docs/delivery)
`[Repo-grounded — confirmed via directory listing]` — an earlier version of this note treated their
existence as an unconfirmed presumption; both are now directly readable, and reading them surfaced a
real gap this plan had missed (`enterprise-java-and-the-jvm`'s undeclared `software-architecture`
prerequisite — see [tech-docs.md's Course Library Catalog](./tech-docs.md#course-library-catalog) and
the `06` row below).

## Depends-on

| Relation      | Plan (full folder name)                                           | Nature                                                                                                                                                                                                                         |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-09-course-authoring-interview-technique` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-09-course-authoring-interview-technique/README\.md` exits 0. This is this plan's only plan-level start gate.

Course-level citations, already-published course bodies, and repository baseline checks inform implementation but do not create additional plan execution prerequisites.

## Band-completion signal (partial Band 6)

This plan authors **9 of Band 6's 16 courses** — the JVM/advanced-language/build-your-own half. It
therefore records its own **partial band-completion signal**, distinct from the low-level sibling
plan's signal, using the same five-field contract
[`ayokoding-learning-path-04-course-authoring/README.md`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md#band-completion-signal-contract)
defines:

| Field               | Content                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BAND`              | `Band 6 (JVM/advanced-language/build-your-own half) — ayokoding-learning-path-10`                                                                                                                                                                                                                                                                                       |
| `PLAN`              | `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`                                                                                                                                                                                                                                                                                                    |
| `LANDED_COURSE_IDS` | all 9 course IDs this plan authors, one per line, in this plan's own cohort order                                                                                                                                                                                                                                                                                       |
| `GROW_MANIFESTS`    | `<MANIFESTS>careers/interview-ready/software-engineer.json`, `<MANIFESTS>careers/immediately-effective/software-engineer.json`, `<MANIFESTS>careers/fundamentally-strong/software-engineer.json` — **exactly these three**, per this plan's commissioning instructions ("Band 6 routes to exactly these three") and consistent with plan04's own Bands-1–8 routing rule |
| Final delivery      | this plan's terminal archival PR; downstream work consumes the signal only after that PR merges                                                                                                                                                                                                                                                                         |

The manifest plan (`ayokoding-learning-path-12-careers-se-manifests`) needs **both** this plan's signal
and plan 07's signal before Band 6's `courseOrder` entries are complete across all 16 courses — but each signal
is independently actionable only after its owning plan's terminal archival PR merges, since the two
halves share no prerequisite edge (see
[the independence check above](#depends-on)).

## Repository baseline

Repository structure, route behavior, schemas, and already-published course data are verified against current `origin/main` during Phase 0. They are implementation context, not plan prerequisites: this plan's only direct execution prerequisite is `ayokoding-learning-path-09-course-authoring-interview-technique`.

## Delivery Mode: worktree-to-pr

This plan has exactly one dedicated worktree, one persistent final-delivery branch, and one PR.
All authoring, verification, and Knowledge Capture phases commit on that branch without a push, PR, merge, or deployment. In Phase 7, the executor commits the archival move and
any index updates, opens the sole draft PR, completes the secret scan, local quality checks, and PR quality-gate verification and CI gates,
marks it ready, and performs the normal AI merge/deploy after the hardened preconditions hold.
No per-course, cohort, stage, or phase worktree/branch/PR is permitted.

## Cohort grouping and reasoning

9 courses is small enough for a single five-course cohort plus a four-course cohort, inheriting the
sequential five-course delivery cadence
[`ayokoding-learning-path-04-course-authoring`'s 2026-07-31 execution amendment](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/delivery.md#delivery-mode-worktree-to-pr)
established for its own remaining bodies:

- **Cohort 1 (5 courses)**: `just-enough-java`, `enterprise-java-and-the-jvm`, `lisp`,
  `just-enough-fsharp`, `type-systems` — the two Primer/By-Example JVM/Lisp pairs plus the
  type-systems course. Per the corrected
  [Course Library Catalog](./tech-docs.md#course-library-catalog), every prerequisite this cohort's
  courses declare — except one — already exists on disk today: `just-enough-java` →
  `object-oriented-programming-essentials`; `lisp` → `functional-programming`,
  `programming-paradigms`; `just-enough-fsharp` → `functional-programming`,
  `object-oriented-programming-essentials`; `type-systems` → `functional-programming`,
  `programming-paradigms`, `just-enough-typescript` (**not** `just-enough-fsharp` — an earlier version
  of this catalog had that backwards). The one genuine external blocker inside this cohort is
  `enterprise-java-and-the-jvm`'s second prerequisite, `software-architecture` (owned by plan `06`, not
  yet on disk) — gated by the hard-gate precondition immediately before this course's own sub-phase in
  [delivery.md's Phase 1](./delivery.md#phase-1-cohort-1--5-bodies-java-lisp-f-type-systems), not
  silently assumed satisfied.
- **Cohort 2 (4 courses)**: `compilers-parsers-and-transpilers`, `build-your-own-git`,
  `build-your-own-database`, `build-your-own-raft` — grouped together because the cohort's last three
  members are exactly the `build-your-own-*` trio, and `compilers-parsers-and-transpilers` is the
  smallest remaining course to round the cohort to four once the trio anchors it. **The trio is
  authored last within this plan, and last within cohort 2**, per this plan's commissioning
  instruction to defer the courses carrying external prerequisites as late as possible — giving the
  sibling plans (`04` for `build-your-own-database`'s Band-1 body, `05`/`06` for
  `build-your-own-raft`'s Band-4/5 bodies) maximum time to land before their bodies are needed.
  `compilers-parsers-and-transpilers` itself needs `just-enough-fsharp` and `type-systems` (both cohort
  1, already merged by the time cohort 2 starts) and the already-shipped
  `computer-science-foundations` (not `data-structures-and-algorithms-essentials` — corrected per the
  [Course Library Catalog](./tech-docs.md#course-library-catalog)), so it carries no additional
  external blocker.

This is a **judgment call** `[Judgment call]` on the cohort split — the task's own instruction offered
this exact 5+4 grouping as one reasonable option among "or your own sensible grouping"; this plan
adopts it as stated rather than inventing an alternative, since it already satisfies every stated
constraint (five-course cadence, build-your-own-last).

## Rule-15 three-tester retest — exemption recorded

**Exempt, with reasons stated**, for the same reasons
[`ayokoding-learning-path-04-course-authoring`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md#rule-15-three-tester-retest--exemption-recorded)
records and this plan inherits verbatim:

1. **It ships no screen and no component.** Every artefact is a markdown page bundle under
   `apps/ayokoding-www/content/en/learn/courses/`. The screens that render those pages are owned by
   `ayokoding-learning-path-03-navigation-ui` (already done), which carried the mandatory retest.
2. **Its output surface is already covered by dedicated checkers** —
   `apps-ayokoding-www-{by-example,primer}-checker` (this plan's 9 courses use only these two formats;
   see [tech-docs.md's Course Library Catalog](./tech-docs.md#course-library-catalog)),
   `apps-ayokoding-www-facts-checker`, and `apps-ayokoding-www-link-checker`.
3. **The retest would test the other plan's surface**, producing findings this plan cannot act on.

This is an exemption, not an omission: manual behavioural verification via Playwright MCP is **still
mandatory and still performed** (see [delivery.md](./delivery.md) Phase 4) — a sample of this plan's 9
authored pages is opened at all three breakpoints in the `en` content locale, with committed screenshot
evidence. Only the three-tester triad is waived.

## Locale scope

This plan's content is authored **`en`-only**, per the source plan's Business-Scope Non-Goals (an
Indonesian mirror is explicitly deferred, not omitted). Every manual-verification step exercises `en`
and states the deferral inline.

## Navigation

- [Business Requirements (brd.md)](./brd.md) — WHY these 9 bodies exist, who they serve, the business
  risks of the plan's dependency-heavy position, and what "done" means in business terms.
- [Product Requirements (prd.md)](./prd.md) — personas, user stories, the Gherkin acceptance criteria
  this plan owns, and product scope.
- [Technical Docs (tech-docs.md)](./tech-docs.md) — the 9-course catalog with concept/example counts
  and syllabus paths, the manifest-ownership diagram, the authoring architecture, and the full
  dependency-verification record.
- [Delivery Checklist (delivery.md)](./delivery.md) — the phased, executable checklist, including
  per-upstream-plan precondition checks in Phase 0.
- [Learnings (learnings.md)](./learnings.md) — knowledge-capture running log.
- **Cross-plan**:
  [`syllabus/` source of truth](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md)
  ·
  [course-authoring baseline plan (04)](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md)
  · [manifest plan (12-careers-se-manifests)](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md)
  · [vercel-function-cost-reduction](../../done/2026-08-02__vercel-function-cost-reduction/README.md)

## Provenance

This plan is one of the further-split sibling plans produced by dividing
`ayokoding-learning-path-04-course-authoring`'s own Band 6 (16 courses, exceeding the 5–15-course
per-plan sizing rule) along a natural low-level/JVM content seam. It shares its `syllabus/` source of
truth, its manifest-ownership invariant, and its `worktree-to-pr` delivery mode with every plan in the
`ayokoding-learning-path-*` family.
