# Delivery Checklist — Learning Path Manifest (AI-engineer)

> **Programme decisions** — the `R*`/`A*` ids cited below are defined in
> [tech-docs §Programme decisions](./tech-docs.md#programme-decisions).
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` plus a `> **Pause Safety**:` note.
>
> **Cross-plan source of truth**: `plans/done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`.
> Do not copy; do not author from any other source.
>
> **The manifest ownership invariant (binding)**: this plan owns exactly
> `<MANIFESTS>careers/immediately-effective/ai-engineer.json` and every step that mutates or
> re-verifies it. The sibling plan `ayokoding-learning-path-12-careers-se-manifests` owns exactly its
> three software-engineer-role files. Neither plan edits the other's manifest.

## One-PR delivery contract (binding, 2026-08-01)

This single-manifest plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Work may still be authored, checked, and committed
in dependency order, but no intermediate phase may push, open a PR, start an external merge,
deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all manifest work,
verification, and Knowledge Capture are green; it includes the archival move to `plans/done/`, then
runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review transition, and the normal
`[AI]` merge/deploy protocol. Plan 12 is this plan's sole direct start prerequisite. After Plan 12 is merged, this plan delivers the AI-engineer manifest and performs any cross-manifest validation that needs both completed deliveries. This
contract supersedes every older delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-13-careers-ai-manifest/` path below is this plan's only
worktree; no per-manifest, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-13-careers-ai-manifest/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-13-careers-ai-manifest` (or `git worktree add -b worktree/ayokoding-learning-path-13-careers-ai-manifest worktrees/ayokoding-learning-path-13-careers-ai-manifest origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

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

| Relation      | Plan (full folder name)                           | Nature                                                                                                                                                                                                                         |
| ------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-12-careers-se-manifests` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-12-careers-se-manifests/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phase 1 is a single manifest-authoring unit** — no internal fan-out.
- **Phase 2 is serial per source-plan signal** — the `06` signal (8 of 9 cluster courses) and the `11`
  signal (the 9th) are each their own sync point; they may arrive in either order, and each is
  processed independently as it lands.
- **Phases 3 → 7 are serial.**
- **This plan's own phases have DAG width 1** — every phase mutates or re-verifies the same one data
  file. This plan begins after plan 12's merged delivery and performs its own cross-manifest validation after both deliveries exist.

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–6      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 7        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Path constants

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/`
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/`
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- This plan's path id: `careers/immediately-effective/ai-engineer`.
- Sibling's path ids (read-only reference, not touched by this plan):
  `careers/interview-ready/software-engineer`, `careers/immediately-effective/software-engineer`,
  `careers/fundamentally-strong/software-engineer`.
- The 11 named SWE-fundamentals IDs: `just-enough-python`, `software-testing`,
  `cicd-and-release-engineering`, `backend-at-scale`, `containers-and-orchestration`,
  `computer-architecture`, `site-reliability-engineering`, `data-engineering`,
  `data-structures-and-algorithms-essentials`, `software-product-engineering`, `frontend-essentials`.
- The 6 net-new AI-engineer-role IDs (light eval gate → statistics for evals → deep evals → product
  patterns for probabilistic systems → inference serving and model deployment → fine-tuning and
  adaptation): `evaluating-ai-output-essentials`, `statistics-for-evaluation`,
  `evaluating-ai-systems-in-depth`, `product-patterns-for-probabilistic-systems`,
  `inference-serving-and-model-deployment`, `fine-tuning-and-adaptation`.
- The 9 AI/harness-cluster IDs: `creating-ai-powered-apps`, `agentic-ai`,
  `browser-automation-with-cdp`, `the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`,
  `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`,
  `capstone-build-your-own-coding-agent`.

One additional constant this plan owns: `<MANIFESTS>careers/careers-ai-manifest.unit.test.ts` — **not**
shared with the sibling plan, which owns its own `careers-se-manifests.unit.test.ts`.

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-13-careers-ai-manifest/ plans/in-progress/ayokoding-learning-path-13-careers-ai-manifest/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      `git ls-tree -r --name-only origin/main -- plans/in-progress/ayokoding-learning-path-13-careers-ai-manifest/README.md | grep -c .`
      returns **1** and the same query against `plans/backlog/ayokoding-learning-path-13-careers-ai-manifest/README.md` returns **0**.
      Falsifiable both ways: before the push lands, the first query returns 0 and the second
      returns 1. Execution never runs out of `plans/backlog/` — this push is a mandatory
      precondition, not a courtesy. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).
- [x] [AI] Enter/provision the worktree and install dependencies: `npm install` — acceptance: exits 0.
- [x] [AI] Converge the toolchain: `npm run doctor -- --fix` — acceptance: exits 0.
- [x] [AI] **Precondition 1** — confirm navigation-ui is merged:
      `gh pr list --search "ayokoding-learning-path-03-navigation-ui" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1.
- [x] [AI] **Repository baseline** — verify the current manifest repository and rendered-route
      behavior directly; this records implementation context and is not an additional plan gate.
- [x] [AI] Confirm Plan 12's three-manifest files are present at this plan's start — command:
      `test ! -e <MANIFESTS>careers/interview-ready/software-engineer.json` — acceptance: exits 0;
      Plan 13 begins only after Plan 12's final PR merges.
- [x] [AI] **Precondition 4** — confirm the six net-new AI-engineer-role courses (or at least enough of
      them for Phase 1's GREEN step) exist:
      `gh pr list --search "ayokoding-learning-path-04-course-authoring" --state merged --json number --jq 'length'`
      returns a value ≥ 1 for its Phase-1 delivery unit **or**
      `find <COURSES> -maxdepth 1 -mindepth 1 -type d -name 'evaluating-ai-output-essentials' | wc -l`
      returns **1** — acceptance: at least one of the two holds.
- [x] [AI] **Precondition 5** — confirm the manifest repository and directory exist:
      `test -f <FEAT>shell/manifest-repository.ts && test -d <MANIFESTS>` — acceptance: exits 0.
- [x] [AI] **Precondition 6** — confirm the 11 named SWE-fundamentals courses already resolve (these are
      existing library courses, not net-new authoring):
      `for id in just-enough-python software-testing cicd-and-release-engineering backend-at-scale containers-and-orchestration computer-architecture site-reliability-engineering data-engineering data-structures-and-algorithms-essentials software-product-engineering frontend-essentials; do test -d <COURSES>$id || echo "MISSING:$id"; done`
      — acceptance: prints nothing (all 11 resolve). If any print, this plan's Phase 1 GREEN step
      transcribes only the subset that resolves and records the rest as a documented gap, closed later
      by the six-source-plan growth this plan's sibling processes for the general library (this
      manifest's own Phase 2 growth covers only the 9-course harness cluster, not these 11).
- [x] [AI] Establish baselines: `npm exec nx run ayokoding-www:build`, `:test:unit`,
      `ayokoding-www-fe-e2e:test:e2e` — acceptance: all exit 0; record pass counts in
      `evidence/phase-0-snapshot.txt`.
- [x] [AI] **Manifest baseline snapshot** —
      `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.json` — acceptance: exits non-zero
      (the file does not exist yet); recorded in `evidence/phase-0-snapshot.txt`.
- [x] [AI] **Hub baseline snapshot** —
      `grep -cF '/en/learn/paths/careers/immediately-effective/ai-engineer' <PATHS>_index.md` —
      acceptance: returns **0**; recorded.
- [x] [AI] Resolve every preexisting failure before proceeding.
- [x] [AI] Confirm `learnings.md` scaffold exists.

### Phase 0 Gate

- [x] [AI] `npm install` and `npm run doctor -- --fix` exit 0.
- [x] [AI] Preconditions 1-2 and 5-6 all hold; the independent-start absence check holds; precondition
      4 holds via at least one of its two checks.
- [x] [AI] Baselines recorded green; zero preexisting failures unresolved.
- [x] [AI] This plan's one manifest path recorded absent; its intended href recorded absent.
- [x] [AI] **No PR opened, nothing pushed** —
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

> **Pause Safety**: only the toolchain was verified and the current state snapshotted. Safe to stop
> indefinitely. To resume: re-run the independent-start checks and the baselines.

---

## Phase 1: Author the AI-engineer manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker` + `web-researcher`._
>
> **Authoring priority #1** (DD-27). This plan begins only after plan 12's merged delivery. This
> manifest is **from-scratch** (DD-35): its SWE-fundamentals prerequisites are **included** at the head
> of `courseOrder`, not linked out. Per DD-33 (still holding in scope) `courseOrder` also **walks**,
> never links, the existing nine-course AI/harness cluster — deliberately deferred here to
> [Phase 2](#phase-2-manifest-growth-to-the-full-harness-cluster-walk), recorded as a documented gap.

### 1.1 · TDD cycle — publish the manifest data file

- [x] [AI] **RED** — create `<MANIFESTS>careers/careers-ai-manifest.unit.test.ts` _(new file)_ with a
      failing assertion that `<MANIFESTS>careers/immediately-effective/ai-engineer.json` loads,
      zod-validates, and contains the 11 named SWE-fundamentals course IDs **at the head of**
      `courseOrder` — command: `npm exec nx run ayokoding-www:test:unit` — acceptance: fails because the
      manifest file does not exist. Also create `<SPECS>path-composition.feature` _(new file)_ with the
      scenario below, and a matching failing step in
      `apps/ayokoding-www-fe-e2e/src/steps/path-composition.steps.ts` _(new file)_ — command:
      `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails.

  **Gherkin (binds) →** "The AI-engineer path includes its software-engineering prerequisites instead
  of linking them"

  ```gherkin
  Scenario: The AI-engineer path includes its software-engineering prerequisites instead of linking them
    Given the careers/immediately-effective/ai-engineer path manifest is published
    When a reader with no prior software-engineering competence inspects its courseOrder
    Then the shared software-engineering-fundamentals courses this path's AI-specific spine depends on are present at the head of courseOrder, ordered prerequisite-consistently
    And that reader can start at courseOrder[0] and finish the whole path from this one manifest, with no external prerequisite link required
  ```

- [x] [AI] **GREEN** — author `<MANIFESTS>careers/immediately-effective/ai-engineer.json` _(new file)_
      with `pathId: careers/immediately-effective/ai-engineer`, a `title`, a `description`, and
      `courseOrder` whose **head** is the prerequisite-consistent ordering of the 11 named
      SWE-fundamentals courses — transcribed verbatim (never re-derived) from
      [`manifest-immediately-effective-ai-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-ai-engineer.md)'s
      Stage 0 — **followed by** the six net-new AI-engineer-role courses in order (light eval gate →
      statistics for evals → deep evals → product patterns for probabilistic systems → inference
      serving and model deployment → fine-tuning and adaptation) — command:
      `npm exec nx run ayokoding-www:test:unit` — acceptance: exits 0, AND all 11 SWE-fundamentals IDs are
      present —
      `grep -oE 'just-enough-python|software-testing|cicd-and-release-engineering|backend-at-scale|containers-and-orchestration|computer-architecture|site-reliability-engineering|data-engineering|data-structures-and-algorithms-essentials|software-product-engineering|frontend-essentials' <MANIFESTS>careers/immediately-effective/ai-engineer.json | sort -u | wc -l`
      returns **11 or more**, AND all six AI-engineer-role IDs are present —
      `grep -oE 'evaluating-ai-output-essentials|statistics-for-evaluation|evaluating-ai-systems-in-depth|product-patterns-for-probabilistic-systems|inference-serving-and-model-deployment|fine-tuning-and-adaptation' <MANIFESTS>careers/immediately-effective/ai-engineer.json | sort -u | wc -l`
      returns **6**, AND `checkPrerequisiteConsistency` passes over the combined order (the automated
      topological check, not a manual grep, is authoritative for inter-course ordering).
- [x] [AI] **REFACTOR** — record inline in the YAML, as a comment, that the nine AI/harness-cluster IDs
      are deliberately absent pending Phase 2 growth, naming the phase — command:
      `npm exec nx run ayokoding-www:test:unit && npm exec nx run ayokoding-www:lint` — acceptance: both exit 0
      and the presence checks above still hold.

### 1.2 · The landing anchor (content — maker/checker/fixer)

- [x] [AI] Author `<PATHS>careers/immediately-effective/ai-engineer/_index.md` _(new file)_ — prose and
      SEO only, framing the path as **from-scratch**: no prior software-engineering competence assumed,
      and the SWE-fundamentals courses a reader needs are already the first courses in this path's own
      `courseOrder` — acceptance: the landing describes the path's endpoint (**building AI systems**)
      without naming or assuming an already-working-software-engineer starting persona —
      `grep -c -i 'already[- ]working\|transitioning\|role transition\|switcher' <PATHS>careers/immediately-effective/ai-engineer/_index.md`
      returns **0** — and contains no `courseOrder` key.
- [x] [AI] Run `apps-ayokoding-www-link-checker` + `apps-ayokoding-www-general-checker`; apply the
      matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero remain on re-run.
- [x] [AI] **A8 clean-room licensing self-check** — acceptance: sources consulted and an explicit
      originality statement recorded in this checklist.
- [x] [AI] Populate this plan's **one** paths-hub card (`AI Engineer` — endpoint-named, not
      `SWE → AI Engineer`, since the path no longer assumes a starting role) in `<PATHS>_index.md` —
      acceptance:
      `grep -cF '/en/learn/paths/careers/immediately-effective/ai-engineer' <PATHS>_index.md` returns
      **1** (this href specifically, not a whole-file count, since the sibling plan edits the same
      shared file concurrently).

### 1.3 · Verification and from-scratch smoothness audit

- [x] [AI] Verify path-aware nav end-to-end: routing resolves, the manifest loads,
      `?path=careers/immediately-effective/ai-engineer` context propagates, prev/next walks the order,
      breadcrumb shows the path, course pages show prerequisites — command:
      `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: passes in `en`.
- [x] [AI] **Record the independent-start assertion (documentation-verified, not harness-executable).**
      Confirm by reading this checklist that this plan's Phase 1 begins after Plan 12's merged delivery,
      and that this plan follows plan 12's merged delivery before its successor validation — acceptance: this ordering is stated here in writing. This is a
      build-order claim about the programme's own delivery sequence across two plan folders; no test
      harness can execute it.
      **This scenario intentionally does not land in `<SPECS>path-composition.feature`** — it has no
      step binding and never will one.

  **Gherkin (documentation-verified) →** "This plan follows its predecessor and completes successor validation" — a deliberate third tag form: neither `(binds)` nor
  `(underpins)` fits, since this scenario will never have a step definition and is not a pure-core unit
  test either.

  ```gherkin
  Scenario: This plan follows its predecessor and completes the AI-manifest validation
    Given Plan 12's three manifests are merged to origin/main
    When this plan's Phase 0 checks its start preconditions
    Then this plan's Phase 1 authoring begins after the Plan 12 merge
    And this plan performs the successor cross-manifest check after its own delivery
  ```

- [x] [AI] **Progression smoothness audit (from-scratch-first)** — walk the manifest order and confirm
      prereq-chaining holds, monotonic-ish difficulty holds, and the light-eval-gate versus deep-evals
      scope boundary is not itself a smoothness break — acceptance: all assessable levers verified; any
      regression fixed by softening or bridging in place, never reordering.

### Phase 1 Gate

- [x] [AI] `find <MANIFESTS>careers/immediately-effective/ai-engineer.json | wc -l` returns **1**.
- [x] [AI] The six-AI-member check returns **6**; the SWE-fundamentals-presence check returns **11 or
      more**.
- [x] [AI] `npm exec nx run ayokoding-www:test:unit` exits 0.
- [x] [AI] `npm exec nx run ayokoding-www:build` + `:specs:behavior:coverage` +
      `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [x] [AI] The hub-card href check returns **1**; the persona-language leak check returns **0**.
- [x] [AI] The independent-start assertion is recorded in writing, with its non-executability stated.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.

> **Pause Safety**: the AI-engineer path is verified end-to-end on `final-delivery` over its smoke-test-scoped
> starting composition — the included SWE-fundamentals prerequisites plus whichever AI-engineer-role
> courses exist by this point. DD-27's authoring priority #1 is delivered. Safe to stop indefinitely. To
> resume: `npm exec nx run ayokoding-www:test:unit && npm exec nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 2: Manifest growth to the full harness-cluster walk

> **Trigger**: each of the two contributing course-authoring successor plans' own band-completion
> signal. Processed as each arrives — the two signals may land in either order.

### 2.1 · Growth from `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` (8 of 9 cluster courses)

- [x] [AI] Record the manifest's entry count immediately before this step —
      `grep -cE '^ *- [a-z0-9-]+' <MANIFESTS>careers/immediately-effective/ai-engineer.json` — save to
      `evidence/phase-2-pre-growth-count.txt` (the falsifiable "before" half of this phase's
      before/after check).
- [x] [AI] On that plan's signal landing, insert the eight cluster course IDs it authored (per its own
      `GROW_MANIFESTS` field, naming this manifest by full path) into
      `<MANIFESTS>careers/immediately-effective/ai-engineer.json` at their correct topological
      positions — command: `npm exec nx run ayokoding-www:test:unit` — acceptance: exits 0, AND those eight
      IDs are present.

### 2.2 · Growth from `ayokoding-learning-path-11-course-authoring-capstones` (9th/final cluster course)

- [x] [AI] On that plan's signal landing, insert `capstone-build-your-own-coding-agent` at its correct
      topological position (after all eight prerequisite cluster courses) — command:
      `npm exec nx run ayokoding-www:test:unit` — acceptance: exits 0, AND all nine cluster IDs are now
      present —
      `grep -oE 'creating-ai-powered-apps|agentic-ai|browser-automation-with-cdp|the-agent-loop|agent-tools-and-mcp|agent-context-and-memory|agent-permissions-and-sandboxing|agent-orchestration-subagents-and-observability|capstone-build-your-own-coding-agent' <MANIFESTS>careers/immediately-effective/ai-engineer.json | sort -u | wc -l`
      returns **9**, AND the entry count grew by **exactly 9** over the recorded pre-growth count —
      `grep -cE '^ *- [a-z0-9-]+' <MANIFESTS>careers/immediately-effective/ai-engineer.json` minus the
      value in `evidence/phase-2-pre-growth-count.txt` equals **9**.
- [x] [AI] Confirm the SWE-fundamentals **inclusion** survived the growth — command:
      `grep -oE 'just-enough-python|software-testing|cicd-and-release-engineering|backend-at-scale|containers-and-orchestration|computer-architecture|site-reliability-engineering|data-engineering|data-structures-and-algorithms-essentials|software-product-engineering|frontend-essentials' <MANIFESTS>careers/immediately-effective/ai-engineer.json | sort -u | wc -l`
      — acceptance: still returns **11 or more**.

### 2.3 · TDD cycle — the full harness-cluster walk is asserted, not merely present

- [x] [AI] **RED** — extend the test file with a persisted assertion that all nine cluster IDs are
      present in `courseOrder` **and** appear strictly after every SWE-fundamentals ID and every
      AI-engineer-role ID — command: `npm exec nx run ayokoding-www:test:unit` — acceptance: fails before
      this assertion is implemented (it is new, not a re-check of 2.1/2.2's ad hoc greps).

  **Gherkin (binds) →** "The AI-engineer manifest walks the full nine-course AI/harness cluster after
  growth"

  ```gherkin
  Scenario: The AI-engineer manifest walks the full nine-course AI/harness cluster after growth
    Given the nine-course AI/harness cluster has landed as authored bodies across two course-authoring successor plans
    When the growth phase appends them to this plan's manifest
    Then all nine cluster course IDs are present in courseOrder at their correct topological position
    And the manifest's entry count has grown by exactly nine over its recorded pre-growth count
  ```

- [x] [AI] **GREEN** — implement the persisted assertion — command: `npm exec nx run ayokoding-www:test:unit`
      — acceptance: exits 0.
- [x] [AI] **REFACTOR** — fold the assertion into the same table-driven shape the SWE-fundamentals and
      AI-engineer-role checks use — command:
      `npm exec nx run ayokoding-www:test:unit && npm exec nx run ayokoding-www:lint` — acceptance: both exit 0.

### Phase 2 Gate

- [x] [AI] Both source-plan signals processed; `test:unit` exited 0 after each.
- [x] [AI] The nine-cluster-ID check returns **9**; the entry-count delta equals **9**.
- [x] [AI] The SWE-fundamentals inclusion check still returns **11 or more**.
- [x] [AI] The persisted walk-order assertion (2.3) passes.
- [x] [AI] `npm exec nx run ayokoding-www:build` + `:test:unit` + `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.

> **Pause Safety**: this plan's manifest is at its **full** composition — the included SWE-fundamentals
> set, the six AI-engineer-role courses, and the full nine-course AI/harness cluster walk. No manifest
> truncation remains. Safe to stop indefinitely. To resume:
> `npm exec nx run ayokoding-www:build && npm exec nx run ayokoding-www:test:unit`.

---

## Phase 3: Section and app verification

**Gherkin (underpins, aggregate) →** "This plan's AI-engineer manifest layer builds and validates
green" ([prd.md](./prd.md#acceptance-criteria-gherkin)) — this scenario has no dedicated
`<SPECS>path-composition.feature` step binding; it is closed by the combination of the build, the
affected test tiers, and the manifest-integrity + prerequisite-consistency sweep below, all four run
together every time this phase's gate is checked.

- [x] [AI] Run affected quality gates: `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones.
- [x] [AI] Run e2e: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0.
- [x] [AI] Build: `npm exec nx run ayokoding-www:build` — acceptance: exits 0.
- [x] [AI] Link + heading + markdown validation:
      `apps/rhino-cli/scripts/rhino-bin.sh md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content` +
      `... md heading-hierarchy validate` + `npm run lint:md` — acceptance: the link validator prints
      `All links valid! No broken links found.`; the other two exit 0.
- [x] [AI] **Manifest-integrity + prerequisite-consistency sweep** for this plan's one manifest —
      command: `npm exec nx run ayokoding-www:test:unit` — acceptance: zero violations.
- [x] [AI] **From-scratch smoothness re-check** — acceptance: passes; regressions fixed in place.
- [x] [AI] **Ownership boundary check (scoped to this plan's one file)** —
      `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.json` — acceptance: exits 0. A
      presence check on this plan's own one file, not a directory-wide count — a directory-wide count
      would be affected by how many of the sibling plan's three manifests have landed, which this
      plan's own gate must not depend on.
- [x] [AI] **Scoped cross-plan link check** —
      `apps/rhino-cli/scripts/rhino-bin.sh md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-13-careers-ai-manifest"`
      — acceptance: no matching line (exit 1).

### Phase 3 Gate

- [x] [AI] Affected `typecheck`/`lint`/`test:quick`/`test:unit`/`specs:behavior:coverage` exit 0;
      `ayokoding-www-fe-e2e:test:e2e` exits 0.
- [x] [AI] Build + link + heading + markdown validation green.
- [x] [AI] Manifest integrity + prerequisite-consistency + smoothness report zero violations.
- [x] [AI] This plan's own manifest file present.
- [x] [AI] Scoped cross-plan link check finds no line naming this plan's folder.
- [x] [AI] Work committed to `final-delivery`; nothing pushed for review yet — the unit's PR opens
      only at Phase 7.

> **Pause Safety**: this plan's one-path composition passes every automated gate. Safe to stop
> indefinitely. To resume: re-run the affected quality gates and the build.

---

## Phase 4: Manual UI verification and Rule-15 three-tester retest

> This plan ships one user-visible path landing plus its own one-card slice of the paths hub, so the
> **Rule-15 three-tester retest is mandatory**, scoped to this plan's own surfaces.

- [x] [AI] Confirm `en` is the only content locale — command:
      `test -d <PATHS> && test ! -d apps/ayokoding-www/content/id/belajar/paths` — acceptance: exits 0.
- [x] [AI] Start the dev server: `npm exec nx dev ayokoding-www`.
- [x] [AI] For `en` × breakpoints (375/768/1280px), via Playwright MCP: open the paths hub, confirm this
      plan's one card renders correctly inside the category-grouped `careers/` group, then this plan's
      one landing, walking 2-3 courses via prev/next confirming `?path=` persists — acceptance: all
      correct at all three breakpoints.
- [x] [AI] For this landing specifically, confirm the **included** SWE-fundamentals prerequisite
      courses render as ordered path steps and that each one's canonical page resolves — acceptance:
      the landing renders all 11 named SWE-fundamentals courses as `courseOrder` steps, and every
      `/en/learn/courses/<id>` link the landing emits returns 200.
- [x] [AI] Verify `html[lang]` is `en` and console is clean on every screen — acceptance: both hold.
- [x] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-4-<screen>-en-<breakpoint>px.png` — acceptance:
      `find evidence -name 'phase-4-*-en-*px.png' | wc -l` returns **6** (2 screens — hub plus this
      plan's 1 landing — × 3 breakpoints).
- [x] [AI] Run `web-exploratory-tester` + `web-usability-tester` + `web-design-tester` against the hub
      and this plan's one landing — acceptance: findings recorded.
- [x] [AI] Append each finding as a new unchecked checkbox (`EWT-NNN`/`UWT-NNN`/`DWT-NNN`).

### Rule-15 retest follow-ups

- [x] [AI] _(populated during the retest — every defect finding must be fixed and ticked before
      archival)_

### Phase 4 Gate

- [x] [AI] Hub (this plan's 1 card) + 1 landing + prerequisite display verified in `en` at all three
      breakpoints; console clean.
- [x] [AI] `find evidence -name 'phase-4-*-en-*px.png' | wc -l` returns **6**.
- [x] [AI] Every Rule-15 defect finding is fixed and ticked, or explicitly permitted to defer.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 7.

> **Pause Safety**: this plan's one-path UI is verified live and defect-clean in `en`, with committed
> evidence. Safe to stop indefinitely. To resume: re-run the three testers against the running app.

---

## Phase 5: Pre-PR readiness verification

- [x] [AI] Run `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`,
      `npm exec nx run ayokoding-www-fe-e2e:test:e2e`, and `npm exec nx run ayokoding-www:build` on
      `final-delivery` — acceptance: all exit 0. Do not push or open a PR in this phase.

### Phase 5 Gate

- [x] [AI] Full affected suite + e2e + build are green on `final-delivery`.
- [x] [AI] Work committed to this delivery unit's branch; nothing pushed for review yet — the unit's PR
      opens only at Phase 7.

> **Pause Safety**: this plan's own product is green on the persistent final-delivery branch and is
> not yet integrated on `main` or deployed; it rides the sole Phase 7 PR.
> Safe to stop indefinitely. To resume: re-run the affected suite.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [x] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [x] [AI] Apply the secret/sensitivity gate to every surviving entry.
- [x] [AI] Apply the repo-relevance gate.
- [x] [AI] Route each surviving learning to exactly one durable home — code homes are ALWAYS filed as a
      separate `plans/backlog/<slug>/` plan, never landed inline.
- [x] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same problem or area — fold the learning into
      that brief instead of creating a new file; only create a new `plans/ideas/<slug>.md` when the
      scan confirms no existing brief overlaps (see
      [Integrate Before You Add](../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
      — acceptance: the entry's routing line names either the folded-into brief or confirms the
      overlap scan found nothing.
- [x] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>`.

### Phase 6 Gate

- [x] [AI] Every `learnings.md` entry is terminal, or the file records the explicit "none" escape.
- [x] [AI] No code-homed learning landed inline.
- [x] [AI] Work committed to `final-delivery`; the unit's PR opens only at Phase 7.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [x] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [x] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [x] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [x] [AI] Verify ALL delivery checklist items are ticked.
- [x] [AI] Verify Knowledge Capture is complete.
- [x] [AI] Verify ALL quality gates pass and the build is green.
- [x] [AI] Verify ALL manual assertions pass with committed evidence.
- [x] [AI] Verify every Rule-15 defect finding is fixed.
- [x] [AI] **Terminal single-manifest assertion (this plan's own scope — not the four-manifest,
      127-catalog check, which is the sibling plan's own final-phase responsibility)** — verify this
      plan's one manifest is published at full composition, its landing is live, and its hub card is
      present:
      `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.json` returns 0, AND
      `grep -cF '/en/learn/paths/careers/immediately-effective/ai-engineer' <PATHS>_index.md` returns
      **1**, AND `npm exec nx run ayokoding-www:test:unit` exits 0 — acceptance: all three hold.
- [x] [AI] **Scoped cross-plan link check** — re-run Phase 3's filtered link validation and confirm it
      still finds no line naming this plan's folder.
- [x] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-13-careers-ai-manifest plans/done/YYYY-MM-DD__ayokoding-learning-path-13-careers-ai-manifest`.
- [x] [AI] Update `plans/in-progress/README.md` and `plans/done/README.md`.
- [x] [AI] Update the sibling plan's cross-references to this plan's archived path, in the same commit —
      the sibling plan's Phase 8 start-condition check will need this plan's new archived location once
      it re-verifies its own merged-PR search.
- [x] [AI] Commit: `chore(plans): move ayokoding-learning-path-13-careers-ai-manifest to done`.

### Phase 7 Gate

- [x] [AI] This plan's one manifest published at full composition; hub card present; `test:unit` and
      `build` exit 0.
- [x] [AI] The filtered link check finds no line naming this plan's folder.
- [x] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-13-careers-ai-manifest`.
- [x] [AI] Draft PR opened for Phases 5-7; secret scan, local quality checks, and PR quality-gate verification complete; CI green; PR `[AI]`-merged;
      deployed (no-op).

> **Pause Safety**: this plan is archived and its final PR `[AI]`-merged to `main`. Terminal state for
> this plan — the sibling plan's own final phase can now proceed once it detects this merge. To resume:
> nothing.

---

## Commit Guidelines (all phases)

- [x] [AI] Commit changes thematically; Conventional Commits; split domains/concerns; preexisting fixes
      get their own commits; never bundle unrelated changes.

## Local Quality Gates (before every push)

- [x] [AI] `npm exec nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` exits 0.
- [x] [AI] `npm exec nx run ayokoding-www-fe-e2e:test:e2e` exits 0 for any phase touching the manifest or
      landing.
- [x] [AI] Fix ALL failures, including preexisting ones (Root Cause Orientation).
