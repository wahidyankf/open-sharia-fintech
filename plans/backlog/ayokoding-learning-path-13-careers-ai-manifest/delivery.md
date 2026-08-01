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
> `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` and every step that mutates or
> re-verifies it. The sibling plan `ayokoding-learning-path-12-careers-se-manifests` owns exactly its
> three software-engineer-role files. Neither plan edits the other's manifest.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-13-careers-ai-manifest/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-13-careers-ai-manifest
```

The plan-execution Step 0 gate enters this worktree by default.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each **delivery unit** works in the shared worktree on its own branch, opens a **draft PR** against
`main` at its boundary phase, runs the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles),
then `[AI]` merges automatically once all quality gates are green (DN-11, repo default), then
dispatches `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www`.

**Delivery-Boundary Integration Protocol** (fires once per delivery boundary; excludes Phase 0):

1. [AI] Sync to latest `origin/main`, branch:
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-13-careers-ai-manifest/<phase-slug>`.
2. [AI] Stage only this unit's paths, commit thematically, push, open a draft PR
   (`gh pr create --draft --base main ...`).
3. [AI] Run the PR-Review Maker→Fixer Cycle (3 cycles), resolve every finding, `gh pr ready` —
   acceptance: zero unresolved threads, zero CRITICAL/HIGH outstanding.
4. [AI] Merge once all quality gates are green — `[AI]` auto-merge per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` — acceptance:
   `git rev-parse origin/prod-ayokoding-www` equals `git rev-parse origin/main` after it returns.

## Depends-on and start preconditions

| Direction   | Plan                                                                                                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `blockedBy` | `ayokoding-learning-path-03-navigation-ui` (done)                                                                                                                                          |
| `blockedBy` | `ayokoding-learning-path-01-url-restructure` (done, transitive)                                                                                                                            |
| `blockedBy` | `ayokoding-learning-path-02-schema-and-prerequisite-dag` (done, transitive)                                                                                                                |
| `blockedBy` | `vercel-function-cost-reduction` (`ayokoding-www` unit merged)                                                                                                                             |
| `blockedBy` | `ayokoding-learning-path-12-careers-se-manifests`, **Phase 1 delivery unit only**, partial — this plan's own Phase 0 start precondition                                                    |
| `blockedBy` | `ayokoding-learning-path-04-course-authoring` Phase 1 (6 AI courses) — needed for Phase 1's GREEN step                                                                                     |
| `blockedBy` | `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`, `ayokoding-learning-path-11-course-authoring-capstones` — needed for Phase 2's growth                           |
| _(no edge)_ | `ayokoding-learning-path-12-careers-se-manifests`, **whole-plan** — this plan has no dependency on the sibling's whole-plan completion; that edge belongs to the sibling's own final phase |

See [README §Depends-on](./README.md#depends-on) for the full table.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phase 1 is a single manifest-authoring unit** — no internal fan-out.
- **Phase 2 is serial per source-plan signal** — the `06` signal (8 of 9 cluster courses) and the `11`
  signal (the 9th) are each their own sync point; they may arrive in either order, and each is
  processed independently as it lands.
- **Phases 3 → 7 are serial.**
- **This plan's own phases have DAG width 1** — every phase mutates or re-verifies the same one data
  file. The parallelism this split bought is _between_ this plan and the sibling plan, which proceed
  concurrently once this plan's Phase 0 start precondition (the sibling's Phase 1 merged) holds.

### Delivery Boundaries

| Phase(s) | Delivery unit                                                            | Worktree / branch                                                                         | PR opens         |
| -------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ---------------- |
| 0        | — (setup and baseline)                                                   | —                                                                                         | no               |
| 1        | AI-engineer manifest + landing + hub card                                | `ayokoding-learning-path-13-careers-ai-manifest/phase-1-ai-engineer`                      | yes — at Phase 1 |
| 2        | Manifest growth to full 9-course harness-cluster walk                    | `ayokoding-learning-path-13-careers-ai-manifest/phase-2-manifest-growth`                  | yes — at Phase 2 |
| 3-4      | Automated verification sweep + manual UI verification and Rule-15 retest | `ayokoding-learning-path-13-careers-ai-manifest/phase-3-4-verify-and-retest`              | yes — at Phase 4 |
| 5-7      | Final `main`/CI checkpoint + Knowledge Capture + Plan Archival           | `ayokoding-learning-path-13-careers-ai-manifest/phase-5-7-final-integration-and-archival` | yes — at Phase 7 |

Phases 1-2 each satisfy the boundary test independently. Phase 3 alone fails coherence (a
re-verification sweep over content Phase 2's gate already proved green); it shares Phase 4's branch,
opening only once Phase 4 adds reviewable retest evidence. Phase 5 alone is a checkpoint confirming
`main` is green, shipping nothing new; it shares Phases 6-7's branch. Phase 6's triage is real but
small; Phase 7 re-verifies it as an archival precondition, so the three share one unit.

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

- [ ] [AI] Enter/provision the worktree and install dependencies: `npm install` — acceptance: exits 0.
- [ ] [AI] Converge the toolchain: `npm run doctor -- --fix` — acceptance: exits 0.
- [ ] [AI] **Precondition 1** — confirm navigation-ui is merged:
      `gh pr list --search "ayokoding-learning-path-03-navigation-ui" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1.
- [ ] [AI] **Precondition 2** — confirm the `vercel-function-cost-reduction` `ayokoding-www` unit is
      merged:
      `gh pr list --search "vercel-function-cost-reduction" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1.
- [ ] [AI] **Precondition 3 (this plan's own start-precondition edge)** — confirm the sibling plan's
      Phase 1 (interview-ready) delivery unit has merged:
      `gh pr list --search "ayokoding-learning-path-12-careers-se-manifests phase-1-interview-ready" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1. Falsifiable both ways: returns `0` while that delivery unit is
      still open, in which case this phase **blocks** — this plan does not proceed on an assumption
      that the sibling's Phase 1 "should" be done by now.
- [ ] [AI] **Precondition 4** — confirm the six net-new AI-engineer-role courses (or at least enough of
      them for Phase 1's GREEN step) exist:
      `gh pr list --search "ayokoding-learning-path-04-course-authoring" --state merged --json number --jq 'length'`
      returns a value ≥ 1 for its Phase-1 delivery unit **or**
      `find <COURSES> -maxdepth 1 -mindepth 1 -type d -name 'evaluating-ai-output-essentials' | wc -l`
      returns **1** — acceptance: at least one of the two holds.
- [ ] [AI] **Precondition 5** — confirm the manifest repository and directory exist:
      `test -f <FEAT>shell/manifest-repository.ts && test -d <MANIFESTS>` — acceptance: exits 0.
- [ ] [AI] **Precondition 6** — confirm the 11 named SWE-fundamentals courses already resolve (these are
      existing library courses, not net-new authoring):
      `for id in just-enough-python software-testing cicd-and-release-engineering backend-at-scale containers-and-orchestration computer-architecture site-reliability-engineering data-engineering data-structures-and-algorithms-essentials software-product-engineering frontend-essentials; do test -d <COURSES>$id || echo "MISSING:$id"; done`
      — acceptance: prints nothing (all 11 resolve). If any print, this plan's Phase 1 GREEN step
      transcribes only the subset that resolves and records the rest as a documented gap, closed later
      by the six-source-plan growth this plan's sibling processes for the general library (this
      manifest's own Phase 2 growth covers only the 9-course harness cluster, not these 11).
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build`, `:test:unit`,
      `ayokoding-www-fe-e2e:test:e2e` — acceptance: all exit 0; record pass counts in
      `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Manifest baseline snapshot** —
      `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` — acceptance: exits non-zero
      (the file does not exist yet); recorded in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Hub baseline snapshot** —
      `grep -cF '/en/learn/paths/careers/immediately-effective/ai-engineer' <PATHS>_index.md` —
      acceptance: returns **0**; recorded.
- [ ] [AI] Resolve every preexisting failure before proceeding.
- [ ] [AI] Confirm `learnings.md` scaffold exists.

### Phase 0 Gate

- [ ] [AI] `npm install` and `npm run doctor -- --fix` exit 0.
- [ ] [AI] Preconditions 1-3 and 5-6 all hold; precondition 4 holds via at least one of its two checks.
- [ ] [AI] Baselines recorded green; zero preexisting failures unresolved.
- [ ] [AI] This plan's one manifest path recorded absent; its intended href recorded absent.
- [ ] [AI] **No PR opened, nothing pushed** —
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

> **Pause Safety**: only the toolchain was verified and the current state snapshotted; the sibling
> plan's Phase 1 merge was confirmed rather than assumed. Safe to stop indefinitely. To resume: re-run
> the six precondition checks and the baselines.

---

## Phase 1: Author the AI-engineer manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker` + `web-researcher`._
>
> **Authoring priority #1** (DD-27), immediately behind the sibling plan's smoke-test MVP. This
> manifest is **from-scratch** (DD-35): its SWE-fundamentals prerequisites are **included** at the head
> of `courseOrder`, not linked out. Per DD-33 (still holding in scope) `courseOrder` also **walks**,
> never links, the existing nine-course AI/harness cluster — deliberately deferred here to
> [Phase 2](#phase-2-manifest-growth-to-the-full-harness-cluster-walk), recorded as a documented gap.

### 1.1 · TDD cycle — publish the manifest data file

- [ ] [AI] **RED** — create `<MANIFESTS>careers/careers-ai-manifest.unit.test.ts` _(new file)_ with a
      failing assertion that `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` loads,
      zod-validates, and contains the 11 named SWE-fundamentals course IDs **at the head of**
      `courseOrder` — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails because the
      manifest file does not exist. Also create `<SPECS>path-composition.feature` _(new file)_ with the
      scenario below, and a matching failing step in
      `apps/ayokoding-www-fe-e2e/src/steps/path-composition.steps.ts` _(new file)_ — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails.

  **Gherkin (binds) →** "The AI-engineer path includes its software-engineering prerequisites instead
  of linking them"

  ```gherkin
  Scenario: The AI-engineer path includes its software-engineering prerequisites instead of linking them
    Given the careers/immediately-effective/ai-engineer path manifest is published
    When a reader with no prior software-engineering competence inspects its courseOrder
    Then the shared software-engineering-fundamentals courses this path's AI-specific spine depends on are present at the head of courseOrder, ordered prerequisite-consistently
    And that reader can start at courseOrder[0] and finish the whole path from this one manifest, with no external prerequisite link required
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` _(new file)_
      with `pathId: careers/immediately-effective/ai-engineer`, a `title`, a `description`, and
      `courseOrder` whose **head** is the prerequisite-consistent ordering of the 11 named
      SWE-fundamentals courses — transcribed verbatim (never re-derived) from
      [`manifest-immediately-effective-ai-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-ai-engineer.md)'s
      Stage 0 — **followed by** the six net-new AI-engineer-role courses in order (light eval gate →
      statistics for evals → deep evals → product patterns for probabilistic systems → inference
      serving and model deployment → fine-tuning and adaptation) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND all 11 SWE-fundamentals IDs are
      present —
      `grep -oE 'just-enough-python|software-testing|cicd-and-release-engineering|backend-at-scale|containers-and-orchestration|computer-architecture|site-reliability-engineering|data-engineering|data-structures-and-algorithms-essentials|software-product-engineering|frontend-essentials' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      returns **11 or more**, AND all six AI-engineer-role IDs are present —
      `grep -oE 'evaluating-ai-output-essentials|statistics-for-evaluation|evaluating-ai-systems-in-depth|product-patterns-for-probabilistic-systems|inference-serving-and-model-deployment|fine-tuning-and-adaptation' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      returns **6**, AND `checkPrerequisiteConsistency` passes over the combined order (the automated
      topological check, not a manual grep, is authoritative for inter-course ordering).
- [ ] [AI] **REFACTOR** — record inline in the YAML, as a comment, that the nine AI/harness-cluster IDs
      are deliberately absent pending Phase 2 growth, naming the phase — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0
      and the presence checks above still hold.

### 1.2 · The landing anchor (content — maker/checker/fixer)

- [ ] [AI] Author `<PATHS>careers/immediately-effective/ai-engineer/_index.md` _(new file)_ — prose and
      SEO only, framing the path as **from-scratch**: no prior software-engineering competence assumed,
      and the SWE-fundamentals courses a reader needs are already the first courses in this path's own
      `courseOrder` — acceptance: the landing describes the path's endpoint (**building AI systems**)
      without naming or assuming an already-working-software-engineer starting persona —
      `grep -c -i 'already[- ]working\|transitioning\|role transition\|switcher' <PATHS>careers/immediately-effective/ai-engineer/_index.md`
      returns **0** — and contains no `courseOrder` key.
- [ ] [AI] Run `apps-ayokoding-www-link-checker` + `apps-ayokoding-www-general-checker`; apply the
      matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero remain on re-run.
- [ ] [AI] **A8 clean-room licensing self-check** — acceptance: sources consulted and an explicit
      originality statement recorded in this checklist.
- [ ] [AI] Populate this plan's **one** paths-hub card (`AI Engineer` — endpoint-named, not
      `SWE → AI Engineer`, since the path no longer assumes a starting role) in `<PATHS>_index.md` —
      acceptance:
      `grep -cF '/en/learn/paths/careers/immediately-effective/ai-engineer' <PATHS>_index.md` returns
      **1** (this href specifically, not a whole-file count, since the sibling plan edits the same
      shared file concurrently).

### 1.3 · Verification and from-scratch smoothness audit

- [ ] [AI] Verify path-aware nav end-to-end: routing resolves, the manifest loads,
      `?path=careers/immediately-effective/ai-engineer` context propagates, prev/next walks the order,
      breadcrumb shows the path, course pages show prerequisites — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: passes in `en`.
- [ ] [AI] **Record the build-order assertion (documentation-verified, not harness-executable).**
      Confirm by reading this checklist that this plan's Phase 1 begins only after the sibling plan's
      interview-ready delivery unit has merged (Phase 0's precondition 3), and that it precedes the
      sibling plan's `immediately-effective/software-engineer` and `fundamentally-strong/software-engineer`
      phases — acceptance: this ordering is stated here in writing. This is a build-order claim about
      the programme's own delivery sequence across two plan folders; no test harness can execute it.
      **This scenario intentionally does not land in `<SPECS>path-composition.feature`** — it has no
      step binding and never will one.

  **Gherkin (documentation-verified) →** "This plan's authoring begins only once the sibling plan's
  interview-ready delivery unit has merged" — a deliberate third tag form: neither `(binds)` nor
  `(underpins)` fits, since this scenario will never have a step definition and is not a pure-core unit
  test either.

  ```gherkin
  Scenario: This plan's authoring begins only once the sibling plan's interview-ready delivery unit has merged
    Given the careers/interview-ready/software-engineer MVP (owned by ayokoding-learning-path-12-careers-se-manifests) has merged its delivery unit to origin/main
    When this plan's Phase 0 checks its start precondition
    Then the merged-PR check for that delivery unit returns a non-zero count
    And this plan's Phase 1 authoring begins only after that check passes
  ```

- [ ] [AI] **Progression smoothness audit (from-scratch-first)** — walk the manifest order and confirm
      prereq-chaining holds, monotonic-ish difficulty holds, and the light-eval-gate versus deep-evals
      scope boundary is not itself a smoothness break — acceptance: all assessable levers verified; any
      regression fixed by softening or bridging in place, never reordering.

### Phase 1 Gate

- [ ] [AI] `find <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | wc -l` returns **1**.
- [ ] [AI] The six-AI-member check returns **6**; the SWE-fundamentals-presence check returns **11 or
      more**.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` +
      `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] The hub-card href check returns **1**; the persona-language leak check returns **0**.
- [ ] [AI] The build-order assertion is recorded in writing, with its non-executability stated.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the AI-engineer path is live end-to-end in production over its smoke-test-scoped
> starting composition — the included SWE-fundamentals prerequisites plus whichever AI-engineer-role
> courses exist by this point. DD-27's authoring priority #1 is delivered. Safe to stop indefinitely. To
> resume: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 2: Manifest growth to the full harness-cluster walk

> **Trigger**: each of the two contributing course-authoring successor plans' own band-completion
> signal. Processed as each arrives — the two signals may land in either order.

### 2.1 · Growth from `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` (8 of 9 cluster courses)

- [ ] [AI] Record the manifest's entry count immediately before this step —
      `grep -cE '^ *- [a-z0-9-]+' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` — save to
      `evidence/phase-2-pre-growth-count.txt` (the falsifiable "before" half of this phase's
      before/after check).
- [ ] [AI] On that plan's signal landing, insert the eight cluster course IDs it authored (per its own
      `GROW_MANIFESTS` field, naming this manifest by full path) into
      `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` at their correct topological
      positions — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND those eight
      IDs are present.

### 2.2 · Growth from `ayokoding-learning-path-11-course-authoring-capstones` (9th/final cluster course)

- [ ] [AI] On that plan's signal landing, insert `capstone-build-your-own-coding-agent` at its correct
      topological position (after all eight prerequisite cluster courses) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND all nine cluster IDs are now
      present —
      `grep -oE 'creating-ai-powered-apps|agentic-ai|browser-automation-with-cdp|the-agent-loop|agent-tools-and-mcp|agent-context-and-memory|agent-permissions-and-sandboxing|agent-orchestration-subagents-and-observability|capstone-build-your-own-coding-agent' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      returns **9**, AND the entry count grew by **exactly 9** over the recorded pre-growth count —
      `grep -cE '^ *- [a-z0-9-]+' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` minus the
      value in `evidence/phase-2-pre-growth-count.txt` equals **9**.
- [ ] [AI] Confirm the SWE-fundamentals **inclusion** survived the growth — command:
      `grep -oE 'just-enough-python|software-testing|cicd-and-release-engineering|backend-at-scale|containers-and-orchestration|computer-architecture|site-reliability-engineering|data-engineering|data-structures-and-algorithms-essentials|software-product-engineering|frontend-essentials' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      — acceptance: still returns **11 or more**.

### 2.3 · TDD cycle — the full harness-cluster walk is asserted, not merely present

- [ ] [AI] **RED** — extend the test file with a persisted assertion that all nine cluster IDs are
      present in `courseOrder` **and** appear strictly after every SWE-fundamentals ID and every
      AI-engineer-role ID — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails before
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

- [ ] [AI] **GREEN** — implement the persisted assertion — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0.
- [ ] [AI] **REFACTOR** — fold the assertion into the same table-driven shape the SWE-fundamentals and
      AI-engineer-role checks use — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0.

### Phase 2 Gate

- [ ] [AI] Both source-plan signals processed; `test:unit` exited 0 after each.
- [ ] [AI] The nine-cluster-ID check returns **9**; the entry-count delta equals **9**.
- [ ] [AI] The SWE-fundamentals inclusion check still returns **11 or more**.
- [ ] [AI] The persisted walk-order assertion (2.3) passes.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:test:unit` + `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: this plan's manifest is at its **full** composition — the included SWE-fundamentals
> set, the six AI-engineer-role courses, and the full nine-course AI/harness cluster walk. No manifest
> truncation remains. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:build && npx nx run ayokoding-www:test:unit`.

---

## Phase 3: Section and app verification

**Gherkin (underpins, aggregate) →** "This plan's AI-engineer manifest layer builds and validates
green" ([prd.md](./prd.md#acceptance-criteria-gherkin)) — this scenario has no dedicated
`<SPECS>path-composition.feature` step binding; it is closed by the combination of the build, the
affected test tiers, and the manifest-integrity + prerequisite-consistency sweep below, all four run
together every time this phase's gate is checked.

- [ ] [AI] Run affected quality gates: `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones.
- [ ] [AI] Run e2e: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0.
- [ ] [AI] Build: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Link + heading + markdown validation:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content` +
      `... md heading-hierarchy validate` + `npm run lint:md` — acceptance: the link validator prints
      `All links valid! No broken links found.`; the other two exit 0.
- [ ] [AI] **Manifest-integrity + prerequisite-consistency sweep** for this plan's one manifest —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: zero violations.
- [ ] [AI] **From-scratch smoothness re-check** — acceptance: passes; regressions fixed in place.
- [ ] [AI] **Ownership boundary check (scoped to this plan's one file)** —
      `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` — acceptance: exits 0. A
      presence check on this plan's own one file, not a directory-wide count — a directory-wide count
      would be affected by how many of the sibling plan's three manifests have landed, which this
      plan's own gate must not depend on.
- [ ] [AI] **Scoped cross-plan link check** —
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-13-careers-ai-manifest"`
      — acceptance: no matching line (exit 1).

### Phase 3 Gate

- [ ] [AI] Affected `typecheck`/`lint`/`test:quick`/`test:unit`/`specs:behavior:coverage` exit 0;
      `ayokoding-www-fe-e2e:test:e2e` exits 0.
- [ ] [AI] Build + link + heading + markdown validation green.
- [ ] [AI] Manifest integrity + prerequisite-consistency + smoothness report zero violations.
- [ ] [AI] This plan's own manifest file present.
- [ ] [AI] Scoped cross-plan link check finds no line naming this plan's folder.
- [ ] [AI] Work committed to this delivery unit's branch; nothing pushed for review yet — the unit's PR
      opens only at Phase 4.

> **Pause Safety**: this plan's one-path composition passes every automated gate. Safe to stop
> indefinitely. To resume: re-run the affected quality gates and the build.

---

## Phase 4: Manual UI verification and Rule-15 three-tester retest

> This plan ships one user-visible path landing plus its own one-card slice of the paths hub, so the
> **Rule-15 three-tester retest is mandatory**, scoped to this plan's own surfaces.

- [ ] [AI] Confirm `en` is the only content locale — command:
      `test -d <PATHS> && test ! -d apps/ayokoding-www/content/id/belajar/paths` — acceptance: exits 0.
- [ ] [AI] Start the dev server: `npx nx dev ayokoding-www`.
- [ ] [AI] For `en` × breakpoints (375/768/1280px), via Playwright MCP: open the paths hub, confirm this
      plan's one card renders correctly inside the category-grouped `careers/` group, then this plan's
      one landing, walking 2-3 courses via prev/next confirming `?path=` persists — acceptance: all
      correct at all three breakpoints.
- [ ] [AI] For this landing specifically, confirm the **included** SWE-fundamentals prerequisite
      courses render as ordered path steps and that each one's canonical page resolves — acceptance:
      the landing renders all 11 named SWE-fundamentals courses as `courseOrder` steps, and every
      `/en/learn/courses/<id>` link the landing emits returns 200.
- [ ] [AI] Verify `html[lang]` is `en` and console is clean on every screen — acceptance: both hold.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-4-<screen>-en-<breakpoint>px.png` — acceptance:
      `find evidence -name 'phase-4-*-en-*px.png' | wc -l` returns **6** (2 screens — hub plus this
      plan's 1 landing — × 3 breakpoints).
- [ ] [AI] Run `web-exploratory-tester` + `web-usability-tester` + `web-design-tester` against the hub
      and this plan's one landing — acceptance: findings recorded.
- [ ] [AI] Append each finding as a new unchecked checkbox (`EWT-NNN`/`UWT-NNN`/`DWT-NNN`).

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every defect finding must be fixed and ticked before
      archival)_

### Phase 4 Gate

- [ ] [AI] Hub (this plan's 1 card) + 1 landing + prerequisite display verified in `en` at all three
      breakpoints; console clean.
- [ ] [AI] `find evidence -name 'phase-4-*-en-*px.png' | wc -l` returns **6**.
- [ ] [AI] Every Rule-15 defect finding is fixed and ticked, or explicitly permitted to defer.
- [ ] [AI] Draft PR opened for Phases 3-4; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed.

> **Pause Safety**: this plan's one-path UI is verified live and defect-clean in `en`, with committed
> evidence. Safe to stop indefinitely. To resume: re-run the three testers against the running app.

---

## Phase 5: Final origin main integration and CI verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-13-careers-ai-manifest" --state open --json number --jq 'length'`
      — acceptance: returns **0**.
- [ ] [AI] Sync to latest `origin/main`: `git fetch origin && git checkout main && git pull`. Run
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`,
      `npx nx run ayokoding-www-fe-e2e:test:e2e`, and `npx nx run ayokoding-www:build` — acceptance:
      all exit 0.
- [ ] [AI] Monitor the final `main` CI run (poll every ~2 minutes, never `gh run watch`) — acceptance:
      all green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves this plan's one path landing and its hub card —
      acceptance: production serves the path.

### Phase 5 Gate

- [ ] [AI] Zero open plan PRs; full affected suite + e2e + build green on the integrated `main`.
- [ ] [AI] `prod-ayokoding-www` serves this plan's path and its hub-card slice.
- [ ] [AI] Work committed to this delivery unit's branch; nothing pushed for review yet — the unit's PR
      opens only at Phase 7.

> **Pause Safety**: this plan's own product is integrated on `main`, green in CI, and live in
> production. Safe to stop indefinitely. To resume: re-run the affected suite and check CI/prod.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the secret/sensitivity gate to every surviving entry.
- [ ] [AI] Apply the repo-relevance gate.
- [ ] [AI] Route each surviving learning to exactly one durable home — code homes are ALWAYS filed as a
      separate `plans/backlog/<slug>/` plan, never landed inline.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>`.

### Phase 6 Gate

- [ ] [AI] Every `learnings.md` entry is terminal, or the file records the explicit "none" escape.
- [ ] [AI] No code-homed learning landed inline.
- [ ] [AI] Work committed to this delivery unit's branch; the unit's PR opens only at Phase 7.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`.

---

## Phase 7: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify Knowledge Capture is complete.
- [ ] [AI] Verify ALL quality gates pass and the build is green.
- [ ] [AI] Verify ALL manual assertions pass with committed evidence.
- [ ] [AI] Verify every Rule-15 defect finding is fixed.
- [ ] [AI] **Terminal single-manifest assertion (this plan's own scope — not the four-manifest,
      127-catalog check, which is the sibling plan's own final-phase responsibility)** — verify this
      plan's one manifest is published at full composition, its landing is live, and its hub card is
      present:
      `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` returns 0, AND
      `grep -cF '/en/learn/paths/careers/immediately-effective/ai-engineer' <PATHS>_index.md` returns
      **1**, AND `npx nx run ayokoding-www:test:unit` exits 0 — acceptance: all three hold.
- [ ] [AI] **Scoped cross-plan link check** — re-run Phase 3's filtered link validation and confirm it
      still finds no line naming this plan's folder.
- [ ] [AI] Move: `git mv plans/backlog/ayokoding-learning-path-13-careers-ai-manifest plans/done/YYYY-MM-DD__ayokoding-learning-path-13-careers-ai-manifest`.
- [ ] [AI] Update `plans/backlog/README.md` and `plans/done/README.md`.
- [ ] [AI] Update the sibling plan's cross-references to this plan's archived path, in the same commit —
      the sibling plan's Phase 8 start-condition check will need this plan's new archived location once
      it re-verifies its own merged-PR search.
- [ ] [AI] Commit: `chore(plans): move ayokoding-learning-path-13-careers-ai-manifest to done`.

### Phase 7 Gate

- [ ] [AI] This plan's one manifest published at full composition; hub card present; `test:unit` and
      `build` exit 0.
- [ ] [AI] The filtered link check finds no line naming this plan's folder.
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-13-careers-ai-manifest`.
- [ ] [AI] Draft PR opened for Phases 5-7; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed (no-op).

> **Pause Safety**: this plan is archived and its final PR `[AI]`-merged to `main`. Terminal state for
> this plan — the sibling plan's own final phase can now proceed once it detects this merge. To resume:
> nothing.

---

## Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically; Conventional Commits; split domains/concerns; preexisting fixes
      get their own commits; never bundle unrelated changes.

## Local Quality Gates (before every push)

- [ ] [AI] `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` exits 0.
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 for any phase touching the manifest or
      landing.
- [ ] [AI] Fix ALL failures, including preexisting ones (Root Cause Orientation).
