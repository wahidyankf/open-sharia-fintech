# Delivery Checklist — Course Authoring: Platform & Concurrency Languages

This checklist authors **14 course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: plan04's **Band 3 — Mobile & desktop
platforms** (10 bodies) and **Band 4 — Concurrency languages** (4 bodies), merged into one plan.

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to the
> manifest-growth plan (`ayokoding-learning-path-12-careers-se-manifests` — the successor to
> plan04's original, since-renamed/split `ayokoding-learning-path-05-manifests` name). This plan's
> only outbound artefact is the **band-completion signal** prepared during authoring and delivered with
> the terminal archival PR. See
> [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else) and
> [tech-docs §The manifest ownership invariant](./tech-docs.md#the-manifest-ownership-invariant-binding).
>
> **Cross-plan source of truth** — the `syllabus/` detail layer lives in
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> Every course body is authored **from** its `syllabus/courses/<course-id>.md` spec. **Never copy
> those files into this plan** — a copy forks the source of truth for 122 course specs.
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`. **This plan contains
> no `[HUMAN]` step.**
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). A gate in a phase named as a
> delivery boundary in the [`### Delivery Boundaries`](#delivery-boundaries) table additionally covers
> **integration** (draft PR opened, 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www`
> deployed); a gate in an **intermediate** phase instead confirms the work is committed to its
> delivery unit's branch with nothing pushed for review yet.
>
> **Executor environment note — RTK-wrapped commands emit an empty-output marker, not true
> emptiness** (inherited verbatim from plan04's own note; see `CLAUDE.md` §RTK): `git diff` appends a
> three-line trailer whenever the result is non-empty, so `| wc -l` prints `N + 3` and `| grep -c .`
> prints `N + 1` for `N` changed paths, and in the clean state the two forms **diverge** (`grep -c .`
> reads `0`; `wc -l` reads `1`). **Every `git diff --name-only …` clause in this plan asserts `0`**,
> and for that assertion the sanctioned form is **`| grep -c .`**. Never use an `ls`-based emptiness
> assertion.

## One-PR delivery contract (binding, 2026-08-01)

This 14-course plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
review cycle, merge, deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the PR-Review Maker→Fixer Cycle, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. This contract supersedes every older
cohort or delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/` path below
is this plan's only worktree; no per-course, cohort, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`

This path is the one and only worktree for the entire plan. Provision it once from current
`origin/main`, create the persistent `final-delivery` branch after Phase 0, and use neither
per-course/cohort/stage worktrees nor per-phase branches. Remove it only after the final PR merges.

## Delivery Mode: worktree-to-pr

This plan has one delivery unit: all change-producing work is committed on the persistent
`final-delivery` branch in the declared worktree. Phases before 7 must not push, open
a PR, run PR review, merge, deploy, or record an in-repository merge SHA. Phase 7 first
commits the archival move and index updates, then opens the sole draft PR, runs the three-cycle
PR-Review Maker→Fixer Cycle plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Depends-on

| Relation        | Plan (full folder name)                                                                                                      | Nature                                                                                                                                                                                        |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **blockedBy**   | `ayokoding-learning-path-01-url-restructure`                                                                                 | Hard, transitive via 04. Populated flat `<COURSES>` bucket + `<COURSES>_index.md`.                                                                                                            |
| **blockedBy**   | `ayokoding-learning-path-02-schema-and-prerequisite-dag`                                                                     | Hard, transitive via 04. `syllabus/` specs + the `prerequisites` frontmatter contract.                                                                                                        |
| **blockedBy**   | `ayokoding-learning-path-04-course-authoring`                                                                                | Hard. Its Phase 0 baseline + populated `<COURSES>` namespace — not Band 2 specifically.                                                                                                       |
| **blockedBy**   | `vercel-function-cost-reduction`                                                                                             | Hard, new. Root layout + middleware fix landed against the same `apps/ayokoding-www` app/route tree.                                                                                          |
| **blocks**      | [`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md) | Needs this plan's band-completion signals to grow the three `software-engineer`-role manifests.                                                                                               |
| **blocks**      | `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`                                                         | Needs `just-enough-go` (Band 4) as `build-your-own-raft`'s declared prerequisite (verified against plan04's own catalog row and independently confirmed by that plan's own dependency table). |
| **independent** | Every other new sibling splitting plan04's remaining scope                                                                   | No shared file, no shared prerequisite edge. Bands are mutually content-independent per plan04's own finding.                                                                                 |

**Start precondition (hard gate, checked in Phase 0)**: `ayokoding-learning-path-01-url-restructure`,
`ayokoding-learning-path-02-schema-and-prerequisite-dag`, and `vercel-function-cost-reduction` are all
merged to `origin/main`; `ayokoding-learning-path-04-course-authoring`'s Phase 0 baseline has been
established (toolchain converged, both its own blocking plans verified merged, its `<COURSES>`
namespace populated). This plan does not start on a promise.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phase 0** is a single serial baseline.
- **Phase 1 (Band 3, 10 bodies)** — author and commit bodies serially on the persistent
  `final-delivery` branch. Each `just-enough-<language>` primer precedes or accompanies its paired
  platform course, because the platform course's `_index.md` declares that prerequisite.
- **Phase 2 (Band 4, 4 bodies)** — author and commit on the same branch: `just-enough-go` before or
  alongside `csp-style-concurrency`, and `just-enough-elixir` before or alongside
  `actor-model-concurrency`.
- **Phases 3–7 (finalization)** are serial.
- **Cleanup is the terminal node** (Phase 7's archival), depending on every delivery node above so it
  can never remove the worktree or branch while an earlier node's work is still in flight.

Phase 1 and Phase 2 are content-independent but serialize their commits on the one persistent branch.
No authoring phase opens a review or delivery unit; Phase 7 is the sole review boundary.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (path-landing anchors — **read-only here**)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/` (**never written here**)
- `<MANIFESTS>` = `<FEAT>manifests/` (**never written here** — manifest-growth-plan property; read-only reference only)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` (cross-plan authoring source of truth — **never copied**)

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–6      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 7        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Enter/provision the worktree and install dependencies: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Provisioned the sole declared worktree from `origin/main` at `278bbb6c8`; `npm install` exited 0.

- [x] [AI] Converge the toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: `npm run doctor -- --fix` exited 0 with no output or unresolved drift.

- [x] [AI] **Verify `ayokoding-learning-path-01-url-restructure` merged** — command (single line):
      `test -d apps/ayokoding-www/content/en/learn/courses && test -f apps/ayokoding-www/content/en/learn/courses/_index.md`
      — acceptance: both exit 0.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The populated courses namespace and its `_index.md` both exist; the prerequisite command exited 0.

- [x] [AI] **Verify `ayokoding-learning-path-02-schema-and-prerequisite-dag` merged** — command:
      `test -d plans/done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses`
      — acceptance: exits 0.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The authoritative syllabus course-spec directory exists; the prerequisite command exited 0.

- [x] [AI] **Verify `ayokoding-learning-path-04-course-authoring`'s Phase 0 baseline is established** —
      command: `test -f plans/done/2026-08-02__ayokoding-learning-path-04-course-authoring/evidence/phase-0-snapshot.txt`
      — acceptance: exits 0. This confirms plan04's own toolchain-convergence and upstream-verification
      baseline exists; this plan does not need Band 2 or any other band of plan04 to have landed —
      only its Phase 0 baseline and its populated `<COURSES>` namespace (already checked above).

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Plan 04's recorded Phase 0 snapshot is present; the prerequisite command exited 0.

- [x] [AI] **Verify `vercel-function-cost-reduction`'s checkable precondition holds** — command
      (single line):
      `test ! -f apps/ayokoding-www/src/app/layout.tsx && test ! -f apps/ayokoding-www/src/middleware.ts`
      — acceptance: both `test` conditions pass (both files absent — `app/layout.tsx` deleted with its
      contents merged into `app/[locale]/layout.tsx`; `src/middleware.ts` deleted). Falsifiable both
      ways: [Repo-grounded] as of this plan's authoring date, `apps/ayokoding-www/src/middleware.ts`
      **still exists**, so this exact command fails today; once
      `vercel-function-cost-reduction` lands, both files are gone and the command passes. Do not
      proceed past this check if it fails — this plan does not start on a promise.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Both dynamic-rendering causes are absent (`src/app/layout.tsx` and `src/middleware.ts`); the checkable precondition exited 0.

- [x] [AI] Establish content baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit`
      — acceptance: both exit 0; record pass state in `evidence/phase-0-snapshot.txt`.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/evidence/phase-0-snapshot.txt`
  - **Notes**: `ayokoding-www:build` and `ayokoding-www:test:unit` exited 0; both results are recorded in the Phase 0 snapshot.

- [x] [AI] **Confirm all fourteen course slugs are absent (no collision)** under `<COURSES>`:

  ```bash
  for s in just-enough-kotlin android-app-development just-enough-swift ios-app-development \
    just-enough-dart hybrid-app-development just-enough-csharp windows-app-development \
    linux-app-development building-production-cli-tools just-enough-go csp-style-concurrency \
    just-enough-elixir actor-model-concurrency; do
    test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS $s"
  done
  ```

  — acceptance: **zero** output lines. Falsifiable both ways:
  `mkdir -p apps/ayokoding-www/content/en/learn/courses/just-enough-kotlin` makes the loop print
  `EXISTS just-enough-kotlin`.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The collision loop produced zero `EXISTS` lines; all 14 target course directories are available.

- [x] [AI] **Create the authored-body slug register** — write the 14 slugs this plan authors, one per
      line, to `evidence/authored-body-slugs.txt`:

  ```bash
  cat > evidence/authored-body-slugs.txt <<'EOF'
  just-enough-kotlin
  android-app-development
  just-enough-swift
  ios-app-development
  just-enough-dart
  hybrid-app-development
  just-enough-csharp
  windows-app-development
  linux-app-development
  building-production-cli-tools
  just-enough-go
  csp-style-concurrency
  just-enough-elixir
  actor-model-concurrency
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **14**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | wc -l` returns **0**.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/evidence/authored-body-slugs.txt`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Created the ordered 14-slug register; line-count and duplicate checks both passed.

- [x] [AI] **Record the authored-body baseline** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **14** today (none authored yet); record in `evidence/phase-0-snapshot.txt`.
      The same command must return **0** at archival (Phase 7).

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/evidence/phase-0-snapshot.txt`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The authored-body absence loop returned 14 and the Phase 0 snapshot records that baseline.

- [x] [AI] Confirm `learnings.md` exists in the plan folder with its H1 — command:
      `test -f learnings.md && head -1 learnings.md` — acceptance: file present and the first line is
      `# Learnings: ayokoding-learning-path-05-course-authoring-platform-and-concurrency`.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: `learnings.md` is present with the required Plan 05 H1.

- [x] [AI] **Cross-plan link gate** — confirm every `../ayokoding-learning-path-*` reference in this
      plan's own files resolves:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-05-course-authoring-platform-and-concurrency"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The scoped link validator exited 0 and produced no Plan 05 matching failure line.

- [x] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The manifest-history diff count is 0; the ownership invariant holds.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Both Phase 0 toolchain commands exited 0.

- [x] [AI] All four upstream plans verified: URL-restructure merged (populated `<COURSES>`), schema
      plan merged (`syllabus/courses/` present), plan04's Phase 0 baseline present, and the
      `vercel-function-cost-reduction` checkable precondition (both files absent) holds.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: All four required upstream conditions passed their explicit commands.

- [x] [AI] `ayokoding-www:build` + `test:unit` baselines recorded green.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/evidence/phase-0-snapshot.txt`
  - **Notes**: The recorded build and unit-test baselines are green.

- [x] [AI] All 14 slugs confirmed absent (zero `EXISTS` lines).

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The collision loop printed no existing Plan 05 course directory.

- [x] [AI] `evidence/authored-body-slugs.txt` holds 14 unique slugs; the ABSENT-count baseline of 14
      is recorded in `evidence/phase-0-snapshot.txt`.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/evidence/authored-body-slugs.txt`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/evidence/phase-0-snapshot.txt`
  - **Notes**: The slug register has 14 distinct rows and its recorded absent-count is 14.

- [x] [AI] Cross-plan link gate green.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The scoped validator found no unresolved Plan 05 cross-plan link.

- [x] [AI] Zero manifest files touched.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The manifest-history diff count remains 0.

- [x] [AI] **No PR was opened for this phase and nothing was pushed** —
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: The branch has no remote head and `gh pr list` returned 0; Phase 0 neither pushed nor opened a PR.

> **Pause Safety**: only the toolchain, the four upstream preconditions, and the slug register were
> established — no course body exists yet, nothing is pushed, and no PR exists. Safe to stop
> indefinitely. To resume: re-run the four blocking-plan verification commands and the baseline build.

---

## Phase 1: Band 3 — Mobile & desktop platforms (10 bodies)

> Each course is authored as a full page-bundle into `<COURSES><course-id>/`. These ten bodies are
> content-independent (each writes only its own subtree) and **pipeline concurrently** through review
> (bounded by the cap). Per-course concept/example/prerequisite/capstone detail is **settled** in the
> cross-plan
> [`syllabus/courses/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md).
> **Author each course body from its `<SYLLABUS>courses/<id>.md` spec, not from a fresh judgment call.**

### Course authoring convention (applies to every step in Phases 1 and 2)

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / market facts via `web-researcher` —
   acceptance: no version-pinned claim written `[Unverified]`.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`); the `course-id` slug and the
   prerequisite chain are **settled** — use the exact values declared in
   `<SYLLABUS>courses/<course-id>.md` — acceptance: `test -d "<COURSES><course-id>"`,
   `test -d "<COURSES><course-id>/learning"`, and `test -d "<COURSES><course-id>/drilling"` all exit
   0, and `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per `prd.md`), concept coverage, example/scenario pages + colocated
   `code/` where code-bearing, and `learning/capstone/` — acceptance: the course's own `overview.md`
   states its scope boundary against any sibling course it could be confused with.
4. [AI] **Author drilling track** — `drilling/overview.md` in the fixed five-section order —
   acceptance: all five sections present.
5. [AI] **Run content checkers** — the matching primer or by-example checker,
   `apps-ayokoding-www-facts-checker`, and `apps-ayokoding-www-link-checker` (plus
   `apps-ayokoding-www-general-checker` on `drilling/overview.md`) — acceptance: findings recorded.
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.
8. [AI] **Confirm no manifest file changed in this course's own diff** —
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
9. [AI] **Licensing self-check (programme `A8`)** — grep this course's own worked-example code for the
   CC-BY-SA Stack Overflow hazard:
   `grep -rn 'stackoverflow\.com\|reddit\.com' "<COURSES><course-id>/learning/code/" 2>/dev/null | grep -c .`
   — acceptance: prints `0` (read the printed output; do not chain with `&&`).

Each course below is its own sub-step inside this phase's single delivery unit (Band 3 lands as one
PR at the end of Phase 1, per the grouped-cohort delivery mode above), applying the convention:

- [x] [AI] `just-enough-kotlin` (Primer · Kotlin, `<SYLLABUS>courses/just-enough-kotlin.md`) — Kotlin
      syntax, null-safety, coroutines — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/just-enough-kotlin/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored the 24-file Kotlin primer (78 annotated examples, 26 concepts, capstone, and five-section drilling). Independent primer/facts/link rechecks found zero CRITICAL/HIGH/MEDIUM issues; `ayokoding-www:build` and `npm run lint:md` pass. Kotlin and Gradle executables are unavailable in this worktree, so source-level runner validation is recorded in lieu of local execution.

  **Gherkin (underpins) →** "Each just-enough primer correctly unlocks its paired platform course"

  ```gherkin
  Scenario: Each just-enough primer correctly unlocks its paired platform course
    Given a just-enough-<language> primer and its paired platform course are both authored
    When a reader completes the primer and starts the platform course
    Then the platform course's own _index.md declares the primer's exact course-id as a prerequisite
    And the platform course does not re-teach the language syntax its paired primer already covers
  ```

- [x] [AI] `android-app-development` (By Example · Kotlin, `<SYLLABUS>courses/android-app-development.md`)
      — native Android with the SDK — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-kotlin' "<COURSES>android-app-development/_index.md"` exits 0 (the
      paired-primer prerequisite is declared).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/android-app-development/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored the Android course with 78 source-matched examples, a deterministic offline-first capstone, and six topic-specific katas. Independent final review found no CRITICAL/HIGH issues; its sole MEDIUM blank bullet was removed. `ayokoding-www:build` and Markdown checks pass; the declared Kotlin prerequisite is in frontmatter.

- [x] [AI] `just-enough-swift` (Primer · Swift, `<SYLLABUS>courses/just-enough-swift.md`) — Swift syntax,
      optionals — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/just-enough-swift/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored 78 executable Swift examples, a runnable capstone, and five-section drilling. Independent review reported zero CRITICAL/HIGH/MEDIUM findings; the scoped structural checks and site validation pass.

- [x] [AI] `ios-app-development` (By Example · Swift, `<SYLLABUS>courses/ios-app-development.md`) — native
      iOS with the SDK — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-swift' "<COURSES>ios-app-development/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/ios-app-development/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the iOS course with 78 source-matched examples, capstone, and five-section drilling. The capstone parser, deterministic reset fixture, and UI-test flow validate cleanly; no CRITICAL/HIGH/MEDIUM findings remain.

- [x] [AI] `just-enough-dart` (Primer · Dart, `<SYLLABUS>courses/just-enough-dart.md`) — Dart syntax,
      async, Flutter idioms — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/just-enough-dart/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored 78 source-matched Dart examples, executable capstone, and five-section drilling. Independent review had one MEDIUM wording correction, now fixed; no CRITICAL/HIGH findings remain.

- [x] [AI] `hybrid-app-development` (By Example · Dart, `<SYLLABUS>courses/hybrid-app-development.md`) —
      cross-platform from one Dart codebase — all 9 convention steps complete; checkers clean;
      additionally: `grep -F -q 'just-enough-dart' "<COURSES>hybrid-app-development/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/hybrid-app-development/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and remediated all 78 topic-specific Flutter/Dart examples, capstone, and five-section drilling. Independent final review reported zero CRITICAL/HIGH/MEDIUM findings, including capstone Mermaid and behavioral test coverage.

- [x] [AI] `just-enough-csharp` (Primer · C#, `<SYLLABUS>courses/just-enough-csharp.md`) — C# syntax,
      LINQ, async, .NET — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/just-enough-csharp/**`, `apps/ayokoding-www/content/en/learn/_index.md`, `apps/ayokoding-www/content/en/learn/courses/_index.md`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and remediated the C# primer with 78 runnable, colocated net10 projects and source files, a passing xUnit capstone, and five drills. Final independent review and generated-index validation reported zero CRITICAL/HIGH/MEDIUM findings.

- [x] [AI] `windows-app-development` (By Example · C#, `<SYLLABUS>courses/windows-app-development.md`) —
      native Windows desktop — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-csharp' "<COURSES>windows-app-development/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/windows-app-development/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the Windows course with 78 source-matched C# probes, genuine Windows project/XAML/API artifacts for host-bound topics, a WPF/SQLite capstone with three passing tests, and five-section drilling. Final review found zero CRITICAL/HIGH/MEDIUM findings; the WinUI compiler's macOS boundary is explicitly documented and structurally validated against the actual WinUI scaffold.

- [x] [AI] `linux-app-development` (By Example · Python, `<SYLLABUS>courses/linux-app-development.md`) —
      native Linux desktop, packaging — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-python' "<COURSES>linux-app-development/_index.md"` exits 0 (builds on
      the existing library primer without re-teaching it).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/linux-app-development/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and remediated the Linux course with 78 source-matched examples and synchronized rendered snippets, a live Unix-socket daemon/CLI capstone with a short-path pytest success test, and all five drilling sections. Final independent review reported zero CRITICAL/HIGH/MEDIUM findings; scoped format, Markdown lint, runtime checks, and pytest pass.

  **Gherkin (binds) →** "linux-app-development builds on the existing Python primer without re-teaching it"

  ```gherkin
  Scenario: linux-app-development builds on the existing Python primer without re-teaching it
    Given linux-app-development is authored
    When a reader who already completed just-enough-python starts it
    Then it declares just-enough-python as its prerequisite
    And it teaches native Linux desktop development and packaging without repeating Python syntax
  ```

- [x] [AI] `building-production-cli-tools` (By Example · Go + Rust,
      `<SYLLABUS>courses/building-production-cli-tools.md`) — distributable CLI tools — all 9 convention
      steps complete; checkers clean; additionally both prerequisites are declared:
      `grep -F -q 'just-enough-go' "<COURSES>building-production-cli-tools/_index.md"` exits 0 **and**
      `grep -F -q 'just-enough-rust' "<COURSES>building-production-cli-tools/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/building-production-cli-tools/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the Go/Rust CLI course with 78 source-matched examples, a standalone TTY-aware capstone, successful two-target cross-build verification, and five-section drilling. Final review found zero CRITICAL/HIGH/MEDIUM findings; scoped checks, capstone tests, and Go/Rust compilation pass.

  **Gherkin (binds) →** "building-production-cli-tools builds on both Go and Rust primers"

  ```gherkin
  Scenario: building-production-cli-tools builds on both Go and Rust primers
    Given building-production-cli-tools is authored
    When a reader inspects its prerequisites and its worked examples
    Then it declares both just-enough-go and just-enough-rust as prerequisites
    And its worked examples cover distributable CLI packaging concerns neither primer alone teaches
  ```

**Per-band closing steps** (applied once, in this phase's own gate):

- [x] [AI] Add each landed course's row to
      [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) (already present at
      authoring time; confirm no drift against the settled spec) and its ID to `<COURSES>_index.md`.
- [x] [AI] Record the band-completion signal in this file with all five fields — `GROW_MANIFESTS` is
      the three software-engineer-role manifests:

  ```text
  BAND: Band 3 — Mobile & desktop platforms
  PLAN: ayokoding-learning-path-05-course-authoring-platform-and-concurrency
  LANDED_COURSE_IDS:
  just-enough-kotlin
  android-app-development
  just-enough-swift
  ios-app-development
  just-enough-dart
  hybrid-app-development
  just-enough-csharp
  windows-app-development
  linux-app-development
  building-production-cli-tools
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.yaml
  ```

  **Recorded signal**

  ```text
  BAND: Band 3 — Mobile & desktop platforms
  PLAN: ayokoding-learning-path-05-course-authoring-platform-and-concurrency
  LANDED_COURSE_IDS: just-enough-kotlin, android-app-development, just-enough-swift, ios-app-development, just-enough-dart, hybrid-app-development, just-enough-csharp, windows-app-development, linux-app-development, building-production-cli-tools
  GROW_MANIFESTS: unchanged (zero files touched)
  CATALOG: generated indexes validated; settled catalog rows confirmed
  ```

- [x] [AI] Confirm zero manifest files were touched:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0**.

### Phase 1 Gate

- [x] [AI] All 10 Band-3 bodies exist:
      `for s in just-enough-kotlin android-app-development just-enough-swift ios-app-development just-enough-dart hybrid-app-development just-enough-csharp windows-app-development linux-app-development building-production-cli-tools; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 10 before this phase).
- [x] [AI] Every primer passed `apps-ayokoding-www-primer-checker`; every By-Example body passed
      `apps-ayokoding-www-by-example-checker`; facts + link checkers clean.
- [x] [AI] Every primer/platform pair's prerequisite grep passes (6 pairing checks: kotlin→android,
      swift→ios, dart→hybrid, csharp→windows, plus linux-app-development→just-enough-python and
      building-production-cli-tools→{just-enough-go, just-enough-rust}).
- [x] [AI] `npx nx run ayokoding-www:build` + `npm run lint:md` exit 0.
- [x] [AI] Catalog rows added; band signal recorded with all five fields; zero manifest files touched.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance: no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.
      of this phase's band-completion signal above.

> **Pause Safety**: all four primer/platform pairs plus the two standalone platform courses are live;
> every pairing's prerequisite resolves. Safe to stop. To resume: re-run the section build.

---

## Phase 2: Band 4 — Concurrency languages (4 bodies)

> These four bodies are content-independent and **pipeline concurrently** through review, bounded by
> the cap. Applies the same **Course authoring convention** defined in Phase 1.

- [x] [AI] `just-enough-go` (Primer · Go, `<SYLLABUS>courses/just-enough-go.md`) — Go syntax, goroutines
      — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/just-enough-go/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the Go primer with 78 source-matched, annotated examples, complete rendered source and test blocks, a passing capstone, and five executable before/after drills. Final review reported zero CRITICAL/HIGH/MEDIUM findings.

- [x] [AI] `csp-style-concurrency` (By Example · Go, `<SYLLABUS>courses/csp-style-concurrency.md`) —
      channels, CSP concurrency — all 9 convention steps complete; checkers clean; additionally both
      prerequisites are declared: `grep -F -q 'just-enough-go' "<COURSES>csp-style-concurrency/_index.md"`
      exits 0 **and**
      `grep -F -q 'concurrency-and-parallelism' "<COURSES>csp-style-concurrency/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/csp-style-concurrency/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the CSP course with 78 annotated, source-matched Go examples, controlled race/deadlock diagnostics, a race-tested worker-pool capstone, and five distinct before/after drills. Final review reported zero CRITICAL/HIGH/MEDIUM findings.

- [x] [AI] `just-enough-elixir` (Primer · Elixir, `<SYLLABUS>courses/just-enough-elixir.md`) — Elixir
      syntax, pattern matching — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/just-enough-elixir/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the Elixir primer with 78 annotated, source-matched examples, real IEx/Mix workflows, passing Mix/ExUnit capstones, and five linked runnable drills. Final review reported zero CRITICAL/HIGH/MEDIUM findings; generated Mix artifacts are ignored and were moved to Trash after validation.

- [x] [AI] `actor-model-concurrency` (By Example · Elixir, `<SYLLABUS>courses/actor-model-concurrency.md`)
      — actors, supervision trees — all 9 convention steps complete; checkers clean; additionally both
      prerequisites are declared:
      `grep -F -q 'just-enough-elixir' "<COURSES>actor-model-concurrency/_index.md"` exits 0 **and**
      `grep -F -q 'concurrency-and-parallelism' "<COURSES>actor-model-concurrency/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Gherkin (binds) →** "The two concurrency-paradigm courses each build on the shared foundation, not on each other"

  ```gherkin
  Scenario: The two concurrency-paradigm courses each build on the shared foundation, not on each other
    Given csp-style-concurrency and actor-model-concurrency are both authored
    When a reader compares their prerequisite chains
    Then each declares concurrency-and-parallelism as a shared prerequisite
    And neither declares the other as a prerequisite, since they teach independent paradigms
  ```

  **Implementation notes**
  - **Date**: 2026-08-03
  - **Status**: complete
  - **Files Changed**: `apps/ayokoding-www/content/en/learn/courses/actor-model-concurrency/**`, `plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md`
  - **Notes**: Authored and independently remediated the actor course with 78 annotated, source-matched examples; concrete GenServer, Registry, supervision, dynamic-supervisor, restart-limit, and recovery demonstrations; a registry-addressed Mix/ExUnit capstone; and five linked runnable drills. All examples, drills, capstone tests, scoped Markdown lint, source-render parity, prerequisite checks, and final review passed with zero CRITICAL/HIGH/MEDIUM findings.

**Per-band closing steps**:

- [x] [AI] Add each landed course's row to
      [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) and its ID to
      `<COURSES>_index.md`.
- [x] [AI] Record the band-completion signal:

  ```text
  BAND: Band 4 — Concurrency languages
  PLAN: ayokoding-learning-path-05-course-authoring-platform-and-concurrency
  LANDED_COURSE_IDS:
  just-enough-go
  csp-style-concurrency
  just-enough-elixir
  actor-model-concurrency
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.yaml
  ```

  **Recorded signal**

  ```text
  BAND: Band 4 — Concurrency languages
  PLAN: ayokoding-learning-path-05-course-authoring-platform-and-concurrency
  LANDED_COURSE_IDS: just-enough-go, csp-style-concurrency, just-enough-elixir, actor-model-concurrency
  GROW_MANIFESTS: unchanged (zero files touched)
  CATALOG: generated indexes validated; settled catalog rows confirmed
  ```

- [x] [AI] Confirm zero manifest files were touched:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0**.

  **Gherkin (binds) →** "just-enough-go is ready as build-your-own-raft's declared prerequisite"

  ```gherkin
  Scenario: just-enough-go is ready as build-your-own-raft's declared prerequisite
    Given just-enough-go is authored on the persistent final-delivery branch
    When ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own's build-your-own-raft authoring begins
    Then the just-enough-go course body resolves under the courses bucket
    And the prepared terminal delivery record names just-enough-go among the Band-4 IDs
  ```

### Phase 2 Gate

- [x] [AI] All 4 Band-4 bodies exist:
      `for s in just-enough-go csp-style-concurrency just-enough-elixir actor-model-concurrency; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 4 before this phase).
- [x] [AI] Both By-Example bodies declare `concurrency-and-parallelism` and their paired primer as
      prerequisites (4 pairing checks total).
- [x] [AI] Checkers clean; build + `lint:md` exit 0.
- [x] [AI] Catalog rows added; band signal recorded with all five fields; zero manifest files touched.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance: no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.
      of this phase's band-completion signal above.

> **Pause Safety**: both concurrency-paradigm tracks are live and complete;
> `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`'s `build-your-own-raft`
> prerequisite (`just-enough-go`) is now present. Safe to stop. To resume: re-run the section build.

---

## Phase 3: Section & Authored-Tree Verification

- [ ] [AI] **Verify all 14 authored bodies are present** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: this returned **14** at the Phase-0 baseline,
      and removing any one bundle makes it return 1.
- [ ] [AI] **Verify every authored body declares prerequisites** —
      `while read -r s; do grep -F -q 'prerequisites:' "apps/ayokoding-www/content/en/learn/courses/$s/_index.md" || echo "MISSING $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0** (returns 14 at baseline).
- [ ] [AI] **Verify every authored body has both tracks** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s/learning" && test -d "apps/ayokoding-www/content/en/learn/courses/$s/drilling" || echo "INCOMPLETE $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**.
- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation).
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md`, plus the scoped link gate:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ose-www/content 2>&1 | grep -F "learn/courses/"
  ```

  — acceptance: the first two exit 0 and the `grep` finds **no** line naming a `learn/courses/` path
  belonging to one of these 14 slugs (exits 1; a hit naming another plan's course is out of this
  plan's scope and is not this plan's own failure — re-run scoped to the 14 slugs in
  `evidence/authored-body-slugs.txt` if ambiguity arises).

  **Gherkin (binds) →** "The authored platform-and-concurrency course library builds and validates green"

  ```gherkin
  Scenario: The authored platform-and-concurrency course library builds and validates green
    Given all 14 course bodies this plan authors have landed under the courses bucket
    When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
    Then the build succeeds over the authored tree
    And link, heading-hierarchy, and markdownlint validation report no errors across the 14 course bodies
  ```

- [ ] [AI] **Verify zero manifest files were touched by this entire plan** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
- [ ] [AI] **Verify both band-completion signals are complete** — anchor the count on the field's
      are never counted:
      returns **2** (one genuine signal block per band).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 3 Gate

- [ ] [AI] All three 14-body structural loops (presence, prerequisites, both tracks) return 0.
- [ ] [AI] Affected `typecheck / lint / test:quick / test:unit / specs:behavior:coverage` exit 0.
- [ ] [AI] Build + heading-hierarchy + markdownlint green; the scoped link gate finds no failure among
      this plan's 14 course paths.
- [ ] [AI] Zero manifest files touched across the whole plan's history; both band signals complete
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance: no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.
      green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the authored library passes every automated gate. Safe to stop. To resume: re-run
> the affected quality gates + build.

---

## Phase 4: Manual Content Verification (Playwright MCP)

> **Locale scope**: this plan's content is authored `en`-only — an Indonesian content mirror is
> explicitly deferred. Verify the authored course pages in `en` only.
>
> **Rule-15 exemption (recorded, not silently omitted)**: the three live-site testers are **exempt for
> this plan**, for the same three reasons plan04 recorded — see
> [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded). **The exemption is
> narrow** — the Playwright manual behavioural verification below is mandatory and performed, with
> committed evidence.

- [ ] [AI] Confirm `en` is the content locale for this plan's course bodies — command:
      `test -d apps/ayokoding-www/content/en/learn/courses/just-enough-kotlin && test ! -d apps/ayokoding-www/content/id/learn/courses/just-enough-kotlin`
      — acceptance: exits 0.
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up on port 3101.
- [ ] [AI] **Sample-verify authored course pages** — for a sample of **six** authored courses (each
      primer/platform pair once, plus `linux-app-development`), at breakpoints 375 / 768 / 1280 px,
      via Playwright MCP: `browser_navigate` to `/en/learn/courses/<course-id>`, `browser_resize`,
      then `browser_snapshot` — acceptance: each page renders its overview, learning track, and
      drilling track; `html[lang]` is `en`; `browser_console_messages` reports **zero** errors per
      page per breakpoint.
- [ ] [AI] **Verify prerequisite rendering** — on `android-app-development`, confirm the declared
      `just-enough-kotlin` prerequisite is displayed and its link resolves to that primer's canonical
      page — acceptance: the link target returns 200 and the landed page is `just-enough-kotlin`.
- [ ] [AI] **Verify a drilling track renders** — open `csp-style-concurrency/drilling/overview.md` and
      confirm all five fixed sections are present in the rendered output — acceptance: five section
      headings visible in `browser_snapshot`.
- [ ] [AI] Capture one screenshot per sampled course per breakpoint to
      `evidence/phase-4-<course-id>-en-<breakpoint>px.png` — acceptance:
      `git ls-files -- 'evidence/phase-4-*-en-*px.png' | grep -c .` returns **18** (6 courses × 3
      breakpoints), once the captures are staged or committed.
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per sampled course.
- [ ] [AI] **Record the rule-15 exemption in `learnings.md`** with its three reasons and a pointer to
      the navigation-UI plan that carries the triad.
- [ ] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 4 Gate

- [ ] [AI] Six sampled courses verified across three breakpoints in `en`; zero console errors;
      prerequisite display and drilling-track rendering confirmed.
- [ ] [AI] 18 screenshots present under `evidence/` and referenced in this checklist.
- [ ] [AI] The rule-15 exemption is recorded with reasons; the triad itself is **not** run here.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR opens for this phase** (intermediate): the evidence commits are on the shared
      worktree, this phase's own gate above is green, and nothing is pushed for review yet — the
      closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: the authored library is verified live and defect-clean in `en`. Safe to stop. To
> resume: restart the dev server and re-open the six sampled courses.

---

## Phase 5: Pre-archival Quality & CI Preparation

- [ ] [AI] Run the full affected suite on the persistent final-delivery branch:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npx nx run ayokoding-www:build` — acceptance: all exit 0 before the terminal PR is opened.
- [ ] [AI] Resolve every failure on the persistent final-delivery branch — acceptance: the terminal PR
      needs no follow-up branch or PR.

### Phase 5 Gate

- [ ] [AI] Full affected suite + build green on the persistent final-delivery branch.
- [ ] [AI] Both band signals are prepared without a merge SHA; downstream notification waits for the
      terminal PR merge.
- [ ] [AI] **No PR opens for this phase**: nothing is pushed for review until Phase 7.

> **Pause Safety**: the branch is ready for archival and terminal review. Safe to stop. To resume:
> re-run the affected suite on the persistent final-delivery branch.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable
      surface would catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize to `<placeholder>`
      tokens or discard if the entry cannot be sanitized without losing its meaning.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays in
      `ose-private` only.
- [ ] [AI] Route each surviving entry to exactly one durable home. **Code homes (`apps/`, `libs/`,
      tests) are ALWAYS filed as a separate `plans/backlog/<slug>/` plan and NEVER landed inline.**
- [ ] [AI] If execution genuinely surfaced no generalizable learning, record the explicit escape
      `No generalizable learnings — <reason>` instead of individual entries.
- [ ] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 6 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded with
      reason) or the explicit "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PRs.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR opens for this phase** (intermediate): the `learnings.md` triage is committed on
      the shared closeout branch, this phase's own gate above is green, and nothing is pushed for
      review yet — the closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [ ] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [ ] [AI] Open exactly one draft PR from that branch and run the PR-Review Maker→Fixer Cycle plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [ ] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or the explicit "none"
      escape present; both safety gates applied to every surviving entry).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`;
      the `en` content locale exercised.
- [ ] [AI] Verify the **rule-15 exemption is recorded with reasons** in `learnings.md` and in Phase 4 —
      acceptance: `grep -F -q 'rule-15' learnings.md` exits 0.
- [ ] [AI] **Verify this plan's authored-body assertion** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      returns **0**, and `wc -l < evidence/authored-body-slugs.txt` returns **14** — acceptance: both
      hold. **This plan asserts 14, not 90 and not 127.**
- [ ] [AI] **Verify the ownership invariant held** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0** on this phase's own diff.
- [ ] [AI] **Verify every cross-plan reference still resolves** — re-run the cross-plan link gate:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-05-course-authoring-platform-and-concurrency"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

- [ ] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/ plans/done/YYYY-MM-DD__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`
      using today's **completion** date, not the creation date (the `evidence/` subfolder moves with
      it).
- [ ] [AI] Update `plans/backlog/README.md` and `plans/in-progress/README.md` — remove the plan entry
      from whichever holds it at that point.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan and notify
      `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own` and the manifest-growth
      plan, whose `Depends-on` tables name this plan by folder path — acceptance: no sibling plan's
      link to this folder is left dangling.
- [ ] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-05-course-authoring-platform-and-concurrency to done`.

### Phase 7 Gate

- [ ] [AI] All 14 authored bodies present (the ABSENT loop returns 0, down from the Phase-0 baseline
      of 14); the slug register holds 14 unique lines.
- [ ] [AI] Zero manifest files touched across the plan's entire history.
- [ ] [AI] The cross-plan link gate is green.
- [ ] [AI] Plan folder is under
      `plans/done/YYYY-MM-DD__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`;
      all READMEs updated; archival committed.
- [ ] [AI] The sole archival PR was opened only after the archival commit; its three review cycles and
      CI gates are green, then it is `[AI]`-merged and deployed once.

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits (one
      course bundle per commit is the natural unit here).
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period) —
      e.g. `feat(ayokoding-www): add just-enough-kotlin course body`.
- [ ] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.
- [ ] [AI] Stage only this plan's paths (`git add <explicit paths>`) — **never** `git add -A`; sibling
      split plans are being authored concurrently in the same repo.

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0.
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] `npm run lint:md` exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Commit preexisting fixes separately with appropriate conventional-commit messages.

### Note: plan location at archival time

This plan was promoted from `plans/backlog/` to
`plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/` (no date
prefix on either). The `git mv` in Phase 7 then archives it to
`plans/done/YYYY-MM-DD__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/` using
the completion date.
