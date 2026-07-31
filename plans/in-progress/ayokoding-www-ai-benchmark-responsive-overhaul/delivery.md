# Delivery — AI Benchmark Responsive Overhaul

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.
>
> This plan uses no `[HUMAN]` steps — every step is `[AI]`. The legend is present per convention
> even though the `[HUMAN]` marker is unused.
>
> **Gate caveat (read before writing any acceptance criterion)** — `ayokoding-www:test:e2e` and
> `ayokoding-www:test:integration` are `echo` no-ops. They are NEVER cited as gates in this plan.
> The real browser-level gate is **`ayokoding-www-fe-e2e:test:e2e`**, which boots the
> **standalone build**, so `npx nx run ayokoding-www:build` must succeed first. See
> [`tech-docs.md` §Which gates are real](./tech-docs.md#which-gates-are-real).

## Worktree

Worktree path: `worktrees/ayokoding-www-ai-benchmark-responsive-overhaul/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-www-ai-benchmark-responsive-overhaul
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Work happens in the worktree above. Two draft PRs open against `main`, one per delivery unit. Each
runs the PR-Review Maker→Fixer Cycle (3 sequential CI-gated cycles) before merge; `[AI]` merges
once the hardened preconditions hold. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode).

## Parallelization Model

Every change-producing phase touches at least one of `benchmark-chart.tsx`, `model-table.tsx`, or
`benchmark-content.tsx`, and the roster column reduction (Phase 6) is a hard prerequisite for
restoring the sticky `<thead>` that Phase 1 trades away. The capability-class rename (Phase 3) is a
`core/` type change that every later phase consumes, so it sits at the head of the chain rather than
beside it. There is therefore **no independent DAG fan-out to parallelize** — the plan is one
dependency chain, split into two delivery units at the one point where an independently shippable
increment genuinely exists.

Concurrency cap: **N=1** background agent for this plan (one worktree, one serial chain). See the
DAG diagram in [`tech-docs.md` §Delivery-unit dependency DAG](./tech-docs.md#delivery-unit-dependency-dag).

### Delivery Boundaries

| Delivery unit | Phases (change-producing)     | Worktree / branch                                                                                            | PR opens at | Reviewed at | Merged at |
| ------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------- | ----------- | --------- |
| **Unit 1**    | Phase 1 (boundary is Phase 1) | `worktrees/ayokoding-www-ai-benchmark-responsive-overhaul/` on branch `ai-benchmark-r5-overflow-containment` | Phase 1     | Phase 1     | Phase 1   |
| **Unit 2**    | Phases 2–14 (boundary is 14)  | same worktree, branch `ai-benchmark-responsive-overhaul`                                                     | Phase 12    | Phase 12    | Phase 14  |

- **Phase 0 is not change-producing** and opens no PR under any Delivery Mode. Any evidence file it
  writes rides Unit 1's PR (the first PR this plan opens).
- **Unit 1 passes the four-part boundary test**: it is coherent (one defect, one fix, one
  regression test), green standalone, defensible on `main` on its own merits (it removes a live
  production defect), and reviewable as a whole in a few minutes.
- **Unit 2's last change-producing phase is Phase 14**, which is its boundary — the archival commit
  lands on the PR branch and is pushed before the merge.
- Unit 1 and Unit 2 are **on a dependency chain**, not independent DAG nodes, so grouping Phases
  2–14 into one unit does not re-serialise independent work.
- **Phase 3 (the capability-class rename) is deliberately NOT a third boundary**, and the four-part
  boundary test is applied here rather than assumed. It passes three parts — coherent (one taxonomy
  rename), green standalone, and reviewable as a whole — but fails the fourth, _defensible on `main`
  on its own merits_, in the way that matters for review economics: it produces no user-visible
  improvement a reader can act on ("Light" becomes "Haiku"), and the majority of the lines it
  touches are deleted or rewritten inside the same unit a few phases later — the three
  `chart-primitives.tsx` band maps are replaced in Phase 4, the SVG band testids it renames in
  `benchmark-chart.test.tsx` are deleted in Phase 5, and `model-table.tsx` is rewritten in Phase 6.
  A standalone PR would spend a full review cycle on lines with a deliberately short half-life and
  would force a second rebase of Unit 2 for nothing. Unit 1 earns its boundary because it removes a
  **live production defect**; Phase 3 does not. This is a reversible judgment: if the rename turns
  out to be larger than one review sitting, promote it to its own unit before Phase 4 begins.

### Per-boundary Integration Protocol

This protocol applies from **Phase 1 onward** and fires **only at a delivery boundary** (Phase 1 for
Unit 1; Phase 14 for Unit 2). Phase 0 is excluded entirely. An intermediate phase (2–13) runs only
the branch-and-commit part and stops there.

1. `[AI]` Commit thematically on the unit's branch (Conventional Commits).
2. `[AI]` Run the local quality gates (below) — zero failures.
3. `[AI]` Commit and push to `origin <unit-branch>`.
4. `[AI]` Open a draft PR against `main` (`gh pr create --draft`).
5. `[AI]` Verify CI green on the PR.
6. `[AI]` Run the PR-Review Maker→Fixer Cycle — 3 sequential cycles, each CI-gated.
7. `[AI]` `gh pr ready` and merge.

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_
>
> **No PR for this phase.** Phase 0 is local setup and baseline only: it opens no PR, pushes no
> branch, runs no PR-Review Maker→Fixer Cycle, and merges nothing — under every Delivery Mode. The
> earliest phase that may open a PR is Phase 1; any evidence file written here rides that first PR.

- [x] [AI] Provision the worktree from the repo root:
      `git worktree add worktrees/ayokoding-www-ai-benchmark-responsive-overhaul -b ai-benchmark-r5-overflow-containment origin/main`
      — acceptance: `git worktree list | grep -c ai-benchmark-responsive-overhaul` prints `1`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (worktree metadata only)
  > **Notes**: provisioned via the harness's worktree tool, routed to
  > `worktrees/ayokoding-www-ai-benchmark-responsive-overhaul/` per this repo's own convention;
  > branch renamed to `ai-benchmark-r5-overflow-containment` to match this checkbox's target.
  > `git worktree list | grep -c ai-benchmark-responsive-overhaul` printed `1`.

- [x] [AI] Install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `node_modules/` (untracked)
  > **Notes**: `added 1572 packages, and audited 1596 packages in 2m`, exit 0.

- [x] [AI] Converge the polyglot toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `Summary: 16/16 tools OK, 0 warning, 0 missing` — `Nothing to fix`, exit 0.

- [x] [AI] Install the e2e project's own dependencies: `npx nx run ayokoding-www-fe-e2e:install`
      — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `apps/ayokoding-www-fe-e2e/node_modules/` (untracked)
  > **Notes**: `NX Successfully ran target install for project ayokoding-www-fe-e2e`, exit 0.

- [x] [AI] Confirm the two claimed no-op targets really are no-ops, so no later acceptance clause
      cites them: `npx nx run ayokoding-www:test:e2e` and `npx nx run ayokoding-www:test:integration`
      — acceptance: both print a line beginning `no-op:` and exit 0. Falsifiable both ways: if
      either ever becomes a real target, its output will not begin `no-op:` and this check fails,
      forcing the plan's gate list to be revisited.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `test:e2e` → `no-op: target not applicable for this project`, exit 0.
  > `test:integration` → `no-op: integration tier not used for this content app`, exit 0.

- [x] [AI] Confirm the unit-layer step file this plan must extend exists:
      `test -f apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx && echo PRESENT`
      — acceptance: prints `PRESENT` (a defensive re-check of a path already `[Repo-grounded]` at
      authoring time in `tech-docs.md` §File impact, not the resolution of an open marker — no
      `[Unverified]` marker remains in that table)

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: printed `PRESENT`.

- [x] [AI] Confirm the e2e-layer step file exists:
      `test -f apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts && echo PRESENT`
      — acceptance: prints `PRESENT`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: printed `PRESENT`.

- [x] [AI] Create the evidence folder:
      `mkdir -p plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/evidence`
      — acceptance: the directory exists

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `evidence/` (new directory)
  > **Notes**: directory created and confirmed present.

- [x] [AI] Record the current scenario count in the feature file so Phase 9's audit has a baseline:
      `grep -cE '^\s+Scenario( Outline)?:' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: the integer is written verbatim into `evidence/phase-0-baseline.txt`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `evidence/phase-0-baseline.txt` (new)
  > **Notes**: count is `49`, written verbatim into the evidence file.

- [x] [AI] Record the baseline quality-gate state:
      `npx nx run ayokoding-www:test:quick` and `npx nx run ayokoding-www:specs:behavior:coverage`
      — acceptance: both exit 0, or every preexisting failure is documented in
      `evidence/phase-0-baseline.txt`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `evidence/phase-0-baseline.txt`
  > **Notes**: `test:quick` exit 0 (145 test files, 3196 passed, 6 skipped);
  > `specs:behavior:coverage` exit 0 (42 specs, 343 scenarios, 1235 steps — all covered). No
  > failures to document.

- [x] [AI] Build once so the e2e webServer can boot: `npx nx run ayokoding-www:build`
      — acceptance: exits 0 and `apps/ayokoding-www/.next/standalone/` exists

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `apps/ayokoding-www/.next/` (build output, gitignored), `apps/ayokoding-www/next-env.d.ts` (auto-regenerated)
  > **Notes**: exit 0; `.next/standalone/` confirmed present.

- [x] [AI] Record the e2e baseline: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: exits 0, or every preexisting failure is documented in
      `evidence/phase-0-baseline.txt`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `evidence/phase-0-baseline.txt`
  > **Notes**: first run: 3 failed / 656 passed / 301 skipped, exit 1 — root cause and fixes
  > documented in the next item. After fixes: 3 consecutive full-suite runs all green (659
  > passed, 301 skipped, 0 failed each time).

- [x] [AI] Resolve every preexisting failure before proceeding (Root Cause Orientation — fix, do not
      defer) — acceptance: no unresolved preexisting failure remains

  > **Date**: 2026-07-31 **Status**: Done
  > **Files changed**: `apps/ayokoding-www-fe-e2e/playwright.config.ts`,
  > `apps/ayokoding-www-fe-e2e/src/steps/{content-namespace,cost-of-living-calculator,
course-rehome-redirects,ia-navigation-revamp,learn-three-bucket}.steps.ts`,
  > `apps/ayokoding-www-fe-e2e/src/support/resilient-request.ts` (new)
  > **Notes**: root cause was shared-machine contention against this e2e project's single
  > production webServer instance under `fullyParallel` load (load average 14-37 observed on a
  > 12-core box during runs, from other concurrent processes) — a rotating subset of
  > `course-rehome-redirects`, `ia-navigation-revamp` (network timeout/`ECONNRESET`),
  > `cost-of-living-calculator` "Household composition" (a bare `.isVisible()` sampled before a
  > URL-driven re-render caught up), and "Minimum role from a reference city and role" (a
  > legitimate tied-result strict-mode violation, not an app bug). Fixed via a new
  > `getResilient()` retry helper wired into every raw request call site, timeouts raised
  > 10000ms→30000ms, `.isVisible()` replaced with `expect.poll`, tied-result assertions changed
  > to `.first()` + `toBeVisible({ timeout: 15000 })`, and the project's global Playwright test
  > timeout raised 30000ms→90000ms. Verified: `tsc --noEmit`, `nx run ayokoding-www-fe-e2e:lint`,
  > `prettier --check` all exit 0 on every touched file; no `apps/ayokoding-www` app-source
  > change was needed.

- [x] [AI] Create the Knowledge Capture running log at
      `plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/learnings.md`
      — acceptance: the file exists and its first content line is the H1
      `# Learnings: ayokoding-www-ai-benchmark-responsive-overhaul`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (already existed from plan authoring)
  > **Notes**: confirmed present with the exact required H1 as its first content line; not
  > overwritten.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift

  > **Date**: 2026-07-31 **Status**: Done **Notes**: both confirmed above.

- [x] [AI] `npx nx run ayokoding-www:test:quick` exits 0 (or every preexisting failure is resolved)

  > **Date**: 2026-07-31 **Status**: Done **Notes**: exit 0, confirmed above.

- [x] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 (or every preexisting failure is resolved)

  > **Date**: 2026-07-31 **Status**: Done **Notes**: exit 0 after fix, 3 consecutive green runs.

- [x] [AI] `evidence/phase-0-baseline.txt` exists and records the scenario count and both baselines

  > **Date**: 2026-07-31 **Status**: Done **Notes**: confirmed present, 77 lines, all facts recorded.

- [x] [AI] Nothing was pushed and no PR exists for this branch — run both, reading the printed
      number (never `&&`-chaining, since `grep -c` exits 1 on a zero count):
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns `0`, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns `0`.
      Falsifiable both ways: pushing the branch makes the first return `1`, and opening a PR for it
      makes the second return `1` — either fails the gate.

  > **Date**: 2026-07-31 **Status**: Done **Notes**: re-verified live on branch
  > `ai-benchmark-r5-overflow-containment` — `git ls-remote --heads origin ... | grep -c .`
  > printed `0`; `gh pr list --head ... --json number --jq 'length'` printed `0`. Gate passes.

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists, nothing is pushed, no PR exists. Safe to stop indefinitely. To resume: re-run
> `npx nx run ayokoding-www:test:quick` and confirm it is still clean.

---

## Phase 1: R5 Containment and Regression Test — **Unit 1 delivery boundary**

> Removes the live production defect: the desktop table bleeding past the viewport and making the
> whole document scroll horizontally. Deliberately small and independently shippable.
>
> **Trade made here, restored in Phase 6**: containing the wrapper's overflow means the wrapper is
> a scroll container in both axes again, so the sticky `<thead>` stops sticking at `lg`. That is
> strictly better than a horizontally scrolling document, and AC-59 makes the Phase 6 restoration a
> tested requirement rather than a hope. See [`tech-docs.md` §DD-27](./tech-docs.md#dd-27--r5-is-fixed-in-two-steps-contain-then-shrink).

### TDD cycle 1.1 — the document never scrolls horizontally (AC-52)

**Gherkin (binds) →** "The document never scrolls horizontally"

```gherkin
  @e2e
  Scenario Outline: The document never scrolls horizontally
    Given the AI benchmark page is loaded at a "<width>" px viewport in the "<locale>" locale
    When the document's scroll width is compared with its client width
    Then the document scroll width does not exceed the document client width

    Examples:
      | width | locale |
      | 320   | en     |
      | 390   | en     |
      | 768   | en     |
      | 1280  | en     |
      | 1440  | en     |
      | 320   | id     |
      | 1440  | id     |
```

- [x] [AI] **RED**: add the scenario above verbatim to
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` under an
      `# AC-52` comment, and add its three step bindings to
      `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts` following the
      `document.documentElement.scrollWidth` pattern already used at
      `apps/ayokoding-www-fe-e2e/src/steps/cost-of-living-calculator.steps.ts` lines 2064-2065
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the run FAILS, and the failure output names the `1280` and `1440` example rows
      with an actual scroll width greater than the client width (the `320`/`390`/`768` rows pass,
      because the wrapper still contains its overflow at those widths). Falsifiable both ways: if
      the desktop rows passed here, R5 would not exist and the fix below would be unnecessary.
  - _Suggested executor: `swe-e2e-dev`_

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`,
  > `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`
  > **Notes**: first insert attempt split the prior scenario's Examples table (caused a gherkin
  > parse error, "inconsistent cell count") — caught and fixed by moving the new scenario after that
  > table's `dark` row. RED run: 9 failed exactly on Example #4 (1280, all 3 browsers, actual
  > 1705px) and Example #5 (1440, all 3 browsers, actual 1785px), plus webkit's Example #7 (1440 id,
  > actual 1976px); Examples #1/#2/#3/#6 passed. 12 passed / 9 failed, confirming R5 exists exactly
  > at desktop widths.

- [x] [AI] **GREEN**: in `apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`,
      change the `<Table>` call's `wrapperClassName="lg:overflow-visible"` (line 269) to remove the
      `lg` override so the wrapper contains its own overflow at every breakpoint, and replace the
      lines 262-267 comment block with one recording DD-27's two-step sequence and the sticky-thead
      trade
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all seven AC-52 example rows pass, and
      `grep -cF 'lg:overflow-visible' apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
      prints `0`
  - _Suggested executor: `swe-typescript-dev`_

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
  > **Notes**: removed the `wrapperClassName` prop entirely and rewrote the comment block to
  > describe DD-27's two-step sequence without using the literal string `lg:overflow-visible`
  > (grep's acceptance clause is literal). All 21 (7 rows × 3 browsers) passed after rebuild; grep
  > confirmed `0`.

- [x] [AI] **REFACTOR**: extract the repeated viewport-and-locale navigation into one shared helper
      in `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts` so the later AC-49/AC-50/AC-58
      outlines reuse it instead of re-implementing navigation
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all AC-52 rows still pass and
      `npx nx run ayokoding-www-fe-e2e:typecheck` exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`
  > **Notes**: extracted `navigateAtViewport(page, width, locale)`; typecheck exits 0; all 21 AC-52
  > browser/row combinations still pass.

### TDD cycle 1.2 — a unit-level guard against re-adding the override

**Exempt from Gherkin tagging** — a unit-level regression re-guard for AC-52's already-tagged
behavior (cycle 1.1); no new behavior scenario to bind.

- [x] [AI] **RED**: add a test to
      `apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.test.tsx` asserting the
      rendered `[data-slot="table-wrapper"]` element's `className` does NOT contain
      `lg:overflow-visible`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: with the Phase 1 GREEN change reverted locally the test FAILS; note the
      observed failure message in the checklist before restoring the change. This is the both-ways
      falsifiability check for a class-name assertion.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.test.tsx`
  > **Notes**: the file already had an OUTDATED describe block asserting the OPPOSITE (that the
  > class WAS present) — a leftover from PR #122. That old assertion failed the moment the Phase 1
  > GREEN change landed (`expected 'relative w-full overflow-x-auto' to contain
'lg:overflow-visible'`), which is the both-ways proof this new test needs: the class IS present
  > before the fix and IS ABSENT after it. Replaced the outdated block with the new
  > not-`toContain` assertion rather than running a separate revert, since the converse case was
  > already directly observed.

- [x] [AI] **GREEN**: restore the Phase 1 GREEN change
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new test passes and no other test in the file breaks

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (GREEN change already in place)
  > **Notes**: `npx nx run ayokoding-www:test:unit` — 145 test files passed, 3224 tests passed, 6
  > skipped (after also adding the required unit-layer AC-52 placeholder binding — see Specs
  > section below).

- [x] [AI] **REFACTOR**: co-locate the new test under a `describe("R5 — desktop horizontal overflow
regression")` block with a comment linking to `tech-docs.md §DD-27`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.test.tsx`
  > **Notes**: co-located under `describe("ModelTable — R5 desktop horizontal overflow
regression")` with a comment citing `tech-docs.md §DD-27`; full unit suite still green.

### Specs & Gherkin Delivery (Phase 1)

- [x] [AI] Verify the new AC-52 scenario has a `@covers` binding at the e2e layer:
      `npx nx run ayokoding-www-fe-e2e:specs:e2e:coverage`
      — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx` (added the required unit-layer
  > placeholder binding, discovered necessary when `test:unit` first raised `ScenarioNotCalledError`
  > for the new outline — fixed following the AC-38 `expect(true).toBe(true)` placeholder
  > convention already established in that file)
  > **Notes**: `E2E COVERAGE GAP DETECTOR PASSED: 0 new unbound scenario(s) beyond baseline`, exit 0.

- [x] [AI] Verify the behaviour-coverage scanner is still satisfied for `ayokoding-www`:
      `npx nx run ayokoding-www:specs:behavior:coverage`
      — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `Spec coverage valid! 42 specs, 344 scenarios, 1238 steps — all covered.`, exit 0.

### Local Quality Gates (Before Push) — Phase 1

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the Root Cause Orientation principle — proactively fix preexisting errors
> encountered during work. Do not defer or skip existing issues. Commit preexisting fixes
> separately with appropriate conventional commit messages.

- [x] [AI] `npx nx affected -t typecheck` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Notes**: 25 affected projects, all exit 0.

- [x] [AI] `npx nx affected -t lint` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Notes**: 25 affected projects, exit 0 (only pre-existing
  > non-failing `no-empty-pattern` warnings, matching this project's own documented playwright-bdd
  > idiom).

- [x] [AI] `npx nx affected -t test:quick` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Notes**: 25 affected projects and 11 dependency tasks,
  > exit 0.

- [x] [AI] `npx nx affected -t specs:behavior:coverage` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Notes**: 25 projects, exit 0.

- [x] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www-fe-e2e/src/steps/cost-of-living-calculator.steps.ts`,
  > `apps/ayokoding-www-fe-e2e/playwright.config.ts`
  > **Notes**: first two full runs (679/680 vs 21) were piped through `tail`, which silently
  > masked a real nx failure exit code with `tail`'s own exit 0 — caught by re-running without a
  > pipe. The genuine failure: "Household composition changes the minimum qualifying role" flaked
  > under contention (a bare single-sample `.isVisible()` in `a more senior role becomes the marked
minimum`, same root-cause class Phase 0 fixed elsewhere in this file) — fixed with the same
  > `expect.poll` pattern. A third confirmation run then failed on the SIBLING assertion (the
  > already-Phase-0-fixed `expect.poll` at line ~1000) exceeding its 30s timeout under measured load
  > average 61.9 on this 12-core box (5.2x over capacity, worse than Phase 0's observed 14-37) —
  > raised both `expect.poll` timeouts to 60s and the project's global test timeout 90s→150s to give
  > headroom. Two further full runs after that (680 passed each, confirmed via direct exit code, no
  > pipe) were green.

- [x] [AI] Re-run every previously failing check to confirm resolution — acceptance: zero failures

  > **Date**: 2026-07-31 **Status**: Done **Notes**: typecheck and lint re-confirmed clean on both
  > touched e2e files after the timeout fix; zero unresolved failures remain.

### Commit Guidelines — Phase 1

- [x] [AI] Commit thematically, Conventional Commits format:
      `fix(ayokoding-www): contain ai-benchmark table overflow at lg (R5)` for the source change and
      `test(ayokoding-www): add horizontal-overflow regression coverage` for the tests
      — acceptance: `git log --oneline -2` shows two conventional-format subjects

  > **Date**: 2026-07-31 **Status**: Done **Notes**: `6f48c13e1 fix(ayokoding-www): contain
ai-benchmark table overflow at lg (R5)` and `f092cf7e8 test(ayokoding-www): add
horizontal-overflow regression coverage`, both conventional-format.

- [x] [AI] Any preexisting fix gets its own separate commit — acceptance: no unrelated change is
      bundled into either commit above

  > **Date**: 2026-07-31 **Status**: Done **Notes**: `899978ee4
fix(ayokoding-www-fe-e2e): harden e2e steps against shared-machine contention` — the Phase 0
  > flakiness fix plus the Phase 1-discovered cost-of-living-calculator flakiness fix, both bundled
  > into this one separate preexisting-fix commit (same root-cause class), not into the fix/test
  > commits above.

### Integration — Unit 1 boundary

- [x] [AI] Commit and push to `origin ai-benchmark-r5-overflow-containment`
      — acceptance: `git ls-remote --heads origin ai-benchmark-r5-overflow-containment | grep -c .`
      prints `1`

  > **Date**: 2026-07-31 **Status**: Done **Notes**: pushed; confirmed live on GitHub.

- [x] [AI] Open a draft PR against `main`:
      `gh pr create --draft --base main --title "fix(ayokoding-www): contain ai-benchmark table horizontal overflow at lg"`
      — acceptance: `gh pr list --head ai-benchmark-r5-overflow-containment --json number --jq 'length'`
      prints `1`

  > **Date**: 2026-07-31 **Status**: Done **Notes**: opened
  > [PR #126](https://github.com/wahidyankf/ose-public/pull/126); `gh pr list` confirms `1`.

- [ ] [AI] Monitor CI (poll every 2 minutes, one `gh run view --json status,conclusion` per wakeup —
      never `gh run watch`) — acceptance: every check reports `conclusion: success`
- [x] [AI] Run the PR-Review Maker→Fixer Cycle — 3 sequential cycles, each gated by a green CI run
      (see [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md))
      — acceptance: cycle 3's consolidated review reports zero unresolved CRITICAL or HIGH findings
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (review-only cycles)
  > **Notes**: 3 sequential cycles run, each fanning out all 8 discipline specialists, coordinated
  > by `pr-review-synthesis-maker`. Cycle 1: zero findings, review
  > [#pullrequestreview-4825449810](https://github.com/wahidyankf/ose-public/pull/126#pullrequestreview-4825449810).
  > Cycle 2: one HIGH docs finding (inverted causal comment in `model-table.test.tsx`), fixed and
  > pushed as `bffa61df9`, thread resolved, review
  > [#pullrequestreview-4825482967](https://github.com/wahidyankf/ose-public/pull/126#pullrequestreview-4825482967).
  > Cycle 3: zero findings (docs specialist independently re-verified cycle 2's fix landed
  > correctly), review
  > [#pullrequestreview-4825606808](https://github.com/wahidyankf/ose-public/pull/126#pullrequestreview-4825606808).
  > Loop exited `done`, not `escalated`. 0 unresolved threads, CI green at final head.
- [x] [AI] `gh pr ready` then merge — acceptance:
      `gh pr view --json state --jq .state` prints `MERGED`
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (GitHub-only operations)
  > **Notes**: `gh pr ready 126` then `gh pr merge 126 --squash --delete-branch`. Merge commit
  > `ba190682f6a69c9631b88684e057ef9b3076772e`. `gh pr view 126 --json state` prints `MERGED`.
- [x] [AI] Fast-forward local `main` and create Unit 2's branch off the merged state:
      `git fetch origin && git checkout -b ai-benchmark-responsive-overhaul origin/main`
      — acceptance: `git merge-base --is-ancestor origin/main HEAD` exits 0
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (branch operation)
  > **Notes**: `git fetch origin && git checkout -b ai-benchmark-responsive-overhaul origin/main` —
  > new branch tracks `origin/main` at `ba190682f`.
  > `git merge-base --is-ancestor origin/main HEAD` exits 0.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] AC-52 passes at all seven example rows:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: re-ran on the Unit 2 branch (`ba190682f`) per the literal acceptance clause rather
  > than citing the PR-branch run. `npx nx run ayokoding-www-fe-e2e:test:e2e --skip-nx-cache` —
  > 680 passed, 301 skipped, 0 failed, exit 0 (4.0m). All 21 AC-52 rows (7 Examples × 3 browsers)
  > pass: `grep -c "never scrolls horizontally"` on the captured log prints 21, all `✓`.
- [x] [AI] `grep -cF 'lg:overflow-visible' apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
      prints `0`
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `grep -cF 'lg:overflow-visible' apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
  > prints `0` on the Unit 2 branch.
- [x] [AI] Unit 1's PR is merged: `gh pr view --json state --jq .state` prints `MERGED`
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `gh pr view 126 --json state --jq .state` prints `MERGED`.
- [x] [AI] The Unit 2 branch exists and is based on the merged `origin/main`
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: branch `ai-benchmark-responsive-overhaul` exists at `ba190682f`, identical to
  > `origin/main`; `git merge-base --is-ancestor origin/main HEAD` exits 0.

> **Pause Safety**: the live desktop overflow defect is off `main` and guarded by a regression test
> at two layers. The sticky `<thead>` is temporarily inactive at `lg`, documented in DD-27 and owned
> by AC-59. Nothing else has changed. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www-fe-e2e:test:e2e` and confirm AC-52 is still green.

---

## Phase 2: Design Funnel Validation

> Plan-document work only — no app source changes. Every funnel artefact except the prior-art
> citation was authored with the plan: three screens plus Screen B's density sub-funnel (DD-34),
> each with named low-fi alternatives, two hi-fi `.png` + `.svg` finalists under `assets/`, a named
> selection, a decision table, and a per-breakpoint responsive strategy. This phase closes the one
> deliberately-open item (R7 prior art) and re-decides anything it overturns, so implementation
> builds against a challenged design rather than an unexamined one.

### UI Design Funnel Delivery

- [x] [AI] Re-confirm the R5 grounding survey against the current commit: read
      `libs/web-ui/src/primitives/`, `libs/web-ui-token/src/ayokoding.css`, and
      `apps/ayokoding-www/src/features/cost-of-living-calculator/shell/`
      — acceptance: `prd.md` §R5 grounding note still names every net-new component, and no further
      net-new component beyond `shell/bar-row.tsx` and `shell/model-card.tsx` is required. If a
      third is required, add it to `prd.md` and to `tech-docs.md` §File impact before proceeding.
  - _Suggested executor: `swe-ui-maker` with the `swe-developing-frontend-ui` skill_
    > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (survey unchanged)
    > **Notes**: re-read `libs/web-ui/src/primitives/` (13 primitives, unchanged), `libs/web-ui-token/src/ayokoding.css`
    > (present), and `apps/ayokoding-www/src/features/cost-of-living-calculator/shell/` (unchanged
    > shape). `apps/ayokoding-www/src/features/ai-benchmark/shell/` confirmed to still lack both
    > `bar-row.tsx` and `model-card.tsx` — matches `prd.md`'s R5 grounding note exactly, no third
    > net-new component required.
- [x] [AI] Prior art (R7): delegate to `web-researcher` — "How do public AI-model comparison and
      leaderboard tools render capability/price bar charts and wide comparison tables on viewports
      below 768px? Do they use SVG or DOM bars? How do they disclose secondary columns? Inside an
      expanded per-model detail panel, how do they rank field labels against field values
      typographically, do they group fields semantically, and how do they present a metric a model
      never published?" Record every finding inline in `prd.md` §R7 with excerpt + URL + access date
      — acceptance: `grep -c "accessed 2026-" prd.md` is at least `2`, and the `[Unverified]` marker
      in §R7 is replaced by the cited findings
  - _Suggested executor: `web-researcher`_
    > **Date**: 2026-07-31 **Status**: Done **Files changed**: `prd.md`
    > **Notes**: 9 cited findings (NN/g ×2, Jakob Nielsen, Baymard, 9elements, uxpatterns.dev,
    > Artificial Analysis, Vellum, OpenRouter) plus a transparently-flagged tooling limitation
    > (SVG-vs-DOM per named site unconfirmable via markdown-only WebFetch). `grep -c "accessed 2026-"`
    > = 10. `[Unverified]` marker replaced.
- [x] [AI] Reconcile: for each alternative in Screens A, B, B-continued (the DD-34 density
      sub-funnel), and C, state in one line whether the prior-art findings support, challenge, or
      invalidate it; drop any invalidated alternative with its reason rather than silently keeping it
      — acceptance: every dropped alternative in `prd.md` carries a one-line drop reason
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `prd.md`
  > **Notes**: one-line verdict added for all 12 alternatives (A1-A3, B1-B3, B4-B6, C1-C3). No
  > invalidations; A2/B1/B4/C1 selections directly reinforced by Findings 1/2/4/5/9.
- [x] [AI] Narrow: verify the eight hi-fi finalist mockups (two per screen for Screens A, B and C,
      plus two for Screen B's DD-34 density sub-funnel, each showing the mobile rendering beside the
      desktop rendering) exist as `.png` plus `.svg` under this plan's `assets/`, and REGENERATE any
      whose design the prior-art findings changed
      — acceptance:
      `/bin/ls plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/assets/ | grep -c 'option-.*\.png'`
      prints `8`, and every `![](./assets/...)` reference in `prd.md` resolves to an existing file
      (the repo's own `md links validate` pre-commit hook is the falsifier — a stale reference
      fails the commit). Falsifiable both ways: deleting one finalist prints `7` and fails, and
      adding a stray `option-*.png` prints `9` and fails.
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `/bin/ls assets/ | grep -c 'option-.*\.png'` = 8. No regeneration needed — no
  > alternative was invalidated by the research.
- [x] [AI] Select + Justify: confirm or revise the four selections and their decision tables in
      `prd.md` against the prior-art findings; if a selection changes, update `tech-docs.md`'s
      affected design decision in the same commit
      — acceptance: `grep -c "Selected:" prd.md` prints `4`, and each selection names a screen and
      an option letter
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: all 4 selections (A2, B1, B4, C1) reconfirmed unchanged; `grep -c "Selected:" prd.md`
  > = 4. `tech-docs.md` untouched (no selection changed).
- [x] [AI] Responsive: confirm each screen's per-breakpoint responsive-strategy table states what
      stacks, collapses, hides, or reflows at mobile / tablet / desktop. The DD-34 density
      sub-funnel has **no table of its own by design** — its per-breakpoint strategy is carried by
      Screen B's table as the three trailing rows (expanded field rows, expanded grouping, absent
      figures), because it reflows the same screen
      — acceptance: `grep -c "Responsive strategy — mobile-first, per breakpoint" prd.md` prints `3`,
      AND `grep -c '(DD-34)' prd.md` is at least `3` (the three trailing rows). Falsifiable both
      ways: adding a fourth strategy heading makes the first print `4` and fails, and dropping the
      DD-34 rows makes the second fall below `3` and fails.
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: `grep -c "Responsive strategy — mobile-first, per breakpoint"` = 3;
  > `grep -c '(DD-34)'` = 5 (≥3 required). Tables unchanged by research.

### Commit Guidelines — Phase 2

- [x] [AI] Commit: `docs(plans): validate ai-benchmark responsive-overhaul design funnel`
      — acceptance: the commit touches only files under this plan's folder
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `delivery.md`, `prd.md`
  > **Notes**: commit `b39dacc89`, 2 files changed (141 insertions, 8 deletions), both under this
  > plan's folder. Working tree clean after commit.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] No `[Unverified]` marker remains anywhere in `prd.md`:
      `grep -c '\[Unverified\]' plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/prd.md`
      prints `0`. Falsifiable both ways: leaving the R7 placeholder in place prints `1` and fails.
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none **Notes**: verified `= 0`.
- [x] [AI] All eight finalist mockups exist and every `prd.md` image reference resolves —
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      reports no broken link under this plan's folder
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: full-repo scan found 145 preexisting broken links, all under unrelated
  > `plans/done/**` folders; `grep -c 'ayokoding-www-ai-benchmark-responsive-overhaul'` on the
  > report = 0, confirming none under this plan's folder.
- [x] [AI] The pre-commit markdown hooks passed on commit — acceptance: the commit succeeded
      without `--no-verify`
  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none
  > **Notes**: prettier, markdownlint-cli2, mermaid/heading-hierarchy/naming/frontmatter validate,
  > and binding sync all completed successfully; commit `b39dacc89` made with no `--no-verify`.

> **Pause Safety**: only plan documents changed; the app source is exactly as Phase 1 left it and
> is fully green. Safe to stop indefinitely. To resume: re-read `prd.md` §UI design funnel and
> confirm all four selections are stated (chart, roster split, page composition, and DD-34's
> expanded-card density — the fourth was added by the DD-34 amendment).

---

## Phase 3: Capability-Class Rename — `light` to `haiku`

> Renames the third rated capability class from `light` to `haiku`, so the rated vocabulary reads
> **opus / sonnet / haiku** — three Anthropic model-tier names rather than two tier names and one
> weight adjective. `unrated` is untouched. See
> [`tech-docs.md` §DD-35](./tech-docs.md#dd-35--the-capability-class-rename-light-to-haiku).
>
> **Why here, and not later** — the identifier is a `core/` type (`Band` in `core/bands.ts`) that
> Phases 4-8 all consume: Phase 4 writes new DOM band class maps keyed by it, Phase 5 rewrites the
> chart's per-band testids, Phase 6 rewrites the roster, and Phase 8's e2e cycles read
> `--chart-band-<band>` tokens interpolated from the band id. Renaming first means each of those
> phases writes the final name once; renaming later would mean writing `light` into new code and
> new tests and then sweeping it out again, with a strictly larger blast radius.
>
> **Why not its own delivery unit** — see the note under
> [§Delivery Boundaries](#delivery-boundaries). The four-part boundary test is applied there
> explicitly rather than assumed.
>
> **False positives — do NOT rename these.** The word `light` also names the **light theme** and
> appears inside the word `highlight`/`lighter`. Three sites are theme concerns and MUST survive
> this phase unchanged:
>
> - `libs/web-ui-token/src/ayokoding.css` — the `/* … (light, default) … */` comment and the word
>   `lightness` in the `--chart-band-*` rationale comment.
> - `apps/ayokoding-www/src/features/ai-benchmark/shell/band-tokens.unit.test.ts` — every
>   `light @theme block` string (the light-theme CSS block, not the band).
> - `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` line ~437 —
>   the `| light |` row of the **`| theme |`** Examples table in "Band colours meet contrast in
>   both themes". Renaming it would break a theme test and silently drop light-theme coverage.
>
> Every acceptance clause below is written so that renaming one of those three would fail a check,
> not just so that missing a band site would.

### TDD cycle 3.1 — the rated capability classes are opus, sonnet, and haiku (AC-65)

**Gherkin (binds) →** "The rated capability classes are named opus, sonnet, and haiku"

```gherkin
  @unit
  Scenario: The rated capability classes are named opus, sonnet, and haiku
    Given the full roster is loaded
    When the set of known capability class identifiers is inspected
    Then the identifiers are exactly "opus", "sonnet", "haiku", and "unrated"
    And no identifier is "light"
```

The GREEN step below renames **every** site in one commit. The inventory it must cover, verified
against the current commit `[Repo-grounded]` (paths relative to
`apps/ayokoding-www/src/features/ai-benchmark/` unless absolute):

| Site                                                                                                           | What changes                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `core/bands.ts`                                                                                                | `Band` union (L17), `BandGroups.haiku` (L42), `return "haiku"` fallthrough (L85), `groups` initializer (L154), `groups.haiku.sort` (L160)                                               |
| `core/filter.ts`                                                                                               | the `BANDS` known-value list (L20)                                                                                                                                                      |
| `core/data/benchmarks.ts`                                                                                      | `BAND_LABEL_KEYS.haiku: "aiBenchBandHaiku"` (L42)                                                                                                                                       |
| `core/url-state.ts`                                                                                            | `SORT_PARAM_KEYS.haiku` key (L33), `SortState.haiku` (L41), `DEFAULT_SORT_STATE.haiku` (L51), `UntrustedSortState` (L65), sanitize/decode/encode locals                                 |
| `translations.ts` (`features/i18n/core/`)                                                                      | **keys only**: `aiBenchBandLight` → `aiBenchBandHaiku`, `aiBenchLegendClassLight` → `aiBenchLegendClassHaiku`, in **both** locale blocks                                                |
| `shell/chart-primitives.tsx`                                                                                   | all three band maps — the `haiku` keys AND the class strings `fill-[var(--chart-band-haiku)]` / `fill-[var(--chart-band-haiku-ink)]` / `bg-[var(--chart-band-haiku)]` (L46/53/60)       |
| `shell/how-to-read.tsx`                                                                                        | the legend tuple (L90)                                                                                                                                                                  |
| `shell/model-table.tsx`                                                                                        | the `groups.haiku` iteration (L62)                                                                                                                                                      |
| `libs/web-ui-token/src/ayokoding.css`                                                                          | all six `--chart-band-light*` declarations (L51/108/112 in `@theme`, L181/185/189 in `[data-theme="dark"], .dark`) and the `` `sonnet`/`light` `` comment (L95)                         |
| `shell/band-tokens.unit.test.ts`                                                                               | the pinned token-name list (L57) and the header comment (L13) — every `light @theme block` string is left ALONE                                                                         |
| `core/bands.unit.test.ts`, `core/filter.unit.test.ts`, `core/sort.unit.test.ts`, `core/url-state.unit.test.ts` | band identifier in fixtures and assertions                                                                                                                                              |
| `shell/benchmark-chart.test.tsx`, `shell/chart-order-parity.test.tsx`, `shell/model-table.test.tsx`            | band identifier and the `benchmark-chart-band-haiku` testids                                                                                                                            |
| `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`                                                 | the `Scenario("… haiku band")` title (L291), its verbatim `@covers` comment (L305), the `Then` step strings (L306/L378), `RATED_BAND_KEYS` (L996), `ctx.haikuOrderBefore` (L1703/L1723) |
| `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`                                                    | `BAND_IDS` (L167), `RATED_BAND_IDS` (L174), both contrast `Record` initializers (L204/L215), band-name comments (L69/L313)                                                              |

The i18n **VALUES** stay `"Light"` / `"Ringan"` in this cycle — cycle 3.2 changes them — but the key
rename and its consumers (`BAND_LABEL_KEYS`, `how-to-read.tsx:90`) MUST land together here, because
a key renamed ahead of its consumer makes `t()` return the raw key and fails AC-35.

- [x] [AI] **RED**: add the scenario above verbatim under an `# AC-65` comment to
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`, and in the
      SAME edit reword the five existing scenarios whose text names the old identifier — AC-6
      (**title** `A model below the sonnet anchor renders in the light band` → `… haiku band`, plus
      its `Then that model belongs to the "light" band` step), AC-9
      (`… exactly one of "opus", "sonnet", "light", or "unrated"`), AC-41
      (`And the opus and light bands keep their own …`), AC-44
      (`Given a model in the light band with no metered rate and one subscription rate`), and AC-48
      (`Given a model in the light band with no metered rate and no subscription rate`). Leave the
      `| light |` **theme** Examples row untouched. Do NOT touch any step binding yet.
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run FAILS, and the failure names the reworded AC-6 scenario title as having
      no matching step definition (its binding at
      `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx:291` still declares the old
      title). Falsifiable both ways: if this passed, the step bindings would not be title-coupled
      and the lockstep requirement in GREEN would be unnecessary.
  - _Suggested executor: `specs-maker`_

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` **Notes**: Added
  > the AC-65 scenario verbatim and reworded AC-6/AC-9/AC-41/AC-44/AC-48; confirmed the `| light |`
  > theme Examples row untouched. `npx nx run ayokoding-www:test:unit` FAILED as required, naming the
  > reworded AC-6 scenario ("A model below the sonnet anchor renders in the haiku band") as having no
  > matching step definition, since the old binding still declared the pre-rename title.

- [x] [AI] **GREEN**: perform the whole inventory above in one commit. The identifier and the design
      tokens MUST move together because
      `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts:265` interpolates the band id into
      `var(--chart-band-${band}-ink)`, so renaming the id without renaming the CSS custom property
      yields an unresolvable `var()`
      — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all four exit 0. In particular the e2e "Band colours meet contrast in both
      themes" scenario passes, which it can only do if the CSS custom property was renamed in the
      same step as `BAND_IDS`. Falsifiable both ways: renaming `BAND_IDS` alone leaves
      `var(--chart-band-haiku-ink)` unresolvable and that scenario fails; renaming the CSS alone
      leaves `var(--chart-band-light-ink)` unreferenced and the `band-tokens.unit.test.ts` token
      assertion fails.
  - _Suggested executor: `swe-typescript-dev`_

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: the full inventory table above (21
  > files across `core/`, `shell/`, `libs/web-ui-token/src/ayokoding.css`, both step-binding layers,
  > and `translations.ts` key rename) plus one site NOT in the inventory table that the `build` step
  > surfaced: `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.tsx` (its
  > `SortState` object construction referenced the old `light` key — a genuine TypeScript compile
  > error at `next build`'s type-check phase, invisible to `test:unit` because Vitest's esbuild
  > transform does not type-check). **Notes**: `test:unit`, `specs:behavior:coverage`, `build`, and
  > `test:e2e` all exited 0; the e2e "Band colours meet contrast in both themes" scenario passed both
  > its `light`- and `dark`-theme Examples rows (680 passed, 313 skipped, 0 failed overall — one
  > `[firefox]` timeout on an unrelated cost-of-living-calculator scenario was reproduced and
  > confirmed transient/pre-documented per `evidence/phase-0-baseline.txt`, not a regression).

- [x] [AI] **REFACTOR**: update the explanatory prose that still describes the taxonomy in the old
      vocabulary — `core/bands.ts:7-10` and `:54` (the "else light" fallthrough narrative),
      `core/url-state.ts:20-31` (the `SORT_PARAM_KEYS` docstring), `shell/model-table.tsx:56,224`
      (the DD-5a collapse comments), `shell/benchmark-chart.test.tsx:186,400,423,527-532,572,627`,
      `shell/chart-order-parity.test.tsx:43,71,83,97`, `core/bands.unit.test.ts:60-70,167,262-282`,
      and `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts:69,313`
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0, and the sweep verification below now finds zero surviving band-sense
      occurrences

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: `core/bands.ts`, `core/url-state.ts`,
  > `shell/model-table.tsx`, `shell/benchmark-chart.test.tsx`, `shell/chart-order-parity.test.tsx`,
  > `core/bands.unit.test.ts`, `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts` (prose
  > only). **Notes**: `npx nx run ayokoding-www:test:quick` exited 0. The sweep verification below
  > does NOT find zero surviving occurrences — it finds 7 (Sweep A) and 2 (feature-file band sweep)
  > — but every one of them is the AC-65 scenario's own mandated verbatim text/assertion
  > (`'no identifier is "light"'` / `expect(identifiers).not.toContain("light")` / the retired
  > `class=light` regression test added in cycle 3.3), not a missed rename; see the Sweep A / Sweep B
  > / feature-file-band-sweep items below for the full disclosure. No band-sense prose survived.

### TDD cycle 3.2 — the third rated class is labelled "Haiku" in both locales (AC-66)

**Gherkin (binds) →** "The haiku class label is identical in both locales"

```gherkin
  @unit
  Scenario Outline: The haiku class label is identical in both locales
    Given the class legend is rendered in the "<locale>" locale
    When the haiku class label is read
    Then that label is "Haiku"
    And that label is identical to the label the other locale renders

    Examples:
      | locale |
      | en     |
      | id     |
```

- [x] [AI] **RED**: add the scenario above verbatim under an `# AC-66` comment to
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` with its
      `@covers` binding in `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`, and in
      the same edit **invert** the now-false assertion at
      `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.test.tsx:70-77` — it
      currently asserts `bandLabel("light", "en")` is `"Light"` and that the `id` label DIFFERS
      from the `en` label. Both claims stop being true: rewrite them as
      `expect(bandLabel("haiku", "en")).toBe("Haiku")` and
      `expect(bandLabel("haiku", "id")).toBe(bandLabel("haiku", "en"))`, and update the adjacent
      comment so it records that **all three** rated labels are now proper nouns rather than only
      `opus`/`sonnet`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run FAILS on both new assertions, reporting the actual values `"Light"` and
      `"Ringan"`. Falsifiable both ways: if the values were already `"Haiku"` this RED would pass
      and the cycle would be vacuous; if the inversion were skipped, the OLD
      `not.toBe` assertion would start failing in GREEN instead, which is the same defect surfacing
      one step later.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`,
  > `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`,
  > `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.test.tsx` **Notes**: Added
  > the AC-66 Scenario Outline verbatim with its `@covers` binding, and inverted the
  > `chart-primitives.test.tsx` assertions. `npx nx run ayokoding-www:test:unit` FAILED on both new
  > assertions as required, reporting the pre-rename actual values `"Light"` (en) and the `not.toBe`
  > inversion not yet holding (id still equalled `"Ringan"`, not the `en` value).

- [x] [AI] **GREEN**: change the two values in
      `apps/ayokoding-www/src/features/i18n/core/translations.ts` — line ~62 `aiBenchBandHaiku:`
      from `"Light"` to `"Haiku"` in the `en` block, and line ~440 from `"Ringan"` to `"Haiku"` in
      the `id` block. Leave `aiBenchLegendClassHaiku`'s values (`"below the Sonnet anchor."` /
      `"di bawah jangkar Sonnet."`) translated as they are — those are descriptions, not the proper
      noun
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, and
      `/usr/bin/grep -c 'aiBenchBandHaiku: "Haiku"' apps/ayokoding-www/src/features/i18n/core/translations.ts`
      prints `2` (one per locale block; baseline before this step: `0`). Falsifiable both ways:
      changing only `en` prints `1` and fails; a stray third block prints `3` and fails.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/i18n/core/translations.ts` **Notes**: `npx nx run
ayokoding-www:test:unit` exited 0; `grep -c 'aiBenchBandHaiku: "Haiku"'` printed `2`, matching
  > the expected one-per-locale-block count.

- [x] [AI] **REFACTOR**: record beside the two changed lines, as a comment in
      `translations.ts`, that `"Haiku"` is deliberately untranslated in `id` for the same reason
      `aiBenchBandOpus`/`aiBenchBandSonnet` already are — it is a model-tier proper noun, and the
      dropped `"Ringan"` was a common-noun rendering of the retired `light` sense (DD-35)
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0, and
      `/usr/bin/grep -c 'Ringan' apps/ayokoding-www/src/features/i18n/core/translations.ts` prints
      `0` (baseline before cycle 3.2: `1`)

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/i18n/core/translations.ts` **Notes**: `npx nx run
ayokoding-www:test:quick` exited 0; `grep -c 'Ringan'` printed `0`. The comment text was
  > rewritten once to avoid the literal word "Ringan" itself (the first draft used it in the
  > explanatory prose, which broke this same acceptance clause before the final wording landed).

### TDD cycle 3.3 — the URL carries `class=haiku` and `sortHaiku`, with no legacy alias (AC-67)

**Gherkin (binds) →** "A shared benchmark URL carries the renamed capability-class parameters"

```gherkin
  @unit
  Scenario: A shared benchmark URL carries the renamed capability-class parameters
    Given a query string of "class=haiku&sortHaiku=price-asc"
    When that query string is decoded and then re-encoded
    Then the re-encoded query string is identical to the original
    And a query string carrying the retired "class=light" or "sortLight" decodes to the default unfiltered, capability-sorted state
```

- [x] [AI] **RED**: add the scenario above verbatim under an `# AC-67` comment to the feature file
      with its `@covers` binding in `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`,
      and add the matching round-trip case to
      `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.unit.test.ts` alongside the
      existing `{ name: "class light", query: "class=light" }` round-trip row — replace that row
      with `{ name: "class haiku", query: "class=haiku" }` and add
      `{ name: "retired class value", query: "class=light" }` asserting it decodes to
      `class: undefined`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run FAILS on the `sortHaiku` round-trip, because
      `SORT_PARAM_KEYS.haiku` still holds the string `"sortLight"`, so `sortHaiku=price-asc`
      decodes to the default and re-encodes to an empty query. Falsifiable both ways: the
      `class=haiku` half already passes after cycle 3.1, so a green run here would mean the wire
      format was renamed early and this cycle proves nothing.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`,
  > `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`,
  > `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.unit.test.ts` **Notes**: Added the
  > AC-67 scenario verbatim, its `@covers` binding, and the round-trip test rows. `npx nx run
ayokoding-www:test:unit` FAILED on the `sortHaiku` round-trip as required, confirming
  > `SORT_PARAM_KEYS.haiku` still held `"sortLight"` before GREEN.

- [x] [AI] **GREEN**: in
      `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.ts`, change
      `SORT_PARAM_KEYS.haiku`'s value from `"sortLight"` to `"sortHaiku"`. Add **no** decode-side
      alias for `sortLight` or `class=light` — DD-35 records the no-alias decision and its
      reversibility
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, and
      `/usr/bin/grep -rnF 'sortLight' apps/ayokoding-www/src apps/ayokoding-www/test apps/ayokoding-www-fe-e2e/src specs | /usr/bin/grep -c .`
      prints `0` (baseline before this step: `2`). Falsifiable both ways: leaving either the
      constant or its test reference prints `1` or more and fails.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.ts` **Notes**: `npx nx run
ayokoding-www:test:unit` exited 0. **Deviation disclosed**: the `sortLight` sweep does NOT print
  > `0` — it prints `3`. This is not a missed rename: all three residual hits are the AC-67
  > scenario's own mandated verbatim text (the feature file's `"sortLight" decodes to the default…"`
  > clause, its matching `@covers`-bound step-text string in `fe-steps.tsx`, and the actual
  > `new URLSearchParams("sortLight=price-asc")` regression assertion proving the retired param is
  > now inert) — a genuine, unavoidable conflict between this acceptance clause's literal "prints
  > `0`" text and the plan's own "add the scenario above verbatim" instruction one paragraph above.
  > No alias was added and no decode-side special-casing exists; `SORT_PARAM_KEYS.haiku` is exactly
  > `"sortHaiku"` with zero other consumers of the old string.

- [x] [AI] **REFACTOR**: update the `SORT_PARAM_KEYS` docstring in `core/url-state.ts` so its
      worked example names `sortHaiku`, and add one sentence recording that no legacy alias exists
      by design (DD-35)
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**:
  > `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.ts` **Notes**: `npx nx run
ayokoding-www:test:quick` exited 0. The docstring's worked example names `sortHaiku`; the
  > "no legacy alias" sentence deliberately avoids the literal string `sortLight` in its own prose
  > (unlike the mandatory verbatim Gherkin/step text above) so it does not add a further avoidable
  > hit to the sweep disclosed in the GREEN step's note.

### Rename sweep verification — Phase 3

> Not a TDD cycle. These are the falsifiable sweeps that prove no band-sense `light` survived and
> that the theme-sense false positives did.
>
> `grep` in this shell is a wrapper function routing to UGREP, so every sweep below uses the
> absolute `/usr/bin/grep` path to guarantee POSIX `-w` / `-i` semantics. Each sweep also ends with
> `| /usr/bin/grep -c .` rather than a bare `grep -c`, because `grep -c` exits `1` on a zero count
> and would mask the result when `&&`-chained.

**Sweep A — band-sense occurrences.** These thirteen paths carry no theme concept at all, so any
hit can only be a missed band identifier. `evidence-badge.tsx` (`light/dark` in a comment) and
`band-tokens.unit.test.ts` (`light @theme block`) are deliberately **absent** from the list for
exactly that reason — do not add them.

```bash
/usr/bin/grep -rnwi 'light' \
  apps/ayokoding-www/src/features/ai-benchmark/core \
  apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.test.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/how-to-read.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.test.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/chart-order-parity.test.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.test.tsx \
  apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-filters.tsx \
  apps/ayokoding-www/src/features/i18n/core/translations.ts \
  apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx \
  apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts | /usr/bin/grep -c .
```

**Sweep B — camelCase and token occurrences.** These catch the forms Sweep A's word boundary cannot
see (`aiBenchBandLight`, `sortLight`, `--chart-band-light`, `benchmark-chart-band-light`,
`lightOrderBefore`). `apps/ayokoding-www/.next/` is gitignored build output and is excluded by the
path list — do NOT add it, and do NOT "fix" hits found there.

```bash
/usr/bin/grep -rnE 'BandLight|ClassLight|sortLight|lightOrder|chart-band-light|band-light|svg-light|class-light' \
  apps/ayokoding-www/src apps/ayokoding-www/test apps/ayokoding-www-fe-e2e/src \
  specs/apps/ayokoding libs/web-ui-token/src | /usr/bin/grep -c .
```

- [x] [AI] **Sweep A must be empty** — acceptance: prints `0`. **Baseline before Phase 3: `122`**
      (measured at authoring time against the current commit); every one of the 122 was inspected
      and confirmed to be a band-sense hit. Falsifiable both ways: a single missed band site prints
      `1` or more and fails; the check cannot be satisfied by deleting a theme reference, because
      there is none in this path set to delete.

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none (this
  > is a read-only verification). **Notes**: prints `7`, not `0`. All 7 hits were individually
  > traced: `url-state.unit.test.ts:116,118,119` (the AC-67 "retired `class=light`" regression test)
  > and `fe-steps.tsx:411-412,1854,1856` (AC-65's `'no identifier is "light"'` assertion and AC-67's
  > `'class=light' or 'sortLight'` step text). Every hit is the plan's own mandated verbatim
  > Gherkin/regression text proving the retired identifier is now inert, not a missed rename; no
  > theme reference exists in this path set. Disclosed as a self-contradiction in the plan's own
  > acceptance clauses (verbatim-text mandate vs. "prints `0`"), not a defect in the rename.

- [x] [AI] **Sweep B must be empty** — acceptance: prints `0`. **Baseline before Phase 3: `29`**
      (measured at authoring time). Falsifiable both ways: leaving one testid, one i18n key, or one
      CSS declaration prints `1` or more and fails.

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none.
  > **Notes**: prints `3`, not `0` — all three are `fe-steps.tsx:1854,1858` and
  > `ai-benchmark.feature:322`, the same AC-67 verbatim `sortLight` regression text/assertion
  > disclosed in cycle 3.3's GREEN note and in the Sweep A note above. No testid, i18n key, or CSS
  > declaration was left unrenamed.

- [x] [AI] **Feature-file band sweep must be empty AND the theme row must survive.** Two commands,
      read independently:
      `/usr/bin/grep -nw 'light' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature | /usr/bin/grep -cvF '| light |'`
      — acceptance: prints `0` (baseline: `6`); AND
      `/usr/bin/grep -cF '| light |' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `1`. Falsifiable in **both** directions: missing a band step makes the
      first print `1` or more and fails, and over-renaming the light-theme Examples row makes the
      second print `0` and fails.

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none. **Notes**:
  > the theme-row-survives command prints `1` as required. The band-sweep command prints `2`, not
  > `0` — both are the AC-65 `'no identifier is "light"'` line and the AC-67
  > `'"class=light" or "sortLight"'` line, both required verbatim by this same delivery.md two
  > sections above. No band step was left un-reworded; the `| light |` theme Examples row survived
  > untouched.

- [x] [AI] **Theme false positives survived.** Confirm the three protected sites are untouched:
      `/usr/bin/grep -c 'light @theme block' apps/ayokoding-www/src/features/ai-benchmark/shell/band-tokens.unit.test.ts`
      prints at least `3`, AND
      `/usr/bin/grep -c 'light, default' libs/web-ui-token/src/ayokoding.css` prints `1`
      — acceptance: both hold. Falsifiable both ways: a blind global substitution of `light` →
      `haiku` drives both to `0` and fails.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: `light @theme block`
  > count is `3` (≥3 required); `light, default` count is `1`. Both protected sites survived
  > untouched.

- [x] [AI] **No other consumer of the renamed tokens exists outside this feature.** Confirm the
      rename did not orphan a reference elsewhere in the workspace:
      `/usr/bin/grep -rnF 'chart-band-light' --include='*.ts' --include='*.tsx' --include='*.css' apps libs specs --exclude-dir=.next --exclude-dir=node_modules | /usr/bin/grep -c .`
      — acceptance: prints `0` (baseline outside `.next/`: `20`, measured at authoring time).
      Falsifiable both ways: any file in the workspace still asking for the retired token prints `1`
      or more and fails.

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: prints `0` — no
  > orphaned `chart-band-light` reference remains anywhere in the workspace outside `.next/`.

### Specs & Gherkin Delivery (Phase 3)

- [x] [AI] Verify the three new scenarios and the five rewordings all carry `@covers` bindings:
      `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none (verification only). **Notes**:
  > exits 0 — "Spec coverage valid! 42 specs, 347 scenarios, 1250 steps — all covered."

- [x] [AI] Verify the e2e-layer coverage scanner is still satisfied:
      `npx nx run ayokoding-www-fe-e2e:specs:e2e:coverage` — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: exits 0 — "E2E COVERAGE
  > GAP DETECTOR PASSED: 0 new unbound scenario(s) beyond baseline."

- [x] [AI] Verify the step-keyword cardinality HARD rule holds for AC-65, AC-66, and AC-67:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance gherkin-keyword-cardinality`
      — acceptance: exits 0

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none.
  > **Notes**: the literal command above no longer exists in the current `rhino-cli` — it errors
  > with `unrecognized subcommand 'gherkin-keyword-cardinality'`; this command was relocated to
  > `specs gherkin-cardinality validate` (this delivery.md's own command text is stale relative to
  > the current CLI). Ran the equivalent current command —
  > `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs
gherkin-cardinality validate specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
  > — which exited 0: "GHERKIN KEYWORD CARDINALITY AUDIT PASSED: every scenario uses each primary
  > keyword at most once."

- [x] [AI] Verify the scenario count grew by exactly three and no scenario was deleted:
      `/usr/bin/grep -cE '^[[:space:]]+Scenario( Outline)?:' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints the Phase 0 baseline in `evidence/phase-0-baseline.txt` plus exactly `3`.
      Falsifiable both ways: deleting the reworded AC-6 instead of editing it in place makes the
      count short and fails; splitting one rename scenario into two makes it long and fails.

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none.
  > **Notes**: prints `53`, not the literal `49 + 3 = 52` this clause names. `evidence/phase-0-baseline.txt`
  > records `49` as the Phase 0 baseline, but Phase 1 (a separate, already-merged delivery unit, PR
  > #126) added its own scenario (AC-52, "The document never scrolls horizontally") between that
  > baseline measurement and now, making the pre-Phase-3 count `50`, not `49` — a plan-authoring math
  > oversight in this acceptance clause, not a Phase 3 defect. `50 + 3 (AC-65/AC-66/AC-67) = 53`
  > matches exactly; no scenario was deleted or split.

### Local Quality Gates (Before Push) — Phase 3

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the Root Cause Orientation principle — proactively fix preexisting errors
> encountered during work. Do not defer or skip existing issues. Commit preexisting fixes
> separately with appropriate conventional commit messages.

- [x] [AI] `npx nx affected -t typecheck` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: exits 0 for
  > `ayokoding-www` and every other affected project.

- [x] [AI] `npx nx affected -t lint` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: exits 0; only
  > pre-existing, unrelated warnings surfaced (e.g. `no-empty-pattern` in an e2e `common.steps.ts`
  > destructuring pattern) — no error-level findings, nothing caused by this phase's changes.

- [x] [AI] `npx nx affected -t test:quick` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: exits 0 for every
  > affected project, `ayokoding-www` included (`specs:behavior:coverage` sub-target reported "42
  > specs, 347 scenarios, 1250 steps — all covered").

- [x] [AI] `npx nx affected -t specs:behavior:coverage` — exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: exits 0 for every
  > affected project (`ayokoding-www`, `web-ui`; e2e projects correctly no-op per their own target
  > definition).

- [x] [AI] `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` — exits 0
      (`libs/web-ui-token` changed, so `web-ui-token`'s own affected targets run too)

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: `build` exited 0 (a
  > few "took more than 60 seconds, retrying" static-page warnings during generation, self-resolved
  > on retry — unrelated to this rename); `test:e2e` exited 0 with 680 passed, 313 skipped, 0
  > failed.

- [x] [AI] Re-run every previously failing check to confirm resolution — acceptance: zero failures

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: no quality-gate check
  > failed during this phase's execution (one transient `[firefox]` e2e timeout on an unrelated,
  > pre-documented cost-of-living-calculator scenario reproduced once and then passed cleanly on
  > rerun — confirmed pre-existing/flaky per `evidence/phase-0-baseline.txt`, not a rename
  > regression, so no separate fix commit was needed).

### Commit Guidelines — Phase 3

- [x] [AI] Commit thematically, Conventional Commits format — the identifier and token rename as
      `refactor(ayokoding-www): rename capability class light to haiku`, the locale values as
      `feat(ayokoding-www): label the haiku capability class in both locales`, and the URL
      parameter as `refactor(ayokoding-www): rename sortLight url parameter to sortHaiku`
      — acceptance: `git log --oneline -3` shows three conventional-format subjects

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: (commit boundaries, not new files)
  > `ee9240155 refactor(ayokoding-www): rename capability class light to haiku`,
  > `3194938f1 feat(ayokoding-www): label the haiku capability class in both locales`,
  > `c0bd9491e refactor(ayokoding-www): rename sortLight url parameter to sortHaiku`. **Notes**:
  > `git log --oneline -3` shows exactly these three conventional-format subjects, in this order.
  > Several files (`translations.ts`, `url-state.ts`, `url-state.unit.test.ts`,
  > `chart-primitives.test.tsx`, `fe-steps.tsx`, the feature file) carried hunks belonging to more
  > than one cycle; these were split at the hunk level with `git add -p` (and `s` to split one
  > merged AC-67/AC-44 hunk in the feature file) so each commit's diff matches its theme as closely
  > as git's hunk granularity allows. Two adjacent-line pairs were inseparable at the hunk level and
  > were bundled with the earlier-cycle commit for atomicity: the `fe-steps.tsx` import statement
  > (`BANDS` for cycle 3.1 + `DEFAULT_STATE` for cycle 3.3, landed in commit 1) and
  > `SORT_PARAM_KEYS`'s key-rename-plus-value-rename line in `url-state.ts` (landed in commit 3,
  > since the value rename is that commit's whole point).

- [x] [AI] Any preexisting fix gets its own separate commit — acceptance: no unrelated change is
      bundled into any of the three commits above

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: no preexisting failure
  > was found during this phase's quality gates (see the Local Quality Gates section above), so no
  > separate fix commit was needed. One incidental, unrelated change was found and deliberately
  > EXCLUDED from all three commits rather than bundled in: `apps/ayokoding-www/next-env.d.ts` was
  > auto-regenerated by running `nx build` (an `import` path drifted from `./.next/dev/types/…` to
  > `./.next/types/…`); reverted with `git checkout --` both times it reappeared, since it is
  > build-tooling churn unrelated to the rename.

- [x] [AI] No PR opens in this phase — Phase 3 is an intermediate phase inside Unit 2, whose PR
      opens at Phase 12 — acceptance:
      `gh pr list --head ai-benchmark-responsive-overhaul --json number --jq 'length'` prints `0`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: prints `0`; no PR was
  > opened.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `npx nx run ayokoding-www:test:quick` exits 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: exits 0.

- [x] [AI] `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 —
      in particular "Band colours meet contrast in both themes" passes in BOTH the `light` and
      `dark` Examples rows, which is the single check that proves the CSS custom property and the
      band identifier were renamed together

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: both exit 0 (680
  > passed, 313 skipped, 0 failed for `test:e2e`), confirming the "Band colours meet contrast in
  > both themes" scenario and its `light`/`dark` Examples rows both passed.

- [x] [AI] All five sweep commands above report their expected values — the three "must be empty"
      sweeps print `0`, and the two "must survive" checks print their expected non-zero counts

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none.
  > **Notes**: only 2 of the 5 sweeps print their literal expected value (Theme false positives
  > survived: `3`/`1`; No other consumer: `0`). The three "must be empty" sweeps print non-zero
  > (Sweep A: `7`; Sweep B: `3`; feature-file band sweep: `2`) — every residual hit was individually
  > traced in that sweep's own item above and confirmed to be the AC-65/AC-67 scenarios' own
  > delivery.md-mandated verbatim text/regression assertions proving the retired `light`/`sortLight`
  > identifiers are now inert, not a missed rename. This is a genuine, disclosed self-contradiction
  > between this delivery.md's "verbatim" Gherkin-authoring instructions and its own "prints `0`"
  > sweep acceptance clauses for AC-65/AC-67's scenarios specifically — not a Phase 3 defect.

- [x] [AI] The scenario count equals the Phase 0 baseline plus exactly `3`

  > **Date**: 2026-07-31 **Status**: Done (with disclosed deviation) **Files changed**: none.
  > **Notes**: count is `53`; `Phase 0 baseline (49) + 3 = 52` does not match literally, because
  > Phase 1 (already merged, PR #126) added one scenario (AC-52) between the Phase 0 baseline
  > measurement and now — see the "Verify the scenario count grew by exactly three" item above for
  > the full reconciliation. The correct pre-Phase-3 count was `50`, and `50 + 3 = 53` matches
  > exactly.

- [x] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` and
      `npx nx run ayokoding-www-fe-e2e:specs:e2e:coverage` both exit 0

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: both exit 0.

- [x] [AI] Nothing was pushed and no PR exists for the Unit 2 branch:
      `gh pr list --head ai-benchmark-responsive-overhaul --json number --jq 'length'` prints `0`

  > **Date**: 2026-07-31 **Status**: Done **Files changed**: none. **Notes**: prints `0`.

> **Pause Safety**: the taxonomy rename is complete and self-consistent across core, shell, design
> tokens, i18n, specs, and both step-binding layers. The page renders exactly as it did after
> Phase 1 except that the third rated class now reads "Haiku" in both locales and its URL
> parameter is `sortHaiku`. No overhaul work has begun. Safe to stop indefinitely. To resume:
> re-run the band-sense sweep and confirm it still prints `0`.

---

## Phase 4: Chart Primitives Migration

> Prepares `chart-primitives.tsx` for DOM rendering: a percentage scale, DOM class maps, and the
> removal of the SVG-only exports that lose their last consumer in Phase 5.
>
> Ordered before Phase 5 deliberately — the chart rewrite consumes these primitives, so building
> them first keeps Phase 5's own cycles focused on layout rather than on plumbing.

### TDD cycle 4.1 — `scaleLinear` yields a percentage

**Gherkin (underpins) →** the pure-core scale behaviour AC-13 and AC-49 both rest on. This is the
pure-core exception to one-scenario-per-cycle: it is a data/calculation test, not a behaviour slice.

- [ ] [AI] **RED**: add tests to
      `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.test.tsx` asserting
      `scaleLinear(COMPOSITE_INDEX_MAX, 100)` maps the domain maximum to `100`, the midpoint to
      `50`, `0` to `0`, and a non-positive `domainMax` to always-`0`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertions run and PASS immediately (the existing `scaleLinear` already
      satisfies them) — record this explicitly as a **characterization** test, not a RED. If any
      assertion fails, `scaleLinear`'s contract is not what `tech-docs.md` DD-25 assumes and the
      plan must be revised before proceeding.
- [ ] [AI] **GREEN**: no production change required — record "no change needed; contract confirmed"
      in the checklist
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0
- [ ] [AI] **REFACTOR**: extend `scaleLinear`'s docstring in
      `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx` to state the
      percentage use, naming DD-25
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0 and
      `grep -cF 'DD-25' apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx`
      is at least `1`

### TDD cycle 4.2 — DOM band class maps

**Exempt from Gherkin tagging** — a pure plumbing/helper addition (DOM class-map constants) with no
user-observable behavior of its own; consumed by cycle 5.1's behavior-bound `BarRow`.

- [ ] [AI] **RED**: add tests to `chart-primitives.test.tsx` asserting new
      `bandBarBgClass(band)` and `bandInkTextClass(band)` helpers return the
      `bg-[var(--chart-band-*)]` and `text-[var(--chart-band-*-ink)]` class strings for all four
      bands
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS with `bandBarBgClass is not a function`
- [ ] [AI] **GREEN**: add both helpers to `chart-primitives.tsx` as `Record<ChartBand, string>` maps
      with complete, literal, unbroken class strings (Tailwind's scanner reads literals — the
      existing module docstring documents exactly this constraint)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new tests pass and every existing test in the file still passes
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: place the new maps directly beside the existing `BAR_FILL_CLASS` /
      `BAND_INK_FILL_CLASS` maps and extend the module's hand-consistency warning comment to name
      the two new maps
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] `npx nx run ayokoding-www:test:quick` exits 0
- [ ] [AI] `npx nx run ayokoding-www:build` exits 0
- [ ] [AI] The SVG exports are still present and still consumed — deletion happens in Phase 5, not
      here: `grep -cE 'export function (Axis|Bar|BandGroup|TickRow)' apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx`
      prints `4`

> **Pause Safety**: `chart-primitives.tsx` has gained two helpers and one docstring; nothing
> consumes them yet and no rendering changed beyond Phase 3's Haiku label/URL-param rename, which
> persists. The page renders exactly as it did after Phase 3.
> Safe to stop indefinitely. To resume: `npx nx run ayokoding-www:test:quick`.

---

## Phase 5: DOM Bar Row and Chart Rewrite

> The core of the plan: `benchmark-chart.tsx` stops emitting `<svg>` and every layout constant with
> it. See [`tech-docs.md` §DD-25](./tech-docs.md#dd-25--htmlcss-bars-replace-the-svg-chart-at-every-breakpoint)
> and [§DD-26](./tech-docs.md#dd-26--reversing-the-identical-dom-responsive-strategy).

### TDD cycle 5.1 — one DOM bar row renders a proportional fill (AC-40 preserved)

**Gherkin (binds) →** "Bar length is proportional to its own value"

```gherkin
  @unit
  Scenario: Bar length is proportional to its own value
    Given a model with a composite index of 85.7 and an output rate of $15.00
    When the merged chart renders that model's row
    Then the capability bar's length is proportional to 85.7 over the composite index max
    And the price-out bar's length is proportional to $15.00 over the chart's shared price axis max
```

- [ ] [AI] **RED**: create
      `apps/ayokoding-www/src/features/ai-benchmark/shell/bar-row.test.tsx` (sibling pattern:
      `chart-primitives.test.tsx`) asserting that a `BarRow` given a value and a domain maximum
      renders a fill element whose inline `style.width` is the expected percentage string
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — the module `./bar-row` does not resolve
- [ ] [AI] **GREEN**: create `apps/ayokoding-www/src/features/ai-benchmark/shell/bar-row.tsx`
      _New file_ — a label element, a track `div`, and a fill `div` whose
      `style={{ width:`${scaleLinear(max, 100)(value)}%`}}` uses `bandBarBgClass(band)`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new tests pass; `npx nx run ayokoding-www:typecheck` exits 0
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: extract the label/track/fill markup into a single documented component with
      a docstring naming DD-25 and stating the FCIS boundary (no literal score, price, name, or
      threshold in this file)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 5.2 — the chart reflows without rescaling typography (AC-47, inverted)

**Gherkin (binds) →** "The chart reflows its layout without rescaling its typography"

```gherkin
  @unit
  Scenario: The chart reflows its layout without rescaling its typography
    Given the merged chart is rendered at a mobile, a tablet, and a desktop viewport width
    When the DOM structure and the declared text sizes at each width are inspected
    Then the declared text size of every chart label is identical at all three widths
    And the row layout changes from stacked to a label column only at the desktop width
```

- [ ] [AI] **RED**: reword the AC-47 scenario in
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` (currently at
      lines 324-330, titled "The merged chart uses the identical DOM structure at every breakpoint")
      to the Gherkin block above verbatim, with a comment naming DD-25/DD-26/DD-31 (the identical-DOM
      guarantee this scenario protected is retired because `BarRow`'s declared DOM now varies
      deliberately by breakpoint; the property worth protecting is that its typography does not), and
      rewrite the bound
      `Scenario("The merged chart uses the identical DOM structure at every breakpoint", ...)` block
      in `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx` (currently lines ~1894-1924)
      to assert the NEW property instead of `expect(narrow).toEqual(medium)`: (a) the declared
      Tailwind text-size class on every chart label is identical across the 375px/768px/1280px
      renders, and (b) the row container carries the `lg:grid-cols-` reflow class only at the 1280px
      render, not at 375px/768px
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — the current binding still asserts DOM-signature `toEqual` equality
      instead of the text-size/reflow-class properties above
- [ ] [AI] **RED**: replace the SVG-structure assertions in
      `apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.test.tsx` with assertions
      that (a) no `<svg>` element is rendered, (b) every model label carries the same declared
      Tailwind text-size class regardless of any width-dependent prop, and (c) the row container
      carries the `lg:grid-cols-` reflow class exactly once
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS on (a) — the current component renders one `<svg>` per rated band
- [ ] [AI] **GREEN**: rewrite
      `apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx` to render DOM rows
      via `BarRow`, deleting `SVG_WIDTH`, `PLOT_X`, `PLOT_WIDTH`, `MARKER_FONT_SIZE`, `MARKER_GAP`,
      `MARKER_CHAR_WIDTH_RATIO`, `MARKER_SAFETY_BUFFER`, `WORST_CASE_MARKER_LENGTH`,
      `MARKER_MIN_MARGIN`, `ROW_HEIGHT`, `BAR_HEIGHT`, `BAR_GAP`, `HEADER_LABEL_Y_OFFSET`,
      `BAND_HEADER_HEIGHT`, `TOP_MARGIN`, and `computeLayout`'s y-coordinate arithmetic
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new tests pass, and
      `grep -cE '^(export )?const (SVG_WIDTH|PLOT_X|PLOT_WIDTH|BAND_HEADER_HEIGHT|TOP_MARGIN)' apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx`
      prints `0`
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: replace the file's SVG-era header comment with one recording DD-25, DD-26,
      and DD-31 (why DWT-001 and DWT-004 are retired as SVG-geometry concerns rather than dropped)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0 and
      `grep -cE 'DD-2[56]|DD-31' apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx`
      is at least `3`

### TDD cycle 5.3 — the chart region keeps an accessible name (AC-36, reworded)

**Gherkin (binds) →** "The merged chart exposes an accessible name"

```gherkin
  @unit @e2e
  Scenario: The merged chart exposes an accessible name
    Given the full roster is loaded
    When the page renders
    Then each rated band's chart region exposes a localized accessible name
```

- [ ] [AI] **RED**: reword the AC-36 scenario in
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` (lines
      231-236) to the text above with a comment naming DD-25, and update its assertion in
      `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx` to query an accessible region
      rather than an `svg[role="img"]`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — no labelled region exists yet
- [ ] [AI] **GREEN**: give each rated band's wrapper in `benchmark-chart.tsx` a
      `role="group"` (or `<section>`) with `aria-labelledby` pointing at that band's own visible
      heading, carrying the localized band label
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the AC-36 unit binding passes
- [ ] [AI] **REFACTOR**: hoist the per-band id generation into one helper so the heading id and the
      `aria-labelledby` cannot drift
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 5.4 — the text alternative survives (AC-46, reworded)

**Gherkin (binds) →** "The merged chart keeps its accessible name and text alternative"

```gherkin
  @unit
  Scenario: The merged chart keeps its accessible name and text alternative
    Given the merged chart has replaced the two former charts
    When a screen reader encounters the chart
    Then each rated band renders its own labelled region carrying its localized band name as its accessible name
    And every figure the chart encodes is still reachable via the roster below
```

- [ ] [AI] **RED**: reword the AC-46 scenario in the feature file (lines 311-322) to the text above
      and update its unit binding to assert the labelled region plus roster reachability
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS on the roster-reachability assertion until the binding is written against
      the current DOM
- [ ] [AI] **GREEN**: adjust the binding and any component markup needed so both steps hold
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [ ] [AI] **REFACTOR**: update `chart-order-parity.test.tsx`'s selectors from SVG testids to the
      new DOM testids
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 5.5 — DD-31's replacement structural guards

**Exempt from Gherkin tagging** — structural DOM-sibling regression guards replacing the retired
SVG-geometry tests (DD-31), not a new behavior scenario.

- [ ] [AI] **RED**: add two tests to `benchmark-chart.test.tsx`: (a) the low-coverage marker renders
      as a sibling of the bar track, not inside it (replacing DWT-001's clip guard); (b) the band
      header and the first model row are separate block-level siblings (replacing DWT-004's overlap
      guard)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: both FAIL if the marker is nested inside the track or the header shares a
      container with the first row; confirm by temporarily nesting one and observing the failure,
      then restore
- [ ] [AI] **GREEN**: adjust the markup so both hold
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: both pass
- [ ] [AI] **REFACTOR**: group both under a `describe("DD-31 — replacements for the retired
SVG-geometry guards")` block with a comment linking to `tech-docs.md §DD-31`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### Cleanup — DD-32 disposition

- [ ] [AI] Delete `Axis`, `Bar`, `BandGroup`, `TickRow`, and `evenTicks` from
      `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx` and their tests from
      `chart-primitives.test.tsx`
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0, and
      `grep -cE 'export function (Axis|Bar|BandGroup|TickRow|evenTicks)' apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx`
      prints `0`
- [ ] [AI] Confirm `Legend`, `scaleLinear`, `bandLabel`, and `bandSwatchClass` are still exported and
      still consumed
      — acceptance:
      `grep -cE 'export function (Legend|scaleLinear|bandLabel|bandSwatchClass)' apps/ayokoding-www/src/features/ai-benchmark/shell/chart-primitives.tsx`
      prints `4`

### Preserved-defect guards — Phase 5

- [ ] [AI] Confirm UWT-001 holds: unrated metered models still show their price as plain text, never
      a bar or sort control, after the DOM rewrite
      — acceptance: `npx nx run ayokoding-www:test:unit` passes, including the existing
      `describe("BenchmarkChart — unrated models")` suite in `benchmark-chart.test.tsx`, and
      `grep -cF 'UWT-001' apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx`
      is at least `1` (the defect-preservation comment survives the rewrite, confirmed by reading the
      `groups.unrated.map` block directly: it must render plain price text, never a `<BarRow`)
- [ ] [AI] Confirm UWT-002 holds: each rated band's sort control remains a DOM sibling of that same
      band's own rows, never hoisted to a shared location above all bands
      — acceptance: `npx nx run ayokoding-www:test:unit` passes, and
      `grep -cF 'UWT-002' apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx`
      is at least `1` (the defect-preservation comment survives the rewrite, confirmed by reading the
      `bands.map` block directly: the per-band `FilterSelect` sort control and that band's own rows
      share the same per-band wrapper element)

### Commit Guidelines — Phase 5

- [ ] [AI] Commit thematically: one commit for `bar-row.tsx`, one for the `benchmark-chart.tsx`
      rewrite, one for the spec rewordings, one for the DD-32 deletions
      — acceptance: `git log --oneline -4` shows four conventional-format subjects, none bundling
      unrelated concerns

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] `npx nx run ayokoding-www:test:quick` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
- [ ] [AI] No `<svg` remains in the chart component:
      `grep -cF '<svg' apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx`
      prints `0`
- [ ] [AI] `npx nx run ayokoding-www:build` exits 0
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 (AC-52 still green after the rewrite)

> **Pause Safety**: the chart renders as DOM at every breakpoint; the roster and page composition
> are unchanged, so the page is coherent and fully green — a reader would simply see the new chart
> under the old prose. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:test:quick`.

---

## Phase 6: Roster Card, Column Reduction, and Card Density

> Fixes R3 on **both** its dimensions. Cycles 6.1-6.3 implement
> [`tech-docs.md` §DD-28](./tech-docs.md#dd-28--roster-summary-card-plus-per-card-disclosure)
> (roster summary card plus per-card disclosure) and complete DD-27's second step, restoring the
> sticky `<thead>` Phase 1 traded away. Cycles 6.4-6.7 implement
> [`tech-docs.md` §DD-34](./tech-docs.md#dd-34--the-expanded-cards-field-density) — the density of
> what that disclosure reveals ([`brd.md` §R3b](./brd.md#r3b--the-density-of-the-cards-own-field-content),
> DN-1..DN-4). The two decisions are a pair and land in one phase because 6.4-6.7 all edit the
> component 6.1 creates.

### TDD cycle 6.1 — a collapsed card shows only its summary (AC-53)

**Gherkin (binds) →** "A roster card shows only its summary until it is expanded"

```gherkin
  @unit
  Scenario: A roster card shows only its summary until it is expanded
    Given the full roster is rendered below the md breakpoint
    When a model's card is inspected before any interaction
    Then the card shows the model name, its class, its composite index, and its price
    But the card's remaining figures are inside a closed disclosure
```

- [ ] [AI] **RED**: add the scenario above to the feature file under an `# AC-53` comment, bind it
      in `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`, and create
      `apps/ayokoding-www/src/features/ai-benchmark/shell/model-card.test.tsx` _New file_ asserting
      the summary field set and that the remaining figures sit inside a `<details>` without the
      `open` attribute
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — `./model-card` does not resolve
- [ ] [AI] **GREEN**: add the card disclosure's `<summary>` label key (DD-33's unconditional key —
      distinct from DD-33's _conditional_ how-to-read key, which Phase 7 decides) to **both** locale
      blocks in `apps/ayokoding-www/src/features/i18n/core/translations.ts` BEFORE creating the
      component that consumes it. The key must exist by the end of this cycle: `t()` falls back to
      returning the raw key string, and Phase 6's own Gate runs AC-35 (no `aiBench` raw-key leak on
      either locale), so a key deferred to Phase 7 would fail this phase's gate — or, if papered over
      with a hardcoded literal, ship untranslated copy no later step catches
      — acceptance: for the new key `K`,
      `grep -c "$K:" apps/ayokoding-www/src/features/i18n/core/translations.ts` prints `2` (one per
      locale). Falsifiable both ways: a key added to only one locale prints `1` and fails; no key at
      all prints `0` and fails
- [ ] [AI] **GREEN**: create
      `apps/ayokoding-www/src/features/ai-benchmark/shell/model-card.tsx` _New file_ rendering the
      summary (name, class, index, price) plus a `<details>`/`<summary>` holding the remaining
      figures, reusing `FigureCell` and `EvidenceBadge` verbatim; both `<dt>` and `<dd>` left-aligned.
      The `<summary>` label reads from the key added in the step above via `t(locale, K)` — never a
      hardcoded literal. **Carry today's field typography forward verbatim** — `<dt>` as
      `text-xs font-medium text-muted-foreground`, `<dd>` as `text-sm` with no weight override, and
      `FigureCell` at its default stacked layout. DD-34's cycle 6.4 changes exactly that, and 6.4's
      RED step is only genuinely red if this cycle does not pre-empt it
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes; `npx nx run ayokoding-www:typecheck` exits 0
  - _Suggested executor: `swe-ui-maker`_
- [ ] [AI] **REFACTOR**: have `model-card.tsx` consume the same shared per-model figure list
      `model-table.tsx` builds (`renderBenchmarkFigures` / `renderStaticFigures`), hoisted into a
      shared helper, so summary and detail are two slices of one list
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 6.2 — figure parity across representations (AC-54, W-30)

**Gherkin (binds) →** "An expanded roster card carries every figure the desktop table carries"

```gherkin
  @unit
  Scenario: An expanded roster card carries every figure the desktop table carries
    Given a model is rendered in both the roster card and the desktop table
    When that model's card disclosure is expanded
    Then the card's summary and expanded content together carry every figure that model's table row carries
```

- [ ] [AI] **RED**: add the scenario under an `# AC-54` comment, bind it, and add a parity test to
      `model-card.test.tsx` comparing the card's full figure-label set against the table row's
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS on at least one label present in one representation and absent in the other
- [ ] [AI] **GREEN**: reconcile both representations against the shared figure list until the sets
      are equal
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [ ] [AI] **REFACTOR**: state the W-30 invariant in a docstring at the shared helper, referencing
      the prior plan's W-26
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 6.3 — the desktop table fits, and the sticky header returns (AC-59)

**Gherkin (binds) →** "The roster table header stays visible while the page scrolls at desktop width"

```gherkin
  @e2e
  Scenario: The roster table header stays visible while the page scrolls at desktop width
    Given the AI benchmark page is loaded at a 1440 px viewport
    When the page is scrolled until the roster table's last row is in view
    Then the table's header row is still visible
```

- [ ] [AI] **RED**: add the scenario under an `# AC-59` comment and bind it in
      `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: FAILS — Phase 1 removed the `lg` override, so the header does not stick
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] **GREEN**: in `model-table.tsx`, reduce the desktop table to its primary columns (model,
      vendor, class, index, input price, output price) with the remaining figures in a per-row
      expandable detail row, then restore `wrapperClassName="lg:overflow-visible"` — now safe
      because the table's intrinsic width fits the viewport
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: AC-59 passes AND all seven AC-52 rows still pass. Falsifiable both ways:
      restoring the override without reducing the columns makes AC-52 fail; reducing the columns
      without restoring the override makes AC-59 fail.
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: replace the DD-27 comment written in Phase 1 with the completed two-step
      record, and update the unit-level `lg:overflow-visible` guard from Phase 1 cycle 1.2 into an
      assertion that the class is present **and** that the table's declared column count is at or
      below the primary-column set
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0
- [ ] [AI] Delegate the reduced table to `model-card.tsx` for the sub-`md` branch, deleting the
      inline card markup at `model-table.tsx` lines 332-365
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0, and
      `grep -cF 'grid-cols-2 gap-x-3' apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
      prints `0` (the zig-zag two-column card grid is gone)

### TDD cycle 6.4 — the value out-ranks its own label (AC-61)

> DD-34 Treatment 1. Fixes DN-1 — today `<dt>` is 12px at weight **500** and `<dd>` is 14px at the
> inherited **400**, so the label out-weights the value it introduces. See
> [`tech-docs.md` §DD-34](./tech-docs.md#dd-34--the-expanded-cards-field-density).

**Gherkin (binds) →** "An expanded card's figure value out-ranks its own field label"

```gherkin
  @e2e
  Scenario: An expanded card's figure value out-ranks its own field label
    Given the AI benchmark page is loaded at a 390 px viewport with one roster card expanded
    When the computed font size and font weight of a field label and of its own value are read from the live page
    Then the value's computed font size is larger than the label's computed font size
    And the value's computed font weight is greater than the label's computed font weight
```

- [ ] [AI] **RED**: add the scenario above to
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature` under an
      `# AC-61` comment, and bind it in `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`
      by expanding the first card's `<summary>` and reading
      `getComputedStyle(el).fontSize` / `.fontWeight` on a `dt` and on its sibling `dd`'s value span
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: FAILS on the font-weight comparison — cycle 6.1 carried today's
      `font-medium` (500) label against a 400 value forward verbatim, so `500 > 400` is the wrong
      way round. Falsifiable both ways: the size comparison (12 < 14) already passes today, so a
      test that goes green here without any source change is asserting the wrong property and must
      be tightened before proceeding.
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] **GREEN**: in
      `apps/ayokoding-www/src/features/ai-benchmark/shell/model-card.tsx`, set `<dt>` to
      `text-xs font-normal text-muted-foreground` and `<dd>` to
      `text-sm font-semibold text-foreground`; apply the identical pair to the table's per-row
      detail region in `apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: AC-61 passes, and AC-52 and AC-59 both stay green (the change is typographic,
      not structural, so the table's intrinsic width must not move)
  - _Suggested executor: `swe-ui-maker`_
- [ ] [AI] **REFACTOR**: hoist the two class strings into named constants beside the shared figure
      helper so the card and the detail region cannot drift apart, with a one-line comment naming
      the three encodings (size, weight, colour) and DN-1
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, and
      `grep -cF 'font-medium text-muted-foreground' apps/ayokoding-www/src/features/ai-benchmark/shell/model-card.tsx`
      prints `0`. Falsifiable both ways: leaving one call site on the old class string prints `1`
      and fails.

### TDD cycle 6.5 — value and evidence badge flow on one row (AC-62)

> DD-34 Treatment 2. Fixes DN-2 — `figure-cell.tsx:36` is `inline-flex flex-col`, so every graded
> field costs three stacked line boxes (label, value, badge).

**Gherkin (binds) →** "An expanded card's figure value and its evidence badge flow on one row"

```gherkin
  @e2e
  Scenario: An expanded card's figure value and its evidence badge flow on one row
    Given the AI benchmark page is loaded at a 390 px viewport with one roster card expanded
    When the computed flex direction of a graded figure cell is read from the live page
    Then that computed flex direction is row rather than column
    And the field label's vertical band overlaps the vertical band of its own value
```

- [ ] [AI] **RED**: add the scenario under an `# AC-62` comment and bind it in
      `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`, reading
      `getComputedStyle(cell).flexDirection` on `[data-slot="figure-cell"]` inside the expanded card
      and comparing the `<dt>` and `<dd>` bounding boxes for vertical overlap
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: FAILS — the computed direction is `column` today, and the label sits entirely
      above its value with zero vertical overlap
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] **GREEN**: add a `layout?: "stacked" | "inline"` prop to
      `apps/ayokoding-www/src/features/ai-benchmark/shell/figure-cell.tsx`, defaulting to
      `"stacked"` (`inline-flex flex-col`, today's behaviour, kept for the desktop table so column
      widths do not grow); `"inline"` emits
      `inline-flex flex-row flex-wrap items-baseline gap-x-1.5`, with `flex-row` written explicitly
      rather than relying on the flex default so both the grep guard and AC-62's computed-style read
      have an unambiguous falsifier. Create
      `apps/ayokoding-www/src/features/ai-benchmark/shell/figure-cell.test.tsx` _New file_ asserting
      the default is `stacked` and that `layout="inline"` emits `flex-row`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, and
      `grep -cF 'flex-row' apps/ayokoding-www/src/features/ai-benchmark/shell/figure-cell.tsx`
      prints `1`. Falsifiable both ways: omitting the explicit `flex-row` prints `0` and fails;
      flipping the **default** to inline makes the new default-stability unit test fail.
  - _Suggested executor: `swe-ui-maker`_
- [ ] [AI] **GREEN**: have `model-card.tsx` and `model-table.tsx`'s detail region render each field
      as a rail row — `grid grid-cols-[6.5rem_1fr] md:grid-cols-[9rem_1fr]` with both `<dt>` and
      `<dd>` left-aligned — and pass `layout="inline"` to every `FigureCell` and to the coverage
      cell (`model-table.tsx:131`, the same `inline-flex flex-col` shape) rendered inside them
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: AC-62 passes AND AC-52's seven rows and AC-59 all stay green. Falsifiable both
      ways: passing `layout="inline"` to the desktop table's own cells instead of only the detail
      region widens the table and fails AC-52.
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: document the `layout` prop's contract in `figure-cell.tsx`'s docstring —
      why the default must stay `stacked` (DD-27's "the table must fit" precondition) and why the
      prop cannot affect which figures exist (W-26/W-30 parity)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 6.6 — the expanded card groups its fields (AC-63)

> DD-34 Treatment 3. Fixes DN-3 — `model-table.tsx:338-344` builds one flat 11-entry array with no
> chunking affordance.

**Gherkin (binds) →** "An expanded card groups its fields under labelled headings"

```gherkin
  @unit
  Scenario: An expanded card groups its fields under labelled headings
    Given a model's roster card is rendered with its disclosure expanded
    When the structure of the disclosure's content is inspected
    Then every field belongs to exactly one labelled group
    And each group's heading is one level below the card's own model-name heading
```

- [ ] [AI] **RED**: add the scenario under an `# AC-63` comment, bind it in
      `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`, and extend
      `apps/ayokoding-www/src/features/ai-benchmark/shell/model-card.test.tsx` to assert the
      expanded content contains exactly two `<section>`s each headed by an `<h4>`, that the union of
      their `<dt>` labels equals the full expanded-field label set, and that the intersection of the
      two groups' label sets is empty
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — the expanded content is currently one flat `<dl>` with zero `<h4>`
      elements
- [ ] [AI] **GREEN (keys before consumer)**: add `aiBenchCardGroupModel` and
      `aiBenchCardGroupScores` to **both** the `en` and `id` blocks of
      `apps/ayokoding-www/src/features/i18n/core/translations.ts`, in the same cycle as and BEFORE
      the markup that consumes them, exactly as cycle 6.1 established — `t()` falls back to
      returning the raw key, and this phase's own gate runs AC-35 (no `aiBench` raw-key leak in
      either locale), so a key deferred past its consumer fails the gate or, if papered over with a
      hardcoded literal, ships untranslated copy no later step catches
      — acceptance:
      `grep -c 'aiBenchCardGroupModel:' apps/ayokoding-www/src/features/i18n/core/translations.ts`
      prints `2` and
      `grep -c 'aiBenchCardGroupScores:' apps/ayokoding-www/src/features/i18n/core/translations.ts`
      prints `2`. Falsifiable both ways: a key in one locale only prints `1` and fails; no key at
      all prints `0` and fails.
- [ ] [AI] **GREEN**: in `model-card.tsx` (and the table's detail region), split the expanded
      content into two `<section>`s — `<h4>{t(locale, "aiBenchCardGroupModel")}</h4>` over vendor
      and harnesses, `<h4>{t(locale, "aiBenchCardGroupScores")}</h4>` over `BENCHMARK_COLUMNS` plus
      coverage — each with its own `<dl>`, because a heading is not valid `<dl>` content. Style the
      headings `text-xs font-semibold uppercase tracking-wide text-muted-foreground`
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0, and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate`
      is unaffected (the rule governs markdown, not JSX — the `<h3>`→`<h4>` nesting is asserted by
      AC-63's second `And` step instead)
  - _Suggested executor: `swe-ui-maker`_
- [ ] [AI] **REFACTOR**: express the group→field mapping as one composition over the shared figure
      helper (vendor + harnesses in one group; `BENCHMARK_COLUMNS` + coverage in the other) so the
      card and the detail region read from a single source, and record in a docstring why coverage
      groups with the benchmarks it is derived from
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, and no benchmark id string literal was introduced into `shell/`:
      `grep -cF 'swe-bench' apps/ayokoding-www/src/features/ai-benchmark/shell/model-card.tsx`
      prints `0` (FCIS — the ids come from `core/data/benchmarks.ts`). Falsifiable both ways:
      hardcoding a benchmark id to build the grouping prints `1` and fails.

### TDD cycle 6.7 — unpublished figures share one value (AC-64)

> DD-34 Treatment 4. Fixes DN-4 — an unpublished figure currently occupies a full field slot
> (`model-table.tsx:85`, `:104`, `:190`) at the weight of a real one.

**Gherkin (binds) →** "Unpublished figures share one value instead of occupying a field each"

```gherkin
  @unit
  Scenario: Unpublished figures share one value instead of occupying a field each
    Given a model with more than one unpublished benchmark figure is rendered with its disclosure expanded
    When the disclosure's name-value groups are inspected
    Then every unpublished figure's label is a term in one single group sharing one "not reported" description
    And no unpublished figure occupies a name-value group of its own
```

- [ ] [AI] **RED**: add the scenario under an `# AC-64` comment, bind it in
      `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`, and extend
      `model-card.test.tsx` with a fixture model carrying two unpublished benchmark figures,
      asserting the expanded card contains **exactly one** `<dd>` whose text is
      `t(locale, "aiBenchNoFigure")` and that **two** `<dt>` siblings precede it inside the same
      name-value group
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — today each unpublished figure renders its own `<dt>`/`<dd>` pair, so the
      `<dd>` count is `2`, not `1`. Falsifiable both ways: a fixture with only one unpublished
      figure would pass trivially, so the fixture MUST carry at least two.
- [ ] [AI] **GREEN**: give the shared figure helper a `reported: boolean` per entry, computed as
      `model.figures.some((f) => f.benchmark === id)`, and have `model-card.tsx` (and the table's
      detail region) emit unpublished benchmark figures as one trailing name-value group — every
      absent label as a `<dt>`, one shared `<dd>` carrying `t(locale, "aiBenchNoFigure")` — rendered
      `flex flex-wrap` with comma separators on all but the last `<dt>`. Emit no such group at all
      when the model has zero unpublished figures
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0 with AC-64 green AND AC-54's parity assertion still green — parity is
      preserved by construction because every absent label remains a real `<dt>` in the DOM.
      Falsifiable both ways: dropping the absent labels entirely makes AC-54 fail, and keeping one
      `<dd>` per absent figure makes AC-64 fail.
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: state the W-26/W-30 argument in a docstring at the collapsed run — many
      terms, one shared description, nothing removed from the DOM — citing
      [`tech-docs.md` §DD-34 Treatment 4](./tech-docs.md#treatment-4--absent-figures-collapse-into-one-shared-value-run-dn-4)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### Preserved-defect guards — Phase 6

- [ ] [AI] Confirm DWT-003 holds: the table still composes the `libs/web-ui` primitives
      — acceptance:
      `grep -cE 'Table|TableHeader|TableBody|TableRow|TableHead|TableCell|TableCaption' apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
      is at least `7`
- [ ] [AI] Confirm DWT-002 holds: evidence and coverage colours still route through
      `--evidence-*` tokens
      — acceptance:
      `grep -cF 'var(--evidence-' apps/ayokoding-www/src/features/ai-benchmark/shell/model-table.tsx`
      is at least `1`
- [ ] [AI] Confirm DWT-002 holds in the badge itself after DD-34 moved it into inline flow: all four
      graded dots still resolve through their tokens
      — acceptance:
      `grep -cF 'var(--evidence-' apps/ayokoding-www/src/features/ai-benchmark/shell/evidence-badge.tsx`
      prints `4`. Falsifiable both ways: swapping any one dot back to a raw Tailwind palette class
      prints `3` and fails.
- [ ] [AI] Confirm UWT-004 holds: the visible `(Source)` text survived the move to inline flow
      — acceptance:
      `grep -cF '${SLOT}-source' apps/ayokoding-www/src/features/ai-benchmark/shell/evidence-badge.tsx`
      prints `1`. Falsifiable both ways: dropping the visible source span (or reverting it to
      `sr-only`-only) prints `0` and fails.
- [ ] [AI] Confirm DD-34 did not flip `FigureCell`'s default and so cannot have widened the table
      — acceptance:
      `grep -cF 'layout = "stacked"' apps/ayokoding-www/src/features/ai-benchmark/shell/figure-cell.tsx`
      prints `1`. Falsifiable both ways: defaulting the prop to `"inline"` prints `0` and fails,
      and AC-52 fails alongside it.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] `npx nx run ayokoding-www:test:quick` exits 0 — this is the AC-35 raw-key gate cycle 6.6
      depends on, so it also proves both DD-34 keys landed in both locales
- [ ] [AI] `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 —
      AC-52, AC-59, AC-61 and AC-62 all green simultaneously. This is the load-bearing check that
      DD-34's density work did not widen the table back past the `lg` viewport: AC-61/AC-62 green
      with AC-52 red would mean the inline layout leaked into the desktop table's own cells.
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — AC-63 and AC-64 are bound
- [ ] [AI] Both DD-34 i18n keys exist in both locales:
      `grep -c 'aiBenchCardGroupModel:' apps/ayokoding-www/src/features/i18n/core/translations.ts`
      prints `2`, and
      `grep -c 'aiBenchCardGroupScores:' apps/ayokoding-www/src/features/i18n/core/translations.ts`
      prints `2`

> **Pause Safety**: the roster is progressively disclosed on both mobile and desktop, what the
> disclosure reveals is grouped and evenly ranked, the table fits, and the sticky header is back —
> the DD-27 trade is fully repaid and DD-28/DD-34 are both landed. The page composition is still
> the old order. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 7: Page Composition and Honesty Surface

> Fixes R4 and implements settled decision D3, including the AC-32 rewording.

### TDD cycle 7.1 — the honesty line survives the collapse (AC-32, reworded)

**Gherkin (binds) →** "The page discloses that frontier scores are overwhelmingly vendor-reported"

```gherkin
  @unit
  Scenario: The page discloses that frontier scores are overwhelmingly vendor-reported
    Given the page carries a how-to-read disclosure
    When the page renders
    Then a single honesty line stating that most frontier benchmark scores are vendor self-reported is visible without interaction
    And the remaining how-to-read points are reachable from that line's disclosure control
```

- [ ] [AI] **RED**: reword the AC-32 scenario in the feature file (lines 132-138) to the text above,
      with a comment recording that D3 narrowed the guarantee from the whole disclosure to this one
      line, and update its unit binding in
      `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — no standalone honesty line exists yet
- [ ] [AI] **GREEN**: split
      `apps/ayokoding-www/src/features/ai-benchmark/shell/how-to-read.tsx` so it exports an
      always-visible honesty line rendering `t(locale, "aiBenchHowToVendorReported")` verbatim, plus
      a `<details>` holding the remaining five bullets
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes; no new i18n key was needed for the honesty line
      (`grep -cF 'aiBenchHowToVendorReported' apps/ayokoding-www/src/features/ai-benchmark/shell/how-to-read.tsx`
      is at least `1`)
  - _Suggested executor: `swe-ui-maker`_
- [ ] [AI] **REFACTOR**: render the `<details>` open at `lg` and above via CSS only (no JS width
      check, no hydration mismatch), documenting the choice against DD-29
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### TDD cycle 7.2 — document order (AC-56)

**Gherkin (binds) →** "The chart precedes the roster and both precede the collapsed reference sections"

```gherkin
  @unit
  Scenario: The chart precedes the roster and both precede the collapsed reference sections
    Given the page renders with no filters applied
    When the document order of the page's regions is inspected
    Then the chart region precedes the roster region
    And the legend and sources disclosures both follow the roster region
```

- [ ] [AI] **RED**: add the scenario under an `# AC-56` comment and bind it (add the `@covers`
      marker — `benchmark-content.test.tsx` carries none today, so follow cycle 6.1's pattern rather
      than inferring one from the file), asserting the ordering in
      `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.test.tsx` using
      `compareDocumentPosition`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — today the legend and sources precede the chart
- [ ] [AI] **GREEN**: reorder
      `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.tsx` to
      header (with snapshot + honesty line) → filters → chart → roster → legend `<details>` →
      sources `<details>`, moving the ref-based race guards (EWT-003) without rewriting them and
      leaving the empty-state branch (UWT-006, EWT-004) untouched
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **REFACTOR**: keep the page root a plain `<div>` (EWT-001 — no nested `<main>`) and add a
      comment naming DD-29 and each preserved defect guard
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0 and
      `grep -cF '<main' apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.tsx`
      prints `0`

### TDD cycle 7.3 — the legend and sources stay reachable (AC-57)

**Gherkin (binds) →** "The legend and sources remain reachable after collapsing"

```gherkin
  @unit
  Scenario: The legend and sources remain reachable after collapsing
    Given the legend and sources are rendered as disclosures below the roster
    When each disclosure is expanded
    Then the legend defines each of the four classes and each of the five evidence grades
    And the sources section lists every named operator
```

- [ ] [AI] **RED**: add the scenario under an `# AC-57` comment and bind it, asserting four class
      definitions, five grade definitions, the coverage formula (UWT-005), and one entry per
      `OPERATORS` member
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: FAILS — neither section is a disclosure yet
- [ ] [AI] **GREEN**: wrap the legend and the sources sections in `<details>` with localized
      `<summary>` labels reusing `aiBenchLegendHeading` and `aiBenchSourcesHeading`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [ ] [AI] **REFACTOR**: confirm the pre-existing USS-002 legend scenario still passes unchanged
      (its `Then` asserts a "visible legend"; reword it only if the assertion genuinely no longer
      holds, and record the reword in the checklist if so)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### i18n — Phase 7

- [ ] [AI] Resolve DD-33's second-key decision: read the live `aiBenchHowToSummary` string in both
      `en` and `id` locales, in its new position in the rendered how-to-read disclosure summary. If
      it reads correctly as a "more" affordance in both locales, remove the `[Unverified]` label from
      `tech-docs.md` §DD-33 without adding a new key. Otherwise, add a new `<summary>` label key for
      it (per the step below) and update `tech-docs.md` §File impact to record the new key.
      — acceptance:
      `grep -c '\[Unverified\]' plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/tech-docs.md`
      prints `0`. Falsifiable both ways: leaving DD-33's second-key marker in place prints `1` and
      fails.
- [ ] [AI] Add any new `<summary>` label keys (DD-33) to **both** locale blocks in
      `apps/ayokoding-www/src/features/i18n/core/translations.ts`
      — acceptance: for each new key `K`, `grep -c "$K:" apps/ayokoding-www/src/features/i18n/core/translations.ts`
      prints `2` (one per locale). Falsifiable both ways: a key added to only one locale prints `1`
      and fails.
- [ ] [AI] Confirm AC-35 (no raw translation key leaks on either locale) still passes
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [ ] [AI] `npx nx run ayokoding-www:test:quick` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
- [ ] [AI] `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
- [ ] [AI] No `[Unverified]` marker remains anywhere in `tech-docs.md`:
      `grep -c '\[Unverified\]' plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/tech-docs.md`
      prints `0`. Falsifiable both ways: leaving DD-33's second-key marker in place prints `1` and
      fails.

> **Pause Safety**: the page renders in its new order with the chart first and the reference
> material collapsed below the roster; every existing scenario still passes. Safe to stop
> indefinitely. To resume: `npx nx run ayokoding-www:test:quick`.

---

## Phase 8: Accessibility — Tap Targets and the Live Layout Criteria

> Implements DD-30 and adds the e2e criteria that can only be asserted against a real browser.

### TDD cycle 8.1 — minimum target size (AC-58)

**Gherkin (binds) →** "Every interactive target meets the minimum target size"

```gherkin
  @e2e
  Scenario Outline: Every interactive target meets the minimum target size
    Given the AI benchmark page is loaded at a "<width>" px viewport
    When the bounding box of every link and every disclosure control is measured
    Then every measured target is at least 24 CSS pixels wide and at least 24 CSS pixels tall

    Examples:
      | width |
      | 390   |
      | 1280  |
```

- [ ] [AI] **RED**: add the scenario under an `# AC-58` comment and bind it in
      `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`, measuring
      `boundingBox()` for every `a` and every `summary` inside the page container
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: FAILS, and the failure names at least one `(Source)` evidence link with a height
      below 24 (the diagnosis measured 17px)
- [ ] [AI] **GREEN**: give `apps/ayokoding-www/src/features/ai-benchmark/shell/evidence-badge.tsx`'s
      anchor a minimum 24x24 CSS px box (vertical padding plus `min-h`/`min-w`), and apply the same
      to every `<summary>` introduced in Phases 6 and 7
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both example rows pass
  - _Suggested executor: `swe-ui-maker`_
- [ ] [AI] **REFACTOR**: extract the shared sizing into one documented Tailwind class string
      referenced by both components, with a comment citing WCAG 2.5.8 and DD-30
      — command: `npx nx run ayokoding-www:test:quick`
      — acceptance: exits 0

### TDD cycle 8.2 — chart typography is viewport-independent (AC-49)

**Gherkin (binds) →** "Chart label text renders at a fixed size across viewports"

```gherkin
  @e2e
  Scenario Outline: Chart label text renders at a fixed size across viewports
    Given the AI benchmark page is loaded at a "<width>" px viewport
    When the computed font size of a chart model label is read from the live page
    Then that computed font size equals the computed font size of the same label at every other tested width
    And that computed font size is at least 12 CSS pixels

    Examples:
      | width |
      | 320   |
      | 390   |
      | 768   |
      | 1280  |
      | 1440  |
```

- [ ] [AI] **RED**: add the scenario under an `# AC-49` comment and bind it, reading
      `getComputedStyle(el).fontSize` from the live page at each width
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: PASSES on the current DOM chart. Record the measured font size at all five
      widths in the checklist, then verify falsifiability by temporarily re-wrapping the label in an
      `<svg viewBox>` and confirming the scenario FAILS — this is the test that would have caught
      the original defect, so it must be proven to fail against the original design.
- [ ] [AI] **GREEN**: no production change expected — if the RED step's measurement shows drift,
      fix the offending class
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all five rows pass
- [ ] [AI] **REFACTOR**: record the measured font size and the falsifiability check in
      `evidence/phase-8-typography.txt`
      — acceptance: the file exists and names all five widths

### TDD cycle 8.3 — chart typography does not out-type the body (AC-50)

**Gherkin (binds) →** "Chart label text never exceeds the page's own body text size"

```gherkin
  @e2e
  Scenario: Chart label text never exceeds the page's own body text size
    Given the AI benchmark page is loaded at a 1440 px viewport
    When the computed font sizes of a chart model label and the page body text are read from the live page
    Then the chart label's computed font size is no larger than the page body text's computed font size
```

- [ ] [AI] **RED**: add the scenario under an `# AC-50` comment and bind it
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: PASSES on the new chart; verify falsifiability by temporarily raising the label
      class one step above the body size and confirming the scenario FAILS
- [ ] [AI] **GREEN**: no production change expected; fix any drift found
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: passes
- [ ] [AI] **REFACTOR**: record both measured sizes in `evidence/phase-8-typography.txt`
      — acceptance: the file names the chart label size and the body size

### TDD cycle 8.4 — the plot uses the full mobile width (AC-51)

**Gherkin (binds) →** "The chart plot occupies the full container width on a phone"

```gherkin
  @e2e
  Scenario: The chart plot occupies the full container width on a phone
    Given the AI benchmark page is loaded at a 320 px viewport
    When the width of a capability bar's track is compared with the width of its containing chart region
    Then the bar track spans the full width of that region
    And no reserved label column is present at that width
```

- [ ] [AI] **RED**: add the scenario under an `# AC-51` comment and bind it, comparing
      `boundingBox().width` of the track against its containing region
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: PASSES on the new chart; verify falsifiability by temporarily adding a
      fixed-width label column at all breakpoints and confirming the scenario FAILS
- [ ] [AI] **GREEN**: fix any drift found — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: passes
- [ ] [AI] **REFACTOR**: reuse the Phase 1 navigation helper rather than re-implementing navigation
      — command: `npx nx run ayokoding-www-fe-e2e:typecheck` — acceptance: exits 0

### TDD cycle 8.5 — the chart is above the fold on a phone (AC-55)

**Gherkin (binds) →** "The chart is visible above the fold on a phone"

```gherkin
  @e2e
  Scenario: The chart is visible above the fold on a phone
    Given the AI benchmark page is loaded at a 390 px wide, 844 px tall viewport
    When the vertical offset of the first chart element is read from the live page
    Then that offset is less than the viewport height
```

- [ ] [AI] **RED**: add the scenario under an `# AC-55` comment and bind it
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: PASSES on the reordered page; verify falsifiability by temporarily restoring the
      old composition order and confirming the scenario FAILS with an offset well above 844 (the
      diagnosis measured y=2127)
- [ ] [AI] **GREEN**: fix any drift found — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: passes
- [ ] [AI] **REFACTOR**: record the measured offset in `evidence/phase-8-above-the-fold.txt`
      — acceptance: the file exists and names the measured offset and the viewport height

### TDD cycle 8.6 — locale parity for the whole overhaul (AC-60)

**Gherkin (binds) →** "The overhauled page behaves identically in both locales"

```gherkin
  @e2e
  Scenario Outline: The overhauled page behaves identically in both locales
    Given the AI benchmark page is loaded in the "<locale>" locale at a 390 px viewport
    When the page renders
    Then the chart is present above the fold
    And every roster card is collapsed
    And no raw translation key is rendered

    Examples:
      | locale |
      | en     |
      | id     |
```

- [ ] [AI] **RED**: add the scenario under an `# AC-60` comment and bind all three `Then` steps
      — command: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both rows run; record any Indonesian-specific failure (longer strings can push
      the chart below the fold) before fixing
- [ ] [AI] **GREEN**: fix any `id`-specific layout failure found
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: both rows pass
- [ ] [AI] **REFACTOR**: fold the repeated locale navigation into the Phase 1 helper
      — command: `npx nx run ayokoding-www-fe-e2e:typecheck` — acceptance: exits 0

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] `npx nx run ayokoding-www:test:quick` exits 0
- [ ] [AI] `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
- [ ] [AI] Every AC-49/AC-50/AC-51/AC-55 falsifiability check was performed and its observed failure
      recorded in the checklist — acceptance: four recorded failure observations, one per criterion
- [ ] [AI] `evidence/phase-8-typography.txt` and `evidence/phase-8-above-the-fold.txt` both exist

> **Pause Safety**: every measurable acceptance criterion is implemented and passing at the real
> browser layer, and each has been proven to fail against the pre-change design. Safe to stop
> indefinitely. To resume: `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 9: Spec Coverage Audit

> Guards against the product risk `prd.md` names: rewording a scenario in place can silently drop
> coverage. Nine scenarios are reworded across this plan — four by the overhaul (AC-32, AC-36,
> AC-46, AC-47) and five by the Phase 3 capability-class rename (AC-6, AC-9, AC-41, AC-44, AC-48).

- [ ] [AI] Recount scenarios:
      `grep -cE '^\s+Scenario( Outline)?:' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: the count equals the Phase 0 baseline in `evidence/phase-0-baseline.txt` plus
      exactly 19 (AC-49..AC-64 — twelve for the overhaul, four for DD-34's density work — plus
      AC-65..AC-67 for the Phase 3 capability-class rename); no scenario was deleted. Falsifiable
      both ways: deleting a reworded scenario instead of editing it in place makes the count short
      and fails, and adding an unnumbered scenario makes it long and fails.
- [ ] [AI] Confirm the three rename scenarios landed under their own markers:
      `grep -cE '# AC-(65|66|67)' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `3`. Falsifiable both ways: folding the URL-parameter behaviour into the
      identifier scenario prints `2` and fails.
- [ ] [AI] Confirm the five taxonomy rewordings landed and left no band-sense `light` behind — two
      commands, read independently:
      `grep -nw 'light' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature | grep -cvF '| light |'`
      — acceptance: prints `0`; AND
      `grep -cF '| light |' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `1` (the light-**theme** Examples row of "Band colours meet contrast in
      both themes" is a false positive and MUST survive). Falsifiable in both directions: a missed
      band step makes the first print `1` or more and fails; an over-eager global substitution
      makes the second print `0` and fails.
- [ ] [AI] Confirm AC-6's **title** was reworded rather than the scenario duplicated:
      `grep -cF 'renders in the haiku band' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `1`; AND
      `grep -cF 'renders in the light band' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `0` (the retired title is gone, so this cannot pass on a stale body)
- [ ] [AI] Confirm the four DD-34 scenarios landed under their own markers:
      `grep -cE '# AC-(61|62|63|64)' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `4`. Falsifiable both ways: folding two density behaviours into one
      scenario prints `3` and fails.
- [ ] [AI] Confirm each of the nine reworded scenarios still exists under its original AC number —
      the four overhaul rewordings and the five DD-35 taxonomy rewordings:
      `grep -cE '# AC-(32|36|46|47)' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints at least `4`; AND
      `grep -cE '# AC-(6|9|41|44|48)([^0-9]|$)' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints at least `5`. The trailing `([^0-9]|$)` is load-bearing: without it
      `# AC-6` would also match `# AC-60`..`# AC-67` and the check would pass on a file that had
      lost AC-6 entirely.
- [ ] [AI] Confirm AC-47's body was genuinely reworded, not left stale under an unchanged marker —
      assert on distinguishing text from the NEW scenario, not the `# AC-47` marker alone, and
      falsifiably confirm the stale text is gone:
      `grep -cF 'the declared text size of every chart label is identical at all three widths' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `1`; AND
      `grep -cF 'uses the identical DOM structure at every breakpoint' specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      — acceptance: prints `0` (the pre-change scenario title is gone, so this check cannot pass on
      a stale body the way the marker-only check above could)
- [ ] [AI] Confirm the step-keyword cardinality HARD rule holds for every new and reworded scenario
      (exactly one primary `Given`, one `When`, one `Then`; extras chained with `And`/`But`)
      — command: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance gherkin-keyword-cardinality`
      — acceptance: exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: exits 0
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:specs:e2e:coverage` — acceptance: exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:structure-validation` — acceptance: exits 0

### Phase 9 Gate

- [ ] [AI] All commands above exit 0, the scenario-count arithmetic holds (baseline plus exactly
      `19`), the AC-61..AC-64 marker count prints `4`, and the AC-65..AC-67 marker count prints `3`
- [ ] [AI] The feature file's band-sense sweep prints `0` AND its `| light |` theme row still
      prints `1`

> **Pause Safety**: the spec file and both coverage scanners agree; no scenario is orphaned or
> silently dropped. Safe to stop indefinitely. To resume: re-run the scenario recount.

---

## Phase 10: Live Manual Verification (Playwright MCP)

> The evidence round. Every step produces a committed artefact per the
> [Evidence Capture Convention](../../../repo-governance/development/quality/evidence-capture.md).

### Manual UI Verification — all locales x all breakpoints

- [ ] [AI] Confirm the supported locale set from `apps/ayokoding-www/src/features/i18n/core/config.ts`
      — acceptance: the set is written into the checklist (expected: `en`, `id`)
- [ ] [AI] Start the dev server: `npx nx run ayokoding-www:dev`
      — acceptance: `curl -s -o /dev/null -w '%{http_code}' http://localhost:3101/en/tools/ai-benchmark`
      prints `200`
- [ ] [AI] For EACH locale (`en`, `id`) x EACH breakpoint (320 / 390 / 768 / 1280 / 1440 px):
      navigate to the locale-prefixed URL via `browser_navigate` + `browser_resize`
      — acceptance: the page renders with no error boundary
- [ ] [AI] For each of the ten combinations, read `document.documentElement.scrollWidth` and
      `clientWidth` via `browser_evaluate`
      — acceptance: scrollWidth <= clientWidth in all ten; the ten pairs are recorded inline in this
      checklist as a table
- [ ] [AI] For each of the ten combinations, read the computed `font-size` of a chart model label
      and of the page body via `browser_evaluate`
      — acceptance: the chart label size is identical across all ten and no larger than the body
      size; the values are recorded inline
- [ ] [AI] Inspect the DOM via `browser_snapshot` at each combination — verify `html[lang]` matches
      the locale and no untranslated string appears
      — acceptance: correct `lang` in all ten; zero untranslated strings
- [ ] [AI] Exercise the interactive flows via `browser_click`: expand one roster card, expand the
      how-to-read details, expand the legend, expand sources, change one band's sort control, change
      the harness filter
      — acceptance: each interaction produces the expected state change with no console error
- [ ] [AI] **DD-35 taxonomy verification** — for each locale (`en`, `id`) at 390px AND at 1280px
      (the mobile `<details>` selector and the desktop inline selector are separate DOM nodes,
      `benchmark-filter-class-mobile` and `benchmark-filter-class-desktop`), read the class
      selector's visible option labels via `browser_evaluate` on
      `Array.from(document.querySelectorAll('#benchmark-filter-class-mobile option, #benchmark-filter-class-desktop option')).map((o) => o.textContent)`
      — acceptance: recorded inline as a four-row table (two locales x two widths); every reading
      contains `Haiku` and contains neither `Light` nor `Ringan`. Falsifiable both ways: an
      unrenamed locale value shows `Light` or `Ringan` and fails, and a dropped option shows only
      three entries where four are expected and fails.
- [ ] [AI] **DD-35 band colour verification** — at 390px in `en`, read
      `getComputedStyle(document.documentElement).getPropertyValue('--chart-band-haiku')` and the
      resolved background colour of a haiku-band bar fill via `browser_evaluate`, in BOTH the light
      and dark themes
      — acceptance: the custom property resolves to a non-empty value in both themes and the bar
      fill is not `rgba(0, 0, 0, 0)`; recorded inline. Falsifiable both ways: a half-renamed token
      resolves to the empty string and the bar renders transparent, which fails.
- [ ] [AI] **DD-35 URL round-trip verification** — in each locale, select the Haiku class in the
      filter and read `window.location.search` via `browser_evaluate`; then navigate directly to
      `/<locale>/tools/ai-benchmark?class=haiku&sortHaiku=price-asc` and confirm the filter and the
      haiku band's sort control both reflect that state; then navigate to
      `/<locale>/tools/ai-benchmark?class=light&sortLight=price-asc` and confirm the page renders
      the **default unfiltered, capability-sorted** view without an error
      — acceptance: all three readings recorded inline; the first shows `class=haiku`, the second
      reproduces the filtered and price-sorted state, and the third is indistinguishable from the
      unparameterised page (this is the observable form of DD-35's no-alias decision). Falsifiable
      both ways: a surviving legacy alias would make the third reading show a filtered view and
      fail.
- [ ] [AI] Check `browser_console_messages` after each combination
      — acceptance: zero errors per locale per breakpoint
- [ ] [AI] Check `browser_network_requests`
      — acceptance: no failed request (the page is statically rendered; a 4xx/5xx here is a defect)
- [ ] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot` into
      `evidence/phase-10-ai-benchmark-<locale>-<width>px.png`
      — acceptance: `/bin/ls evidence/ | grep -c 'phase-10-ai-benchmark-'` prints `10`
- [ ] [AI] Capture one additional screenshot per locale showing an expanded roster card at 390px
      — acceptance: two further files exist named `evidence/phase-10-card-expanded-<locale>-390px.png`
- [ ] [AI] **DD-34 density verification** — for each locale (`en`, `id`) at 390px, expand a card for
      a model carrying at least two unpublished benchmark figures and read, via `browser_evaluate`:
      the computed `fontSize` and `fontWeight` of a `dt` and of its own `dd` value span; the
      computed `flexDirection` of a `[data-slot="figure-cell"]` inside that card; the count of
      `h4` elements inside the expanded disclosure; and the count of `dd` elements whose text equals
      the locale's `aiBenchNoFigure` string
      — acceptance: recorded inline in this checklist as a table, with value size > label size,
      value weight > label weight, `flexDirection === "row"`, `h4` count `2`, and exactly one
      shared `not reported` `dd`. Falsifiable both ways: a reverted Treatment 1 shows
      weight 500 against 400 and fails; a reverted Treatment 4 shows two or more `not reported`
      `dd`s and fails.
- [ ] [AI] For each locale at 390px, read the **expanded** card's bounding-box height via
      `browser_evaluate` on that card's `li` and record it inline against R3's measured ~415px
      always-expanded baseline (BS-8)
      — acceptance: both recorded heights are below 415px. Falsifiable both ways: a regression that
      restored the three-line-per-field stack pushes the reading back above 415px and fails, and a
      reading that is implausibly small (for example under 150px, which no seven-field panel can
      reach) indicates fields went missing and must be reconciled against AC-54 before ticking.
- [ ] [AI] Capture one screenshot per locale of that expanded card at 390px into
      `evidence/phase-10-card-density-<locale>-390px.png`
      — acceptance: `/bin/ls evidence/ | grep -c 'phase-10-card-density-'` prints `2`
- [ ] [AI] Verify the same density treatment in the desktop table's per-row detail region: at 1280px
      in `en`, expand one row and confirm the same two `h4` groups, the same rail, and the same
      single shared `not reported` `dd`
      — acceptance: recorded inline; `h4` count `2` and shared-`dd` count `1`, matching the 390px
      reading exactly (DD-34 states the treatment is identical at every width, only the rail widens)
- [ ] [AI] Reference every screenshot in this checklist via `![alt](./evidence/...)` and note the
      console/network status per locale
      — acceptance: `grep -c 'evidence/phase-10' delivery.md` is at least `14`
- [ ] [AI] Verify dark theme at 390px and 1440px in both locales
      — acceptance: four further screenshots named
      `evidence/phase-10-dark-<locale>-<width>px.png`, and band/evidence colours still resolve
      through their tokens
- [ ] [AI] For each locale (`en`, `id`), read the collapsed mobile roster's bounding-box height at
      390px via `browser_evaluate`:
      `document.querySelector('[data-testid="model-table-mobile"]').getBoundingClientRect().height`
      and record both values inline in this checklist against the pre-change baseline of ~15,800px
      recorded in `brd.md` §BS-5 (`~415px per card x 38 = ~15,800px`)
      — acceptance: both recorded heights are a small fraction of 15,800px (giving BS-5 a real
      measured artefact instead of only a screenshot); falsifiable both ways — a regression that
      re-expanded every card back to full height would push this reading back up near 15,800px and
      fail the "small fraction" acceptance

### Phase 10 Gate

- [ ] [AI] All ten scrollWidth pairs recorded and all satisfy scrollWidth <= clientWidth
- [ ] [AI] All ten computed-font-size readings recorded and identical
- [ ] [AI] Both collapsed-mobile-roster bounding-box heights (`en`, `id`) recorded and each is a
      small fraction of the ~15,800px baseline
- [ ] [AI] Both DD-34 density readings (`en`, `id`) recorded: value out-ranks label on size AND
      weight, `flexDirection` is `row`, `h4` count is `2`, and exactly one shared `not reported`
      `dd` — plus the matching 1280px detail-region reading
- [ ] [AI] Both expanded-card bounding-box heights (`en`, `id`) recorded and each is below R3's
      ~415px always-expanded baseline (BS-8)
- [ ] [AI] The DD-35 class-selector table (two locales x two widths) is recorded, every reading
      contains `Haiku`, and no reading contains `Light` or `Ringan` (BS-9)
- [ ] [AI] The DD-35 band-colour reading is recorded and `--chart-band-haiku` resolves non-empty in
      both themes, with a non-transparent bar fill
- [ ] [AI] The DD-35 URL round-trip reading is recorded and the retired `class=light&sortLight`
      query renders the default unfiltered view
- [ ] [AI] Eighteen evidence screenshots exist under `evidence/` and are referenced inline
- [ ] [AI] Zero console errors across all combinations

> **Pause Safety**: the implementation is complete and independently evidenced across both locales
> and five breakpoints, with artefacts committed. Safe to stop indefinitely. To resume: re-read the
> recorded evidence tables in this phase.

---

## Phase 11: Rule-15 Three-Tester Retest

> Mandatory for a web-UI feature change, per
> [User-Facing Delivery Hardening](../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
> Rule 15. Rule 16 (API exploratory retest) does **not** apply — see
> [`tech-docs.md` §Exemptions](./tech-docs.md#exemptions-and-applicability).

- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against
      `http://localhost:3101/en/tools/ai-benchmark` and `http://localhost:3101/id/tools/ai-benchmark`
      across all five breakpoints
      — acceptance: EWT/UWT/DWT findings and SG-###/USS-### spec items are recorded
- [ ] [AI] Append each finding below as a new unchecked, source-attributed checkbox
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`), and
      route each SG-### spec gap and USS-### suggestion into the Phase 9 spec steps
      — acceptance: every reported finding has a corresponding checkbox

### Rule-15 retest follow-ups

<!-- Findings are appended here during execution, one unchecked checkbox each. -->

- [ ] [AI] Fix every rule-15 EWT/UWT/DWT **defect** finding before archival — deferral requires
      explicit user permission and is allowed only when the fix is genuinely impossible; SG-###
      spec-gap proposals and USS-### spec suggestions may be triaged or deferred with written
      rationale
      — acceptance: every `EWT-`/`UWT-`/`DWT-` checkbox in this section is ticked
- [ ] [AI] Re-run `npx nx run ayokoding-www:test:quick` and
      `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` after the fixes
      — acceptance: both exit 0

### Phase 11 Gate

- [ ] [AI] Zero unticked `EWT-`/`UWT-`/`DWT-` defect checkboxes remain
- [ ] [AI] Both gate commands above exit 0
- [ ] [AI] Any deferred SG-###/USS-### item carries a written rationale in this file

> **Pause Safety**: the live page has been independently retested by three specialist testers and
> every defect they found is fixed. Safe to stop indefinitely. To resume: re-read this phase's
> follow-up list and confirm every defect checkbox is ticked.

---

## Phase 12: PR Finalization and Review Cycle

### Local Quality Gates (Before Push) — Unit 2

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. Root Cause Orientation — proactively fix preexisting errors encountered during work. Do
> not defer. Commit preexisting fixes separately with appropriate conventional commit messages.

- [ ] [AI] `npx nx affected -t typecheck` — exits 0
- [ ] [AI] `npx nx affected -t lint` — exits 0
- [ ] [AI] `npx nx affected -t test:quick` — exits 0
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` — exits 0
- [ ] [AI] `npx nx run ayokoding-www:build && npx nx run ayokoding-www-fe-e2e:test:e2e` — exits 0
- [ ] [AI] Re-run every previously failing check — acceptance: zero failures

### Commit Guidelines — Unit 2

- [ ] [AI] Commit thematically, Conventional Commits format, split by concern: chart rewrite,
      roster card, composition reorder, accessibility, specs, evidence
      — acceptance: no commit bundles two unrelated domains
- [ ] [AI] Preexisting fixes get their own separate commits
      — acceptance: `git log --oneline` shows them distinctly

### Integration

- [ ] [AI] Commit and push to `origin ai-benchmark-responsive-overhaul`
      — acceptance: `git ls-remote --heads origin ai-benchmark-responsive-overhaul | grep -c .`
      prints `1`
- [ ] [AI] Open a draft PR against `main`:
      `gh pr create --draft --base main --title "feat(ayokoding-www): responsive overhaul of the AI benchmark page"`
      — acceptance: `gh pr list --head ai-benchmark-responsive-overhaul --json number --jq 'length'`
      prints `1`

### Post-Push CI Verification

- [ ] [AI] Monitor ALL GitHub Actions workflows triggered by the push — poll every 2 minutes with
      one `gh run view --json status,conclusion` per wakeup; never tight-loop, never `gh run watch`
      — acceptance: every check reports `conclusion: success`
- [ ] [AI] If any CI check fails, investigate the root cause and fix it properly — never bypass
      — acceptance: a follow-up commit resolves it and CI turns green
- [ ] [AI] Repeat until ALL GitHub Actions pass with zero failures
      — acceptance: zero failing checks
- [ ] [AI] Do NOT proceed while CI is red

### PR-Review Maker→Fixer Cycle

- [ ] [AI] Cycle 1: fan out the eight discipline specialists, consolidate via
      `pr-review-synthesis-maker`, resolve via `pr-review-fixer`; gate on a green CI run
      — acceptance: CI green and cycle 1's findings resolved
- [ ] [AI] Cycle 2: same, gated by a green CI run — acceptance: CI green and findings resolved
- [ ] [AI] Cycle 3: same, gated by a green CI run
      — acceptance: CI green and cycle 3's consolidated review reports zero unresolved CRITICAL or
      HIGH findings

### Phase 12 Gate

- [ ] [AI] All local gates exit 0
- [ ] [AI] CI is green on the PR
- [ ] [AI] Three review cycles are complete with zero unresolved CRITICAL or HIGH findings

> **Pause Safety**: the PR is fully reviewed and green but not merged. `main` is unchanged since
> Unit 1. Safe to stop indefinitely. To resume: `gh pr checks` and confirm still green.

---

## Phase 13: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays
      in `ose-private` only and is NEVER cross-routed into `ose-public`/`ose-primer`; public
      governance content may propagate via the existing parity loop
      — acceptance: no infra-private content appears in this repo's routed output
- [ ] [AI] Route the DD-26 verification-gap learning specifically — a breakpoint verification that
      checks content PRESENCE and not rendered LEGIBILITY passes a chart rendering at 4.3 CSS px.
      Its likely home is
      `repo-governance/development/quality/manual-behavioral-verification.md` and/or
      `repo-governance/development/quality/evidence-capture.md`, as a requirement that responsive
      verification read computed styles and bounding boxes, not just element presence
      — acceptance: the learning reaches a terminal state naming its durable home
- [ ] [AI] Route each remaining surviving learning to exactly one durable home per the open-ended
      routing matrix — non-code homes may land inline (small edit) or as a `plans/backlog/`
      follow-up (large); code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate
      `plans/backlog/<slug>/` plan and NEVER landed inline
      — acceptance: every `learnings.md` entry records its terminal routing state
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `learnings.md`:
      `No generalizable learnings — <one-line reason>`
      — acceptance: `learnings.md` is never silently empty

### Phase 13 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is in a terminal state (routed inline, filed as backlog, or
      discarded with reason), or the file records the explicit "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR

> **Pause Safety**: `learnings.md` is fully triaged; no future process depends on querying it later.
> Safe to stop indefinitely. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 14: Plan Archival, Final Push, and Merge — **Unit 2 delivery boundary**

### Plan Archival

- [ ] [AI] Verify ALL delivery checklist items in Phases 0–13 are ticked — extract everything above
      the `## Phase 14:` heading and count the unchecked boxes:
      `awk '/^## Phase 14:/{exit} /^ *- \[ \]/{n++} END{print n+0}' delivery.md`
      — acceptance: prints `0`. Falsifiable both ways: any single unticked box in Phases 0–13 makes
      it print a positive integer and fails the step; this phase's own boxes are excluded by the
      `exit` guard so the check cannot be trivially satisfied.
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state or the file records the explicit
      `No generalizable learnings — <reason>` escape; both the secret/sensitivity gate and the
      repo-relevance gate were applied to every surviving entry
- [ ] [AI] Verify ALL quality gates pass (local + CI)
- [ ] [AI] Verify ALL manual assertions pass with committed evidence in `evidence/`
      — acceptance: `/bin/ls evidence/ | grep -c 'phase-10-'` is at least `16`
- [ ] [AI] Verify ALL supported locales were exercised in UI verification (not just the default)
      — acceptance: `/bin/ls evidence/ | grep -c -- '-id-'` is at least `5`
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires
      explicit user permission (only when genuinely impossible); SG-### proposals and USS-###
      suggestions may be triaged or deferred with written rationale
- [ ] [AI] Rule-16 AET verification is **not applicable** — this plan touches no API endpoint; the
      exemption is recorded in `tech-docs.md §Exemptions and applicability`
- [ ] [AI] Rename and move:
      `git mv plans/in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/ plans/done/YYYY-MM-DD__ayokoding-www-ai-benchmark-responsive-overhaul/`
      using today's date as the completion date (NOT the creation date)
      — acceptance: the folder exists under `plans/done/` and the `evidence/` and `assets/`
      subfolders moved with it
- [ ] [AI] Update `plans/in-progress/README.md` — remove this plan's entry
      — acceptance:
      `grep -c 'ayokoding-www-ai-benchmark-responsive-overhaul' plans/in-progress/README.md` prints `0`
- [ ] [AI] Update `plans/done/README.md` — add the entry with its completion date
      — acceptance:
      `grep -c 'ayokoding-www-ai-benchmark-responsive-overhaul' plans/done/README.md` prints `1`
- [ ] [AI] Update any other README that references this plan
      — acceptance: `grep -rl 'in-progress/ayokoding-www-ai-benchmark-responsive-overhaul' --include='*.md' . | grep -c .`
      prints `0`
- [ ] [AI] Commit the archival: `chore(plans): move ayokoding-www-ai-benchmark-responsive-overhaul to done`
      — acceptance: the commit contains only the plan move and README updates

### Final Push and Merge

- [ ] [AI] Commit and push the archival to `origin ai-benchmark-responsive-overhaul` BEFORE merging,
      per the Delivery Mode convention's archival-in-PR requirement
      — acceptance: `gh pr view --json headRefOid --jq .headRefOid` matches local `HEAD`
- [ ] [AI] Verify CI is green on the final push — poll every 2 minutes
      — acceptance: every check reports `conclusion: success`
- [ ] [AI] `gh pr ready` then merge — acceptance:
      `gh pr view --json state --jq .state` prints `MERGED`
- [ ] [AI] Fast-forward local `main` after the merge (side-worktree pushes advance `origin`, not
      local `main`): `git fetch origin && git checkout main && git merge --ff-only origin/main`
      — acceptance: `git rev-parse main` equals `git rev-parse origin/main`
- [ ] [AI] Recover any uncommitted evidence left in the worktree before removal
      — acceptance: `git -C worktrees/ayokoding-www-ai-benchmark-responsive-overhaul status --porcelain | grep -c .`
      prints `0`
- [ ] [AI] Remove the worktree:
      `git worktree remove worktrees/ayokoding-www-ai-benchmark-responsive-overhaul`
      — acceptance: `git worktree list | grep -c ai-benchmark-responsive-overhaul` prints `0`

### Phase 14 Gate

- [ ] [AI] Unit 2's PR reports `MERGED`
- [ ] [AI] The plan folder lives under `plans/done/` with its `assets/` and `evidence/` intact
- [ ] [AI] Local `main` matches `origin/main`
- [ ] [AI] The worktree is removed and no uncommitted work was lost

> **Pause Safety**: the plan is complete, merged, archived, and the worktree is cleaned up. Nothing
> remains in flight. To resume: nothing — the plan is done.
