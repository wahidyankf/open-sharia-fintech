# Delivery Checklist — Learning Path Course Authoring: Capstones (Band 8)

This checklist authors **8 capstone course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: `capstone-build-your-own-coding-agent`,
`capstone-build-your-own-pentest-engine`, `capstone-secure-service`, `capstone-data-pipeline`,
`capstone-concurrency-showdown` (Cohort A, mutually independent), then
`capstone-concurrency-and-systems`, `capstone-real-world-delivery`, `capstone-lead-at-altitude`
(Cohort B, a genuine dependency chain — see [README.md §Exact scope](./README.md#exact-scope-8-courses-in-two-cohorts)).

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to
> `ayokoding-learning-path-12-careers-se-manifests` and `ayokoding-learning-path-13-careers-ai-manifest`.
> This plan's only outbound artefact is the **one band-completion signal** recorded at the close of
> Cohort B. See
> [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else) and
> [tech-docs §The manifest ownership invariant](./tech-docs.md#the-manifest-ownership-invariant-binding).
>
> **Cross-plan source of truth** — the `syllabus/` detail layer lives in
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> Six of the eight capstone specs are embedded inter-topic sections inside donor course files
> (`defensive-security.md` ×3, `compilers-parsers-and-transpilers.md` ×2,
> `site-reliability-engineering.md` ×1); the remaining two have dedicated spec files. **Never copy
> those files into this plan.**
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`. **This plan contains
> no `[HUMAN]` step.**
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note. A gate in a phase named as a delivery boundary in the
> [`### Delivery Boundaries`](#delivery-boundaries) table additionally covers integration (draft PR
> opened, 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www` deployed); a gate in an
> intermediate phase confirms the work is committed to its delivery unit's branch with nothing pushed
> for review yet.
>
> **Executor environment note — RTK-wrapped commands** (inherited from plan 04's own note, unchanged):
> `git diff --name-only … | grep -c .` is the sanctioned zero-assertion form in this repo, never
> `wc -l`, because RTK's filtering emits a non-empty trailer on non-empty diffs and a lone newline on
> clean ones, making `wc -l` read `1` on a clean state where `grep -c .` correctly reads `0`. Never use
> an `ls`-based emptiness assertion.

## One-PR delivery contract (binding, 2026-08-01)

This 8-course plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
review cycle, merge, deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the PR-Review Maker→Fixer Cycle, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. This contract supersedes every older
cohort or delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-11-course-authoring-capstones/` path below is this plan's
only worktree; no per-course, cohort, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-11-course-authoring-capstones/`

This path is the one and only worktree for the entire plan. Provision it once from current
`origin/main`, create the persistent `final-delivery` branch after Phase 0, and use neither
per-course/cohort/stage worktrees nor per-phase branches. Remove it only after the final PR merges.

## Delivery Mode: worktree-to-pr

**CI scope note**: "CI green"/"CI gates" below mean the PR's own check run
(`pr-quality-gate.yml`) — never `.github/workflows/main-ci.yml`, which is deprecated,
schedule-only, and must not be monitored or gated on.

This plan has one delivery unit: all change-producing work is committed on the persistent
`final-delivery` branch in the declared worktree. Phases before 7 must not push, open
a PR, run PR review, merge, deploy, or record an in-repository merge SHA. Phase 7 first
commits the archival move and index updates, then opens the sole draft PR, runs the three-cycle
PR-Review Maker→Fixer Cycle plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Depends-on

| Relation        | Plan (full folder name)                                                   | Nature                                                                                                                 |
| --------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **blockedBy**   | `ayokoding-learning-path-01-url-restructure`                              | transitive hard, already done                                                                                          |
| **blockedBy**   | `ayokoding-learning-path-02-schema-and-prerequisite-dag`                  | transitive hard, already done                                                                                          |
| **blockedBy**   | `ayokoding-learning-path-04-course-authoring`                             | hard — Band 1/2 content (see tech-docs confirmed dependency map)                                                       |
| **blockedBy**   | `ayokoding-learning-path-05-course-authoring-platform-and-concurrency`    | hard — Band 4 concurrency primitives                                                                                   |
| **blockedBy**   | `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` | hard — Band 5 harness cluster + architecture courses                                                                   |
| **blockedBy**   | `ayokoding-learning-path-08-course-authoring-security-and-ops`            | hard — Band 7 security/ops courses                                                                                     |
| **blockedBy**   | `vercel-function-cost-reduction`                                          | hard — static-rendering fix must land first                                                                            |
| **blocks**      | `ayokoding-learning-path-12-careers-se-manifests`                         | hard — the three software-engineer manifests' `courseOrder` entries for these 8 IDs resolve only after this plan lands |
| **blocks**      | `ayokoding-learning-path-13-careers-ai-manifest`                          | hard — needs the 9th of 9 AI-cluster course IDs                                                                        |
| **independent** | `ayokoding-learning-path-07-...`, `09-...`, `10-...`                      | none — verified absent, see tech-docs                                                                                  |

**Start precondition (hard gate, checked in Phase 0)**: all five `blockedBy` plans merged to
`origin/main`, verified per-course against the specific prerequisite IDs each capstone needs (not
merely "the plan folder exists").

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phase 0** is a single serial baseline.
- **Cohort A (5 capstones)** — content-independent bodies (each writes only its own `<COURSES><id>/`
  subtree) that pipeline concurrently through review, bounded by the cap. No ordering constraint among
  the five.
- **Cohort B (3 capstones)** — `capstone-concurrency-and-systems` and `capstone-real-world-delivery`
  are mutually independent and pipeline concurrently; `capstone-lead-at-altitude` is a **serial**
  successor that begins only after both land.
- **Final phases (verification, manual, CI, knowledge capture, archival)** are serial.

**Path constants**:

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/`
- `<MANIFESTS>` = `apps/ayokoding-www/src/features/course-paths/manifests/` (**never written here**)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` (**never copied**)

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–6      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 7        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Enter/provision the worktree and install dependencies: `npm install` — acceptance: exits 0,
      `node_modules/` synchronized.
- [x] [AI] Converge the toolchain: `npm run doctor -- --fix` — acceptance: exits 0 with no unresolved
      drift.
- [ ] [AI] **Verify `ayokoding-learning-path-01-url-restructure` and `ayokoding-learning-path-02-schema-and-prerequisite-dag`
      are both archived to `done/`** — command:
      `git ls-files -- 'plans/done/*ayokoding-learning-path-01-url-restructure/README.md' 'plans/done/*ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md' | grep -c .`
      — acceptance: returns **2**.
- [ ] [AI] **Verify `ayokoding-learning-path-04-course-authoring`'s Band 1/2 handoff** — the specific
      courses this band's capstones cite from Band 1/2 exist under `<COURSES>`:

  ```bash
  for s in async-python-and-fastapi-services data-engineering containers-and-orchestration cloud-and-iac cicd-and-release-engineering backend-at-scale; do
    test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"
  done | grep -c .
  ```

  — acceptance: returns **0** (all six present — `backend-at-scale` was added after this plan's own
  dependency re-audit confirmed `capstone-secure-service` and `capstone-data-pipeline` cite topic 39
  as `backend-at-scale`, not `backend-essentials`; see tech-docs). Falsifiable both ways: `git mv` any
  one of these six out of `<COURSES>` temporarily makes the count return ≥1, proving the check fires.

- [ ] [AI] **Verify `ayokoding-learning-path-05-course-authoring-platform-and-concurrency`'s Band 4
      handoff**:

  ```bash
  test "$(gh pr view 136 --repo wahidyankf/ose-public --json state --jq '.state')" = "MERGED"
  for s in csp-style-concurrency actor-model-concurrency; do
    test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"
  done | grep -c .
  ```

  — acceptance: the merge assertion exits **0** and the directory check returns **0**.

- [ ] [AI] **Verify `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`'s Band 5
      handoff**:

  ```bash
  for s in the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing \
    agent-orchestration-subagents-and-observability browser-automation-with-cdp agentic-ai \
    system-design event-driven-architecture creating-ai-powered-apps software-architecture \
    domain-driven-design; do
    test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"
  done | grep -c .
  ```

  — acceptance: returns **0** (all twelve present). `software-architecture` and `domain-driven-design`
  were added to this list after this plan's own dependency re-audit confirmed
  `capstone-real-world-delivery` cites both (topics 42/43 in its "Integrates topics" list) and that
  both are **confirmed absent on disk** as of this plan's authoring time — see
  [tech-docs.md §Confirmed per-capstone dependency map](./tech-docs.md#confirmed-per-capstone-dependency-map).

- [ ] [AI] **Verify `ayokoding-learning-path-08-course-authoring-security-and-ops`'s Band 7 handoff**:

  ```bash
  for s in offensive-security defensive-security detection-engineering-and-siem-operations \
    vulnerability-management-and-assessment it-and-application-security site-reliability-engineering; do
    test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"
  done | grep -c .
  ```

  — acceptance: returns **0** (all six present).

- [ ] [AI] **Verify the `ayokoding-learning-path-01-url-restructure`-re-homed prerequisites this band
      cites directly are present** (should already hold, independent of the four plans above):

  ```bash
  for s in capstone-solid-core security-essentials just-enough-typescript \
    sql-essentials advanced-sql-and-query-performance software-engineering-practices \
    software-product-engineering engineering-management; do
    test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"
  done | grep -c .
  ```

  — acceptance: returns **0** (`backend-essentials` was removed from this list — this plan's
  dependency re-audit found no Band-8 capstone actually cites it; `backend-at-scale`, the course the
  capstones actually cite, is checked under the Band 1/2 handoff above).

- [ ] [AI] **Verify the `vercel-function-cost-reduction` precondition**:

  ```bash
  test ! -f apps/ayokoding-www/src/app/layout.tsx \
    && test ! -f apps/ayokoding-www/src/middleware.ts \
    && grep -rn "await searchParams" apps/ayokoding-www/src/app --exclude-dir=node_modules | grep -c .
  ```

  — acceptance: both `test` commands exit 0 and the `grep -c .` returns **0**. Additionally,
  `npx nx run ayokoding-www:build && jq '.routes | length' apps/ayokoding-www/.next/prerender-manifest.json`
  returns **≥ 2000**. [Repo-grounded — at this plan's authoring time, `apps/ayokoding-www/src/middleware.ts`
  and `apps/ayokoding-www/src/app/layout.tsx` (calling `await headers()`) both still exist, so this
  check currently fails, correctly reflecting that `vercel-function-cost-reduction` has not yet
  landed.] Falsifiable both ways: once the fix lands, re-running this exact command returns the
  passing state; reverting the fix locally reproduces the failing state.

- [ ] [AI] **Confirm all eight capstone slugs are absent (no collision)** under `<COURSES>`:

  ```bash
  for s in capstone-build-your-own-coding-agent capstone-build-your-own-pentest-engine \
    capstone-real-world-delivery capstone-secure-service capstone-data-pipeline \
    capstone-concurrency-and-systems capstone-concurrency-showdown capstone-lead-at-altitude; do
    test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS $s"
  done | grep -c .
  ```

  — acceptance: returns **0**. Falsifiable both ways: `mkdir -p apps/ayokoding-www/content/en/learn/courses/capstone-secure-service`
  makes the count return 1.

- [ ] [AI] **Create the authored-body slug register** — write the 8 slugs, one per line, to
      `evidence/authored-body-slugs.txt`, in cohort order:

  ```bash
  mkdir -p evidence && cat > evidence/authored-body-slugs.txt <<'EOF'
  capstone-build-your-own-coding-agent
  capstone-build-your-own-pentest-engine
  capstone-secure-service
  capstone-data-pipeline
  capstone-concurrency-showdown
  capstone-concurrency-and-systems
  capstone-real-world-delivery
  capstone-lead-at-altitude
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **8**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | wc -l` returns **0**.

- [ ] [AI] **Record the authored-body baseline** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **8** today; must return **0** at archival (Phase 7). Record in
      `evidence/phase-0-snapshot.txt`.
- [ ] [AI] Confirm `learnings.md` exists with its H1 — command: `test -f learnings.md && head -1 learnings.md`
      — acceptance: first line is `# Learnings: ayokoding-learning-path-11-course-authoring-capstones`.
- [ ] [AI] **Cross-plan link gate** — confirm every reference in this plan's own files resolves:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-11-course-authoring-capstones"
  ```

  — acceptance: no matching line (exits 1).

- [ ] [AI] **Confirm no manifest file changed in this phase**:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] All five `blockedBy` plans' handoffs verified (plans 01/02 archived; plans 04/05/06/08's
      specific cited courses present under `<COURSES>`; `vercel-function-cost-reduction`'s checkable
      signal green).
- [ ] [AI] All eight capstone slugs confirmed absent (zero `EXISTS` lines).
- [ ] [AI] `evidence/authored-body-slugs.txt` holds 8 unique slugs; ABSENT baseline of 8 recorded.
- [ ] [AI] Cross-plan link gate green.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR was opened for this phase and nothing was pushed**:
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

> **Pause Safety**: only the toolchain, the five upstream preconditions, and the slug register were
> established — no capstone body exists yet, nothing is pushed, no PR exists. Safe to stop
> indefinitely. To resume: re-run the five blocking-plan verification commands.

---

## Phase 1: Cohort A — five independent capstones

> Each capstone is a full page-bundle authored into `<COURSES><course-id>/`. These five bodies are
> content-independent (each writes only its own subtree) and pipeline concurrently through review.

### Per-capstone authoring convention

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / benchmark claims via
   `web-researcher` — acceptance: no version-pinned claim written unverified; every volatile fact
   (dependency versions, METR/Scale-AI benchmark figures) sits in a dated accuracy-note sidebar.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`) — the prerequisite chain is
   **settled**; use the exact values from `<SYLLABUS><course-id>.md` (or its embedded
   inter-topic section) — acceptance: `test -d` on the three subdirectories all exit 0, and
   `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author the assembly project** — `overview.md` (purpose + `## Prerequisites` + the scope
   boundary stating this is an integration of prior courses, not new concepts) + the capstone's own
   ordered-steps structure (subfolders per its spec: e.g. `target/`, `engine/core/` for the pentest
   capstone; `code/core/` for the coding-agent capstone) + `learning/capstone/` where applicable —
   acceptance: `overview.md` states which prior courses it assembles.
4. [AI] **Author drilling track** — `drilling/overview.md` in the fixed five-section order —
   acceptance: all five sections present.
5. [AI] **Run content checkers** — the matching learning checker, `apps-ayokoding-www-facts-checker`,
   `apps-ayokoding-www-link-checker`, `apps-ayokoding-www-general-checker` on `drilling/overview.md`.
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding.
7. [AI] **Re-verify** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.
8. [AI] **Confirm no manifest file changed in this course's own diff**:
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
   — acceptance: returns **0**.
9. [AI] **Licensing self-check (programme A8)** — grep this course's own worked-example code for the
   CC-BY-SA Stack Overflow hazard:
   `grep -rn 'stackoverflow\.com\|reddit\.com' "<COURSES><course-id>/" 2>/dev/null | grep -c .`
   — acceptance: prints `0`.

Each course below is its own sub-step. Its work may have its own thematic commit, but all commits
remain on the persistent `final-delivery` branch and ship together in the one Phase 7 archival PR:

- [ ] [AI] `capstone-build-your-own-coding-agent` (Harness milestone, Python, settled per
      `<SYLLABUS>capstone-build-your-own-coding-agent.md`) — assembles the five-course harness
      cluster into a working coding-agent CLI — acceptance: all 9 convention steps complete; checkers
      report zero CRITICAL/HIGH/MEDIUM; `grep -F -q 'the-agent-loop' "<COURSES>capstone-build-your-own-coding-agent/_index.md"`
      exits 0 (the harness-cluster prerequisite is declared) **and** the reader's agent completes a
      real TDD coding task per the spec's acceptance criteria — the deterministic test suite passes
      with no live model calls.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-build-your-own-pentest-engine` (Security milestone, TypeScript, settled per
      `<SYLLABUS>capstone-build-your-own-pentest-engine.md`) — acceptance: all 9 convention steps
      complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'authorized' "<COURSES>capstone-build-your-own-pentest-engine/overview.md"` exits 0
      (the non-negotiable authorized-lab-only rule is restated) **and** no worked example references
      any target other than a reader-controlled isolated lab.

  **Gherkin (binds) →** "capstone-build-your-own-pentest-engine hard-enforces authorized-lab-only scope"

  ```gherkin
  Scenario: capstone-build-your-own-pentest-engine hard-enforces authorized-lab-only scope
    Given the capstone-build-your-own-pentest-engine spec's non-negotiable authorization-and-scope rule
    When the course body's overview.md and learning content are authored
    Then the body restates the authorized-lab-target-only rule as a hard, non-tunable requirement
    And no worked example or exercise references any target other than a reader-controlled isolated lab
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `capstone-secure-service` (Security milestone, Python + shell, settled per the embedded
      spec in `<SYLLABUS>defensive-security.md` lines 339–366) — acceptance: all 9 convention
      steps complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'OWASP' "<COURSES>capstone-secure-service/overview.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-data-pipeline` (Data milestone, SQL + Python, settled per the embedded spec in
      `<SYLLABUS>defensive-security.md` lines 368–395) — acceptance: all 9 convention steps
      complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'creating-ai-powered-apps' "<COURSES>capstone-data-pipeline/_index.md"` exits 0
      (confirms the RAG-interface prerequisite is declared, not a Band-7 security course).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-concurrency-showdown` (Comparison milestone, Go + Elixir, settled per the
      embedded spec in `<SYLLABUS>compilers-parsers-and-transpilers.md` lines 293–316) —
      acceptance: all 9 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'csp-style-concurrency' "<COURSES>capstone-concurrency-showdown/_index.md"` exits 0
      **and** `grep -F -q 'actor-model-concurrency' "<COURSES>capstone-concurrency-showdown/_index.md"`
      exits 0 (both, and only these two, prerequisites declared).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] All five Cohort-A bodies pass their own 9-step convention with zero CRITICAL/HIGH/MEDIUM
      findings outstanding.
- [ ] [AI] `npx nx run ayokoding-www:build` and `npm run lint:md` both exit 0 over the Cohort-A tree.
- [ ] [AI] Zero manifest files touched:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0**.
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.

> **Pause Safety**: Cohort A's five capstones are committed on `final-delivery`; Cohort B has not
> started. Safe to stop. To resume: re-verify Cohort A's five slugs exist under `<COURSES>`, then begin Phase 2.

---

## Phase 2: Cohort B — three-course dependency chain + band-completion signal

> `capstone-concurrency-and-systems` and `capstone-real-world-delivery` are mutually independent and
> pipeline concurrently; `capstone-lead-at-altitude` is a serial successor.

- [ ] [AI] `capstone-concurrency-and-systems` (Systems milestone, Go or Elixir + C, settled per the
      embedded spec in `<SYLLABUS>compilers-parsers-and-transpilers.md` lines 266–291) — applies
      the same 9-step convention as Cohort A — acceptance: all 9 steps complete; checkers zero
      CRITICAL/HIGH/MEDIUM; `grep -F -q 'site-reliability-engineering' "<COURSES>capstone-concurrency-and-systems/_index.md"`
      exits 0 (the SRE-instrumentation prerequisite is declared).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-real-world-delivery` (Full-stack milestone, Python + TS + IaC, settled per the
      embedded spec in `<SYLLABUS>defensive-security.md` lines 303–338) — applies the same
      9-step convention — acceptance: all 9 steps complete; checkers zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'capstone-solid-core' "<COURSES>capstone-real-world-delivery/_index.md"` exits 0
      **and** its own per-course precondition check passes:
      `for s in backend-at-scale software-architecture domain-driven-design it-and-application-security offensive-security; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | grep -c .`
      returns **0** (all five of this capstone's specific confirmed prerequisites — topics 39/42/43/58/59
      from the embedded spec's "Integrates topics" list — are present before authoring begins).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Confirm both Cohort-B leaf capstones exist before starting `capstone-lead-at-altitude`**:
      `test -d apps/ayokoding-www/content/en/learn/courses/capstone-concurrency-and-systems && test -d apps/ayokoding-www/content/en/learn/courses/capstone-real-world-delivery`
      — acceptance: both exit 0.

  **Gherkin (binds) →** "capstone-lead-at-altitude is authored only after its intra-band candidate prerequisites land"

  ```gherkin
  Scenario: capstone-lead-at-altitude is authored only after its intra-band candidate prerequisites land
    Given this plan's own Cohort B ordering places capstone-concurrency-and-systems and capstone-real-world-delivery before capstone-lead-at-altitude
    When capstone-lead-at-altitude's own authoring step begins
    Then both "apps/ayokoding-www/content/en/learn/courses/capstone-concurrency-and-systems/" and "apps/ayokoding-www/content/en/learn/courses/capstone-real-world-delivery/" already exist
    And capstone-lead-at-altitude's own _index.md prerequisites field names at least one of the two course IDs, per the spec's disjunctive "one of ... or ..." framing
  ```

- [ ] [AI] `capstone-lead-at-altitude` (Whole-journey milestone, polyglot + prose, settled per the
      embedded spec in `<SYLLABUS>site-reliability-engineering.md` lines 226–257 — the spec's own
      "Goal" states disjunctively that the capstone takes **one of** `capstone-concurrency-and-systems`
      **or** `capstone-real-world-delivery` as its starting artefact, not both) — applies the same
      9-step convention — acceptance: all 9 steps complete; checkers zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'capstone-concurrency-and-systems' "<COURSES>capstone-lead-at-altitude/_index.md"`
      exits 0 **or** `grep -F -q 'capstone-real-world-delivery' "<COURSES>capstone-lead-at-altitude/_index.md"`
      exits 0 (at least one of the two prerequisites is declared, matching the spec's disjunctive framing;
      the author is free to declare both if the chosen artefact genuinely draws on both, but the spec
      does not require it).
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] **Record the band-completion signal** — append the five-field signal block (verbatim, per
      [README §Band-completion signal contract](./README.md#band-completion-signal-contract)) to this
      SHA once merged:

  ```text
  BAND: Band 8 — Remaining capstones
  PLAN: ayokoding-learning-path-11-course-authoring-capstones
  LANDED_COURSE_IDS:
  capstone-build-your-own-coding-agent
  capstone-build-your-own-pentest-engine
  capstone-secure-service
  capstone-data-pipeline
  capstone-concurrency-showdown
  capstone-concurrency-and-systems
  capstone-real-world-delivery
  capstone-lead-at-altitude
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/ai-engineer.yaml
  ```

  — acceptance: all five fields present, `LANDED_COURSE_IDS` lists all 8 slugs from
  `evidence/authored-body-slugs.txt` in the same order, `GROW_MANIFESTS` names exactly the four
  manifest paths above.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] All three Cohort-B bodies pass their own 9-step convention with zero CRITICAL/HIGH/MEDIUM
      findings outstanding, authored in order (the two leaves first, `capstone-lead-at-altitude`
      last).
- [ ] [AI] `npx nx run ayokoding-www:build` and `npm run lint:md` both exit 0 over the Cohort-B tree.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7. The band-completion signal becomes consumable
      only after the terminal archival PR merges.

> **Pause Safety**: all 8 capstones and the band-completion signal are committed on `final-delivery`.
> Safe to stop. To resume: proceed to Phase 3's plan-wide verification sweep.

---

## Phase 3: Final content-correctness sweep

- [ ] [AI] **Structural verification** — confirm all 8 bundles hold the fixed anatomy:
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s/learning" && test -d "apps/ayokoding-www/content/en/learn/courses/$s/drilling" || echo "MALFORMED $s"; done < evidence/authored-body-slugs.txt | grep -c .`
      — acceptance: returns **0**.
- [ ] [AI] **Full build**: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] **Markdown quality**: `npm run lint:md` — acceptance: exits 0.
- [ ] [AI] **Link validation**:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --quiet --exclude plans/done --exclude apps/ose-www/content 2>&1 | grep -F "capstone-"`
      — acceptance: no matching line naming any of the 8 capstone slugs as broken.
- [ ] [AI] **Terminal authored-body assertion** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0** (all 8 present; contrast with Phase 0's baseline of 8 absent).
- [ ] [AI] **Regression check**: `npx nx affected -t typecheck lint test:quick specs:behavior:coverage`
      — acceptance: all exit 0.
- [ ] [AI] **Confirm no manifest file changed across the whole plan**:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 3 Gate

- [ ] [AI] All structural, build, lint, link, regression, and manifest-isolation checks pass.
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.

> **Pause Safety**: the plan-wide content-correctness sweep is complete on `final-delivery`. Safe to
> resume: proceed to Phase 4's manual verification.

---

## Phase 4: Manual Content Verification (Playwright MCP)

- [ ] [AI] Open a sample of authored course pages (at minimum one per cohort — e.g.
      `capstone-build-your-own-coding-agent` and `capstone-lead-at-altitude`) at all three breakpoints
      (mobile/tablet/desktop) in the `en` content locale via Playwright MCP; commit screenshots to
      `evidence/phase-4-<slug>-<breakpoint>.png` — acceptance: screenshots committed, page renders
      without console error.

### Phase 4 Gate

- [ ] [AI] Screenshot evidence committed for the sampled pages at all three breakpoints.

> **Pause Safety**: manual verification evidence is committed locally (rides the Phase 7 closeout PR).
> Safe to stop. To resume: proceed to Phase 5.

---

## Phase 5: Final CI/Regression Check

- [ ] [AI] Re-run `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` against
      `final-delivery` — acceptance: all exit 0, confirming no regression introduced by this plan's
      cumulative changes.

### Phase 5 Gate

- [ ] [AI] All affected targets green.

> **Pause Safety**: no routine change in this phase. Safe to stop.

---

## Phase 6: Knowledge Capture

- [ ] [AI] Triage every entry in `learnings.md` through the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)'s
      routing matrix — each surviving learning routed to exactly one durable home, or discarded with a
      one-line reason. If no generalizable learning was recorded, state
      `No generalizable learnings — <reason>` explicitly.

### Phase 6 Gate

- [ ] [AI] Every `learnings.md` entry reaches a terminal state (routed, filed as backlog, discarded,
      or the explicit no-learnings escape is recorded).

> **Pause Safety**: knowledge capture is complete. Safe to stop.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [ ] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [ ] [AI] Open exactly one draft PR from that branch and run the PR-Review Maker→Fixer Cycle plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [ ] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [ ] [AI] Move this plan folder from `plans/backlog/ayokoding-learning-path-11-course-authoring-capstones/`
      to `plans/done/YYYY-MM-DD__ayokoding-learning-path-11-course-authoring-capstones/` (today's
      completion date), update `plans/backlog/README.md` and `plans/done/README.md`.
- [ ] [AI] Push `final-delivery` and open the one terminal archival PR, then run the PR-Review
      Maker→Fixer Cycle, CI verification, `[AI]` merge, and deployment.
- [ ] [AI] Remove the declared worktree only after the terminal archival PR merges and it has no
      uncommitted changes.

### Phase 7 Gate

- [ ] [AI] Plan folder present under `plans/done/` with the completion-date prefix; both index
      `README.md` files updated; terminal archival PR merged; worktree then removed.

> **Pause Safety**: this is the plan's terminal phase. Once complete, the plan is fully archived.
