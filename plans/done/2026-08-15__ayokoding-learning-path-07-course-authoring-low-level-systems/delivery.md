# Delivery Checklist — Course Authoring: Low-Level Systems & Native Languages

This checklist authors **7 course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: `just-enough-c`, `just-enough-cpp`,
`linux-os`, `windows-os`, `system-programming`, `just-enough-rust`, `modern-system-programming` — the
C-family/OS/Rust half of the original Band 6 split described in [README.md](./README.md) and
[tech-docs.md](./tech-docs.md).

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to
> [`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md).
> This plan's only outbound artefact toward that plan is the **one** band-completion signal recorded
> at the end of Phase 2. See
> [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else).
>
> **Cross-plan source of truth** — every course body is authored **from** its
> `syllabus/courses/<course-id>.md` spec at
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> **Never copy those files into this plan.**
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`. **This plan contains
> no `[HUMAN]` step.**
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note. A gate in a phase named as a delivery boundary in the
> [`### Delivery Boundaries`](#delivery-boundaries) table additionally covers integration (draft PR
> opened, secret scan, local quality checks, and PR quality-gate verification, CI green, `[AI]` merge, `ayokoding-www` deployed); a gate in an
> **intermediate** phase confirms the work is committed to its delivery unit's branch with nothing
> pushed for review yet — see
> [Plans Organization Convention §PRs Open at Delivery Boundaries](../../../repo-governance/conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
>
> **Executor environment note — RTK / `grep -c` sanctioned-zero-assertion rule (inherited, condensed
> from `ayokoding-learning-path-04-course-authoring`'s own delivery.md).** This repo routes `git` (and
> other commands) through RTK via a Claude Code hook (see `CLAUDE.md` §RTK). For a clean `git diff`,
> `| grep -c .` reads **0** and is the sanctioned zero-assertion form used throughout this file; `| wc -l`
> is **never** used for a zero-assertion here, because RTK's own empty-output marker makes it read `1`
> on a clean diff, not `0`. For a non-zero count, interpose an explicit `grep -F …` / `grep -E …` path
> filter rather than trusting a bare `wc -l`. Count files with `git ls-files`, never `ls … | wc -l`
> (`ls` is `eza`-aliased and its OSC-8 hyperlinks corrupt anything piped further) and never a **bare**
> `find` (rewritten by the hook to `rtk find`, which reformats the result and drops unknown flags) —
> use a **piped** `find … | wc -l` when a real count is needed, or `git ls-files` when the search is
> pathspec-shaped.

## One-PR delivery contract (binding, 2026-08-01)

This 7-course plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
merge, deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. This contract supersedes every older
cohort or delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-07-course-authoring-low-level-systems/` path below is this
plan's only worktree; no per-course, cohort, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-07-course-authoring-low-level-systems/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-07-course-authoring-low-level-systems` (or `git worktree add -b worktree/ayokoding-learning-path-07-course-authoring-low-level-systems worktrees/ayokoding-learning-path-07-course-authoring-low-level-systems origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

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

| Relation      | Plan (full folder name)                                                   | Nature                                                                                                                                                                                                                         |
| ------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phase 0** is a single serial baseline.
- **Phase 1 (Cohort A, 5 courses)** — authored **one course at a time** on the persistent
  final-delivery branch in DAG order
  (`just-enough-c` → `just-enough-cpp`/`linux-os`/`windows-os` in any order → `system-programming`
  last, since it needs `linux-os`).
- **Phase 2 (Cohort B, 2 courses)** — authored one at a time (`just-enough-rust` →
  `modern-system-programming`, since the latter needs the former), on the same branch.
- **Phases 3–6 (verification, manual test, CI preparation, knowledge capture)** are serial on the
  same branch and fold into Phase 7's sole PR.
- **Phase 7 (archival)** is the terminal serial node, depending on every prior phase.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at
  `/en/learn/courses/<course-id>`)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/` (**never written here**)
- `<MANIFESTS>` = `<FEAT>manifests/` (**never written here**)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`
  (cross-plan authoring source of truth — **never copied**)
- `<PLAN04>` = the resolved path to `ayokoding-learning-path-04-course-authoring`'s folder at
  execution time (`plans/in-progress/...` or, once archived, `plans/done/YYYY-MM-DD__...`) — resolved
  once in Phase 0 and recorded to `evidence/phase-0-snapshot.txt`.

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–6      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 7        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-07-course-authoring-low-level-systems/ plans/in-progress/ayokoding-learning-path-07-course-authoring-low-level-systems/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      **Protected-main exception (user approved 2026-08-15):** `origin/main` rejects direct pushes,
      while this plan's binding one-PR contract forbids a promotion-only PR. The promotion commit
      (`d2c1d87a4`) is therefore the first commit on this plan's declared worktree branch and is
      included in the sole terminal PR. Before Phase 1, confirm the promoted path is present in
      `HEAD` and absent from the backlog with `git ls-tree -r --name-only HEAD --
plans/in-progress/ayokoding-learning-path-07-course-authoring-low-level-systems/README.md |
grep -c .` (**1**) and the same query against `plans/backlog/.../README.md` (**0**).
      Execution never runs out of `plans/backlog/`; this exception changes only the unavailable
      direct-push mechanism, not the promotion or the one-PR delivery boundary. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).
- [x] [AI] Enter/provision the worktree and install dependencies: `npm install` — acceptance: exits
      0, `node_modules/` synchronized.
- [x] [AI] Converge the toolchain: `npm run doctor -- --fix` — acceptance: exits 0 with no unresolved
      drift.
- [x] [AI] **Resolve `<PLAN04>` and verify Band 6 is trimmed from its own scope** — command (run as
      one call):

  ```bash
  git ls-files -- 'plans/*/*ayokoding-learning-path-04-course-authoring/evidence/authored-body-slugs.txt'
  ```

  — acceptance: prints **exactly one** path (pipe to `grep -c .`, read **1**); record it as
  `<PLAN04_SLUGS>` in `evidence/phase-0-snapshot.txt`. Then:

  ```bash
  grep -cE '^(just-enough-c|just-enough-cpp|linux-os|windows-os|system-programming|just-enough-rust|modern-system-programming)$' "<PLAN04_SLUGS>"
  ```

  — acceptance: returns **0** (none of this plan's 7 slugs remain in plan04's own claimed list — the
  trim landed). This is the **load-bearing check** for this precondition. Falsifiable both ways:
  today (2026-08-01, before the trim lands), this reads **7** — verified live against plan04's
  current register, which still lists Phase 8 / Band 6 with all 16 slugs including this plan's 7 and
  still totals **90** lines. **Do not additionally assert a fixed total line count** (e.g. "90 − 16 =
  74") for `<PLAN04_SLUGS>`: this plan does not control, and cannot predict at authoring time, how
  many of plan04's _other_ remaining bands the concurrently-authored sibling plans
  (`05-course-authoring-platform-and-concurrency`, `06-course-authoring-architecture-and-ai-harness`,
  `08-course-authoring-security-and-ops`, `09-course-authoring-interview-technique`,
  `11-course-authoring-capstones`) also carve out of plan04's scope before this plan's own execution
  begins — plan04's final total could land anywhere from 74 (only Band 6 removed) down to a much
  smaller remainder (if every other band is also extracted). Pinning a specific total here would be a
  fabricated acceptance criterion this plan cannot ground. The only fact this plan needs, and the only
  one it asserts, is that its own 7 slugs are gone from plan04's list.

- [x] [AI] **Verify the rendering repository baseline** — two checks,
      both required (`test ! -f` and a zero-count `grep`, read the printed number rather than
      `&&`-chaining since `grep -c` exits 1 on a zero count):

  ```bash
  test ! -f apps/ayokoding-www/src/middleware.ts
  rg -n 'await headers\(\)' apps/ayokoding-www/src/app
  ```

  — acceptance: the `test` exits 0 and `rg` emits no match (exit 1): the now-purposeless middleware
  is deleted and no current App Router layout awaits `headers()`. **Current-build adjustment:**
  `src/app/layout.tsx` and `.next/prerender-manifest.json` no longer exist after the upstream Next
  routing/build changes, so neither is a valid probe. The outcome-based confirmation is instead
  `npm exec nx run ayokoding-www:test:unit`, including the static-content-route unit test, plus a
  successful `npm exec nx run ayokoding-www:build`.

- [x] [AI] **Confirm all 7 course slugs are absent (no collision)** under `<COURSES>` — command:

  ```bash
  for s in just-enough-c just-enough-cpp linux-os windows-os system-programming just-enough-rust modern-system-programming; do
    test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS COURSES $s"
  done
  ```

  — acceptance: **zero** output lines. Falsifiable both ways:
  `mkdir -p apps/ayokoding-www/content/en/learn/courses/just-enough-cpp` makes the loop print
  `EXISTS COURSES just-enough-cpp`.

- [x] [AI] Establish content baselines: `npm exec nx run ayokoding-www:build` and
      `npm exec nx run ayokoding-www:test:unit` — acceptance: both exit 0; record pass state in
      `evidence/phase-0-snapshot.txt`.
- [x] [AI] **Create the authored-body slug register** —

  ```bash
  cat > evidence/authored-body-slugs.txt <<'EOF'
  just-enough-c
  just-enough-cpp
  linux-os
  windows-os
  system-programming
  just-enough-rust
  modern-system-programming
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **7**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | wc -l` returns **0**.

- [x] [AI] **Record the authored-body baseline** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **7** today; must return **0** at archival (Phase 7). Record in
      `evidence/phase-0-snapshot.txt`.
- [x] [AI] Confirm `learnings.md` exists in the plan folder with its H1 — command:
      `test -f learnings.md && head -1 learnings.md` — acceptance: file present, first line is
      `# Learnings: ayokoding-learning-path-07-course-authoring-low-level-systems`.
- [x] [AI] **Cross-plan link gate** — confirm every reference in this plan's own files resolves:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-07-course-authoring-low-level-systems"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

- [x] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [x] [AI] `<PLAN04_SLUGS>` resolved to exactly one path; the trim confirmed (0 of this plan's 7 slugs
      remain in plan04's register — no assertion made about that register's total line count, which
      this plan does not control).
- [x] [AI] `vercel-function-cost-reduction`'s signal confirmed (`middleware.ts` absent, no App Router
      layout awaits `headers()`, and the static-content-route unit test plus site build pass).
- [x] [AI] All 7 course slugs confirmed absent under `<COURSES>` (zero `EXISTS` lines).
- [x] [AI] `ayokoding-www:build` + `test:unit` baselines recorded green.
- [x] [AI] `evidence/authored-body-slugs.txt` holds 7 unique slugs; the ABSENT-count baseline of 7 is
      recorded.
- [x] [AI] Cross-plan link gate green.
- [x] [AI] Zero manifest files touched.
- [x] [AI] **No PR was opened for this phase and nothing was pushed**:
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.
      only the toolchain, the two upstream preconditions, and the slug register were
  > established — no course body exists yet, nothing is pushed, and no PR exists. Safe to stop
  > indefinitely. To resume: re-run the two blocking-plan verification commands and the baseline build.

---

## Phase 1: Author Cohort A (5 courses — the C-family chain)

> Each course is authored as a full page-bundle into `<COURSES><course-id>/`, following the
> nine-step convention in
> [tech-docs.md §The per-course authoring convention](./tech-docs.md#the-per-course-authoring-convention-maker-checker-fixer-not-code-tdd).
> **Author each course body from its `<SYLLABUS>courses/<id>.md` spec, not from a fresh judgment call.**
> all 5 land.

- [x] [AI] `just-enough-c` (Primer · C, `<SYLLABUS>courses/just-enough-c.md`) — convention steps 1–9
      complete; checkers clean (zero CRITICAL/HIGH/MEDIUM) — acceptance:
      `test -d "apps/ayokoding-www/content/en/learn/courses/just-enough-c/learning"` and
      `test -d "apps/ayokoding-www/content/en/learn/courses/just-enough-c/drilling"` both exit 0.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [x] [AI] `just-enough-cpp` (Primer · C++, `<SYLLABUS>courses/just-enough-cpp.md`; declares
      `just-enough-c` a prerequisite — DD-14's dedicated on-ramp) — convention steps 1–9 complete;
      checkers clean — acceptance: the `prerequisites` frontmatter array must list `just-enough-c` as
      a quoted exact element (matching the repo's `prerequisites: ["id1", "id2"]` convention), not
      merely contain `just-enough-cpp`'s own slug as a substring —
      `grep -F -q '"just-enough-c"' "apps/ayokoding-www/content/en/learn/courses/just-enough-cpp/_index.md"`
      exits 0.

  **Gherkin (binds) →** "just-enough-cpp declares its C on-ramp prerequisite"

  ```gherkin
  Scenario: just-enough-cpp declares its C on-ramp prerequisite
    Given the just-enough-cpp course is authored
    When a reader inspects its declared prerequisites
    Then it names just-enough-c as a prerequisite
    And its overview states the C-to-C++ progression rationale (DD-14's dedicated on-ramp)
  ```

  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

- [x] [AI] `linux-os` (By Example · C + shell, `<SYLLABUS>courses/linux-os.md`; declares `just-enough-c`
      and `just-enough-bash` as prerequisites) — convention steps 1–9 complete; checkers clean —
      acceptance:
      `grep -F -q 'just-enough-c' "apps/ayokoding-www/content/en/learn/courses/linux-os/_index.md"`
      exits 0 **and**
      `grep -F -q 'just-enough-bash' "apps/ayokoding-www/content/en/learn/courses/linux-os/_index.md"`
      exits 0 **and** its `overview.md` states an explicit Linux-family scope boundary against
      `windows-os`.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] `windows-os` (By Example · C + PowerShell, `<SYLLABUS>courses/windows-os.md`; declares
      `just-enough-c` a prerequisite) — convention steps 1–9 complete; checkers clean — acceptance:
      `grep -F -q 'just-enough-c' "apps/ayokoding-www/content/en/learn/courses/windows-os/_index.md"`
      exits 0 **and** its `overview.md` states an explicit Windows-family scope boundary against
      `linux-os`.

  **Gherkin (binds) →** "linux-os and windows-os state distinct OS-family scope boundaries"

  ```gherkin
  Scenario: linux-os and windows-os state distinct OS-family scope boundaries
    Given linux-os and windows-os are both authored
    When a reader compares their overviews
    Then each explicitly scopes to its own OS family (Linux syscalls/filesystems vs. Windows internals/the API)
    And neither overview presents the other's OS family as in scope
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] `system-programming` (By Example · C, `<SYLLABUS>courses/system-programming.md`; declares
      `just-enough-c` and `linux-os` as prerequisites — authored **last** in this cohort since it
      needs `linux-os`) — convention steps 1–9 complete; checkers clean — acceptance:
      `grep -F -q 'just-enough-c' "apps/ayokoding-www/content/en/learn/courses/system-programming/_index.md"`
      exits 0 **and**
      `grep -F -q 'linux-os' "apps/ayokoding-www/content/en/learn/courses/system-programming/_index.md"`
      exits 0.

  **Gherkin (binds) →** "The C-family prerequisite chain resolves in declaration order"

  ```gherkin
  Scenario: The C-family prerequisite chain resolves in declaration order
    Given just-enough-c, linux-os, and system-programming are all authored
    When the library's prerequisite DAG is read for these three IDs
    Then linux-os declares just-enough-c and just-enough-bash as prerequisites
    And system-programming declares just-enough-c and linux-os as prerequisites
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] **Confirm no manifest file changed across this cohort's whole diff** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.
- [x] [AI] **Add all 5 catalog rows** to `tech-docs.md` §Course Library Catalog (already present at
      authoring time in this plan's own file — verify they match the settled specs, do not re-derive)
      and list all 5 in `<COURSES>_index.md` — acceptance: 5 new list entries present.

### Phase 1 Gate

- [x] [AI] All 5 Cohort-A bodies exist:
      `for s in just-enough-c just-enough-cpp linux-os windows-os system-programming; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 5 before this phase).
- [x] [AI] `just-enough-cpp` declares `just-enough-c`; `linux-os` declares `just-enough-c` and
      `just-enough-bash`; `windows-os` declares `just-enough-c`; `system-programming` declares
      `just-enough-c` and `linux-os`.
- [x] [AI] Checkers clean across all 5; `npm exec nx run ayokoding-www:build` and `npm run lint:md` exit 0.
- [x] [AI] Catalog rows added for all 5; run `npm exec nx run ayokoding-www:generate-indexes` then `npm exec nx run ayokoding-www:validate-indexes`; zero manifest files
      touched.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance: no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.
      green; PR `[AI]`-merged; `ayokoding-www` deployed.

> **Pause Safety**: the complete C-family chain (`just-enough-c` → `just-enough-cpp` / `linux-os` /
> `windows-os` → `system-programming`) is live at canonical URLs; no manifest references any of it
> yet. Safe to stop indefinitely. To resume: re-run the 5-course presence check and the build.

---

## Phase 2: Author Cohort B (2 courses — the Rust chain) + band-completion signal

> Cohort B is DAG-independent of Cohort A (neither `just-enough-rust` nor
> `modern-system-programming` references any Cohort-A course), and follows Phase 1 on the same
> persistent final-delivery branch.

- [x] [AI] `just-enough-rust` (Primer · Rust, `<SYLLABUS>courses/just-enough-rust.md`) — convention
      steps 1–9 complete; checkers clean — acceptance:
      `test -d "apps/ayokoding-www/content/en/learn/courses/just-enough-rust/learning"` and
      `test -d "apps/ayokoding-www/content/en/learn/courses/just-enough-rust/drilling"` both exit 0.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [x] [AI] `modern-system-programming` (By Example · Rust, `<SYLLABUS>courses/modern-system-programming.md`;
      declares `just-enough-rust` a prerequisite; states itself as `system-programming`'s (81) Rust
      counterpart — DD-LLS-2) — convention steps 1–9 complete; checkers clean — acceptance:
      `grep -F -q 'just-enough-rust' "apps/ayokoding-www/content/en/learn/courses/modern-system-programming/_index.md"`
      exits 0 **and** its `overview.md` contains the literal phrase
      `` `Rust counterpart to system-programming` `` verbatim (a fixed distinguishing phrase, not a
      bare substring match — `modern-system-programming`'s own self-referential slug/title mentions
      can never coincidentally produce this exact phrase) —
      `grep -F -q 'Rust counterpart to system-programming' "apps/ayokoding-www/content/en/learn/courses/modern-system-programming/overview.md"`
      exits 0 (the counterpart relationship is stated, not merely implied).

  **Gherkin (binds) →** "system-programming and modern-system-programming state their counterpart relationship"

  ```gherkin
  Scenario: system-programming and modern-system-programming state their counterpart relationship
    Given system-programming (C) and modern-system-programming (Rust) are both authored
    When a reader compares their overviews
    Then modern-system-programming's overview names system-programming as its C counterpart
    And each teaches the same close-to-metal principles in its own language's idiom without reproducing the other's worked examples
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [x] [AI] **Confirm no manifest file changed across this cohort's whole diff** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.
- [x] [AI] **Add both catalog rows** to `tech-docs.md` §Course Library Catalog and list both in
      `<COURSES>_index.md`.
- [x] [AI] **Record the one band-completion signal** — append this fenced block, verbatim with real
      values substituted, directly under this cohort's own section:

  ```text
  BAND: Band 6 (Low-level systems & native-languages half) — ayokoding-learning-path-07
  PLAN: ayokoding-learning-path-07-course-authoring-low-level-systems
  LANDED_COURSE_IDS:
  just-enough-c
  just-enough-cpp
  linux-os
  windows-os
  system-programming
  just-enough-rust
  modern-system-programming
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.json
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.json
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.json
  ```

  ```text
  BAND: Band 6 (Low-level systems & native-languages half) — ayokoding-learning-path-07
  PLAN: ayokoding-learning-path-07-course-authoring-low-level-systems
  LANDED_COURSE_IDS:
  just-enough-c
  just-enough-cpp
  linux-os
  windows-os
  system-programming
  just-enough-rust
  modern-system-programming
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.json
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.json
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.json
  FINAL_PR: #200 — terminal archival PR; delivered when this branch reaches origin/main
  ```

  — acceptance: all seven `LANDED_COURSE_IDS` resolve to a directory under `<COURSES>`; all three
  `GROW_MANIFESTS` paths are the software-engineer-role manifests only (never the `ai-engineer`
  **after** the terminal archival PR merges; keep the merge field pending during intermediate phases.

### Phase 2 Gate

- [x] [AI] Both Cohort-B bodies exist:
      `for s in just-enough-rust modern-system-programming; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0**.
- [x] [AI] `modern-system-programming` declares `just-enough-rust` and names `system-programming` as
      its counterpart in its own overview.
- [x] [AI] Checkers clean across both; `npm exec nx run ayokoding-www:build` and `npm run lint:md` exit 0.
- [x] [AI] Catalog rows added for both; run `npm exec nx run ayokoding-www:generate-indexes` then `npm exec nx run ayokoding-www:validate-indexes`; zero manifest files touched.
- [x] [AI] The one band-completion signal is prepared with its course IDs and manifest paths; its
      `FINAL_PR` remains pending until the terminal archival PR merges.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.

> **Pause Safety**: all 7 authored bodies are ready on the persistent branch; the one band-completion
> signal is prepared for the terminal delivery record. Safe to stop. To resume: re-run

---

## Phase 3: Section & Authored-Tree Verification

- [x] [AI] **Verify all 7 authored bodies are present** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0** (returned 7 at the Phase-0 baseline).
- [x] [AI] **Verify every authored body declares prerequisites** —
      `while read -r s; do grep -F -q 'prerequisites:' "apps/ayokoding-www/content/en/learn/courses/$s/_index.md" || echo "MISSING $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**.
- [x] [AI] **Verify every authored body has both tracks** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s/learning" && test -d "apps/ayokoding-www/content/en/learn/courses/$s/drilling" || echo "INCOMPLETE $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**.
- [x] [AI] Run affected quality gates: `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately.
- [x] [AI] Build the site: `npm exec nx run ayokoding-www:build` — acceptance: exits 0.
- [x] [AI] Run link + heading-hierarchy + markdown validation:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate
  npm run lint:md
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ose-www/content 2>&1 | grep -F "learn/courses/"
  ```

  — acceptance: the first two exit 0 and the scoped `grep` finds no line naming a `learn/courses/`
  path relevant to this plan's 7 bodies (exits 1).

  **Gherkin (binds) →** "The authored low-level-systems course bodies build and validate green"

  ```gherkin
  Scenario: The authored low-level-systems course bodies build and validate green
    Given all seven course bodies this plan authors have landed under the courses bucket
    When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
    Then the build succeeds over the authored tree
    And link, heading-hierarchy, and markdownlint validation report no errors across the authored course bodies
  ```

- [x] [AI] **Confirm zero manifest files touched across this plan's entire history** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`

### Phase 3 Gate

- [x] [AI] All three 7-body structural loops (presence, prerequisites, both tracks) return 0.
- [x] [AI] Affected `typecheck / lint / test:quick / test:unit / specs:behavior:coverage` exit 0.
- [x] [AI] Build + heading-hierarchy + markdownlint green; the scoped link gate finds no failure.
- [x] [AI] Zero manifest files touched on this branch.
- [x] [AI] **No PR opens for this phase** (intermediate): committed on the shared closeout branch;
      nothing pushed for review yet — the closeout PR opens at Phase 7.

> **Pause Safety**: the authored 7-course tree passes every automated gate. Safe to stop. To resume:
> re-run the affected quality gates + build.

---

## Phase 4: Manual Content Verification (Playwright MCP)

> **Locale scope**: `en`-only — an Indonesian mirror is explicitly deferred.
>
> **Rule-15 exemption (recorded, not silently omitted)**: the three live-site testers are exempt for
> this plan, for the same three reasons recorded in
> [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded). The exemption is
> narrow — the Playwright manual behavioural verification below is mandatory and performed.

- [x] [AI] Confirm `en` is the content locale for these 7 courses — command:
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "MISSING $s"; done < evidence/authored-body-slugs.txt | wc -l`
      returns **0**, and `test ! -d apps/ayokoding-www/content/id/learn/courses/just-enough-c`
      exits 0.
- [x] [AI] Start dev server: `npm exec nx dev ayokoding-www` — acceptance: server up on port 3101.
- [x] [AI] **Sample-verify all 7 authored course pages** at breakpoints 375 / 768 / 1280 px, via
      Playwright MCP: `browser_navigate` to `/en/learn/courses/<course-id>`, `browser_resize`, then
      `browser_snapshot` — acceptance: each page renders its overview, learning track, and drilling
      track; `html[lang]` is `en`; `browser_console_messages` reports **zero** errors per page per
      breakpoint.
- [x] [AI] **Verify prerequisite rendering** — on `system-programming` (declares `just-enough-c` and
      `linux-os`), confirm both prerequisites are displayed and each link resolves to its canonical
      page — acceptance: both link targets return 200 and land on the named prerequisite.
- [x] [AI] **Verify a drilling track renders** — open `linux-os`'s `drilling/overview.md` page and
      confirm all five fixed sections are present — acceptance: five section headings visible in
      `browser_snapshot`.
- [x] [AI] Capture one screenshot per course per breakpoint to
      `evidence/phase-4-<course-id>-en-<breakpoint>px.png` — acceptance:
      `git ls-files -- 'evidence/phase-4-*-en-*px.png' | grep -c .` returns **21** (7 courses × 3
      breakpoints).
- [x] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per course.

  All routes returned 200 and emitted zero console errors at every width.
  ![Just Enough C 375](./evidence/phase-4-just-enough-c-en-375px.png) ![Just Enough C 768](./evidence/phase-4-just-enough-c-en-768px.png) ![Just Enough C 1280](./evidence/phase-4-just-enough-c-en-1280px.png)
  ![Just Enough C++ 375](./evidence/phase-4-just-enough-cpp-en-375px.png) ![Just Enough C++ 768](./evidence/phase-4-just-enough-cpp-en-768px.png) ![Just Enough C++ 1280](./evidence/phase-4-just-enough-cpp-en-1280px.png)
  ![Linux OS 375](./evidence/phase-4-linux-os-en-375px.png) ![Linux OS 768](./evidence/phase-4-linux-os-en-768px.png) ![Linux OS 1280](./evidence/phase-4-linux-os-en-1280px.png)
  ![Windows OS 375](./evidence/phase-4-windows-os-en-375px.png) ![Windows OS 768](./evidence/phase-4-windows-os-en-768px.png) ![Windows OS 1280](./evidence/phase-4-windows-os-en-1280px.png)
  ![System Programming 375](./evidence/phase-4-system-programming-en-375px.png) ![System Programming 768](./evidence/phase-4-system-programming-en-768px.png) ![System Programming 1280](./evidence/phase-4-system-programming-en-1280px.png)
  ![Just Enough Rust 375](./evidence/phase-4-just-enough-rust-en-375px.png) ![Just Enough Rust 768](./evidence/phase-4-just-enough-rust-en-768px.png) ![Just Enough Rust 1280](./evidence/phase-4-just-enough-rust-en-1280px.png)
  ![Modern System Programming 375](./evidence/phase-4-modern-system-programming-en-375px.png) ![Modern System Programming 768](./evidence/phase-4-modern-system-programming-en-768px.png) ![Modern System Programming 1280](./evidence/phase-4-modern-system-programming-en-1280px.png)

- [x] [AI] **Record the rule-15 exemption in `learnings.md`** with its three reasons.
- [x] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 4 Gate

- [x] [AI] All 7 courses verified across three breakpoints in `en`; zero console errors; prerequisite
      display and drilling-track rendering confirmed.
- [x] [AI] 21 screenshots present under `evidence/` and referenced in this checklist.
- [x] [AI] The rule-15 exemption is recorded with reasons; the triad itself is **not** run here.
- [x] [AI] Zero manifest files touched.
- [x] [AI] **No PR opens for this phase** (intermediate) — folds into Phase 7's closeout PR.

> **Pause Safety**: the authored 7-course tree is verified live and defect-clean in `en`. Safe to
> stop. To resume: restart the dev server and re-open one course per cohort.

---

## Phase 5: Pre-archival Quality & CI Preparation

- [x] [AI] Run the full affected suite on the persistent final-delivery branch:
      `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npm exec nx run ayokoding-www:build` — acceptance: all exit 0 before Phase 7 opens the terminal PR.
- [x] [AI] Resolve every failure on the persistent final-delivery branch — acceptance: no follow-up
      worktree, branch, or PR is required.

### Phase 5 Gate

- [x] [AI] Full affected suite + build green on the persistent final-delivery branch.
- [x] [AI] The band signal is prepared without a merge SHA; downstream notification waits for the
      terminal PR merge.
- [x] [AI] **No PR opens for this phase** — it folds into the Phase 7 archival PR.

> **Pause Safety**: the branch is ready for archival and terminal review. Safe to stop. To resume:
> re-run the affected suite on the persistent final-delivery branch.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [x] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [x] [AI] Apply the **secret/sensitivity gate** to every surviving entry.
- [x] [AI] Apply the **repo-relevance gate** — infra-private content never cross-routes into this
      repo.
- [x] [AI] Route each surviving learning to exactly one durable home per the routing matrix; code
      homes are ALWAYS filed as a separate `plans/backlog/<slug>/` follow-up plan, never landed
      inline.
- [x] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same problem or area — fold the learning into
      that brief instead of creating a new file; only create a new `plans/ideas/<slug>.md` when the
      scan confirms no existing brief overlaps (see
      [Integrate Before You Add](../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
      — acceptance: the entry's routing line names either the folded-into brief or confirms the
      overlap scan found nothing.
- [x] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md`.
- [x] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 6 Gate

- [x] [AI] Every `learnings.md` entry is terminal or the explicit "none" escape is present.
- [x] [AI] No code-homed learning landed inline in this plan's own commits/PRs.
- [x] [AI] Zero manifest files touched.
- [x] [AI] **No PR opens for this phase** (intermediate) — folds into Phase 7's closeout PR.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`
> and confirm every entry is terminal.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [x] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [x] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [x] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [x] [AI] Verify ALL delivery checklist items are ticked.
- [x] [AI] Verify the Knowledge Capture phase is complete.
- [x] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [x] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`.
- [x] [AI] Verify the **rule-15 exemption is recorded with reasons** in `learnings.md` and in Phase 4
      — acceptance: `grep -F -q 'rule-15' learnings.md` exits 0.
- [x] [AI] **Verify this plan's authored-body assertion** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      returns **0**, and `wc -l < evidence/authored-body-slugs.txt` returns **7** — this plan asserts
      **7**, not the sibling plan's 9 nor the original band's 16.
- [x] [AI] **Verify the ownership invariant held across this plan's entire history** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0** on the persistent final-delivery branch.
- [x] [AI] **Re-run the cross-plan link gate**:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-07-course-authoring-low-level-systems"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

- [x] [AI] Move:
      `git mv plans/in-progress/ayokoding-learning-path-07-course-authoring-low-level-systems/ plans/done/YYYY-MM-DD__ayokoding-learning-path-07-course-authoring-low-level-systems/`
      using today's **completion** date. The source is always `plans/in-progress/` — Phase 0's
      promotion step is a mandatory precondition, so the plan never sits in `plans/backlog/` at
      archival time.
- [x] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [x] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [x] [AI] Notify `ayokoding-learning-path-12-careers-se-manifests` that this band's signal is on
      `origin/main` (that plan's own Phase 0 preconditions read this plan's `delivery.md`) —
      acceptance: no dangling reference in that plan's `Depends-on` table.
- [x] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-07-course-authoring-low-level-systems to done`.

### Phase 7 Gate

- [x] [AI] All 7 authored bodies present; the slug register holds 7 unique lines.
- [x] [AI] Zero manifest files touched across the plan's entire history.
- [x] [AI] The cross-plan link gate is green.
- [x] [AI] Plan folder is under
      `plans/done/YYYY-MM-DD__ayokoding-learning-path-07-course-authoring-low-level-systems/`; all
      READMEs updated; archival committed.
- [x] [AI] The sole archival PR was opened only after the archival commit; its secret scan, local quality checks, and
      CI gates are green, then it is `[AI]`-merged and deployed once.

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [x] [AI] Commit changes thematically — one course bundle per commit is the natural unit here.
- [x] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period) —
      e.g. `feat(ayokoding-www): add just-enough-cpp course body`.
- [x] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [x] [AI] Do NOT bundle unrelated changes into a single commit.
- [x] [AI] Stage only this plan's paths (`git add <explicit paths>`) — **never** `git add -A`; the
      sibling split plan and other work may be authored concurrently in the same repo.

### Local Quality Gates (Before Every Push)

- [x] [AI] `npm exec nx affected -t typecheck` exits 0.
- [x] [AI] `npm exec nx affected -t lint` exits 0.
- [x] [AI] `npm exec nx affected -t test:quick test:unit` exits 0.
- [x] [AI] `npm exec nx affected -t specs:behavior:coverage` exits 0.
- [x] [AI] `npm run lint:md` exits 0.
- [x] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

### Note: plan location at archival time

This plan is created in
`plans/backlog/ayokoding-learning-path-07-course-authoring-low-level-systems/`. When work starts it
is promoted to
`plans/in-progress/ayokoding-learning-path-07-course-authoring-low-level-systems/` (no date prefix on
either); the `git mv` in Phase 7 then archives it to
`plans/done/YYYY-MM-DD__ayokoding-learning-path-07-course-authoring-low-level-systems/` using the
completion date.
