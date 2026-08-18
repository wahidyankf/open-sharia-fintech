# Delivery Checklist — Course Authoring: JVM, Advanced Languages & Build-Your-Own Internals

This checklist authors **9 course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: `just-enough-java`,
`enterprise-java-and-the-jvm`, `lisp`, `just-enough-fsharp`, `type-systems`,
`compilers-parsers-and-transpilers`, `build-your-own-git`, `build-your-own-database`,
`build-your-own-raft` — the JVM/advanced-language/build-your-own half of
`ayokoding-learning-path-04-course-authoring`'s Band 6.

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to
> [`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md)
> (successor to the retired `ayokoding-learning-path-05-manifests`). This
> plan's only outbound artefact is the **partial band-completion signal** recorded at the end of
> Phase 2. See [README.md §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else)
> and [tech-docs.md §The manifest ownership invariant](./tech-docs.md#the-manifest-ownership-invariant-binding).
>
> **Cross-plan source of truth** — the shared `syllabus/` detail layer lives in
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> Every course body is authored **from** its `syllabus/courses/<course-id>.md` spec. **Never copy**
> those files into this plan.
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`. **This plan contains
> no `[HUMAN]` step.**
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note. A gate in a phase named as a delivery boundary in the
> [`### Delivery Boundaries`](#delivery-boundaries) table additionally covers **integration** (draft
> PR opened, secret scan, local quality checks, and PR quality-gate verification, CI green, `[AI]` merge, `ayokoding-www` deployed); a gate in an
> **intermediate** phase confirms the work is committed to its delivery unit's branch with nothing
> pushed for review yet.
>
> **Executor environment note (RTK)** — this repo routes `git` through RTK via a Claude Code hook.
> For a **non-empty** `git diff --name-only`, `| grep -c .` reads the true changed-path count; for the
> **clean** state, `| grep -c .` reads `0` while `| wc -l` reads `1` (RTK's empty-output marker is a
> lone newline, not true zero-byte emptiness). **Every zero-count assertion in this plan therefore
> uses `| grep -c .`, never `| wc -l`.** See
> [`ayokoding-learning-path-04-course-authoring/delivery.md`'s fuller RTK note](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/delivery.md)
> (its own intro blockquote, near the top of the file) for the fully-measured detail this plan
> inherits without re-deriving.

## One-PR delivery contract (binding, 2026-08-01)

This 9-course plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
merge, deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. This contract supersedes every older
cohort or delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/` path below is
this plan's only worktree; no per-course, cohort, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own` (or `git worktree add -b worktree/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own worktrees/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

This path is the one and only worktree for the entire plan. Provision it once from current
`origin/main`, create the persistent `final-delivery` branch after Phase 0, and use neither
per-course/cohort/stage worktrees nor per-phase branches. Remove it only after the final PR merges.

> **Worktree Cap conformance note (added when the rule landed):** this plan already declared a
> single, plan-wide worktree before the
> [Worktree Cap](../../../repo-governance/conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)
> and
> [Per-Repository Delivery Mode Restrictions](../../../repo-governance/conventions/structure/plans/per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
> rules landed. Reviewed against both — already compliant, no change required.

## Delivery Mode: worktree-to-pr

**CI scope note**: "CI green"/"CI gates" below mean the PR's own check run
(`pr-quality-gate.yml`) — never `.github/workflows/main-ci.yml`, which is deprecated,
schedule-only, and must not be monitored or gated on.

This plan has one delivery unit: all change-producing work is committed on the persistent
`final-delivery` branch in the declared worktree. Phases before 7 must not push, open
a PR, start an external merge, deploy, or record an in-repository merge SHA. Phase 7 first
commits the archival move and index updates, then opens the sole draft PR, runs the secret scan, local quality checks, and PR quality-gate verification plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Content-only delivery safeguards

This plan produces content only and has exactly one final PR. It has no review-cycle requirement. Before pushing that PR:

- [x] [AI] Inspect the staged diff and confirm it contains no machine-secret value.
- [x] [AI] Use a scoped Conventional Commit (for example, `docs(plans): refresh course-preparation backlog`).
- [x] [AI] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`; acceptance: exits 0 for the affected scope.
- [x] [AI] Push the single branch, then wait for `.github/workflows/pr-quality-gate.yml`; acceptance: the PR quality gate is green before merge.

## Depends-on

| Relation      | Plan (full folder name)                                           | Nature                                                                                                                                                                                                                         |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-09-course-authoring-interview-technique` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-09-course-authoring-interview-technique/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap, matching every sibling
course-authoring plan.

- **Phase 0** is a single serial baseline.
- **Phase 1 (Cohort 1, 5 bodies)** — content-independent bodies that pipeline concurrently through
  review, bounded by the cap. One internal ordering constraint: `enterprise-java-and-the-jvm` declares
  `just-enough-java` a prerequisite — both are inside this same cohort, so ordering is a convenience
  (author `just-enough-java` first, or in the same delivery sequence), not a cross-cohort blocker.
  `enterprise-java-and-the-jvm`'s other prerequisite, `software-architecture`, is external (plan `06`,
  not yet on disk) and is hard-gated immediately before this course's own sub-phase (see Phase 1's
  hard gate below) rather than assumed satisfied. `type-systems` does **not** declare
  `just-enough-fsharp` as a prerequisite — its actual prerequisites (`functional-programming`,
  `programming-paradigms`, `just-enough-typescript`) are all already-shipped, so it carries no ordering
  constraint of its own within this cohort.
- **Phase 2 (Cohort 2, 4 bodies)** — `compilers-parsers-and-transpilers` and `build-your-own-git` have
  no external blocker beyond cohort 1 (already merged) and already-shipped courses; `build-your-own-database`
  re-confirms its Band-1 prerequisite exists (it already does, per Phase 0); `build-your-own-raft`
  additionally re-confirms `just-enough-go` and `distributed-systems` exist before its own sub-phase
  starts. The trio is ordered **last within this cohort**, per the commissioning instruction to defer
  externally-gated courses as late as possible.
- **Phases 3–7 (closeout)** is serial.

**Path constants**:

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/`
- `<MANIFESTS>` = `apps/ayokoding-www/src/features/course-paths/manifests/` (**never written here**)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` (never copied)

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–6      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 7        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_
>
> **Cross-plan precondition (hard, five plans).** Unlike a dependency-light band, this plan has three
> content-prerequisite plans (`01`, `02`, `04`) plus two sibling plans (`05`, `06` — both now exist on
> disk; `05` is archived in terminal PR #133 and its body is not usable until that PR merges, while `06` remains under `plans/backlog/`) gating `enterprise-java-and-the-jvm`'s
> (`06`, `software-architecture`) and `build-your-own-raft`'s (`05` + `06`, `just-enough-go` +
> `distributed-systems`) sub-phases specifically, plus one infrastructure plan
> (`vercel-function-cost-reduction`) gating every deploy.

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/ plans/in-progress/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      `git ls-tree -r --name-only origin/main -- plans/in-progress/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/README.md | grep -c .`
      returns **1** and the same query against `plans/backlog/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/README.md` returns **0**.
      Falsifiable both ways: before the push lands, the first query returns 0 and the second
      returns 1. Execution never runs out of `plans/backlog/` — this push is a mandatory
      precondition, not a courtesy. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).
- [x] [AI] Enter/provision the worktree and install dependencies: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [x] [AI] Converge the toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [x] [AI] **Verify repository baseline: course bucket** — the `<COURSES>` bucket exists and holds its
      `_index.md` — command:
      `test -d apps/ayokoding-www/content/en/learn/courses && test -f apps/ayokoding-www/content/en/learn/courses/_index.md`
      — acceptance: both exit 0. Falsifiable both ways: before the URL-restructure plan merges, the
      first `test -d` exits non-zero.
- [x] [AI] **Verify repository baseline: locate the syllabus root** — command:
      `git ls-files -- 'plans/done/*ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md'`
      — acceptance: prints **exactly one** path (pipe to `grep -c .`, read `1`); record it to
      `evidence/phase-0-snapshot.txt` as `SYLLABUS_ROOT=<path>`.
- [x] [AI] **Verify all 9 syllabus spec files exist** — command:
      `for s in just-enough-java enterprise-java-and-the-jvm lisp just-enough-fsharp type-systems compilers-parsers-and-transpilers build-your-own-git build-your-own-database build-your-own-raft; do test -f "<SYLLABUS_ROOT>/$s.md" || echo "ABSENT $s"; done | grep -c .`
      — acceptance: reads **0**. Falsifiable both ways: renaming one spec file makes the count read 1.
- [x] [AI] **Verify plan `04`'s Band-1 prerequisite body is present** (the already-satisfied edge for
      `build-your-own-database`) — command:
      `test -d apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines`
      — acceptance: exits 0. `[Repo-grounded — confirmed present at plan-authoring time]`.
- [x] [AI] **Record plan `05`/`06`'s not-yet-satisfied state** (informational at Phase 0; the hard gates
      are re-checked immediately before `enterprise-java-and-the-jvm`'s own sub-phase in Phase 1 and
      `build-your-own-raft`'s own sub-phase in Phase 2) — command:
      `for s in just-enough-go distributed-systems software-architecture; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" && echo "PRESENT $s" || echo "ABSENT $s"; done`
      — record the output to `evidence/phase-0-snapshot.txt`. No acceptance gate here — this is a
      baseline snapshot, not a blocker, since `enterprise-java-and-the-jvm` and `build-your-own-raft`
      are each hard-gated immediately before their own sub-phase (see Phase 1 and Phase 2 respectively).
- [x] [AI] **Record the current rendering baseline signal** — command:
      `test -f apps/ayokoding-www/.next/prerender-manifest.json && jq '.routes | length' apps/ayokoding-www/.next/prerender-manifest.json || echo "no build artifact yet — run npm exec nx run ayokoding-www:build first"`
      — record the printed value to `evidence/phase-0-snapshot.txt`. This is re-checked (not merely
      recorded) immediately before every delivery-boundary deploy step (see Delivery-Boundary
      Integration Protocol step 5 above).
- [x] [AI] Establish content baselines: `npm exec nx run ayokoding-www:build` and
      `npm exec nx run ayokoding-www:test:unit` — acceptance: both exit 0; record pass state in
      `evidence/phase-0-snapshot.txt`.
- [x] [AI] **Confirm all 9 slugs are absent (no collision)** — command:
      `for s in just-enough-java enterprise-java-and-the-jvm lisp just-enough-fsharp type-systems compilers-parsers-and-transpilers build-your-own-git build-your-own-database build-your-own-raft; do test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS $s"; done | grep -c .`
      — acceptance: reads **0**. Falsifiable both ways: `mkdir -p apps/ayokoding-www/content/en/learn/courses/lisp` makes the loop print `EXISTS lisp`.
- [x] [AI] **Create the authored-body slug register** — write the 9 slugs to
      `evidence/authored-body-slugs.txt`, one per line, in cohort order:

  ```bash
  cat > evidence/authored-body-slugs.txt <<'EOF'
  just-enough-java
  enterprise-java-and-the-jvm
  lisp
  just-enough-fsharp
  type-systems
  compilers-parsers-and-transpilers
  build-your-own-git
  build-your-own-database
  build-your-own-raft
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **9**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | grep -c .` returns **0** (no duplicate).

- [x] [AI] **Record the authored-body baseline** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | grep -c .`
      — acceptance: returns **9** today (none authored yet), recorded in
      `evidence/phase-0-snapshot.txt`. Must return **0** at archival (Phase 7).
- [x] [AI] Confirm `learnings.md` exists in the plan folder with its H1 — command:
      `test -f learnings.md && head -1 learnings.md` — acceptance: file present and first line is
      `# Learnings: ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`.
- [x] [AI] **Cross-plan link gate** — confirm every reference in this plan's own files resolves:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

- [x] [AI] **Confirm no manifest file changed in this phase** — command:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [x] [AI] Plans `01` and `02` verified merged; all 9 syllabus spec files confirmed present;
      `SYLLABUS_ROOT` recorded.
- [x] [AI] Plan `04`'s Band-1 body (`database-internals-and-storage-engines`) confirmed present.
- [x] [AI] Plan `05`/`06`'s current state recorded (informational; not a Phase-0 blocker).
- [x] [AI] Vercel cost-reduction route-count signal recorded.
- [x] [AI] `ayokoding-www:build` + `test:unit` baselines recorded green.
- [x] [AI] All 9 slugs confirmed absent (zero `EXISTS` lines).
- [x] [AI] `evidence/authored-body-slugs.txt` holds 9 unique slugs; ABSENT-count baseline of 9 recorded.
- [x] [AI] Cross-plan link gate green.
- [x] [AI] Zero manifest files touched.
- [x] [AI] No PR opened, nothing pushed for this phase:
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

> **Pause Safety**: only the toolchain, the five upstream preconditions, and the slug register are
> established — no course body exists yet, nothing is pushed, no PR exists. Safe to stop indefinitely.
> To resume: re-run the precondition checks and the baseline build.

---

## Phase 1: Cohort 1 — 5 bodies (Java, Lisp, F#, type systems)

> Each course is authored as a full page bundle into `<COURSES><course-id>/`, from its
> `<SYLLABUS_ROOT>/<course-id>.md` spec, following the NEW-course authoring convention
> [`ayokoding-learning-path-04-course-authoring/delivery.md`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/delivery.md#new-course-authoring-convention-applies-to-every-authoring-step-in-phases-1-and-311)
> defines (V pre-verify → skeleton → learning track → drilling track → content checkers → fixers →
> re-verify → manifest-isolation self-check → licensing self-check). This plan applies the same
> nine-step convention to every one of its 9 courses without restating it verbatim per course.

- [x] [AI] `just-enough-java` (Primer · Java) — convention complete; checkers clean; declares
      `object-oriented-programming-essentials` as its prerequisite (already-shipped) — acceptance:
      `grep -F -q 'object-oriented-programming-essentials' "apps/ayokoding-www/content/en/learn/courses/just-enough-java/_index.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [x] [AI] **Hard gate — re-confirm `enterprise-java-and-the-jvm`'s external prerequisite body
      `software-architecture` is present** (immediately before its own sub-phase; STOP and surface to
      the user if absent, rather than authoring a dangling prerequisite edge, mirroring the
      `build-your-own-raft` gate in Phase 2) — command:
      `test -d apps/ayokoding-www/content/en/learn/courses/software-architecture`
      — acceptance: exits 0. If it returns non-zero, this checklist item is **not** ticked and
      execution pauses here until plan `06` merges the missing body.
- [x] [AI] `enterprise-java-and-the-jvm` (By Example · Java) — convention complete; checkers clean;
      declares `just-enough-java` and `software-architecture` as its prerequisites — acceptance:
      `for p in just-enough-java software-architecture; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/enterprise-java-and-the-jvm/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.

  **Gherkin (binds) →** "enterprise-java-and-the-jvm declares just-enough-java and software-architecture as its prerequisites"

  ```gherkin
  Scenario: enterprise-java-and-the-jvm declares just-enough-java and software-architecture as its prerequisites
    Given the just-enough-java course is authored and software-architecture is confirmed present
    When a reader opens enterprise-java-and-the-jvm's frontmatter
    Then it declares just-enough-java in its prerequisites list
    And it also declares software-architecture in its prerequisites list
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] `lisp` (By Example · Scheme + Clojure) — convention complete; checkers clean; declares the
      already-shipped `functional-programming` and `programming-paradigms` as its prerequisites (not an
      entry point) — acceptance:
      `for p in functional-programming programming-paradigms; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/lisp/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] `just-enough-fsharp` (Primer · F#) — convention complete; checkers clean; declares the
      already-shipped `functional-programming` and `object-oriented-programming-essentials` as its
      prerequisites (not an entry point) — acceptance:
      `for p in functional-programming object-oriented-programming-essentials; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/just-enough-fsharp/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [x] [AI] `type-systems` (By Example · OCaml + Haskell + F#) — convention complete; checkers clean;
      declares the already-shipped `functional-programming`, `programming-paradigms`, and
      `just-enough-typescript` as prerequisites (**not** `just-enough-fsharp` — corrected) —
      acceptance:
      `for p in functional-programming programming-paradigms just-enough-typescript; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/type-systems/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.

  **Gherkin (binds) →** "type-systems declares functional-programming, programming-paradigms, and just-enough-typescript as its prerequisites"

  ```gherkin
  Scenario: type-systems declares functional-programming, programming-paradigms, and just-enough-typescript as its prerequisites
    Given the type-systems course is authored
    When a reader opens type-systems's frontmatter
    Then it declares the already-shipped functional-programming course in its prerequisites list
    And it also declares the already-shipped programming-paradigms and just-enough-typescript courses
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] **Confirm no manifest file changed in this cohort's own diff** — command:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.
- [x] [AI] **Licensing self-check (programme A8)** on all 5 bodies' worked-example code:
      `for s in just-enough-java enterprise-java-and-the-jvm lisp just-enough-fsharp type-systems; do grep -rln 'stackoverflow\.com\|reddit\.com' "apps/ayokoding-www/content/en/learn/courses/$s/learning/code/" 2>/dev/null; done | grep -c .`
      — acceptance: prints `0`.

### Local Quality Gates (Before Push)

- [x] [AI] `npm exec nx affected -t typecheck` exits 0.
- [x] [AI] `npm exec nx affected -t lint` exits 0.
- [x] [AI] `npm exec nx affected -t test:quick test:unit` exits 0.
- [x] [AI] `specs:coverage` / `specs:behavior:coverage` is intentionally **not** run here — this is a
      content-authoring cohort, exempt per `prd.md`'s stated content-exemption (no route/component/schema
      change in this cohort's diff); stated here explicitly rather than by silent omission.
- [x] [AI] Fix ALL failures found — including preexisting issues not caused by this plan's own changes
      (Root Cause Orientation) — committing any preexisting fixes separately from this cohort's own
      thematic commits.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Do not defer or mention-and-skip existing issues.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] All 5 Cohort-1 bodies exist:
      `for s in just-enough-java enterprise-java-and-the-jvm lisp just-enough-fsharp type-systems; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | grep -c .`
      returns **0**.
- [x] [AI] `just-enough-java` declares `object-oriented-programming-essentials`; `enterprise-java-and-the-jvm`
      declares both `just-enough-java` and `software-architecture`; `lisp` declares both
      `functional-programming` and `programming-paradigms`; `just-enough-fsharp` declares both
      `functional-programming` and `object-oriented-programming-essentials`; `type-systems` declares
      `functional-programming`, `programming-paradigms`, and `just-enough-typescript` (not
      `just-enough-fsharp`).
- [x] [AI] `software-architecture`'s hard gate (immediately before `enterprise-java-and-the-jvm`'s own
      sub-phase) passed with a zero-exit `test -d`, confirming no dangling prerequisite edge shipped.
- [x] [AI] Checkers clean across all 5; `npm exec nx run ayokoding-www:build` and `npm run lint:md` exit 0;
      the Local Quality Gates section above (`typecheck`, `lint`, `test:quick test:unit`) all pass.
- [x] [AI] Zero manifest files touched.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.

> **Pause Safety**: the JVM/Lisp/functional-typing quintet is committed on `final-delivery`; every internal prerequisite pair
> (Java, F#) resolves within this same cohort, and `enterprise-java-and-the-jvm`'s external
> prerequisite (`software-architecture`, plan `06`) was hard-gated present before authoring — no
> dangling edge. Safe to stop. To resume: re-run the section build.

---

## Phase 2: Cohort 2 — 4 bodies (compilers, build-your-own trio)

> The `build-your-own-*` trio is authored **last within this cohort**, per the commissioning
> instruction to defer externally-gated courses as late as possible, giving plans `05`/`06` the maximum
> window to land.

- [x] [AI] `compilers-parsers-and-transpilers` (By Example · F#) — convention complete; checkers clean;
      declares `just-enough-fsharp` and `type-systems` (both cohort 1, already merged) and the
      already-shipped `computer-science-foundations` as prerequisites (**not**
      `data-structures-and-algorithms-essentials` — corrected) — acceptance:
      `for p in just-enough-fsharp type-systems computer-science-foundations; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/compilers-parsers-and-transpilers/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.

  **Gherkin (binds) →** "compilers-parsers-and-transpilers declares its three prerequisites"

  ```gherkin
  Scenario: compilers-parsers-and-transpilers declares its three prerequisites
    Given the compilers-parsers-and-transpilers and type-systems courses are authored
    When a reader opens compilers-parsers-and-transpilers's frontmatter
    Then it declares just-enough-fsharp and type-systems in its prerequisites list
    And it declares the already-shipped computer-science-foundations course
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] `build-your-own-git` (By Example · Python) — convention complete; checkers clean; declares
      `just-enough-python` and the already-shipped `version-control-and-git` as prerequisites —
      acceptance:
      `for p in just-enough-python version-control-and-git; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/build-your-own-git/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.

  **Gherkin (binds) →** "build-your-own-git declares its two prerequisites"

  ```gherkin
  Scenario: build-your-own-git declares its two prerequisites
    Given the build-your-own-git course is authored
    When a reader opens its frontmatter
    Then it declares just-enough-python in its prerequisites list
    And it declares the already-shipped version-control-and-git course
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] **Re-confirm `build-your-own-database`'s prerequisite body is present** (immediately before
      authoring, not only at Phase 0) — command:
      `test -d apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines`
      — acceptance: exits 0.

  **Gherkin (binds) →** "build-your-own-database's prerequisite body is confirmed present before authoring"

  ```gherkin
  Scenario: build-your-own-database's prerequisite body is confirmed present before authoring
    Given database-internals-and-storage-engines already exists under the courses namespace (Band 1, plan04)
    When build-your-own-database's own authoring sub-phase begins
    Then a repo-grounded check confirms the course directory exists before the body is written
    And build-your-own-database's frontmatter declares it as a prerequisite
  ```

- [x] [AI] `build-your-own-database` (By Example · Python) — convention complete; checkers clean;
      declares `database-internals-and-storage-engines` and the already-shipped `sql-essentials` as
      prerequisites (**not** `just-enough-python` — corrected) — acceptance:
      `for p in database-internals-and-storage-engines sql-essentials; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/build-your-own-database/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] **Hard gate — re-confirm `build-your-own-raft`'s two external prerequisite bodies are
      present** (immediately before its own sub-phase; STOP and surface to the user if either is
      absent, rather than authoring a dangling prerequisite edge) — command:

  ```bash
  test "$(gh pr view 136 --repo wahidyankf/ose-public --json state --jq '.state')" = "MERGED"
  for s in just-enough-go distributed-systems; do
    test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"
  done | grep -c .
  ```

  — acceptance: the merge assertion exits **0** and the directory check returns **0**. If either
  fails, this checklist item is **not** ticked and execution pauses here until plan `05` is merged
  and plans `05`/`06` provide the required bodies.

  **Gherkin (binds) →** "build-your-own-raft's two external prerequisite bodies are confirmed present before authoring"

  ```gherkin
  Scenario: build-your-own-raft's two external prerequisite bodies are confirmed present before authoring
    Given just-enough-go and distributed-systems are each declared prerequisites of build-your-own-raft
    When build-your-own-raft's own authoring sub-phase begins
    Then a repo-grounded check confirms both course directories exist under the courses namespace
    And the check blocks authoring until both directories are present
  ```

- [x] [AI] `build-your-own-raft` (By Example · Go) — convention complete; checkers clean; declares
      `just-enough-go` and `distributed-systems` as prerequisites — acceptance:
      `for p in just-enough-go distributed-systems; do grep -F -q "$p" "apps/ayokoding-www/content/en/learn/courses/build-your-own-raft/_index.md" || echo "MISSING $p"; done | grep -c .`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] **Confirm no manifest file changed in this cohort's own diff** — command:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.
- [x] [AI] **Licensing self-check (programme A8)** on all 4 bodies' worked-example code:
      `for s in compilers-parsers-and-transpilers build-your-own-git build-your-own-database build-your-own-raft; do grep -rln 'stackoverflow\.com\|reddit\.com' "apps/ayokoding-www/content/en/learn/courses/$s/learning/code/" 2>/dev/null; done | grep -c .`
      — acceptance: prints `0`.
- [x] [AI] **Record the partial band-completion signal** — append to this file, in a fenced `text`
      block:

  ```text
  BAND: Band 6 (JVM/advanced-language/build-your-own half) — ayokoding-learning-path-10
  PLAN: ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own
  LANDED_COURSE_IDS:
  just-enough-java
  enterprise-java-and-the-jvm
  lisp
  just-enough-fsharp
  type-systems
  compilers-parsers-and-transpilers
  build-your-own-git
  build-your-own-database
  build-your-own-raft
  GROW_MANIFESTS:
  <MANIFESTS>careers/interview-ready/software-engineer.json
  <MANIFESTS>careers/immediately-effective/software-engineer.json
  <MANIFESTS>careers/fundamentally-strong/software-engineer.json
  ```

  — acceptance: all five fields present, `LANDED_COURSE_IDS` names exactly the 9 slugs in
  `evidence/authored-body-slugs.txt`, `GROW_MANIFESTS` names exactly the three software-engineer
  manifests (never the AI-engineer manifest — this plan authors no AI-engineering course).

### Local Quality Gates (Before Push)

- [x] [AI] `npm exec nx affected -t typecheck` exits 0.
- [x] [AI] `npm exec nx affected -t lint` exits 0.
- [x] [AI] `npm exec nx affected -t test:quick test:unit` exits 0.
- [x] [AI] `specs:coverage` / `specs:behavior:coverage` is intentionally **not** run here — this is a
      content-authoring cohort, exempt per `prd.md`'s stated content-exemption (no route/component/schema
      change in this cohort's diff); stated here explicitly rather than by silent omission.
- [x] [AI] Fix ALL failures found — including preexisting issues not caused by this plan's own changes
      (Root Cause Orientation) — committing any preexisting fixes separately from this cohort's own
      thematic commits.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Do not defer or mention-and-skip existing issues.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] All 4 Cohort-2 bodies exist:
      `for s in compilers-parsers-and-transpilers build-your-own-git build-your-own-database build-your-own-raft; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | grep -c .`
      returns **0**.
- [x] [AI] All 4 bodies' declared prerequisites verified present (per each item's own acceptance
      clause above).
- [x] [AI] Checkers clean across all 4; build + `lint:md` exit 0; the Local Quality Gates section
      above (`typecheck`, `lint`, `test:quick test:unit`) all pass.
- [x] [AI] Zero manifest files touched.
- [x] [AI] Partial band-completion signal recorded with its four content fields complete; it becomes
      actionable only after the Phase 7 terminal archival PR merges.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.
- [x] [AI] **Confirm all 9 course bodies now exist** (both cohorts combined):
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | grep -c .`
      returns **0**.

> **Pause Safety**: all 9 course bodies are committed on `final-delivery`; `build-your-own-raft`'s two external prerequisite
> bodies were re-confirmed present immediately before its own authoring, so no dangling edge exists.
> The partial band-completion signal is recorded for the manifest plan to consume. Safe to stop. To
> resume: re-run the section build and re-verify the signal fields.

---

## Phase 3: Final content-correctness sweep

> Intermediate phase — folds into the Phase 7 terminal archival PR (see Delivery Boundaries table).

- [x] [AI] Re-run every content checker across all 9 bodies (`apps-ayokoding-www-primer-checker` for
      the 2 Primers, `apps-ayokoding-www-by-example-checker` for the 7 By-Example bodies,
      `apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`) — acceptance: zero
      CRITICAL/HIGH/MEDIUM findings remain across all 9.
- [x] [AI] Re-run the cross-plan link gate (same command as Phase 0) — acceptance: `grep` finds no
      matching line naming this plan's folder.
- [x] [AI] `npm exec nx run ayokoding-www:build` and `npm run lint:md` — acceptance: both exit 0.
- [x] [AI] Re-run the independence-from-plan-07 check from tech-docs.md — command:
      `for s in just-enough-c just-enough-cpp linux-os windows-os system-programming just-enough-rust modern-system-programming; do grep -rl "$s" apps/ayokoding-www/content/en/learn/courses/{just-enough-java,enterprise-java-and-the-jvm,lisp,just-enough-fsharp,type-systems,compilers-parsers-and-transpilers,build-your-own-git,build-your-own-database,build-your-own-raft}/_index.md 2>/dev/null; done | grep -c .`
      — acceptance: returns **0** (none of this plan's 9 `_index.md` files declares a plan-07 course
      as a prerequisite).

### Phase 3 Gate

- [x] [AI] All checkers clean; build + lint green; cross-plan link gate green; independence check
      returns 0.
- [x] [AI] Nothing pushed for review yet at this intermediate phase (commits remain on
      `final-delivery`).

> **Pause Safety**: all 9 bodies pass every content-correctness check with zero outstanding findings.
> Safe to stop. To resume: re-run the checker sweep.

---

## Phase 4: Manual Behavioral Verification (Playwright MCP)

> Rule-15 three-tester triad exempt (see [README.md](./README.md#rule-15-three-tester-retest--exemption-recorded)).
> A sample of this plan's 9 authored pages is still opened and screenshotted manually, `en` locale only
> (this plan's content is `en`-only by design; the `id` deferral is stated, not silently skipped).

- [x] [AI] Start dev server: `nx dev ayokoding-www`.
- [x] [AI] For a representative sample — `just-enough-java` (Primer), `build-your-own-database`
      (By Example, Band-1-dependent), and `build-your-own-raft` (By Example, cross-plan-dependent) —
      navigate to `/en/learn/courses/<course-id>` at 375px, 768px, and 1280px via `browser_navigate` +
      `browser_resize`.
- [x] [AI] Inspect DOM via `browser_snapshot` — verify `html[lang]` is `en`, prerequisites render, no
      untranslated strings.
- [x] [AI] Check for JS errors via `browser_console_messages` — zero errors per page per breakpoint.
- [x] [AI] Capture one screenshot per page per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-4-<course-id>-en-<breakpoint>px.png` (9 screenshots total: 3 courses × 3
      breakpoints).
- [x] [AI] Document each screenshot inline: `![alt](./evidence/phase-4-<course-id>-en-<breakpoint>px.png)`.

### Phase 4 Gate

- [x] [AI] All 9 screenshots committed under `evidence/`.
- [x] [AI] Zero console errors recorded across all sampled pages/breakpoints.

> **Pause Safety**: manual verification evidence is committed; nothing pushed for review yet at this
> intermediate phase. Safe to stop. To resume: re-open the dev server and re-capture any missing
> screenshot.

---

## Phase 5: Pre-PR CI Readiness Check

- [x] [AI] Run the full applicable quality suite against `final-delivery`; acceptance: all commands
      exit 0. Do not push or open a PR in this phase.

### Phase 5 Gate

- [x] [AI] The full applicable quality suite is green on `final-delivery`.

> **Pause Safety**: both cohorts are verified on `final-delivery`. Safe to stop. To resume: re-run
> the local quality suite.

---

## Phase 6: Knowledge Capture

- [x] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable
      surface would catch this automatically next time; discard the rest with a one-line reason.
- [x] [AI] Apply the secret/sensitivity gate to every surviving entry.
- [x] [AI] Apply the repo-relevance gate to every surviving entry.
- [x] [AI] Route each surviving entry to exactly one durable home (a small non-code edit lands inline;
      larger non-code work or any code-homed learning files a `plans/backlog/` follow-up plan).
- [x] [AI] Record the terminal state of every entry directly in `learnings.md`.
- [x] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same problem or area — fold the learning into
      that brief instead of creating a new file; only create a new `plans/ideas/<slug>.md` when the
      scan confirms no existing brief overlaps (see
      [Integrate Before You Add](../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
      — acceptance: the entry's routing line names either the folded-into brief or confirms the
      overlap scan found nothing.
- [x] [AI] If execution surfaced no generalizable learning, record the explicit escape
      `No generalizable learnings — <one-line reason>` instead.

### Phase 6 Gate

- [x] [AI] Every `learnings.md` entry reached a terminal state or the explicit "none" escape is
      present.
- [x] [AI] No code-homed learning landed inline — every code-routed learning has a corresponding
      `plans/backlog/` folder.

> **Pause Safety**: all learnings are triaged or explicitly discarded. Safe to stop. To resume:
> re-check `learnings.md` for any entry without a terminal-state marker.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [x] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [x] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [x] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [x] [AI] Verify all delivery checklist items above are ticked.
- [x] [AI] Verify all quality gates pass (local + CI).
- [x] [AI] Verify all manual assertions pass with committed evidence in `evidence/`.
- [x] [AI] Verify the `en`-only locale scope was exercised and the `id` deferral stated, not silently
      skipped.
- [x] [AI] Move plan folder from `plans/backlog/` to `plans/done/` via
      `git mv plans/in-progress/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own plans/done/<completion-date>__ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`
      (the `evidence/` subfolder moves with it).
- [x] [AI] Update `plans/in-progress/README.md` — remove this plan's entry.
- [x] [AI] Update `plans/done/README.md` — add this plan's entry with its completion date.
- [x] [AI] Update any other READMEs that reference this plan (sibling plans' Depends-on tables, once
      those plans exist on disk).
- [x] [AI] Push `final-delivery`, open the one terminal archival draft PR, run the secret scan, local quality checks, and PR quality-gate verification,
      `[AI]`-merge, and deploy (after rendering-baseline verification).
- [x] [AI] Commit: `chore(plans): move ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own to done`.
- [x] [AI] Prompt the user before removing this plan's worktree; remove it only on explicit
      confirmation, and only once nothing is uncommitted or unpushed.

### Local Quality Gates (Before Push)

- [x] [AI] `npm exec nx affected -t typecheck` exits 0.
- [x] [AI] `npm exec nx affected -t lint` exits 0.
- [x] [AI] `npm exec nx affected -t test:quick test:unit` exits 0.
- [x] [AI] `specs:coverage` / `specs:behavior:coverage` is intentionally **not** run here — this is a
      content-authoring plan, exempt per `prd.md`'s stated content-exemption (no route/component/schema
      change across this plan's closeout diff); stated here explicitly rather than by silent omission.
- [x] [AI] Fix ALL failures found — including preexisting issues not caused by this plan's own changes
      (Root Cause Orientation) — committing any preexisting fixes separately from this closeout's own
      thematic commits.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Do not defer or mention-and-skip existing issues.

### Phase 7 Gate

- [x] [AI] Plan folder confirmed under `plans/done/`; both `README.md` indexes updated; closeout PR
      merged to `origin/main`.
- [x] [AI] `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < plans/done/*ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/evidence/authored-body-slugs.txt | grep -c .`
      returns **0** — all 9 authored bodies confirmed present on `origin/main` at archival.
- [x] [AI] The Local Quality Gates section above (`typecheck`, `lint`, `test:quick test:unit`) all
      passed before this closeout PR merged.

> **Pause Safety**: the plan is archived, all 9 bodies are live on `origin/main`, and the manifest plan
> has a complete, five-field partial band-completion signal to act on. Nothing further to resume — the
> plan is done.
