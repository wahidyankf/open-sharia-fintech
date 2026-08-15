# Delivery Checklist — Learning Path Course Authoring: Security, Ops & Delivery (Band 7)

This checklist authors **eleven course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: `it-and-application-security`,
`offensive-security`, `defensive-security`, `detection-engineering-and-siem-operations`,
`vulnerability-management-and-assessment`, `it-governance-grc`, `bare-metal-virtualization`,
`self-managed-kubernetes-and-gitops`, `platform-engineering-and-devex`,
`site-reliability-engineering`, and `analytics-and-experimentation` — Band 7 of the shared course
library, carved out of `ayokoding-learning-path-04-course-authoring`'s own delivery checklist.

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to
> [`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md). This
> plan's only outbound artefact is the **single band-completion signal** prepared during authoring and
> delivered with the terminal archival PR. See [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else)
> and [tech-docs §The manifest ownership invariant](./tech-docs.md#the-manifest-ownership-invariant-binding).
>
> **Cross-plan source of truth** — the 128-file `syllabus/` detail layer lives in
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> Every course body is authored **from** its `syllabus/courses/<course-id>.md` spec. **Never copy
> those files into this plan.**
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
> **integration** (draft PR opened, secret scan, local quality checks, and PR quality-gate verification, CI green, `[AI]` merge, `ayokoding-www`
> deployed); a gate in an **intermediate** phase instead confirms the work is committed with nothing
> pushed for review yet — see [Plans Organization Convention §PRs Open at Delivery
> Boundaries](../../../repo-governance/conventions/structure/plans/25-prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
> A phase is not complete until every gate check is green.
>
> **Executor environment note — RTK-wrapped commands emit an empty-output marker, not true
> emptiness** (inherited verbatim from plan 04's own delivery.md, since the same harness routes this
> plan's commands identically): `git diff --name-only … | grep -c .` is the sanctioned zero-assertion
> form here; `wc -l` is never used for one, because RTK appends a three-line trailer to a non-empty
> `git diff` and a lone newline to an empty one, so `wc -l` reads `1` even on a genuinely clean diff.
> Never use an `ls`-based emptiness assertion for the same family of reasons.

## One-PR delivery contract (binding, 2026-08-01)

This 11-course plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
merge, deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. This contract supersedes every older
cohort or delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-08-course-authoring-security-and-ops/` path below is this
plan's only worktree; no per-course, cohort, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-08-course-authoring-security-and-ops/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-08-course-authoring-security-and-ops` (or `git worktree add -b worktree/ayokoding-learning-path-08-course-authoring-security-and-ops worktrees/ayokoding-learning-path-08-course-authoring-security-and-ops origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

This path is the one and only worktree for the entire plan. Provision it once from current
`origin/main`, create the persistent `final-delivery` branch after Phase 0, and use neither
per-course/cohort/stage worktrees nor per-phase branches. Remove it only after the final PR merges.

> **Worktree Cap conformance note (added when the rule landed):** this plan already declared a
> single, plan-wide worktree before the
> [Worktree Cap](../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)
> and
> [Per-Repository Delivery Mode Restrictions](../../../repo-governance/conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
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

- [ ] [AI] Inspect the staged diff and confirm it contains no machine-secret value.
- [ ] [AI] Use a scoped Conventional Commit (for example, `docs(plans): refresh course-preparation backlog`).
- [ ] [AI] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`; acceptance: exits 0 for the affected scope.
- [ ] [AI] Push the single branch, then wait for `.github/workflows/pr-quality-gate.yml`; acceptance: the PR quality gate is green before merge.

## Depends-on

| Relation      | Plan (full folder name)                                         | Nature                                                                                                                                                                                                                         |
| ------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-07-course-authoring-low-level-systems` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-07-course-authoring-low-level-systems/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phase 0** is a single serial baseline.
- **Phase 1 (Cohort A, 5 bodies)** — author and commit bodies serially on the persistent
  final-delivery branch. Author `defensive-security` before
  `detection-engineering-and-siem-operations`, whose prerequisite and distinctness lines cross-check it.
- **Phase 2 (Cohort B, 6 bodies)** — author and commit on the same branch.
- **Phases 3–7 (finalization)** are serial on the same branch.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at
  `/en/learn/courses/<course-id>`)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/` (**never written here**)
- `<MANIFESTS>` = `<FEAT>manifests/` (**never written here** — manifest-plan property; read-only
  reference only)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`
  (cross-plan authoring source of truth — **never copied**)
- `<PLAN04>` = the resolved location of `ayokoding-learning-path-04-course-authoring` — currently
  `../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/`; Phase 0 re-resolves this if that
  plan has archived by execution time.

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
> **Cross-plan precondition (hard).** Two blocking predecessors must both be merged before any
> authoring begins — a body authored into a `<COURSES>` bucket that does not yet exist lands in the
> wrong place, and eleven new always-dynamic pages landing before the cost-reduction fix ships would
> compound an already-overrun function-duration bill.

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-08-course-authoring-security-and-ops/ plans/in-progress/ayokoding-learning-path-08-course-authoring-security-and-ops/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      `git ls-tree -r --name-only origin/main -- plans/in-progress/ayokoding-learning-path-08-course-authoring-security-and-ops/README.md | grep -c .`
      returns **1** and the same query against `plans/backlog/ayokoding-learning-path-08-course-authoring-security-and-ops/README.md` returns **0**.
      Falsifiable both ways: before the push lands, the first query returns 0 and the second
      returns 1. Execution never runs out of `plans/backlog/` — this push is a mandatory
      precondition, not a courtesy. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/44-example-usage-and-iteration-example.md#execute-plan-from-backlog).
      _Implementation note (2026-08-15): moved the plan and updated both indexes in the designated
      single-plan worktree on its delivery branch, per the one-PR delivery contract. The specified
      `origin/main` location proof is deferred to Phase 7, when this branch's sole archival PR merges._
- [x] [AI] Enter/provision the worktree and install dependencies: `npm install` — acceptance: exits 0,
      `node_modules/` synchronized.
      _Implementation note (2026-08-15): ran successfully in the designated plan worktree._
- [x] [AI] Converge the toolchain: `npm run doctor -- --fix` — acceptance: exits 0 with no unresolved
      drift.
      _Implementation note (2026-08-15): 16/16 tools OK; doctor applied no unresolved drift._
- [x] [AI] **Verify repository baseline: course-authoring catalog is present**
      — resolve its actual location rather than assuming a folder name, since it was still `in-progress`
      at authoring time — command (single line):
      `git ls-files -- 'plans/done/*ayokoding-learning-path-04-course-authoring/README.md'`
      — acceptance: prints **exactly one** path — pipe it to `grep -c .` and read **1**. Record the
      printed path to `evidence/phase-0-snapshot.txt` as `PLAN04_ROOT=<path>`. Falsifiable both ways:
      before plan 04 archives, this prints nothing and the count reads **0**; if the corpus were
      somehow archived under two different dates, the count would read **2** — either failure blocks
      this gate. **Do not hardcode a guessed completion date** in this command or anywhere else in this
      plan's files — every cross-plan reference to plan 04 must be re-pointed to the printed
      `PLAN04_ROOT` value once resolved (see the BF-8-style link gate below).
      _Implementation note (2026-08-15): resolved exactly one catalog path and recorded it as
      `PLAN04_ROOT` in `evidence/phase-0-snapshot.txt`._

- [x] [AI] **Verify none of this band's eleven course IDs was already authored by plan 04** (Band 7 must
      not be double-authored) — command:

  ```bash
  for s in it-and-application-security offensive-security defensive-security \
    detection-engineering-and-siem-operations vulnerability-management-and-assessment \
    it-governance-grc bare-metal-virtualization self-managed-kubernetes-and-gitops \
    platform-engineering-and-devex site-reliability-engineering analytics-and-experimentation; do
    test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS $s"
  done
  ```

  — acceptance: **zero** output lines. Falsifiable both ways:
  `mkdir -p apps/ayokoding-www/content/en/learn/courses/it-governance-grc` makes the loop print
  `EXISTS it-governance-grc`, proving the check fires.
  _Implementation note (2026-08-15): the authoritative eleven-slug loop produced zero `EXISTS`
  lines._

- [x] [AI] **Verify the rendering repository baseline** — two checks, both
      required, matching the concrete signal recorded in
      [README §Why the cost-reduction dependency is hard](./README.md#depends-on):
      `test ! -f apps/ayokoding-www/src/app/layout.tsx` (Phase 1's Cause-A fix promoted the locale
      layout and deleted the root one) and `test ! -f apps/ayokoding-www/src/middleware.ts` (Phase 3's
      middleware elimination) — acceptance: both exit 0. Falsifiable both ways: today, before that plan
      merges, `apps/ayokoding-www/src/app/layout.tsx` still exists and this check fails; once fixed,
      re-introducing either file would fail it again. Additionally resolve the plan's archived location
      for cross-plan link purposes:
      `git ls-files -- 'plans/done/*vercel-function-cost-reduction/README.md'` — acceptance: prints
      exactly one path (`grep -c .` reads **1**). Record it to `evidence/phase-0-snapshot.txt` as
      `VFR_ROOT=<path>`.
- [x] [AI] Establish content baselines: `npm exec nx run ayokoding-www:build` and
      `npm exec nx run ayokoding-www:test:unit` — acceptance: both exit 0; record pass state in
      `evidence/phase-0-snapshot.txt`.
      _Implementation note (2026-08-15): both commands exited 0; pass state recorded in the Phase-0
      snapshot._
- [x] [AI] **Create the authored-body slug register** — write this band's eleven slugs, one per line,
      to `evidence/authored-body-slugs.txt`:

  ```bash
  cat > evidence/authored-body-slugs.txt <<'EOF'
  it-and-application-security
  offensive-security
  defensive-security
  detection-engineering-and-siem-operations
  vulnerability-management-and-assessment
  it-governance-grc
  bare-metal-virtualization
  self-managed-kubernetes-and-gitops
  platform-engineering-and-devex
  site-reliability-engineering
  analytics-and-experimentation
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **11**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | wc -l` returns **0** (no duplicate slug).
  Falsifiable both ways: deleting one line makes the first check return 10; duplicating one makes the
  second return 1.
  _Implementation note (2026-08-15): wrote 11 unique slugs; both count checks passed._

- [x] [AI] **Record the authored-body baseline** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **11** today (none authored yet), recorded in
      `evidence/phase-0-snapshot.txt`. The same command must return **0** at archival (Phase 7).
      _Implementation note (2026-08-15): the authoritative loop returned and recorded 11 absent
      bodies._
- [x] [AI] Confirm `learnings.md` exists in the plan folder with its H1 — command:
      `test -f learnings.md && head -1 learnings.md` — acceptance: file present and the first line is
      `# Learnings: ayokoding-learning-path-08-course-authoring-security-and-ops`.
      _Implementation note (2026-08-15): the file exists and its H1 matches the plan identifier._
- [x] [AI] **Cross-plan link gate** — confirm every reference in this plan's own files resolves,
      including the `<PLAN04>` and `<VFR>` references just resolved above:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-08-course-authoring-security-and-ops"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1). If `PLAN04_ROOT` or `VFR_ROOT` above
  resolved to a path different from this plan's current `../../in-progress/...` references, **first
  re-point every such reference in this plan's own files to the resolved path**, then re-run this
  check — never edit the referenced plan's own folder to fix a link.
  _Implementation note (2026-08-15): scoped link validation passed with no line naming this plan
  folder._

- [x] [AI] **Confirm no manifest file changed in this phase** — this phase only writes `evidence/`
      files and opens no PR:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.
      _Implementation note (2026-08-15): manifest-path diff count is 0._

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
      _Implementation note (2026-08-15): install exited 0; doctor reported 16/16 tools OK and no
      unresolved drift._
- [x] [AI] Direct predecessor and repository baseline verified: plan 04's archived `README.md` resolves to exactly one
      path (`PLAN04_ROOT` recorded); `vercel-function-cost-reduction`'s two concrete file-absence
      checks both exit 0 and its archived `README.md` resolves to exactly one path (`VFR_ROOT`
      recorded).
      _Implementation note (2026-08-15): `PLAN04_ROOT` and `VFR_ROOT` each resolve exactly once;
      both rendering file-absence checks pass._
- [x] [AI] None of this band's eleven slugs already exists under `<COURSES>` (zero `EXISTS` lines).
      _Implementation note (2026-08-15): the authoritative eleven-slug loop produced zero `EXISTS`
      lines._
- [x] [AI] `ayokoding-www:build` + `test:unit` baselines recorded green.
      _Implementation note (2026-08-15): both passed and are recorded in the Phase-0 snapshot._
- [x] [AI] `evidence/authored-body-slugs.txt` holds 11 unique slugs; the ABSENT-count baseline of 11 is
      recorded in `evidence/phase-0-snapshot.txt`.
      _Implementation note (2026-08-15): 11 unique slugs and `AUTHORED_BODY_ABSENT_COUNT=11` are
      recorded._
- [x] [AI] Cross-plan link gate green (no line naming this plan's folder); every reference re-pointed
      to a resolved path if plan 04 or the cost-reduction plan had already archived.
      _Implementation note (2026-08-15): scoped validation passed with no matching plan-folder line._
- [x] [AI] Zero manifest files touched.
      _Implementation note (2026-08-15): manifest-path diff count is 0._
- [x] [AI] **No PR was opened for this phase and nothing was pushed** — read the printed number from
      each (never `&&`-chained):
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.
      _Implementation note (2026-08-15): both required remote counts are 0._

> **Pause Safety**: only the toolchain, the two upstream preconditions, and the slug register were
> established — no course body exists yet, nothing is pushed, and no PR exists. Safe to stop
> indefinitely. To resume: re-run the two blocking-plan verification commands and the baseline build.

---

## Per-course authoring convention (applies to every authoring step in Phases 1–2)

Reproduced from `ayokoding-learning-path-04-course-authoring`'s own "NEW-course authoring convention"
(shared authoring methodology across every split-plan folder in this programme, not owned by plan 04
alone):

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / SIEM-platform / security-tooling
   facts via `web-researcher` — acceptance: no version-pinned claim written `[Unverified]`; every
   volatile fact sits in a dated accuracy-note sidebar, not the stable spine.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`); the `course-id` slug and the
   prerequisite chain are **settled** — use the exact values declared in `<SYLLABUS>courses/<course-id>.md`,
   not a fresh decision — acceptance: `test -d "<COURSES><course-id>"`,
   `test -d "<COURSES><course-id>/learning"`, and `test -d "<COURSES><course-id>/drilling"` all exit 0,
   and `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per `prd.md`), concept coverage, example/scenario pages + colocated
   `code/` where code-bearing, and `learning/capstone/`; the concept-coverage floor and example volume
   are **settled** in the spec's `co-NN`/`ex-NN` enumeration — acceptance: the course's own
   `overview.md` states its scope boundary against any sibling course it could be confused with.
4. [AI] **Author drilling track** — `drilling/overview.md` in the fixed five-section order —
   acceptance: all five sections present.
5. [AI] **Run content checkers** — the matching learning checker, `apps-ayokoding-www-facts-checker`,
   and `apps-ayokoding-www-link-checker` (plus `apps-ayokoding-www-general-checker` on
   `drilling/overview.md`) — acceptance: findings recorded.
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run checkers + `npm exec nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.
8. [AI] **Confirm no manifest file changed in this course's own diff**:
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
   — acceptance: returns **0** on the persistent final-delivery branch before the final PR opens.
9. [AI] **Licensing self-check (programme `A8`)** — grep this course's own worked-example code for the
   CC-BY-SA Stack Overflow / lifted-forum hazard:
   `grep -rn 'stackoverflow\.com\|reddit\.com' "<COURSES><course-id>/learning/code/" 2>/dev/null | grep -c .`
   — acceptance: prints `0` (do not chain with `&&`; read the printed output). This is a targeted
   heuristic, not a full copyright audit — the maker-checker-fixer content checkers (step 5) remain the
   primary `A8` control for prose, figures, and structure.

**Per-cohort closing steps** (identical for each cohort; applied once per phase, at the end):

1. [AI] Confirm each landed course's row is present in
   [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) and its ID is added to
   `<COURSES>_index.md`.
2. [AI] Confirm zero manifest files were touched across the cohort:
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
   returns **0**.
3. [AI] **Cohort B only** — record the single band-completion signal (see
   [Phase 2](#phase-2-cohort-b--governance-ops--analytics-6-bodies) below); Cohort A does not emit a
   signal of its own, since the band is not complete until Cohort B lands (per
   [README's adaptation note](./README.md#band-completion-signal-contract)).

---

## Phase 1: Cohort A — Security core (5 bodies)

- [x] [AI] `it-and-application-security` (Annotated-concept · Python) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
    _Implementation note (2026-08-15): authored the 21-file course bundle with 52 structured examples
    covering `co-01`–`co-30`, safe runnable Python mechanisms, capstone, and five-section drilling.
    Scoped structural/fact/link equivalents, Python execution, build, and Markdown lint passed; the
    licensing heuristic and manifest-path assertion both returned 0._
- [x] [AI] `offensive-security` (By Example · Python + shell) — convention complete; checkers clean; the
      body states its **lab-local, authorized-scope-only** rules of engagement — acceptance:
      `for w in "authorized" "lab"; do grep -F -q -i "$w" "apps/ayokoding-www/content/en/learn/courses/offensive-security/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "The offensive-security course states its lab-local rules of engagement"

  ```gherkin
  Scenario: The offensive-security course states its lab-local rules of engagement
    Given the offensive-security course is authored
    When a reader reads its overview
    Then it explicitly states the material is lab-local and authorized-scope-only
    And no lesson presents exploitation technique as guidance for unauthorized real-world targets
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
    _Implementation note (2026-08-15): authored the 18-file bundle with 78 lab-only examples, local
    Python/shell fixture checks, capstone, and five-section drilling. The overview explicitly states
    lab-local, authorized-scope-only rules; scope guard, Python artifacts, pyright, diff check,
    licensing heuristic, Markdown lint, build, and zero-manifest assertion all passed._

- [x] [AI] `defensive-security` (By Example · Python + shell — **hands-on, NOT concept**, DL-9/DD-12) —
      convention complete; checkers clean; the body delivers Sigma-on-ELK/OpenSearch + the IR lifecycle + hardening as generalist blue-team breadth.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
    _Implementation note (2026-08-15): authored the hands-on 78-example blue-team bundle with
    synthetic offline Sigma/OpenSearch telemetry, IR lifecycle, hardening, capstone, and five-section
    drilling. Course-local structural/safety/link checks, lab artifacts, Markdown lint, build, and
    zero-manifest assertion passed; the boundary to Wazuh-specific detection engineering is explicit._
- [x] [AI] `detection-engineering-and-siem-operations` (By Example · XML/rules + config + Python;
      declares `defensive-security` a prerequisite) — convention complete; checkers clean —
      distinctness acceptance: this course has the reader author working Wazuh decoders, correlation
      rules, and a dashboard with false-positive tuning; `defensive-security` retains the generalist
      Sigma/ELK breadth, IR, and hardening as its distinct scope. Verify the prerequisite
      (`grep -F -q 'defensive-security' "<COURSES>detection-engineering-and-siem-operations/_index.md"`
      exits 0) and verify **no lesson title is duplicated** across the two courses' syllabi:
      `comm -12 <(grep -h '^# ' apps/ayokoding-www/content/en/learn/courses/defensive-security/learning/*.md | sort -u) <(grep -h '^# ' apps/ayokoding-www/content/en/learn/courses/detection-engineering-and-siem-operations/learning/*.md | sort -u) | wc -l`
      returns **0**. Falsifiable both ways: copying one lesson title between the two courses makes it
      return 1. **The two `<(...)` process substitutions are load-bearing — never unwrap them** (the
      bare `grep -h` form is rewritten by the harness hook to a help-banner call that always exits 0
      with a fixed-length banner; inside `<(...)` the hook does not rewrite the call).

  **Gherkin (binds) →** "Hands-on detection engineering stays distinct from generalist defensive security"

  ```gherkin
  Scenario: Hands-on detection engineering stays distinct from generalist defensive security
    Given the detection-engineering-and-siem-operations course is authored
    When a reader compares it with the hands-on defensive-security course
    Then it has the reader author working Wazuh decoders, correlation rules, and a dashboard with false-positive tuning
    And defensive-security keeps the generalist Sigma/ELK breadth, IR, and hardening as its distinct scope
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
    _Implementation note (2026-08-15): authored the 19-file, 78-example offline Wazuh-style bundle
    with original decoder/rule/config/dashboard artifacts and local verification. Prerequisite, scope
    boundary, zero duplicate-title, XML/JSON, safety/licensing/manifest, Markdown/prettier, and build
    checks passed._

- [x] [AI] `vulnerability-management-and-assessment` (By Example · Python) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
    _Implementation note (2026-08-15): authored the 19-file course bundle with 80 contiguous,
    concept-mapped offline exercises, typed fixtures, capstone modules, and five-section drilling.
    Structural/density/fact/link, safety/licensing/manifest, Markdown/heading, Python runtime, and
    build validations passed._
- [x] [AI] Apply the per-cohort closing steps (catalog rows confirmed, zero-manifest check). Cohort A
      does not emit a band-completion signal — Band 7 is not complete until Cohort B lands.
      _Implementation note (2026-08-15): all five Catalog rows and course-index entries are present;
      the new detection-engineering course retains its catalog `N` label rather than duplicating
      vulnerability management's topic 61. The manifest-path diff remains 0._

### Phase 1 Gate

- [x] [AI] All 5 Cohort-A bodies exist:
      `for s in it-and-application-security offensive-security defensive-security detection-engineering-and-siem-operations vulnerability-management-and-assessment; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 5 before this phase).
      _Implementation note (2026-08-15): the five-body absence loop returned 0._
- [x] [AI] `defensive-security` is authored By-Example hands-on (DL-9/DD-12 label correction applied);
      `detection-engineering-and-siem-operations` declares it as a prerequisite; the duplicate-lesson-title
      `comm` check returns 0.
      _Implementation note (2026-08-15): prerequisite grep and duplicate-title `comm` check both
      returned 0; the reviewed course bundle is hands-on By-Example._
- [x] [AI] `offensive-security` states its lab-local, authorized-scope-only rules of engagement.
      _Implementation note (2026-08-15): both required overview terms are present; missing-term count
      is 0._
- [x] [AI] Checkers clean across all 5; build + `lint:md` exit 0.
      _Implementation note (2026-08-15): each course's scoped checker-equivalent evidence is clean;
      aggregate build and Markdown lint both exited 0._
- [x] [AI] Catalog rows confirmed present; zero manifest files touched.
      _Implementation note (2026-08-15): all rows/index entries resolve and the manifest-path diff is 0._
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance: no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.

> **Pause Safety**: the security-core cluster is live; `detection-engineering-and-siem-operations` and
> `defensive-security` cross-reference each other correctly. Safe to stop. To resume: re-run the
> section build, then start Phase 2.

---

## Phase 2: Cohort B — Governance, ops & analytics (6 bodies)

- [ ] [AI] `it-governance-grc` (Annotated-concept · no code) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `bare-metal-virtualization` (By Example · HCL/YAML/shell) — convention complete; checkers
      clean; its `overview.md` states the two-altitude boundary against `self-hosting-essentials`
      (plan 04's DD-14) — acceptance:
      `grep -F -q 'self-hosting-essentials' "apps/ayokoding-www/content/en/learn/courses/bare-metal-virtualization/overview.md"`
      exits 0.

  **Gherkin (binds) →** "Bare-metal virtualization stays the full-depth sibling of light self-hosting"

  ```gherkin
  Scenario: Bare-metal virtualization stays the full-depth sibling of light self-hosting
    Given the bare-metal-virtualization course is authored
    When a reader compares it with self-hosting-essentials
    Then bare-metal-virtualization names self-hosting-essentials as its lighter-altitude sibling
    And it covers Proxmox and hypervisor depth self-hosting-essentials deliberately excludes
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `self-managed-kubernetes-and-gitops` (By Example · YAML/CLI) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `platform-engineering-and-devex` (Annotated-concept · no code) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] **Gate**: `system-design` exists before authoring the next course — acceptance:
      `test -d "apps/ayokoding-www/content/en/learn/courses/system-design"` exits 0; if it does not,
      **STOP** — `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` (the plan
      that authors `system-design`) has not yet merged, and `site-reliability-engineering` cannot
      declare a resolvable prerequisite. Surface this and wait rather than authoring with a dangling
      reference.
- [ ] [AI] `site-reliability-engineering` (Annotated-concept · Python) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `analytics-and-experimentation` (By Example · Python) — convention complete; checkers clean;
      its `overview.md` states the boundary against `statistics-for-evaluation` (plan 04's DD-26) —
      acceptance:
      `grep -F -q 'statistics-for-evaluation' "apps/ayokoding-www/content/en/learn/courses/analytics-and-experimentation/overview.md"`
      exits 0.

  **Gherkin (binds) →** "Analytics and experimentation stays distinct from statistics for evals"

  ```gherkin
  Scenario: Analytics and experimentation stays distinct from statistics for evals
    Given the analytics-and-experimentation course is authored
    When a reader compares it with statistics-for-evaluation
    Then analytics-and-experimentation names statistics-for-evaluation as its scope-boundary sibling
    And it covers classical product metrics and A/B testing, not evals-specific judge concordance
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] Apply the per-cohort closing steps (catalog rows confirmed, zero-manifest check), **plus**
      record the single band-completion signal below — `GROW_MANIFESTS` = the three
      `software-engineer`-role manifests.

### Phase 2 Gate

- [ ] [AI] All 6 Cohort-B bodies exist:
      `for s in it-governance-grc bare-metal-virtualization self-managed-kubernetes-and-gitops platform-engineering-and-devex site-reliability-engineering analytics-and-experimentation; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 6 before this phase).
- [ ] [AI] Both two-altitude/scope boundaries stated (`bare-metal-virtualization` ↔
      `self-hosting-essentials`; `analytics-and-experimentation` ↔ `statistics-for-evaluation`).
- [ ] [AI] Checkers clean across all 6; build + `lint:md` exit 0.
- [ ] [AI] All 11 course rows present in the catalog; `<COURSES>_index.md` lists all 11; zero manifest
      files touched across the whole plan.
- [ ] [AI] The single band-completion signal is recorded below with all five fields.
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance: no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.

```text
BAND: Band 7 — Security, ops, quality & delivery
PLAN: ayokoding-learning-path-08-course-authoring-security-and-ops
LANDED_COURSE_IDS:
  it-and-application-security
  offensive-security
  defensive-security
  detection-engineering-and-siem-operations
  vulnerability-management-and-assessment
  it-governance-grc
  bare-metal-virtualization
  self-managed-kubernetes-and-gitops
  platform-engineering-and-devex
  site-reliability-engineering
  analytics-and-experimentation
GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.json
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.json
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.json
```

> **Pause Safety**: all eleven Band-7 bodies are live at canonical URLs; the single band-completion
> signal is recorded and ready for the manifest plan to consume; no manifest references them yet, so no
> path can break. Safe to stop. To resume: re-run the section build.

---

## Phase 3: Section & Authored-Tree Verification

- [ ] [AI] **Verify all 11 authored bodies are present** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: this returned **11** at the Phase-0 baseline,
      and removing any one bundle makes it return 1.
- [ ] [AI] **Verify every authored body declares prerequisites** —
      `while read -r s; do grep -F -q 'prerequisites:' "apps/ayokoding-www/content/en/learn/courses/$s/_index.md" || echo "MISSING $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0** (returns 11 at baseline).
- [ ] [AI] **Verify every authored body has both tracks** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s/learning" && test -d "apps/ayokoding-www/content/en/learn/courses/$s/drilling" || echo "INCOMPLETE $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**.
- [ ] [AI] **Supersession sweep (Q-A-conditional)** — read the Q-A ruling already recorded in
      `ayokoding-learning-path-01-url-restructure`'s archived `tech-docs.md` (resolved by the time this
      plan starts, since plan 04's own repository baseline context already required it). If ruled A (staging pen)
      or a hybrid covering the overlapping subjects: for every course in
      `evidence/authored-body-slugs.txt` whose subject overlaps a remaining
      `apps/ayokoding-www/content/en/learn/legacy/` page, append a `Superseded by:` line to that
      course's own `overview.md`, and record the identified slug list to
      `evidence/supersession-sweep-slugs.txt` — acceptance:
      `grep -lF 'Superseded by:' <COURSES>*/overview.md | wc -l` equals
      `wc -l < evidence/supersession-sweep-slugs.txt`. If ruled B (permanent archive): edit no
      `overview.md`; record `Q-A ruled B — no supersession sweep performed` in `learnings.md` —
      acceptance: `grep -lF 'Superseded by:' <COURSES>*/overview.md | wc -l` returns **0**.
- [ ] [AI] Run affected quality gates from the worktree:
      `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` — acceptance:
      exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation), committing
      preexisting fixes separately.
- [ ] [AI] Build the site: `npm exec nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate` +
      `npm run lint:md`, plus the scoped link gate:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ose-www/content 2>&1 | grep -F "learn/courses/"
  ```

  — acceptance: the first two exit 0 and the `grep` finds no line naming any of this plan's own
  `learn/courses/<course-id>/` paths (exits 1 or names only other plans' courses).

  **Gherkin (binds) →** "The authored Band-7 course bodies build and validate green"

  ```gherkin
  Scenario: The authored Band-7 course bodies build and validate green
    Given every course body this plan authors has landed under the courses bucket
    When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
    Then the build succeeds over the eleven authored bodies
    And link, heading-hierarchy, and markdownlint validation report no errors across them
  ```

- [ ] [AI] **Verify zero manifest files were touched by this entire plan**:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.
- [ ] [AI] **Verify the band-completion signal is complete** — anchor the count on the field's
      line-start form:
      **1** (this plan's own single band signal).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 3 Gate

- [ ] [AI] All three 11-body structural loops (presence, prerequisites, both tracks) return 0.
- [ ] [AI] Supersession sweep resolved one way or the other (never left unresolved).
- [ ] [AI] Affected `typecheck / lint / test:quick / test:unit / specs:behavior:coverage` exit 0.
- [ ] [AI] Build + heading-hierarchy + markdownlint green; the scoped link gate finds no failure among
      this plan's own paths.
- [ ] [AI] Zero manifest files touched across the whole plan's history; the single band signal is
      prepared without a merge SHA.
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or `FINAL_PR` occurs before Phase 7.

> **Pause Safety**: the authored library passes every automated gate. Safe to stop. To resume: re-run
> the affected quality gates + build.

---

## Phase 4: Manual Content Verification (Playwright MCP)

> **Locale scope**: this plan's course content is authored `en`-only — per
> [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals), an Indonesian content mirror
> is explicitly deferred. Verify the authored course pages in `en` only.
>
> **Rule-15 exemption (recorded, not silently omitted)**: the three live-site testers are **exempt for
> this plan**, for the same three reasons plan 04 recorded — see
> [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded). **The exemption is
> narrow** — the Playwright manual behavioural verification below is mandatory and performed, with
> committed evidence.

- [ ] [AI] Confirm `en` is the content locale for these bodies — command:
      `test -d apps/ayokoding-www/content/en/learn/courses/it-and-application-security && test ! -d apps/ayokoding-www/content/id/learn/courses/it-and-application-security`
      — acceptance: exits 0.
- [ ] [AI] Start dev server: `npm exec nx dev ayokoding-www` — acceptance: server up on port 3101.
- [ ] [AI] **Sample-verify authored course pages** — for **all eleven** authored courses, at breakpoints
      375 / 768 / 1280 px, via Playwright MCP: `browser_navigate` to `/en/learn/courses/<course-id>`,
      `browser_resize`, then `browser_snapshot` — acceptance: each page renders its overview, learning
      track, and drilling track; `html[lang]` is `en`; `browser_console_messages` reports **zero**
      errors per page per breakpoint.
- [ ] [AI] **Verify prerequisite rendering** — on `detection-engineering-and-siem-operations`, which
      declares `defensive-security`, confirm the prerequisite is displayed and its link resolves to
      `defensive-security`'s canonical page — acceptance: the link target returns 200.
- [ ] [AI] **Verify a drilling track renders** — open one authored `drilling/overview.md` page and
      confirm all five fixed sections are present in the rendered output.
- [ ] [AI] Capture one screenshot per course per breakpoint to
      `evidence/phase-4-<course-id>-en-<breakpoint>px.png` — acceptance:
      `git ls-files -- 'evidence/phase-4-*-en-*px.png' | grep -c .` returns **33** (11 courses × 3
      breakpoints).
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per course.
- [ ] [AI] **Record the rule-15 exemption in `learnings.md`** with its three reasons and a pointer to
      the navigation-UI plan that carries the triad.
- [ ] [AI] **Confirm no manifest file changed in this phase**:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 4 Gate

- [ ] [AI] All eleven courses verified across three breakpoints in `en`; zero console errors;
      prerequisite display and drilling-track rendering confirmed.
- [ ] [AI] 33 screenshots present under `evidence/` and referenced in this checklist.
- [ ] [AI] The rule-15 exemption is recorded with reasons; the triad itself is **not** run here.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR opens for this phase** (intermediate): the evidence commits are on the shared
      worktree, this phase's own gate above is green, and nothing is pushed for review yet — the
      closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: the authored library is verified live and defect-clean in `en`. Safe to stop. To
> resume: restart the dev server and re-open one sampled course.

---

## Phase 5: Pre-archival Quality & CI Preparation

- [ ] [AI] Run the full affected suite on the persistent final-delivery branch:
      `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npm exec nx run ayokoding-www:build` — acceptance: all exit 0 before Phase 7 opens the terminal PR.
- [ ] [AI] Resolve every failure on the persistent final-delivery branch — acceptance: no follow-up
      worktree, branch, or PR is required.

### Phase 5 Gate

- [ ] [AI] Full affected suite + build green on the persistent final-delivery branch.
- [ ] [AI] The band signal is prepared without a merge SHA; downstream notification waits for the
      terminal PR merge.

> **Pause Safety**: the branch is ready for archival and terminal review. Safe to stop. To resume:
> re-run the affected suite on the persistent final-delivery branch.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable.
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays in `ose-private` only and is
      NEVER cross-routed into `ose-public`/`ose-primer`.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix — **code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate
      `plans/backlog/<slug>/` plan and NEVER landed inline**; this plan's own artefacts are content, not
      code.
- [ ] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same problem or area — fold the learning into
      that brief instead of creating a new file; only create a new `plans/ideas/<slug>.md` when the
      scan confirms no existing brief overlaps (see
      [Integrate Before You Add](../../../repo-governance/conventions/structure/plans/03-ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
      — acceptance: the entry's routing line names either the folded-into brief or confirms the
      overlap scan found nothing.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md`.
- [ ] [AI] **Confirm no manifest file changed in this phase**:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 6 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded with
      reason) or the explicit "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PRs.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR opens for this phase** (intermediate): the `learnings.md` triage is committed on the
      shared closeout branch — the closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [ ] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [ ] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [ ] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete.
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`;
      the `en` content locale exercised.
- [ ] [AI] Verify the **rule-15 exemption is recorded with reasons** in `learnings.md` and in Phase 4 —
      acceptance: `grep -F -q 'rule-15' learnings.md` exits 0.
- [ ] [AI] **Verify this plan's authored-body assertion** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      returns **0**, and `wc -l < evidence/authored-body-slugs.txt` returns **11** — acceptance: both
      hold. **This plan asserts 11, not 127.** The 127-course catalog total is
      `ayokoding-learning-path-12-careers-se-manifests`'s terminal assertion.
- [ ] [AI] **Verify the ownership invariant held**:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0** — acceptance: no manifest file was touched on this branch.
- [ ] [AI] **Verify every cross-plan reference still resolves after upstream archival** — re-run the
      link gate:

  ```bash
  apps/rhino-cli/scripts/rhino-bin.sh md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-08-course-authoring-security-and-ops"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1). Fix references in **this plan's own
  files** if any upstream plan archived mid-execution — never edit the other plan's folder.

- [ ] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-08-course-authoring-security-and-ops/ plans/done/YYYY-MM-DD__ayokoding-learning-path-08-course-authoring-security-and-ops/`
      using today's **completion** date, not the creation date (the `evidence/` subfolder moves with
      it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan and notify
      `ayokoding-learning-path-12-careers-se-manifests`,
      `ayokoding-learning-path-11-course-authoring-capstones` (once its folder exists), and
      `ayokoding-learning-path-12-careers-se-manifests` (once its folder exists) — acceptance: no
      sibling plan's link to this folder is left dangling.
- [ ] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-08-course-authoring-security-and-ops to done`.

### Phase 7 Gate

- [ ] [AI] All 11 authored bodies present (the ABSENT loop returns 0, down from the Phase-0 baseline of
      11); the slug register holds 11 unique lines.
- [ ] [AI] Zero manifest files touched across the plan's entire history.
- [ ] [AI] The cross-plan link gate is green after any upstream archival.
- [ ] [AI] Plan folder is under
      `plans/done/YYYY-MM-DD__ayokoding-learning-path-08-course-authoring-security-and-ops/`; all
      READMEs updated; archival committed.
- [ ] [AI] The sole archival PR was opened only after the archival commit; its secret scan, local quality checks, and
      CI gates are green, then it is `[AI]`-merged and deployed once.

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits (one
      course bundle per commit is the natural unit here).
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period) — e.g.
      `feat(ayokoding-www): add it-governance-grc course body`.
- [ ] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.
- [ ] [AI] Stage only this plan's paths (`git add <explicit paths>`) — **never** `git add -A`; sibling
      plans may be authored concurrently in the same repo.

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npm exec nx affected -t typecheck` exits 0.
- [ ] [AI] `npm exec nx affected -t lint` exits 0.
- [ ] [AI] `npm exec nx affected -t test:quick test:unit` exits 0.
- [ ] [AI] `npm exec nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] `npm run lint:md` exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Commit preexisting fixes separately with appropriate conventional-commit messages.

### Note: plan location at archival time

This plan is created in
`plans/backlog/ayokoding-learning-path-08-course-authoring-security-and-ops/`. When work starts it is
promoted to
`plans/in-progress/ayokoding-learning-path-08-course-authoring-security-and-ops/` (no date prefix on
either); the `git mv` in Phase 7 then archives it to
`plans/done/YYYY-MM-DD__ayokoding-learning-path-08-course-authoring-security-and-ops/` using the
completion date.
