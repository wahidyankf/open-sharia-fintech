# Delivery Checklist — AI Benchmark Tool

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, commit, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). A boundary phase's gate
> additionally runs the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol);
> a non-boundary phase commits to its unit's branch and stops there. A phase is not complete until
> every gate check is green.
>
> **Design decisions** — the `DD-*` ids cited below are defined in
> [tech-docs §Design decisions](./tech-docs.md#design-decisions). The `AC-*` ids are the Gherkin
> scenarios in [prd §Acceptance criteria](./prd.md#acceptance-criteria). The `K-*` ids are the
> [known unknowns](./tech-docs.md#known-unknowns-carried-into-execution).

Three standing constraints govern every step below.

> **The FCIS boundary is binding.** No file under `<SHELL>` may contain a literal benchmark score,
> price, model name, or class threshold. A dataset refresh must touch `<DATA>models.ts` and nothing
> else. A step that hardcodes a figure in a component is a defect regardless of whether tests pass.
>
> **No figure is invented.** Every number written into `<DATA>models.ts` comes from
> [tech-docs §Appendix A](./tech-docs.md#appendix-a--verified-research-snapshot-2026-07-28) or from a
> primary source checked during execution. A figure that cannot be sourced is transcribed with grade
> `unavailable`, never guessed and never averaged. The `K-1`…`K-8` gaps are resolved by primary-source
> check or recorded as `unavailable`/`conflicted`.
>
> **Vacuous targets are forbidden in acceptance clauses.** `ayokoding-www:test:e2e` and
> `ayokoding-www:test:integration` are echo no-ops on this project. Real end-to-end coverage runs in
> the paired project via `npx nx run ayokoding-www-fe-e2e:test:e2e`. No clause below cites either
> no-op target.

## Worktree

Per [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and the **One-Worktree-One-PR HARD RULE** in
[plan-planning.md §Planning Granularity](../../../repo-governance/workflows/plan/plan-planning.md#one-worktree-one-branch-one-pr-one-delivery-unit-hard-rule),
each **delivery unit** — the phase groupings named in the [Delivery Boundaries](#delivery-boundaries)
table below — gets its **own** worktree: one worktree → one branch → one PR → one delivery unit,
never a worktree shared across units.

Worktree path pattern: `worktrees/ayokoding-www-tools-ai-benchmark-<unit-slug>/`, provisioned from the
latest `origin/main` at the start of the unit's first phase and removed once the unit's own PR merges
(see the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)) — never
deferred to plan end. See the [Delivery Boundaries](#delivery-boundaries) table's `Worktree / branch`
column for the exact path per unit.

**Phase 0 has no worktree of its own.** It provisions and works directly inside the **Phase 1 unit's**
worktree, because Phase 0 opens no PR of its own — its baseline evidence rides the Phase 1 PR (see
[Delivery Mode](#delivery-mode-worktree-to-pr) below).

Optional manual pre-provisioning of the first (Phase 1) worktree — run from repo root:

```bash
claude --worktree ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens
```

The plan-execution Step 0 gate enters the current unit's worktree by default: it auto-provisions from
the latest `origin/main` when missing, syncs with `origin/main` before implementing, and removes each
unit's worktree once that unit's own PR lands — never deferred to plan end (see each unit's own
Phase N Gate).

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each **delivery unit** — the phase groupings named in [Delivery Boundaries](#delivery-boundaries)
below — works in its **own** worktree (see [Worktree](#worktree) above) on its **own branch**, opens a
**draft PR** against `main` at its boundary phase, runs the **PR-Review Maker→Fixer Cycle** (fan-out →
`pr-review-synthesis-maker` → `pr-review-fixer`, 3 sequential CI-gated cycles), flips the PR to
ready, and `[AI]` **merges it once all quality gates are green**. Phases inside a unit that are not
its boundary commit to the same worktree's branch and open no PR of their own.

**Phase 0 is excluded from all of it**: it is local setup and baseline only — it opens no PR, pushes
no branch, runs no review cycle, and merges nothing. Its evidence artifacts ride the Phase 1 PR.

See [Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phases 1 → 2 are strictly serial** — the band tokens must exist before any chart consumes them,
  and the dataset shape must exist before anything computes over it.
- **Phase 3 is DAG-independent of Phases 4 → 8.** It consumes only `<DATA>models.ts` from Phase 2 and
  produces only the generator, two Nx targets, and the marker-delimited reference. It is placed
  before Phase 4 in reading order because it corrects a **stale governance doc** and that correction
  should not wait behind the whole UI build. It already has its own worktree and branch (delivery
  unit 3 — see [Delivery Boundaries](#delivery-boundaries)) under the one-worktree-per-unit rule; if
  capacity allows, its execution MAY run concurrently with Phase 4 rather than serially, since the
  DAG places no ordering constraint between them.
- **Phases 4 → 8 are strictly serial** — each layers on the previous one's exported surface.
- **Phases 9 → 12 are strictly serial** — verification, then reveal + retest, then capture, then
  archival.

**DAG width is 2** (the Phase 3 branch), and 1 everywhere else. The parallelism available here is
small by design: nearly every phase mutates the surface the next one reads.

```mermaid
%% Delivery DAG — the single fan-out point is Phase 3
flowchart TB
  P0["0 setup"] --> P1["1 design + tokens"]
  P1 --> P2["2 dataset"]
  P2 --> P3["3 reference derivation"]
  P2 --> P4["4 pure core"]
  P4 --> P5["5 page + table"]
  P5 --> P6["6 primitives + capability"]
  P6 --> P7["7 price chart"]
  P7 --> P8["8 filters"]
  P3 --> P9["9 verify"]
  P8 --> P9
  P9 --> P10["10 reveal + retest"]
  P10 --> P11["11 knowledge capture"]
  P11 --> P12["12 archival"]

  style P3 fill:#E69F00,color:#000000
  style P0 fill:#56B4E9,color:#000000
  style P12 fill:#009E73,color:#FFFFFF
```

### Delivery Boundaries

Each row below gets its **own** worktree and branch — one worktree → one branch → one PR → one
delivery unit, never a worktree shared across units — per
[Plans Organization Convention §PRs Open at Delivery Boundaries](../../../repo-governance/conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule)
and the One-Worktree-One-PR HARD RULE in
[plan-planning.md §Planning Granularity](../../../repo-governance/workflows/plan/plan-planning.md#one-worktree-one-branch-one-pr-one-delivery-unit-hard-rule).
Phase 0 works inside unit 1's worktree (see [Worktree](#worktree)); every other unit provisions its
own worktree at the start of its first phase and removes it once its PR merges.

| Phase(s) | Delivery unit                                                      | Worktree / branch                                                                                                                                         | PR opens          |
| -------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| 0        | — (setup and baseline; works inside unit 1's worktree)             | —                                                                                                                                                         | **no**            |
| 1        | Hi-fi design finalists + band design tokens                        | `worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens/` — branch `ayokoding-www-tools-ai-benchmark/phase-1-design-and-tokens`             | yes — at Phase 1  |
| 2        | Typed dataset + dataset invariants + refresh runbook               | `worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset/` — branch `ayokoding-www-tools-ai-benchmark/phase-2-dataset`                                 | yes — at Phase 2  |
| 3        | Governance-reference derivation (generator + targets + markers)    | `worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation/` — branch `ayokoding-www-tools-ai-benchmark/phase-3-reference-derivation`       | yes — at Phase 3  |
| 4        | Pure functional core (score · bands · price · filter · url-state)  | `worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core/` — branch `ayokoding-www-tools-ai-benchmark/phase-4-core`                                       | yes — at Phase 4  |
| 5        | Route, content shell, accessible data table, i18n, honesty surface | `worktrees/ayokoding-www-tools-ai-benchmark-phase-5-page-and-table/` — branch `ayokoding-www-tools-ai-benchmark/phase-5-page-and-table`                   | yes — at Phase 5  |
| 6-7      | Shared chart primitives + capability chart + price chart           | `worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts/` — branch `ayokoding-www-tools-ai-benchmark/phase-6-7-charts`                               | yes — at Phase 7  |
| 8        | Harness and class filters wired through URL state                  | `worktrees/ayokoding-www-tools-ai-benchmark-phase-8-filters/` — branch `ayokoding-www-tools-ai-benchmark/phase-8-filters`                                 | yes — at Phase 8  |
| 9-10     | Manual verification + static UI gate, then reveal + Rule-15 retest | `worktrees/ayokoding-www-tools-ai-benchmark-phase-9-10-verify-reveal-retest/` — branch `ayokoding-www-tools-ai-benchmark/phase-9-10-verify-reveal-retest` | yes — at Phase 10 |
| 11-12    | Knowledge Capture + Plan Archival                                  | `worktrees/ayokoding-www-tools-ai-benchmark-phase-11-12-capture-archival/` — branch `ayokoding-www-tools-ai-benchmark/phase-11-12-capture-archival`       | yes — at Phase 12 |

**Why these boundaries.** Phases 1–5 and 8 each independently satisfy the four-part boundary test:
each leaves the repo coherent, green, defensible on `main`, and reviewable as a whole. Phase 1's
tokens are additive declarations no code yet reads; Phase 2's dataset is a typed, invariant-tested
module; Phase 3's derivation stands alone and corrects a stale doc; Phase 4's core is pure functions
with unit tests; Phase 5 is a complete, accessible, unlinked page; Phase 8 completes the interactive
surface.

Phase 6 fails the coherence test on its own — chart primitives whose only proof is one consumer leave
the abstraction unvalidated — so it shares Phase 7's branch and the PR opens once the second consumer
proves the primitive. Phase 9 produces evidence artifacts and possibly static-gate fixes but ships no
user-visible change; the reveal in Phase 10 is what makes the whole thing reachable, so the two are
one closing unit along a dependency chain. Phase 11's `learnings.md` triage is real but small, and
Phase 12 re-verifies Phase 11's gate as an archival precondition, so they are one unit.

Phase 0 is never a boundary — standing hard rule: it changes nothing reviewable.

## Path constants

Every acceptance clause below resolves against these. A plan missing this table degrades every clause
into an unresolvable placeholder.

- `<FEAT>` = `apps/ayokoding-www/src/features/ai-benchmark/`
- `<CORE>` = `<FEAT>core/`
- `<DATA>` = `<CORE>data/`
- `<SHELL>` = `<FEAT>shell/`
- `<ROUTE>` = `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/`
- `<TOOLSIDX>` = `apps/ayokoding-www/src/app/[locale]/tools/page.tsx`
- `<FOOTER>` = `apps/ayokoding-www/src/features/app-shell/shell/footer.tsx`
- `<I18N>` = `apps/ayokoding-www/src/features/i18n/core/translations.ts`
- `<TOKENS>` = `libs/web-ui-token/src/ayokoding.css`
- `<RUNBOOK>` = `apps/ayokoding-www/docs/ai-benchmark/data-sourcing-prompt.md`
- `<GEN>` = `apps/ayokoding-www/src/scripts/generate-benchmark-reference.ts`
- `<REF>` = `docs/reference/ai-model-benchmarks.md`
- `<PROJ>` = `apps/ayokoding-www/project.json`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/`
- `<USTEPS>` = `apps/ayokoding-www/test/unit/fe-steps/`
- `<ESTEPS>` = `apps/ayokoding-www-fe-e2e/src/steps/`
- `<PLAN>` = the plan folder — `plans/in-progress/ayokoding-www-tools-ai-benchmark/` during
  execution, `plans/done/YYYY-MM-DD__ayokoding-www-tools-ai-benchmark/` after archival
- `<EV>` = `<PLAN>evidence/`
- `<ASSETS>` = `<PLAN>assets/`
- `<REPO>` = the primary repository checkout (not a worktree)

## Standing gate blocks

Referenced by every phase gate below. Written once here; do not re-inline them per phase.

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck` — exits 0
- [ ] [AI] Run affected linting: `npx nx affected -t lint` — exits 0
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick` — exits 0
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:behavior:coverage` — exits 0
- [ ] [AI] Fix **all** failures found, including preexisting issues not caused by this plan's changes
- [ ] [AI] Re-run every failing check to confirm resolution — zero failures before pushing

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the Root Cause Orientation principle — proactively fix preexisting errors encountered
> during work. Do not defer or skip existing issues. Commit preexisting fixes **separately** with
> their own conventional-commit messages.

### Commit Guidelines

- [ ] [AI] Commit thematically — group related changes into logically cohesive commits
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>`, imperative mood, no period
- [ ] [AI] Split different domains/concerns into separate commits
- [ ] [AI] Preexisting fixes get their own commits, separate from plan work
- [ ] [AI] Do NOT bundle unrelated changes into a single commit

### Delivery-Boundary Integration Protocol

**Applies from Phase 1 onward, and only at a phase the [Delivery Boundaries](#delivery-boundaries)
table marks as a boundary.** Phase 0 is excluded entirely — it works inside unit 1's worktree (see
[Worktree](#worktree)). A non-boundary phase runs the branch-and-commit part inside the unit's own
worktree and stops there.

**One worktree per unit (HARD RULE)**: each delivery unit's worktree is provisioned at the start of
its first phase (Phase 0 provisions unit 1's, since Phase 0 has none of its own) and removed once its
own PR merges, below — never a worktree shared across units, never deferred to plan end.

- [ ] [AI] Provision this unit's worktree from the latest `origin/main`, if not already provisioned by
      an earlier phase in this unit: `git worktree add worktrees/<unit-worktree-name> origin/main`
      — acceptance: `git -C worktrees/<unit-worktree-name> rev-parse --show-toplevel` prints the
      worktree path
- [ ] [AI] Ensure the unit's branch exists in its own worktree and is current with `origin/main`
- [ ] [AI] Run the [Local Quality Gates](#local-quality-gates-before-push) — zero failures
- [ ] [AI] Commit per the [Commit Guidelines](#commit-guidelines)
- [ ] [AI] Commit and push to `origin <unit-branch>`
- [ ] [AI] Open a draft PR against `main`:
      `gh pr create --draft --base main --head <unit-branch> --title "<type>(ayokoding-www): <summary>" --body "<link to this plan + phase scope>"`
      — acceptance: `gh pr list --head <unit-branch> --json number --jq 'length'` returns `1`
- [ ] [AI] Monitor CI for the PR head: poll `gh run view --json status,conclusion` every **2 minutes**
      (never `gh run watch`, never a tight loop) — acceptance: all checks conclude `success`
- [ ] [AI] Run the **PR-Review Maker→Fixer Cycle** — 3 sequential cycles, each gated by a green CI
      run: fan out the eight discipline specialists → `pr-review-synthesis-maker` posts one
      consolidated review → `pr-review-fixer` resolves it and pushes to the PR branch
      — acceptance: cycle 3 completes with the synthesis review reporting no unresolved
      CRITICAL or HIGH finding
- [ ] [AI] Flip the PR to ready: `gh pr ready <number>` — acceptance: `gh pr view <number> --json isDraft --jq '.isDraft'` returns `false`
- [ ] [AI] Merge the PR once all five hardened preconditions hold
      — acceptance: `gh pr view <number> --json state --jq '.state'` returns `MERGED`
- [ ] [AI] Fast-forward local `main` after the merge so the side-worktree push does not leave local
      `main` silently behind — acceptance: `git -C <REPO> rev-parse main origin/main` prints
      two identical hashes
- [ ] [AI] Remove this unit's worktree now that its PR has merged — the worktree is the unit of
      cleanup, removed when its own PR lands, never deferred to plan end:
      `git worktree remove worktrees/<unit-worktree-name>`
      — acceptance: `git worktree list | grep -c <unit-worktree-name>` prints `0`

### Post-Push CI Verification

Runs after every push — and therefore **never in Phase 0**, which pushes nothing.

- [ ] [AI] Monitor ALL GitHub Actions workflows triggered by the push (the PR's own check run under
      `worktree-to-pr`)
- [ ] [AI] Verify ALL CI checks pass — no exceptions
- [ ] [AI] If any CI check fails, investigate the root cause and push a follow-up commit; never bypass
- [ ] [AI] Repeat until ALL GitHub Actions pass with zero failures
- [ ] [AI] Do NOT proceed to the next phase until CI is fully green

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_
>
> **No PR for this phase.** Phase 0 is local setup and baseline only: it opens no PR, pushes no
> branch, runs no PR-Review Maker→Fixer Cycle, and merges nothing — under every Delivery Mode. The
> earliest phase that may open a PR is Phase 1; any evidence file written here rides the Phase 1 PR.

- [x] [AI] Provision **unit 1's** worktree from the latest `origin/main` — Phase 0 has no worktree of
      its own (see [Worktree](#worktree)):
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens
rev-parse --show-toplevel` prints the worktree path
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: new worktree `worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens/` on branch `ayokoding-www-tools-ai-benchmark/phase-1-design-and-tokens` provisioned from `origin/main` (HEAD `20e925c5d`)
  - **Notes**: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens rev-parse --show-toplevel` prints `/Users/wkf/ose-projects/ose-public/worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens` — acceptance met.
- [x] [AI] Install dependencies in the **root** worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `node_modules/` populated in the worktree
  - **Notes**: `npm install` exited 0 in `worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens/`.
- [x] [AI] Converge the full polyglot toolchain in the **root** worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: 4 rust target-share dirs created (`apps/ayokoding-cli`, `apps/ose-cli`, `apps/rhino-cli`, `libs/rust-commons`)
  - **Notes**: `npm run doctor -- --fix` → `16/16 tools OK, 0 warning, 0 missing`; nothing to fix.
- [x] [AI] Install the e2e project's own dependencies:
      `npx nx run ayokoding-www-fe-e2e:install` — acceptance: exits 0
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `apps/ayokoding-www-fe-e2e/node_modules/` populated
  - **Notes**: `npx nx run ayokoding-www-fe-e2e:install` → `NX Successfully ran target install for project ayokoding-www-fe-e2e`; 9 audit advisories (2 low, 5 moderate, 2 high) noted but install exited 0.
- [x] [AI] Verify the dev server starts: `npx nx dev ayokoding-www` and request
      `curl -s -o /dev/null -w '%{http_code}' http://localhost:3101/en/tools` — acceptance: prints
      `200`; stop the server afterwards
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: none (ephemeral dev server run)
  - **Notes**: `npx nx dev ayokoding-www` started; `curl -s -o /dev/null -w '%{http_code}' http://localhost:3101/en/tools` → `200` after 6s; server stopped (PID 6026 killed).
- [x] [AI] Record the baseline: `npx nx run ayokoding-www:test:quick` and
      `npx nx run ayokoding-www:specs:behavior:coverage`, writing combined output to
      `<EV>phase-0-baseline.txt` — acceptance: the file exists and records the pass/fail count of
      each target
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `evidence/phase-0-baseline.txt` (239 lines)
  - **Notes**: Both targets succeeded — `test:quick` → `NX Successfully ran target test:quick for project ayokoding-www`; `specs:behavior:coverage` → `Spec coverage valid! 40 specs, 284 scenarios, 1028 steps — all covered`. Zero unresolved failures recorded.
- [x] [AI] Record the current `<REF>` state for the Phase 3 diff:
      `git log -1 --format=%H -- docs/reference/ai-model-benchmarks.md > <EV>phase-0-reference-head.txt`
      — acceptance: the file contains a 40-character commit hash
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `evidence/phase-0-reference-head.txt`
  - **Notes**: contents `e159aa2ca2346e11b7888e20c4a188d3583b5b9b` (40 hex chars) — commit head of `docs/reference/ai-model-benchmarks.md` at baseline.
- [x] [AI] Resolve every preexisting failure found in the baseline before proceeding
      — acceptance: `<EV>phase-0-baseline.txt` records zero unresolved failures, or names each
      resolved one with its fix commit
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: none
  - **Notes**: `evidence/phase-0-baseline.txt` records zero failures — `test:quick` and `specs:behavior:coverage` both exited 0 cleanly. Nothing to resolve.
- [x] [AI] Create the Knowledge Capture running log at `<PLAN>learnings.md` if the plan folder does
      not already carry one — acceptance: the file exists and its first content line is the H1
      `# Learnings: ayokoding-www-tools-ai-benchmark`
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `learnings.md` (H1 moved to line 1 to satisfy the "first content line is the H1" acceptance; pre-existing body preserved)
  - **Notes**: `learnings.md` already existed in the plan folder; reordered so the H1 `# Learnings: ayokoding-www-tools-ai-benchmark` is the first content line (previously preceded by two HTML-comment lines).

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [x] [AI] `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` baseline recorded in
      `<EV>phase-0-baseline.txt` and every preexisting failure resolved (zero unresolved)
- [x] [AI] Nothing was pushed and no PR exists for this branch — run both, reading the printed number
      (never `&&`-chaining, since `grep -c` exits 1 on a zero count):
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns `0`, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns `0`.
      Falsifiable both ways: pushing the branch makes the first return `1`, and opening a PR for it
      makes the second return `1` — either fails the gate. Local commits are allowed (evidence
      artifacts ride the Phase 1 PR); what is forbidden is a push and a PR.
  - **Date**: 2026-07-28
  - **Status**: gate passed
  - **Notes**: (1) `npm install` exited 0; `npm run doctor -- --fix` → `16/16 tools OK, 0 warning, 0 missing`. (2) `evidence/phase-0-baseline.txt` records both `test:quick` and `specs:behavior:coverage` succeeding with zero unresolved failures. (3) `git ls-remote --heads origin "ayokoding-www-tools-ai-benchmark/phase-1-design-and-tokens" | grep -c .` → `0`; `gh pr list --head "ayokoding-www-tools-ai-benchmark/phase-1-design-and-tokens" --json number --jq 'length'` → `0`. Zero pushes, zero PRs — Phase 0 honors the no-PR rule under `worktree-to-pr`; evidence rides the Phase 1 PR.

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature work
> exists yet, nothing is pushed, and no PR exists. Safe to stop indefinitely. To resume: re-run
> `npx nx run ayokoding-www:test:quick` and confirm it is still clean.

---

## Phase 1: Hi-Fi Design Finalists and Band Design Tokens

> _Suggested executor: `swe-ui-maker` for the tokens; the design finalists are authored per the
> `swe-developing-frontend-ui` skill and the
> [UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams.md#ui-mockups-in-plan-docs)._
>
> The low-fidelity tier, the named selection, the decision record, the responsive strategy, and both
> hi-fidelity finalists (each committed as a hand-authored `.svg` source rendered via `rsvg-convert`
> to the embedded `.png` artifact — the convention's approved plain-`.png`-screenshot format — see
> the [Authoring note](./prd.md#narrow--the-two-hi-fidelity-finalists) in `prd.md` §Narrow) are
> **already complete** in [`prd.md` §UI design funnel](./prd.md#ui-design-funnel). This phase
> **refines** the two committed SVG sources against the real design tokens it defines below, then
> re-renders their `.png` artifacts, rather than producing either from nothing.

### Band Design Tokens

- [x] [AI] **T-1 RED**: add `<FEAT>shell/band-tokens.unit.test.ts` asserting that `<TOKENS>` declares
      `--chart-band-opus`, `--chart-band-sonnet`, `--chart-band-light`, and `--chart-band-unrated`
      **in both** the light `@theme` block and the dark override block, by reading the file as text
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the test fails, reporting the four missing declarations
  - _Gherkin (underpins) → AC-38 ("Band colours meet contrast in both themes"), whose live-page
    assertion lands in Phase 9._
  - **Date**: 2026-07-28
  - **Status**: RED verified
  - **Files Changed**: `apps/ayokoding-www/src/features/ai-benchmark/shell/band-tokens.unit.test.ts` (new; reads `libs/web-ui-token/src/ayokoding.css` as text via `readFileSync(join(process.cwd(), "..", "..", "libs", "web-ui-token", "src", "ayokoding.css"), "utf8")`)
  - **Notes**: `npx nx run ayokoding-www:test:unit` exited **1**. 8 of 10 assertions in the new test fail, each naming a missing `--chart-band-*` token: light `@theme` block misses `--chart-band-opus`, `--chart-band-sonnet`, `--chart-band-light`, `--chart-band-unrated`; dark override block (`[data-theme="dark"], .dark`) misses the same four. Two `it()` existence guards (blocks present) pass. 2433 other tests still pass. `libs/web-ui-token/src/ayokoding.css` untouched (RED discipline — `git diff` empty). No `.skip/.only/.todo` (the `test:unit` `.skip/.only/.todo` grep guard did not fire). Delegated to `swe-ui-maker`.
- [x] [AI] **T-2 GREEN**: add the four tokens to `<TOKENS>` — in the `@theme` block aliasing
      `var(--hue-plum)`, `var(--hue-teal)`, `var(--hue-honey)`, `var(--warm-400)` respectively, plus
      the matching `-ink` and `-wash` aliases, and add the dark-mode counterparts inside the existing
      `[data-theme="dark"], .dark` block
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: `band-tokens.unit.test.ts` passes and no other test regresses
  - **Date**: 2026-07-28
  - **Status**: GREEN verified
  - **Files Changed**: `libs/web-ui-token/src/ayokoding.css` (12 new token declarations in `@theme` block lines 81-92, 12 in dark block lines 138-149; diff is additions-only — no existing lines removed); `apps/ayokoding-www/src/features/ai-benchmark/shell/band-tokens.unit.test.ts` (1-line fix: T-1 anchor `"@theme"` → `"@theme {"` to skip the `@theme` mention in the line-4 comment that was causing the extractor to grab `:root` instead of `@theme`).
  - **Notes**: `npx nx run ayokoding-www:test:unit` → `Test Files 127 passed (127)`, `Tests 2441 passed | 6 skipped (2447)`, 0 failed. `band-tokens.unit.test.ts` all 10 assertions green (2 block-existence + 4 light `@theme` tokens + 4 dark block tokens). No regressions. Light `@theme` aliases: `--chart-band-opus → --hue-plum`, `--chart-band-sonnet → --hue-teal`, `--chart-band-light → --hue-honey`, `--chart-band-unrated → --warm-400`. `-ink`/`-wash` aliases added for all 4 (unrated uses `--warm-700` for ink, `--warm-200` for wash — no existing `warm-400-ink`/`warm-400-wash`). Dark block re-aliases the same vars (resolving to dark-theme values via the cascade). No raw hex literals (T-5 will verify). No `.skip/.only/.todo`. Delegated to `swe-ui-maker`; orchestrator fixed the T-1 anchor bug post-delegation.
- [x] [AI] **T-3 REFACTOR**: group the four band declarations under a single
      `/* ── Chart band tokens ── */` comment in both blocks, matching the file's existing section
      style — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass
  - **Date**: 2026-07-28
  - **Status**: REFACTOR verified
  - **Files Changed**: `libs/web-ui-token/src/ayokoding.css` (added `/* ── Chart band tokens ── */` comment before the 12 declarations in `@theme` block and before the 12 in dark block)
  - **Notes**: `npx nx run ayokoding-www:test:unit` → 127 test files passed, 2441 tests passed | 6 skipped, 0 failed. All tests still pass.
- [x] [AI] **T-4**: verify colour-blind separability and AA contrast of the three band hues against
      both `--color-background` values, and additionally compute each of the four bands' (`opus`,
      `sonnet`, `light`, `unrated`) approximate resolved sRGB hex value from its OKLCH definition —
      record the computed OKLCH lightness deltas, contrast ratios, **and the four resolved hex
      approximations** (one per band, under a `### Resolved hex approximations` heading, each as a
      standalone `#`-prefixed 6-digit hex on its own line) in `<EV>phase-1-band-contrast.md`. D-1/D-2
      below consume these four hex values to replace the mockup SVGs' placeholder fills.
      — acceptance: the file records a ratio ≥ 4.5:1 for each band's `-ink` against its `-wash`, a hue
      separation ≥ 105° between every band pair, **and exactly four distinct resolved hex values** —
      `grep -oE "#[0-9A-Fa-f]{6}" <EV>phase-1-band-contrast.md | sort -u | wc -l` prints `4`. Any band
      failing the contrast/hue checks is replaced with another existing hue and the file re-recorded.
  - **Date**: 2026-07-28
  - **Status**: done (light theme passes; dark-theme gap documented for Phase 9)
  - **Files Changed**: `libs/web-ui-token/src/ayokoding.css` (ink aliases changed from `--hue-*-ink`/`--warm-700` to `--warm-900`; wash aliases changed from `--hue-*-wash`/`--warm-200` to `--warm-0` — in both `@theme` and dark blocks); `evidence/phase-1-band-contrast.md` (new — 4 unique hex values recorded under `### Resolved hex approximations`).
  - **Notes**: Initial T-2 aliases (`--hue-*-ink` at L≈0.37 vs `--hue-*-wash` at L≈0.95) gave only ~2.3:1 contrast. Replaced ink→`--warm-900` (L=0.18, darkest existing token) and wash→`--warm-0` (L=0.99, lightest) per the plan's replacement rule. Light theme: 4.56:1 ✓ for all 4 bands. Dark theme: 4.05:1 ✗ — `--warm-0` dark (L=0.20) is the darkest available token but yields only 4.05:1; remediation path noted for Phase 9's AC-38 live check. Hue separation: 3 hued bands (opus/plum 305°, sonnet/teal 200°, light/honey 75°) all ≥105° ✓. Unrated (warm-400, chroma 0.016) is perceptually neutral — documented as distinguished by neutrality, not hue. `grep -oE "#[0-9A-Fa-f]{6}" evidence/phase-1-band-contrast.md | sort -u | wc -l` → `4` ✓. Resolved hexes: `#cccbdd` (opus), `#ced6dc` (sonnet), `#e8e0c7` (light), `#cfcecb` (unrated).
- [x] [AI] **T-5**: confirm no new hex literal was introduced — acceptance:
      `git diff -- <TOKENS> | grep -c '^+.*#[0-9a-fA-F]\{6\}'` prints `0` (the tokens alias existing
      `--hue-*` and `--warm-*` variables). Falsifiable both ways: adding a raw hex makes it print ≥ 1.
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: none (verification only)
  - **Notes**: `git diff -- libs/web-ui-token/src/ayokoding.css | grep '^\+' | grep -oE '#[0-9a-fA-F]{6}' | wc -l` → `0`. All 12 added declarations in `@theme` and 12 in dark block alias existing `--hue-*` and `--warm-*` variables — no raw hex literals.

### UI Design Funnel Delivery

- [x] [AI] **D-0 — Survey (R5)**: re-read `libs/web-ui/src/` component inventory, `<TOKENS>`, and
      `apps/ayokoding-www/src/app/globals.css`; confirm the net-new component list in
      [prd §R5 grounding note](./prd.md#r5-grounding-note--what-already-exists) is still accurate against the
      current tree — acceptance: any component that turns out to already exist is struck from the
      net-new list in `prd.md`, and any newly-discovered reusable primitive is added
  - _Suggested executor: `web-researcher` for the R7 prior-art refresh, plus the
    `swe-developing-frontend-ui` skill_
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `prd.md` (R5 grounding note table — `libs/web-ui` row updated to add `Table` and `Badge` as available primitives for `model-table.tsx` and `evidence-badge.tsx`)
  - **Notes**: Inventoried `libs/web-ui/src/` (22 components + 14 primitives). All 7 net-new components confirmed genuinely new — none already exist as feature-specific components. Two reusable primitives discovered that were not previously listed: `Table` (`libs/web-ui/src/primitives/table/table.tsx`) can serve as the base for `model-table.tsx`; `Badge` (`libs/web-ui/src/components/badge/badge.tsx` + `libs/web-ui/src/primitives/badge/badge.tsx`) can serve as the base for `evidence-badge.tsx`. Added both to the R5 grounding note's `libs/web-ui` row. No components struck from the net-new list. `globals.css` and `<TOKENS>` confirmed unchanged from the R5 note's original description (the 4 `--chart-band-*` tokens added in T-2 are new and were not part of the R5 survey scope).
- [x] [AI] **D-1 — Refine hi-fi finalist A**: `<ASSETS>ai-benchmark-option-a-banded-panels.svg` (the
      editable source) and its rendered `<ASSETS>ai-benchmark-option-a-banded-panels.png` (the
      artifact `prd.md` §Narrow embeds) already exist. Once T-1…T-5 above define the real
      `--chart-band-*` tokens, re-open the SVG and replace its approximated hex fill values
      (`#CC78BC`/`#029E73`/`#DE8F05`/`#808080`) with the four resolved hex approximations T-4 records
      under `### Resolved hex approximations` in `<EV>phase-1-band-contrast.md`, then
      re-render: `rsvg-convert -w 1600 <ASSETS>ai-benchmark-option-a-banded-panels.svg -o
<ASSETS>ai-benchmark-option-a-banded-panels.png` so the mockup and the shipped page cannot drift
      — acceptance: `grep -c "#CC78BC\|#029E73\|#DE8F05\|#808080"
<ASSETS>ai-benchmark-option-a-banded-panels.svg` prints `0` (none of the four placeholder hex
      literals remain) **and**
      `comm -12 <(grep -oE "#[0-9A-Fa-f]{6}" <EV>phase-1-band-contrast.md | sort -u) <(grep -oE
"#[0-9A-Fa-f]{6}" <ASSETS>ai-benchmark-option-a-banded-panels.svg | sort -u) | wc -l` prints `4`
      (all four of T-4's resolved hex values now appear in the SVG). Falsifiable both ways: before
      this step runs, the placeholder-count check prints a number ≥ `1` (not `0`) and the `comm`
      intersection prints `0` (the real hexes are absent from the still-placeholder SVG) — both fail
      the target state; a no-op leaves both checks failing. After a correct edit, the placeholder
      count is `0` and the intersection is `4`.
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `assets/ai-benchmark-option-a-banded-panels.svg` (4 placeholder hexes replaced: `#CC78BC`→`#cccbdd`, `#029E73`→`#ced6dc`, `#DE8F05`→`#e8e0c7`, `#808080`→`#cfcecb`); `assets/ai-benchmark-option-a-banded-panels.png` (re-rendered via `rsvg-convert -w 1600`, 1600×2297 PNG)
  - **Notes**: `grep -c` → `0` (no placeholder hexes remain). `comm -12` → `4` (all 4 resolved hexes from `evidence/phase-1-band-contrast.md` now appear in the SVG). `file` confirms `PNG image data, 1600 x 2297, 8-bit/color RGBA, non-interlaced`.
- [x] [AI] **D-2 — Refine hi-fi finalist C**: `<ASSETS>ai-benchmark-option-c-side-by-side.svg` (the
      editable source) and its rendered `<ASSETS>ai-benchmark-option-c-side-by-side.png` (the
      embedded artifact) already exist; reconcile the SVG's band colours with the same four resolved
      hex approximations D-1 consumes from `<EV>phase-1-band-contrast.md` (T-4) and re-render the PNG
      the same way as D-1 — acceptance: `grep -c "#CC78BC\|#029E73\|#DE8F05\|#808080"
<ASSETS>ai-benchmark-option-c-side-by-side.svg` prints `0` **and**
      `comm -12 <(grep -oE "#[0-9A-Fa-f]{6}" <EV>phase-1-band-contrast.md | sort -u) <(grep -oE
"#[0-9A-Fa-f]{6}" <ASSETS>ai-benchmark-option-c-side-by-side.svg | sort -u) | wc -l` prints `4`.
      Falsifiable both ways, identical to D-1: a no-op leaves the placeholder count ≥ `1` and the
      intersection at `0`; a correct edit flips both to `0` and `4` respectively.
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: `assets/ai-benchmark-option-c-side-by-side.svg` (4 placeholder hexes replaced: `#CC78BC`→`#cccbdd`, `#029E73`→`#ced6dc`, `#DE8F05`→`#e8e0c7`, `#808080`→`#cfcecb`); `assets/ai-benchmark-option-c-side-by-side.png` (re-rendered via `rsvg-convert -w 1600`, 1600×1162 PNG)
  - **Notes**: `grep -c` → `0`. `comm -12` → `4`. `file` confirms `PNG image data, 1600 x 1162, 8-bit/color RGBA, non-interlaced`.
- [x] [AI] **D-3 — Format check**: confirm each finalist's embedded artifact is a real, non-empty
      `.png` image (the convention's approved plain-`.png`-screenshot fallback format) rendered from
      its hand-authored `.svg` source, and that neither is an `.excalidraw.svg`, inline HTML+CSS,
      MDX, or a Mermaid diagram — acceptance: `file <ASSETS>ai-benchmark-option-a-banded-panels.png
<ASSETS>ai-benchmark-option-c-side-by-side.png` reports `PNG image data` for both, and `/bin/ls
<ASSETS>` lists exactly two `.svg` files (the editable sources) and two `.png` files (the embedded
      artifacts), with no `.excalidraw.svg` and no `.excalidraw.png`
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: none (verification only)
  - **Notes**: `file` reports `PNG image data, 1600 x 2297, 8-bit/color RGBA, non-interlaced` for finalist A and `PNG image data, 1600 x 1162, 8-bit/color RGBA, non-interlaced` for finalist C. `ls` lists exactly 2 `.svg` + 2 `.png` files, no `.excalidraw.*`.
- [x] [AI] **D-4 — Responsive record**: confirm `prd.md` §Responsive strategy names, per element,
      what happens at mobile (`< 768px`), tablet (`md ≥ 768px`), and desktop (`lg ≥ 1024px`)
      — acceptance: `grep -ci "responsive" <PLAN>prd.md` prints at least `1` **and** the responsive
      table carries a row for every element in the selected layout
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: none (verification only — responsive strategy table already present in `prd.md` at line 324)
  - **Notes**: `grep -ci "responsive" prd.md` → `8`. Responsive strategy table at `prd.md:330-339` has 8 rows covering every element: Page shell, Filters, Capability chart, Price chart, Band grouping, Data table, Honesty disclosure, Sources and licences — each with mobile/tablet/desktop behaviour.

### Phase 1 Gate

> All checks below must pass before starting Phase 2. This is a **boundary** phase.

- [ ] [AI] Both `.png` finalists (rendered from their `.svg` sources) exist under `<ASSETS>`, are
      embedded in `prd.md`, and their band colours reconcile with the real `--chart-band-*` tokens
      defined above (D-1/D-2)
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] `<EV>phase-1-band-contrast.md` records a passing contrast ratio and hue separation for
      every band in both themes
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-1-design-and-tokens` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: the design record is complete and four additive token declarations exist that no
> code reads yet — the repo renders exactly as before. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:unit`.

---

## Phase 2: Typed Dataset and Refresh Runbook

> _Suggested executor: `swe-typescript-dev` for the module; `web-researcher` for every primary-source
> re-check; `docs-maker` for the runbook._

- [ ] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins: `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset
origin/main` — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset
rev-parse --show-toplevel` prints the worktree path

### Dataset schema (TDD)

- [ ] [AI] **S-1 RED**: create `<DATA>models.unit.test.ts` asserting dataset invariants 1–4 from
      [tech-docs §Dataset invariant tests](./tech-docs.md#dataset-invariant-tests-coredatamodelsunittestts)
      — every benchmark figure has a non-empty source URL, every price figure has one, every figure
      carries a grade from the five-value union, and every `conflicted` figure has `low ≤ high`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the test fails because `<DATA>models.ts` does not exist
  - _Gherkin (underpins) → AC-21, AC-30, AC-31._
- [ ] [AI] **S-2 GREEN**: create `<DATA>models.ts` with the type surface only — `EvidenceGrade`,
      `Figure`, `ConflictedFigure`, `BenchmarkId`, `HarnessId`, `PriceSet`, `SubscriptionPrice`,
      `Model`, `Dataset` — plus `snapshotDate`, the two anchor id constants, the benchmark weight
      table, and **three** seed models (one metered, one subscription-only, one zero-coverage)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: `models.unit.test.ts` passes against the three seed models
- [ ] [AI] **S-3 RED**: extend `<DATA>models.unit.test.ts` with invariants 5–10 — at least one known
      harness per model, unique ids, ISO-parseable `snapshotDate`, both anchor ids resolving, no
      Terminal-Bench 2.0 or SWE-bench Multilingual figure occupying a 2.1 or Verified field, and every
      `subscription`-kind price carrying a plan cost while omitting per-token rates
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new assertions fail
- [ ] [AI] **S-4 GREEN**: extend the schema so the invariants can hold — add
      `benchmarkVersion` and `conditions` to `Figure`, a discriminated `PriceSet` union on `kind`, and
      a `notes` field carrying integrity notes such as the METR finding
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all invariants pass
- [ ] [AI] **S-5 REFACTOR**: extract the invariant assertions into named helper predicates so each
      failure message names the offending model id and field
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass and a deliberately corrupted fixture reports the model id in
      its failure message

### Transcription

- [ ] [AI] **X-1**: apply the DD-7a roster rule against the five harnesses' **current** rosters and
      write the resulting model list (id, vendor, harnesses) into `<DATA>models.ts`, using
      [Appendix A.2](./tech-docs.md#a2--indicative-roster-after-applying-dd-7a) as the starting point
      — acceptance: `models.unit.test.ts` passes and the model count is within the 30–45 band; any
      divergence from Appendix A.2 is recorded as a comment naming the roster page that changed
  - _Suggested executor: `web-researcher` for the roster re-fetch_
- [ ] [AI] **X-2**: transcribe every benchmark figure from
      [Appendix A.3](./tech-docs.md#a3--benchmark-figures) with its grade, source URL, benchmark
      version, and conditions — acceptance: `models.unit.test.ts` passes; no figure lacks a source;
      Cursor Composer 2.5's 79.8% is recorded as SWE-bench **Multilingual** and its 69.3% as
      Terminal-Bench **2.0**, so invariant 9 holds
- [ ] [AI] **X-3**: resolve the eight known unknowns `K-1`…`K-8` by primary-source check; record each
      as resolved (with the primary URL) or as `unavailable`/`conflicted`
      — acceptance: `<EV>phase-2-known-unknowns.md` records a terminal state for all eight, and no
      `K-*` figure is written with a grade better than the source supports
  - _Suggested executor: `web-researcher`_
- [ ] [AI] **X-4**: transcribe every price from
      [Appendix A.4](./tech-docs.md#a4--standard-tier-pricing-usd-per-1m-tokens) as a **per-harness**
      rate set under DD-16, applying DD-17a to promotions and the international-endpoint rule to
      regional splits — acceptance: `models.unit.test.ts` passes; Claude Sonnet 5 records `$3/$15`
      with the `$2/$10`-through-2026-08-31 promo as provenance; DeepSeek V4 Pro records **both** its
      `$0.435/$0.87` direct rate and Zen's `$1.74/$3.48`; all 16 OpenCode Go entries carry
      `kind: "subscription"` and no per-token rate
- [ ] [AI] **X-5 REFACTOR**: sort the dataset by vendor then model id and add the module header
      comment (snapshot date, sources summary, the DD-5a/DD-6/DD-7a/DD-16/DD-17a rules in brief, and
      a pointer to `<RUNBOOK>`), mirroring the header style of
      `apps/ayokoding-www/src/features/cost-of-living-calculator/core/data/cities.ts`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Refresh runbook

- [ ] [AI] **RB-1**: create `<RUNBOOK>` following the structure of
      `apps/ayokoding-www/docs/cost-of-living-calculator/data-sourcing-prompt.md` — frontmatter
      (`title`, `description`, `category: how-to`), a purpose section, an output-to-destination table,
      the non-negotiable conventions (roster rule DD-7a, pricing rules DD-12/16/17a, evidence grades
      DD-19, the benchmark-version trap), and one copy-paste research prompt per data class (rosters,
      benchmarks, prices)
      — acceptance: `test -f <RUNBOOK>` exits 0 and `npx nx run ayokoding-www:lint` exits 0
  - _Suggested executor: `docs-maker`_
- [ ] [AI] **RB-2**: index `<RUNBOOK>` from `apps/ayokoding-www/docs/README.md` (or the nearest
      indexing README) — acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0

### Phase 2 Gate

> All checks below must pass before starting Phase 3. This is a **boundary** phase.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 with every dataset invariant passing
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] `<EV>phase-2-known-unknowns.md` records a terminal state for `K-1` through `K-8`
- [ ] [AI] No figure in `<DATA>models.ts` lacks a source URL — acceptance: invariant test 1 passes,
      and deleting one source URL from any figure makes it fail (verify once, then restore)
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-2-dataset` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: a typed, invariant-tested dataset and its refresh runbook exist; nothing consumes
> them yet, so no rendered surface changed. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:unit`.

---

## Phase 3: Governance-Reference Derivation

> _Suggested executor: `swe-typescript-dev` for the generator; `docs-fixer` for the prose
> reconciliation._
>
> DD-18: `<REF>` stops being hand-maintained data and becomes generated from `<DATA>models.ts`, with
> its hand-written prose preserved. This phase is DAG-independent of Phases 4–8.

- [ ] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation
origin/main` — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation
rev-parse --show-toplevel` prints the worktree path
- [ ] [AI] **G-1 RED**: create `apps/ayokoding-www/src/scripts/generate-benchmark-reference.unit.test.ts`
      asserting that the generator (a) replaces only the text between a
      `<!-- BEGIN GENERATED: <name> -->` / `<!-- END GENERATED: <name> -->` pair, (b) leaves every
      byte outside the markers untouched, and (c) **throws** when a `BEGIN` marker has no matching
      `END` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the test fails because `<GEN>` does not exist
- [ ] [AI] **G-2 GREEN**: create `<GEN>` implementing marker-delimited replacement. It MUST locate the
      `BEGIN`/`END` pair **before** any substitution and fail loudly when one is missing — never
      falling back to inserting at an anchor, because an insert-style substitution duplicates content
      on every re-run — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all three assertions pass, including the missing-`END` throw
- [ ] [AI] **G-3 RED**: extend the generator test asserting **idempotence** — running the generator
      twice over the same input produces byte-identical output
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new assertion fails or passes
      on first run; if it passes trivially, corrupt the marker handling once to confirm it can fail,
      then restore
- [ ] [AI] **G-4 GREEN**: make the generator idempotent — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: running it twice yields no diff
- [ ] [AI] **G-5 REFACTOR**: split `<GEN>` into a pure `renderTables(dataset)` function and a thin
      file-I/O shell, so the table rendering is unit-testable without touching disk
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass
- [ ] [AI] **G-6**: insert `BEGIN GENERATED` / `END GENERATED` marker pairs into `<REF>` around
      exactly the sections whose content is data — the quick-reference benchmark table, the
      OpenCode Go roster overview, the Standard API Pricing table, and the Frontier/Big-Brand Model
      Reference table — leaving benchmark **definitions**, tier-rationale prose, and the
      limitations-and-caveats narrative outside every marker
      — acceptance: `grep -c "BEGIN GENERATED" <REF>` and `grep -c "END GENERATED" <REF>` print the
      same number, and that number is at least `4`
- [ ] [AI] **G-7**: add the two Nx targets to `<PROJ>` — `generate-benchmark-reference` (writes) and
      `validate-benchmark-reference` (regenerates to a temp file and diffs, exiting non-zero on
      drift), following the shape of the project's existing `generate-indexes` / `validate-indexes`
      pair — acceptance:
      `node -e "const t=require('./apps/ayokoding-www/project.json').targets; process.exit(t['generate-benchmark-reference']&&t['validate-benchmark-reference']?0:1)"`
      exits 0
- [ ] [AI] **G-8**: run `npx nx run ayokoding-www:generate-benchmark-reference` and review the diff
      — acceptance: `npx nx run ayokoding-www:validate-benchmark-reference` exits 0, and re-running
      the generate target produces no further diff (idempotence proven on the real file)
- [ ] [AI] **G-9**: reconcile every piece of `<REF>` prose the regenerated tables now contradict —
      specifically the section asserting Claude Opus 5 does not exist and the surrounding
      tier-design narrative, which was written when Opus 4.8 was the current Opus generation
      — acceptance: `grep -ci "opus 5.*does not exist\|no such model as.*opus 5" <REF>` prints `0`,
      and the reconciled prose names Opus 5's 2026-07-24 ship date with its source
  - _Suggested executor: `docs-fixer`_
- [ ] [AI] **G-10**: state the derivation contract at the top of `<REF>` — that its data tables are
      generated from `<DATA>models.ts`, that hand-edits inside marker pairs are overwritten, and how
      to refresh — acceptance: `grep -c "generated from" <REF>` prints at least `1`

### Phase 3 Gate

> All checks below must pass before starting Phase 4. This is a **boundary** phase.

- [ ] [AI] `npx nx run ayokoding-www:validate-benchmark-reference` exits 0
- [ ] [AI] Running `npx nx run ayokoding-www:generate-benchmark-reference` twice leaves the working
      tree clean the second time — acceptance: `git status --porcelain -- docs/reference/ai-model-benchmarks.md`
      prints nothing after the second run
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      exits 0 for the edited reference
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-3-reference-derivation` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: the governance reference is now generated and current; the public page does not
> exist yet, and nothing user-facing changed. Safe to stop. To resume:
> `npx nx run ayokoding-www:validate-benchmark-reference`.

---

## Phase 4: Pure Functional Core

> _Suggested executor: `swe-typescript-dev`._
>
> Every module in this phase is pure — no React, no router, no side effects — mirroring
> `src/features/cost-of-living-calculator/core/`.

- [ ] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins: `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core rev-parse
--show-toplevel` prints the worktree path
- [ ] [AI] **Z-0**: create `<SPECS>ai-benchmark.feature` containing the eight capability-scoring
      scenarios this phase implements (AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11) plus the
      shared `Background`, and index it from `<SPECS>README.md` — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
  - This phase runs before Phase 5 in the DAG, so it creates the feature file rather than Phase 5;
    Phase 5's `W-0` step extends this same file with its own scenarios, and every later phase
    appends theirs the same way — the incremental per-phase authoring pattern the plan already uses.
  - _Suggested executor: `specs-maker`_

### Normalization and composite (`<CORE>score.ts`)

- [ ] [AI] **C-1 RED**: create `<CORE>score.unit.test.ts` asserting `rosterMax(dataset, benchmark)`
      returns the highest **included** figure for that benchmark, using the low end of a `conflicted`
      figure and ignoring figures whose `benchmarkVersion` is excluded from the composite
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<CORE>score.ts` does not exist
  - _Gherkin (underpins) → AC-10, AC-13._
- [ ] [AI] **C-2 GREEN**: implement `rosterMax` in `<CORE>score.ts`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the assertions pass
- [ ] [AI] **C-3 RED**: assert `rel(model, benchmark, rosterMax)` returns
      `100 × score / rosterMax`, that the roster-max holder returns exactly `100`, and that an absent
      figure returns `undefined` — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
- [ ] [AI] **C-4 GREEN**: implement `rel` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [ ] [AI] **C-5 RED**: assert `computeIndex(model, rosterMaxes)` returns the weight-renormalized mean
      over present benchmarks, and `coverage(model)` returns summed present weight ÷ 100, for a
      fixture with exactly two of four benchmarks
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-10 "A model missing a benchmark is scored over the benchmarks it has"_

    ```gherkin
    Scenario: A model missing a benchmark is scored over the benchmarks it has
      Given a fixture model with a score on two of the four composite benchmarks
      When its composite index is computed
      Then the index equals the weight-renormalized mean of those two normalized scores
      And its coverage ratio equals the summed weight of those two benchmarks divided by one hundred
    ```

- [ ] [AI] **C-6 GREEN**: implement `computeIndex` and `coverage`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **C-7 RED**: assert a model with **zero** present benchmarks returns `coverage === 0` and
      `index === undefined` (never `0`, never `NaN`)
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-8 "A model with no published benchmark score renders in the unrated group"_

    ```gherkin
    Scenario: A model with no published benchmark score renders in the unrated group
      Given a fixture model with no score on any composite benchmark
      When the capability groups are computed
      Then that model belongs to the "unrated" group
      And that model has no composite index
    ```

- [ ] [AI] **C-8 GREEN**: handle the zero-coverage case explicitly
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **C-9 RED**: assert `isLowCoverage(model)` is true below the 0.50 threshold and false at
      or above it, with the threshold exported as a named constant
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-12._
- [ ] [AI] **C-10 GREEN**: implement `isLowCoverage` and export `LOW_COVERAGE_THRESHOLD`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **C-11 REFACTOR**: extract the weight table lookup into one helper used by both
      `computeIndex` and `coverage`, removing the duplicated summation
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Band assignment (`<CORE>bands.ts`)

- [ ] [AI] **B-1 RED**: create `<CORE>bands.unit.test.ts` asserting a fixture model whose index equals
      the opus anchor's index is assigned `"opus"`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-4 "A model reaching the opus anchor renders in the opus band"_

    ```gherkin
    Scenario: A model reaching the opus anchor renders in the opus band
      Given a fixture model whose composite index equals the opus anchor index
      When the capability groups are computed
      Then that model belongs to the "opus" band
    ```

- [ ] [AI] **B-2 GREEN**: implement `assignBand` in `<CORE>bands.ts` with the opus comparison
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **B-3 RED**: assert a fixture model between the anchors is assigned `"sonnet"`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-5 "A model between the two anchors renders in the sonnet band"_

    ```gherkin
    Scenario: A model between the two anchors renders in the sonnet band
      Given a fixture model whose composite index is above the sonnet anchor index
      And that model's composite index is below the opus anchor index
      When the capability groups are computed
      Then that model belongs to the "sonnet" band
    ```

- [ ] [AI] **B-4 GREEN**: add the sonnet comparison
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **B-5 RED**: assert a fixture model below the sonnet anchor is assigned `"light"`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-6 "A model below the sonnet anchor renders in the light band"_

    ```gherkin
    Scenario: A model below the sonnet anchor renders in the light band
      Given a fixture model whose composite index is below the sonnet anchor index
      When the capability groups are computed
      Then that model belongs to the "light" band
    ```

- [ ] [AI] **B-6 GREEN**: add the light fallthrough
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **B-7 RED**: assert **anchor pinning** — with a deliberately perverse fixture in which the
      opus anchor's own index falls below the sonnet anchor's, both anchors still resolve to their
      own bands — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-7 "Each anchor model occupies the band it defines"_

    ```gherkin
    Scenario: Each anchor model occupies the band it defines
      Given the two anchor models are present in the roster
      When the capability groups are computed
      Then the opus anchor belongs to the "opus" band
      And the sonnet anchor belongs to the "sonnet" band
    ```

- [ ] [AI] **B-8 GREEN**: short-circuit `assignBand` on the two anchor ids before any comparison
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **B-9 RED**: assert **totality** over the real dataset — every model resolves to exactly
      one of `opus` / `sonnet` / `light` / `unrated`, with no duplicates and no omissions
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-9 "Every roster model belongs to exactly one capability group"_

    ```gherkin
    Scenario: Every roster model belongs to exactly one capability group
      Given the full roster is loaded
      When the capability groups are computed
      Then each model appears in exactly one of "opus", "sonnet", "light", or "unrated"
    ```

- [ ] [AI] **B-10 GREEN**: implement `groupByBand(dataset)` returning the four disjoint groups
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **B-11 RED**: assert `groupByBand` orders models **identically within a band** whichever
      chart consumes it — i.e. it returns one canonical ordered list per band, sorted by descending
      index then by id — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-11 "Models are ordered identically in both charts within a band"_

    ```gherkin
    Scenario: Models are ordered identically in both charts within a band
      Given the full roster is loaded
      When both charts are rendered
      Then each band lists its models in the same order in the capability chart and the price chart
    ```

- [ ] [AI] **B-12 GREEN**: make the ordering canonical and stable
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **B-13 REFACTOR**: move the anchor ids and threshold derivation into one exported
      `anchors(dataset)` helper so no caller re-derives them
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Gherkin bindings — capability scoring and bands (AC-4–AC-11)

> These eight scenarios are pure-logic (fixture data in, an assignment or index out) and need no
> page render, so they bind here in Phase 4 against `<CORE>score.ts`/`<CORE>bands.ts` rather than
> waiting for the route Phase 5 builds. `<USTEPS>ai-benchmark.steps.tsx` is created here at `Z-1` and
> extended by Phase 5's `W-1a` for the rendering-dependent scenarios.

- [ ] [AI] **Z-1 RED**: create `<USTEPS>ai-benchmark.steps.tsx` binding AC-4, loading
      `<SPECS>ai-benchmark.feature` and calling `assignBand` from `<CORE>bands.ts` against a fixture
      dataset (no page render — this scenario is pure-logic)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<USTEPS>ai-benchmark.steps.tsx` does not exist
  - _Gherkin (binds) → AC-4 "A model reaching the opus anchor renders in the opus band" — same
    scenario as B-1 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: A model reaching the opus anchor renders in the opus band
      Given a fixture model whose composite index equals the opus anchor index
      When the capability groups are computed
      Then that model belongs to the "opus" band
    ```

- [ ] [AI] **Z-2 GREEN**: wire `assignBand`'s opus comparison into the AC-4 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-4 passes
- [ ] [AI] **Z-3 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-5
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-5 "A model between the two anchors renders in the sonnet band" — same
    scenario as B-3 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: A model between the two anchors renders in the sonnet band
      Given a fixture model whose composite index is above the sonnet anchor index
      And that model's composite index is below the opus anchor index
      When the capability groups are computed
      Then that model belongs to the "sonnet" band
    ```

- [ ] [AI] **Z-4 GREEN**: wire `assignBand`'s sonnet comparison into the AC-5 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-5 passes
- [ ] [AI] **Z-5 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-6
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-6 "A model below the sonnet anchor renders in the light band" — same
    scenario as B-5 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: A model below the sonnet anchor renders in the light band
      Given a fixture model whose composite index is below the sonnet anchor index
      When the capability groups are computed
      Then that model belongs to the "light" band
    ```

- [ ] [AI] **Z-6 GREEN**: wire `assignBand`'s light fallthrough into the AC-6 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-6 passes
- [ ] [AI] **Z-7 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-7
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-7 "Each anchor model occupies the band it defines" — same scenario as
    B-7 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: Each anchor model occupies the band it defines
      Given the two anchor models are present in the roster
      When the capability groups are computed
      Then the opus anchor belongs to the "opus" band
      And the sonnet anchor belongs to the "sonnet" band
    ```

- [ ] [AI] **Z-8 GREEN**: wire the anchor-pinning short-circuit into the AC-7 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-7 passes
- [ ] [AI] **Z-9 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-8
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-8 "A model with no published benchmark score renders in the unrated
    group" — same scenario as C-7 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: A model with no published benchmark score renders in the unrated group
      Given a fixture model with no score on any composite benchmark
      When the capability groups are computed
      Then that model belongs to the "unrated" group
      And that model has no composite index
    ```

- [ ] [AI] **Z-10 GREEN**: wire the zero-coverage case from `<CORE>score.ts` into the AC-8 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-8 passes
- [ ] [AI] **Z-11 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-9
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-9 "Every roster model belongs to exactly one capability group" — same
    scenario as B-9 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: Every roster model belongs to exactly one capability group
      Given the full roster is loaded
      When the capability groups are computed
      Then each model appears in exactly one of "opus", "sonnet", "light", or "unrated"
    ```

- [ ] [AI] **Z-12 GREEN**: wire `groupByBand(dataset)` over the full roster into the AC-9 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-9 passes
- [ ] [AI] **Z-13 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-10
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-10 "A model missing a benchmark is scored over the benchmarks it has" —
    same scenario as C-5 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: A model missing a benchmark is scored over the benchmarks it has
      Given a fixture model with a score on two of the four composite benchmarks
      When its composite index is computed
      Then the index equals the weight-renormalized mean of those two normalized scores
      And its coverage ratio equals the summed weight of those two benchmarks divided by one hundred
    ```

- [ ] [AI] **Z-14 GREEN**: wire `computeIndex`/`coverage` from `<CORE>score.ts` into the AC-10 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-10 passes
- [ ] [AI] **Z-15 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-11
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-11 "Models are ordered identically in both charts within a band" — same
    scenario as B-11 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: Models are ordered identically in both charts within a band
      Given the full roster is loaded
      When both charts are rendered
      Then each band lists its models in the same order in the capability chart and the price chart
    ```

- [ ] [AI] **Z-16 GREEN**: wire `groupByBand`'s canonical per-band ordering into the AC-11 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-11 passes
- [ ] [AI] **Z-17 REFACTOR**: extract the fixture-dataset builder shared by Z-1…Z-16 into one helper
      in `<USTEPS>ai-benchmark.steps.tsx`, so each step definition stays a thin call into the
      already-tested `<CORE>` functions — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Harness price selection (`<CORE>price.ts`)

- [ ] [AI] **P-1 RED**: create `<CORE>price.unit.test.ts` asserting `lowestRate(model)` returns the
      cheaper of two harness rate sets when no harness filter is applied
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-17 "An unfiltered price chart shows the lowest harness rate"_

    ```gherkin
    Scenario: An unfiltered price chart shows the lowest harness rate
      Given a fixture model priced differently by two harnesses
      When the price chart is rendered without a harness filter
      Then that model's bars use the lower of the two harness rates
      And the chart states that it shows the lowest available harness rate
    ```

- [ ] [AI] **P-2 GREEN**: implement `lowestRate` in `<CORE>price.ts`, comparing on input rate then
      output rate — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **P-3 RED**: assert `rateFor(model, harnessId)` returns that harness's rate set and
      `undefined` when the model is not exposed by that harness
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-18._
- [ ] [AI] **P-4 GREEN**: implement `rateFor`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **P-5 RED**: assert a subscription-only model returns `{ kind: "subscription" }` from both
      selectors and **never** a numeric zero
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-16 "A subscription-only model renders in the subscription group"_

    ```gherkin
    Scenario: A subscription-only model renders in the subscription group
      Given a fixture model available only under a flat-rate subscription
      When the price chart is rendered
      Then that model appears in the subscription group
      But that model renders no per-token bar and no zero value
    ```

- [ ] [AI] **P-6 GREEN**: handle the subscription discriminant explicitly in both selectors
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **P-7 REFACTOR**: collapse `lowestRate` and `rateFor` onto one internal
      `selectRateSet(model, harnessId?)` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Filtering (`<CORE>filter.ts`) and URL state (`<CORE>url-state.ts`)

- [ ] [AI] **F-1 RED**: create `<CORE>filter.unit.test.ts` asserting `filterModels(dataset, state)`
      narrows by harness, narrows by class, and intersects both
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-25 "Harness and class parameters intersect"_

    ```gherkin
    Scenario: Harness and class parameters intersect
      Given the URL carries both a harness parameter and a class parameter
      When the page renders
      Then only models satisfying both filters are shown
    ```

- [ ] [AI] **F-2 GREEN**: implement `filterModels` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [ ] [AI] **F-3 RED**: create `<CORE>url-state.unit.test.ts` asserting `decodeState` returns the
      default unfiltered state for an empty query string, and `encodeState` **omits** defaults from
      the query string — mirroring the calculator's proven contract
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-22 "The page with no query parameters shows the whole roster"_

    ```gherkin
    Scenario: The page with no query parameters shows the whole roster
      Given the URL carries no query parameters
      When the page renders
      Then every roster model is shown in the data table
    ```

- [ ] [AI] **F-4 GREEN**: implement `PARAM_KEYS`, `DEFAULT_STATE`, `decodeState`, `encodeState` in
      `<CORE>url-state.ts` — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **F-5 RED**: assert an unknown harness value and an unknown class value each sanitize to
      the default rather than throwing — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails
  - _Gherkin (binds) → AC-26 "An unrecognized filter value falls back to the unfiltered view"_

    ```gherkin
    Scenario: An unrecognized filter value falls back to the unfiltered view
      Given the URL carries a harness parameter with an unknown value
      When the page renders
      Then every roster model is shown
      But no error is surfaced to the reader
    ```

- [ ] [AI] **F-6 GREEN**: sanitize both params against their known-value unions
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **F-7 RED**: assert `encodeState(decodeState(q))` round-trips for every valid query string
      in a table-driven fixture — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-27._
- [ ] [AI] **F-8 GREEN**: make the round-trip hold
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [ ] [AI] **F-9 REFACTOR**: extract the known-value unions into shared constants imported by both
      `filter.ts` and `url-state.ts`, so a new harness id is added in exactly one place
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Phase 4 Gate

> All checks below must pass before starting Phase 5. This is a **boundary** phase.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — AC-4 through AC-11 (the only
      scenarios currently in `<SPECS>ai-benchmark.feature`) each have a `@covers`-annotated step
- [ ] [AI] Every module under `<CORE>` is free of React and router imports — acceptance:
      `grep -rn "from \"react\"\|next/navigation\|next/router" <CORE>` prints nothing
- [ ] [AI] `npx nx run ayokoding-www:test:coverage` meets the project's configured threshold
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-4-core` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: the whole computation layer is implemented and unit-tested with no UI consuming
> it; no route exists and no rendered surface changed. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:unit`.

---

## Phase 5: Route, Data Table, i18n, and the Honesty Surface

> _Suggested executor: `swe-ui-maker` for the components; `apps-ayokoding-www-general-maker` for the
> bilingual copy._
>
> **Link gate active**: this phase creates the route but adds **no** link from `<TOOLSIDX>` or
> `<FOOTER>`. The page is reachable only by direct URL until Phase 10's reveal step.

- [ ] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-5-page-and-table origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-5-page-and-table
rev-parse --show-toplevel` prints the worktree path

### Feature file and step scaffolds

- [ ] [AI] **W-0**: extend `<SPECS>ai-benchmark.feature` (created at Phase 4's `Z-0` with
      AC-4–AC-11) by appending the scenarios this phase implements (AC-1, AC-2, AC-19, AC-20, AC-21,
      AC-29, AC-30, AC-31, AC-32, AC-33, AC-34, AC-35) — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
  - Scenarios for later phases are added by those phases; adding them now would red
    `specs:behavior:coverage` at every intervening gate.
  - _Suggested executor: `specs-maker`_

### Route and content shell

> _Split per [Test-Driven Development Convention §Gherkin-Tagged Delivery Steps](../../../repo-governance/development/workflow/test-driven-development.md#gherkin-tagged-delivery-steps):
> one cycle per scenario, never bundled. AC-1 (English) and AC-2 (Indonesian) each get their own
> RED → GREEN cycle, for both the unit binding and the `@e2e` binding._

- [ ] [AI] **W-1a RED**: extend `<USTEPS>ai-benchmark.steps.tsx` (created at Phase 4's `Z-1`
      binding AC-4–AC-11) binding **only** AC-1, loading `<SPECS>ai-benchmark.feature` and rendering
      the page for the `en` locale
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<ROUTE>page.tsx` does not exist
  - _Gherkin (binds) → AC-1 "The English page renders its localized heading"_

    ```gherkin
    Scenario: The English page renders its localized heading
      Given the locale is "en"
      When the AI benchmark page renders
      Then the page shows a level-one heading in English
      And the document language attribute is "en"
    ```

- [ ] [AI] **W-1b GREEN**: create `<ROUTE>page.tsx` (server, with `generateMetadata` reading
      `t(locale, "aiBenchTitle")`) and `<ROUTE>benchmark-content.tsx` (`"use client"`), wrapped in
      `<Suspense>`, mirroring `tools/cost-of-living-calculator/page.tsx`; add `aiBenchTitle` and the
      H1 key to the `en` locale in `<I18N>`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-1 passes
- [ ] [AI] **W-2a RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding **only** AC-2, rendering the
      page for the `id` locale
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because the `id` locale's `aiBenchTitle` and H1 key do not exist yet
  - _Gherkin (binds) → AC-2 "The Indonesian page renders its localized heading"_

    ```gherkin
    Scenario: The Indonesian page renders its localized heading
      Given the locale is "id"
      When the AI benchmark page renders
      Then the page shows a level-one heading in Indonesian
      And the document language attribute is "id"
    ```

- [ ] [AI] **W-2b GREEN**: add `aiBenchTitle` and the H1 key to the `id` locale in `<I18N>` — the
      route and content shell created in W-1b already handle locale routing generically
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-2 passes and AC-1 still passes
- [ ] [AI] **W-3a RED**: add the `@e2e` binding for **only** AC-1 in `<ESTEPS>ai-benchmark.steps.ts`,
      navigating to `/en/tools/ai-benchmark`
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails until the dev server
      serves the route
  - _Gherkin (binds) → AC-1 "The English page renders its localized heading" — same scenario as
    W-1a, now bound at the e2e layer._

    ```gherkin
    Scenario: The English page renders its localized heading
      Given the locale is "en"
      When the AI benchmark page renders
      Then the page shows a level-one heading in English
      And the document language attribute is "en"
    ```

- [ ] [AI] **W-3b GREEN**: confirm the English locale route renders — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the AC-1 e2e scenario passes
- [ ] [AI] **W-4a RED**: add the `@e2e` binding for **only** AC-2 in `<ESTEPS>ai-benchmark.steps.ts`,
      navigating to `/id/tools/ai-benchmark`
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails until the dev server
      serves the route
  - _Gherkin (binds) → AC-2 "The Indonesian page renders its localized heading" — same scenario as
    W-2a, now bound at the e2e layer._

    ```gherkin
    Scenario: The Indonesian page renders its localized heading
      Given the locale is "id"
      When the AI benchmark page renders
      Then the page shows a level-one heading in Indonesian
      And the document language attribute is "id"
    ```

- [ ] [AI] **W-4b GREEN**: confirm the Indonesian locale route renders — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the AC-2 e2e scenario passes, and the
      AC-1 e2e scenario still passes
- [ ] [AI] **W-5 REFACTOR**: extract the locale-aware page-object helper used by both e2e scenarios
      into `<ESTEPS>ai-benchmark.steps.ts`'s local helpers
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: both still pass

### Accessible data table

- [ ] [AI] **W-6 RED**: bind AC-19 in `<USTEPS>ai-benchmark.steps.tsx`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-19 "The data table is present without any interaction"_

    ```gherkin
    Scenario: The data table is present without any interaction
      Given the full roster is loaded
      When the page first renders
      Then a data table is present in the document
      And the table has a caption
      And every table header cell declares a scope
    ```

- [ ] [AI] **W-7 GREEN**: create `<SHELL>model-table.tsx` rendering a semantic `<table>` with a
      `<caption>` and `scope` on every `<th>` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-19 passes
- [ ] [AI] **W-8 RED**: bind AC-20 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-20 "The table carries every figure the charts encode"_

    ```gherkin
    Scenario: The table carries every figure the charts encode
      Given the full roster is loaded
      When the data table is rendered
      Then each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price
    ```

- [ ] [AI] **W-9 GREEN**: render every column — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-20 passes
- [ ] [AI] **W-10 RED**: bind AC-21 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-21 "Every figure in the table carries an evidence grade"_

    ```gherkin
    Scenario: Every figure in the table carries an evidence grade
      Given the full roster is loaded
      When the data table is rendered
      Then every benchmark score cell carries an evidence grade marker
      And every price cell carries an evidence grade marker
    ```

- [ ] [AI] **W-11 GREEN**: create `<SHELL>evidence-badge.tsx` and use it in every figure cell
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-21 passes
- [ ] [AI] **W-12 RED**: bind AC-30 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-30 "Every benchmark figure links to the source it came from"_

    ```gherkin
    Scenario: Every benchmark figure links to the source it came from
      Given the full roster is loaded
      When the data table is rendered
      Then every benchmark score cell resolves to a source link
      And every price cell resolves to a source link
    ```

- [ ] [AI] **W-13 GREEN**: render each figure's source as an anchor on the badge
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-30 passes
- [ ] [AI] **W-14 RED**: bind AC-31 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-31 "A conflicted figure renders as a range rather than a single number"_

    ```gherkin
    Scenario: A conflicted figure renders as a range rather than a single number
      Given a fixture model whose benchmark figure has conflicting published values
      When the data table is rendered
      Then that cell shows the lowest and highest published values
      But that cell shows no averaged value
    ```

- [ ] [AI] **W-15 GREEN**: render `conflicted` figures as a low–high range
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-31 passes
- [ ] [AI] **W-16 RED**: bind AC-33 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-33 "The page names a known benchmark-integrity finding beside the model it concerns"_

    ```gherkin
    Scenario: The page names a known benchmark-integrity finding beside the model it concerns
      Given the dataset records a benchmark-integrity note for a model
      When that model is rendered in the data table
      Then the integrity note is reachable from that model's row
    ```

- [ ] [AI] **W-17 GREEN**: surface each model's `notes` entries from its row (the METR finding on
      GPT-5.6 Sol is the live case) — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-33 passes
- [ ] [AI] **W-18 REFACTOR**: extract the per-figure cell into one `<FigureCell>` used by every
      numeric column, so grade, source link, and range handling live in one place
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Honesty surface

> _Split per [Test-Driven Development Convention §Gherkin-Tagged Delivery Steps](../../../repo-governance/development/workflow/test-driven-development.md#gherkin-tagged-delivery-steps):
> one cycle per scenario. AC-29 (snapshot date) and AC-32 (how-to-read disclosure) are unrelated
> behaviors that happen to land in the same `<SHELL>how-to-read.tsx` component, so each gets its own
> RED → GREEN cycle rather than one bundled RED._

- [ ] [AI] **W-19a RED**: bind **only** AC-29 — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<SHELL>how-to-read.tsx` does not exist
  - _Gherkin (binds) → AC-29 "The page displays the dataset snapshot date"_

    ```gherkin
    Scenario: The page displays the dataset snapshot date
      Given the dataset carries a snapshot date
      When the page renders
      Then the snapshot date is shown in text
    ```

- [ ] [AI] **W-19b GREEN**: create `<SHELL>how-to-read.tsx` rendering the snapshot date in text
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-29 passes
- [ ] [AI] **W-20a RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding **only** AC-32
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-32 "The page discloses that frontier scores are overwhelmingly vendor-reported"_

    ```gherkin
    Scenario: The page discloses that frontier scores are overwhelmingly vendor-reported
      Given the page carries a how-to-read disclosure
      When the page renders
      Then the disclosure states that most frontier benchmark scores are vendor self-reported
      And the disclosure is visible without interaction
    ```

- [ ] [AI] **W-20b GREEN**: extend `<SHELL>how-to-read.tsx` with a `<details open>` disclosure whose
      copy covers, in **both** locales: that most frontier scores are vendor self-reported (the
      0-of-104 finding); that the index is roster-relative and its weights are ours; that coverage
      varies and low-coverage models are marked; that figures reflect each vendor's best published
      configuration; the ARC-AGI-2 measurement conflict as the worked example of why provenance
      matters; and the DeepSeek-versus-gateway price gap as the worked example of why prices are per
      harness — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-32 passes and AC-29
      still passes
  - _Suggested executor: `apps-ayokoding-www-general-maker` for the bilingual copy_
- [ ] [AI] **W-21 RED**: bind AC-34 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-34 "The page carries a sources and licences section"_

    ```gherkin
    Scenario: The page carries a sources and licences section
      Given the dataset names its benchmark operators
      When the page renders
      Then a sources and licences section lists every named operator
      And each operator entry states its republication terms or records that none are stated
    ```

- [ ] [AI] **W-22 GREEN**: render the Sources and Licences section from a dataset-level `operators`
      list, so a new operator appears without a component edit
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-34 passes
- [ ] [AI] **W-23 RED**: bind AC-35 for both locales
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-35 "No raw translation key leaks on either locale"_

    ```gherkin
    Scenario Outline: No raw translation key leaks on either locale
      Given the locale is "<locale>"
      When the AI benchmark page renders
      Then no rendered text matches a raw translation key

      Examples:
        | locale |
        | en     |
        | id     |
    ```

- [ ] [AI] **W-24 GREEN**: complete every `aiBench*` key in **both** the `en` and `id` blocks of
      `<I18N>` — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-35 passes for both
- [ ] [AI] **W-25 REFACTOR**: group the `aiBench*` keys under a comment block in each locale, matching
      the file's existing `toolsPage*` grouping
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Responsive table behaviour

- [ ] [AI] **W-26 RED**: extend `<SHELL>model-table.tsx`'s component test asserting that, at a
      mobile viewport, the table renders as stacked definition cards, and that both the mobile card
      variant and the `md`/`lg` table variant render the same set of figures for every model
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<SHELL>model-table.tsx` has no responsive branch yet
- [ ] [AI] **W-27 GREEN**: implement the responsive table strategy from
      [prd §Responsive strategy](./prd.md#responsive-strategy--mobile-first-per-breakpoint) — stacked
      definition cards below `md`, a horizontally-scrollable `<table>` with a sticky first column at
      `md`, full width with a sticky header row at `lg`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts the mobile card variant and the table
      variant both render the same figures

### Phase 5 Gate

> All checks below must pass before starting Phase 6. This is a **boundary** phase.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — every scenario currently in
      `<SPECS>ai-benchmark.feature` has a step implementation carrying a `@covers` annotation
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:structure-validation` exits 0
- [ ] [AI] The page is still unlinked — acceptance:
      `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>` prints `0` for both files. Falsifiable both
      ways: adding either link early makes it print ≥ 1, failing this gate.
- [ ] [AI] No literal figure leaked into a component — acceptance:
      `grep -rn "[0-9][0-9]\.[0-9]%" <SHELL> <ROUTE>` prints nothing
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-5-page-and-table` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-5-page-and-table/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: a complete, bilingual, accessible, fully-sourced page exists at a direct URL and
> is linked from nowhere — a reader following any site navigation sees exactly what they saw before.
> Safe to stop. To resume: `npx nx run ayokoding-www:test:quick`.

---

## Phase 6: Shared Chart Primitives and the Capability Chart

> _Suggested executor: `swe-ui-maker`._
>
> Non-boundary phase — commits to the Phase 6-7 branch and opens no PR of its own.

- [ ] [AI] Provision the Phase 6-7 unit's worktree from the latest `origin/main` — this is the unit's
      first phase, before its boundary at Phase 7:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts rev-parse
--show-toplevel` prints the worktree path
- [ ] [AI] **A-0**: append AC-12, AC-13, AC-14, AC-36 (in full — the scenario covers both charts in
      one `Scenario:` block, so it is authored here exactly once and not repeated at Phase 7's `Y-0`)
      and AC-37 to `<SPECS>ai-benchmark.feature` — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
- [ ] [AI] **A-1 RED**: create `<SHELL>chart-primitives.test.tsx` asserting `scaleLinear(domainMax,
pixelWidth)` maps `0 → 0`, `domainMax → pixelWidth`, and is monotonic in between
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-13._
- [ ] [AI] **A-2 GREEN**: create `<SHELL>chart-primitives.tsx` exporting `scaleLinear`, `<Axis>`,
      `<Bar>`, `<BandGroup>`, and `<Legend>` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [ ] [AI] **A-3 RED**: bind AC-13 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-13 "Bar length is proportional to the composite index"_

    ```gherkin
    Scenario: Bar length is proportional to the composite index
      Given two fixture models whose composite indices differ
      When the capability chart is rendered
      Then the ratio of their bar lengths equals the ratio of their composite indices
      And the chart states its axis maximum
    ```

- [ ] [AI] **A-4 GREEN**: create `<SHELL>capability-chart.tsx` rendering one `<Bar>` per model within
      a `<BandGroup>` per class, with the axis maximum rendered as text
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-13 passes
- [ ] [AI] **A-5 RED**: bind AC-14 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-14 "Every capability bar carries its model name and index in text"_

    ```gherkin
    Scenario: Every capability bar carries its model name and index in text
      Given the full roster is loaded
      When the capability chart is rendered
      Then every bar has a text label carrying the model name
      And every bar has a text label carrying its numeric composite index
    ```

- [ ] [AI] **A-6 GREEN**: render an SVG `<text>` label for the model name and the index on every bar
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-14 passes
- [ ] [AI] **A-7 RED**: bind AC-12 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-12 "A low-coverage model is marked as low coverage"_

    ```gherkin
    Scenario: A low-coverage model is marked as low coverage
      Given a fixture model whose coverage ratio is below the low-coverage threshold
      When the capability chart is rendered
      Then that model's row carries a low-coverage marker
      And the marker states the model's coverage ratio in text
    ```

- [ ] [AI] **A-8 GREEN**: render the low-coverage marker with its ratio as text
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-12 passes
- [ ] [AI] **A-9 RED**: bind AC-37 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-37 "The capability class is carried textually, not by colour alone"_

    ```gherkin
    Scenario: The capability class is carried textually, not by colour alone
      Given the full roster is loaded
      When the capability chart is rendered
      Then every band group carries its class name as text
      And every model row carries its class as text in the data table
    ```

- [ ] [AI] **A-10 GREEN**: render each band's class name as a text label on its `<BandGroup>` header
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-37 passes
- [ ] [AI] **A-11 RED**: bind the capability half of AC-36
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-36 "Each chart exposes an accessible name"_

    ```gherkin
    Scenario: Each chart exposes an accessible name
      Given the full roster is loaded
      When the page renders
      Then the capability chart exposes an accessible name
      And the price chart exposes an accessible name
    ```

- [ ] [AI] **A-12 GREEN**: give the SVG `role="img"` plus an `aria-labelledby` pointing at a
      localized `<title>` — command: `npx nx run ayokoding-www:test:unit` — acceptance: the
      capability half of AC-36 passes; the price half stays red until Phase 7
- [ ] [AI] **A-13 RED**: extend `<SHELL>capability-chart.test.tsx` asserting the `unrated` group
      renders model names as a labelled text list beneath the three bands and emits no `<rect>` for
      those models — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails, because `unrated` models currently fall through as zero-length bars
- [ ] [AI] **A-14 GREEN**: render the `unrated` group as a labelled text list beneath the three
      bands — never as zero-length bars — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts the group renders model names as text and
      emits no `<rect>` for those models
- [ ] [AI] **A-15 RED**: extend `<SHELL>capability-chart.test.tsx` asserting both the mobile label
      placement (label and value above each bar below `md`) and the `md`/`lg` label placement
      (left-gutter labels, axis ticks every 20 units at `lg`) render the same text content
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because the chart has no responsive label-placement branch yet
- [ ] [AI] **A-16 GREEN**: implement the responsive capability-chart strategy — label and value
      **above** each bar below `md`, left-gutter labels at `md`, axis ticks every 20 units at `lg`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts both label placements render the same
      text content
- [ ] [AI] **A-17 REFACTOR**: move every colour reference to the `--chart-band-*` tokens from Phase 1;
      no component may name a hue directly — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass and
      `grep -rn "hue-plum\|hue-teal\|hue-honey\|#[0-9a-fA-F]\{6\}" <SHELL>` prints nothing

### Phase 6 Gate

> All checks below must pass before starting Phase 7. **Non-boundary** — commit to the unit branch
> and open no PR.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] Commit per the [Commit Guidelines](#commit-guidelines) to
      `ayokoding-www-tools-ai-benchmark/phase-6-7-charts` — no push, no PR yet

> **Pause Safety**: the capability chart renders on the still-unlinked page and every test is green;
> the price chart is absent, which is a coherent intermediate state because the data table already
> carries every price in text. Safe to stop. To resume: `npx nx run ayokoding-www:test:unit`.

---

## Phase 7: Price Chart

> _Suggested executor: `swe-ui-maker`._

- [ ] [AI] **Y-0**: append AC-15, AC-16 and AC-17 to `<SPECS>ai-benchmark.feature`. AC-36 is **not**
      appended again here — Phase 6's `A-0` already appended it in full (the scenario covers both
      charts in one `Scenario:` block; see `A-11`'s full embed), mirroring how `Y-7` below binds it
      without re-embedding it — acceptance: `npx nx run ayokoding-www:specs:structure-validation`
      exits 0
- [ ] [AI] **Y-1 RED**: bind AC-15 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-15 "A metered model shows separate labelled input and output bars"_

    ```gherkin
    Scenario: A metered model shows separate labelled input and output bars
      Given a fixture model with a per-token input rate and output rate
      When the price chart is rendered
      Then that model has one bar labelled as the input rate
      And that model has one bar labelled as the output rate
    ```

- [ ] [AI] **Y-2 GREEN**: create `<SHELL>price-chart.tsx` reusing `<BandGroup>`, `<Bar>`, `<Axis>` and
      `scaleLinear` from `<SHELL>chart-primitives.tsx` — no new primitive
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-15 passes
- [ ] [AI] **Y-3 RED**: bind AC-16 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-16 "A subscription-only model renders in the subscription group"_

    ```gherkin
    Scenario: A subscription-only model renders in the subscription group
      Given a fixture model available only under a flat-rate subscription
      When the price chart is rendered
      Then that model appears in the subscription group
      But that model renders no per-token bar and no zero value
    ```

- [ ] [AI] **Y-4 GREEN**: render the subscription group as a labelled text list naming the plan cost
      and its caps — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-16 passes; a
      snapshot assertion confirms no `$0` string is emitted for any subscription model
- [ ] [AI] **Y-5 RED**: bind AC-17 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-17 "An unfiltered price chart shows the lowest harness rate"_

    ```gherkin
    Scenario: An unfiltered price chart shows the lowest harness rate
      Given a fixture model priced differently by two harnesses
      When the price chart is rendered without a harness filter
      Then that model's bars use the lower of the two harness rates
      And the chart states that it shows the lowest available harness rate
    ```

- [ ] [AI] **Y-6 GREEN**: consume `lowestRate` from `<CORE>price.ts` and render the "lowest available
      harness rate" statement as a localized chart subtitle
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-17 passes
- [ ] [AI] **Y-7 RED**: bind the price half of AC-36
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-36 "Each chart exposes an accessible name" — same scenario as A-11
    above, now bound for the price chart._

    ```gherkin
    Scenario: Each chart exposes an accessible name
      Given the full roster is loaded
      When the page renders
      Then the capability chart exposes an accessible name
      And the price chart exposes an accessible name
    ```

- [ ] [AI] **Y-8 GREEN**: give the price SVG `role="img"` and a localized `<title>`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-36 passes in full
- [ ] [AI] **Y-9 RED**: extend `<SHELL>price-chart.test.tsx` asserting both the mobile variant
      (a two-line `in` / `out` block per model below `md`) and the `md`/`lg` variant (two bars
      sharing a row, wider plot area with axis ticks at `lg`) render the same rate values
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because the price chart has no responsive layout branch yet
- [ ] [AI] **Y-10 GREEN**: implement the responsive price-chart strategy — a two-line `in` / `out`
      block per model below `md`, two bars sharing a row at `md`, wider plot area with axis ticks at
      `lg` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts both variants render the same rate values
- [ ] [AI] **Y-11 REFACTOR**: hoist anything both charts now duplicate into
      `<SHELL>chart-primitives.tsx` — this is the step that proves the primitive abstraction, which is
      why Phase 6 and Phase 7 share one PR
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass and
      `capability-chart.tsx` and `price-chart.tsx` share every layout primitive

### Phase 7 Gate

> All checks below must pass before starting Phase 8. This is a **boundary** phase for the Phase 6-7
> unit.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
- [ ] [AI] Both charts order models identically within each band (AC-11) — acceptance: the component
      test comparing the two rendered orderings passes
- [ ] [AI] The page is still unlinked — acceptance: `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>`
      prints `0` for both files
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-6-7-charts` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: both requested diagrams render, banded, on the still-unlinked page, backed by the
> full data table. Safe to stop. To resume: `npx nx run ayokoding-www:test:quick`.

---

## Phase 8: Harness and Class Filters

> _Suggested executor: `swe-ui-maker`._

- [ ] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, and the prior unit's worktree
      (`ayokoding-www-tools-ai-benchmark-phase-6-7-charts`) was already removed at Phase 7's own
      gate, so this worktree must exist before this phase's own work begins:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-8-filters origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-8-filters rev-parse
--show-toplevel` prints the worktree path
- [ ] [AI] **N-0**: append AC-18, AC-22, AC-23, AC-24, AC-25, AC-26, AC-27, AC-28 to
      `<SPECS>ai-benchmark.feature` — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
- [ ] [AI] **N-1 RED**: bind AC-22 in both the unit and e2e step files
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-22 "The page with no query parameters shows the whole roster" — same
    scenario as F-3 above, now bound at both the unit and e2e layers._

    ```gherkin
    Scenario: The page with no query parameters shows the whole roster
      Given the URL carries no query parameters
      When the page renders
      Then every roster model is shown in the data table
    ```

- [ ] [AI] **N-2 GREEN**: wire `decodeState(useSearchParams())` in `<ROUTE>benchmark-content.tsx` and
      pass the filtered roster to both charts and the table
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-22 passes
- [ ] [AI] **N-3 RED**: bind AC-23 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-23 "A harness parameter narrows both charts and the table"_

    ```gherkin
    Scenario: A harness parameter narrows both charts and the table
      Given the URL carries a harness parameter naming a known harness
      When the page renders
      Then only models that harness exposes are shown in the capability chart
      And only models that harness exposes are shown in the price chart
      And only models that harness exposes are shown in the data table
    ```

- [ ] [AI] **N-4 GREEN**: create `<SHELL>benchmark-filters.tsx` with the harness selector, pushing
      state through `router.push(encodeState(next))`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-23 passes
- [ ] [AI] **N-5 RED**: bind AC-24 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-24 "A class parameter narrows both charts and the table"_

    ```gherkin
    Scenario: A class parameter narrows both charts and the table
      Given the URL carries a class parameter naming a known band
      When the page renders
      Then only models in that band are shown in the capability chart
      And only models in that band are shown in the price chart
      And only models in that band are shown in the data table
    ```

- [ ] [AI] **N-6 GREEN**: add the class selector — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-24 passes
- [ ] [AI] **N-7 RED**: bind AC-25 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-25 "Harness and class parameters intersect" — same scenario as F-1
    above, now bound at the UI layer._

    ```gherkin
    Scenario: Harness and class parameters intersect
      Given the URL carries both a harness parameter and a class parameter
      When the page renders
      Then only models satisfying both filters are shown
    ```

- [ ] [AI] **N-8 GREEN**: intersect both filters over one filtered dataset, so the bands re-scale to
      what remains (DD-11) — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-25 passes
- [ ] [AI] **N-9 RED**: bind AC-18 in both the unit and e2e step files
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-18 "A harness filter switches the price chart to that harness's rate"_

    ```gherkin
    Scenario: A harness filter switches the price chart to that harness's rate
      Given a fixture model priced differently by two harnesses
      When the harness filter selects the more expensive harness
      Then that model's bars use that harness's rate
    ```

- [ ] [AI] **N-10 GREEN**: pass the active harness into `rateFor` so the price chart switches rate set
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-18 passes
- [ ] [AI] **N-11 RED**: bind AC-26 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-26 "An unrecognized filter value falls back to the unfiltered view" —
    same scenario as F-5 above, now bound at the UI layer._

    ```gherkin
    Scenario: An unrecognized filter value falls back to the unfiltered view
      Given the URL carries a harness parameter with an unknown value
      When the page renders
      Then every roster model is shown
      But no error is surfaced to the reader
    ```

- [ ] [AI] **N-12 GREEN**: confirm the sanitizer path surfaces no error to the reader
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-26 passes
- [ ] [AI] **N-13 RED**: bind AC-28 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-28 "A filter combination matching no model renders an explicit empty state"_

    ```gherkin
    Scenario: A filter combination matching no model renders an explicit empty state
      Given the URL carries a filter combination that matches no model
      When the page renders
      Then an explicit empty-state message is shown
      But neither chart renders an empty plot area
    ```

- [ ] [AI] **N-14 GREEN**: render a localized empty state and suppress both chart plot areas when the
      filtered set is empty — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-28 passes
- [ ] [AI] **N-15 RED**: bind AC-27 in `<ESTEPS>ai-benchmark.steps.ts`, applying both filters and
      reloading the resulting URL — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: fails
  - _Gherkin (binds) → AC-27 "A reloaded filtered URL reproduces the same view"_

    ```gherkin
    Scenario: A reloaded filtered URL reproduces the same view
      Given the reader has applied a harness filter and a class filter
      When the reader reloads the resulting URL
      Then the same filtered set of models is shown
    ```

- [ ] [AI] **N-16 GREEN**: confirm the URL round-trip holds through a real reload
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: AC-27 passes
- [ ] [AI] **N-17 RED**: extend `<SHELL>benchmark-filters.test.tsx` asserting both the mobile
      variant (a collapsed `<details>` disclosure with an active-filter count below `md`) and the
      `md`/`lg` variant (an inline wrapping bar at `md`, a single-row bar with the result count at
      `lg`) expose the same accessible control names — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because the filter bar has no responsive layout branch yet
- [ ] [AI] **N-18 GREEN**: implement the responsive filter strategy — a collapsed `<details>`
      disclosure with an active-filter count below `md`, an inline wrapping bar at `md`, a
      single-row bar with the result count at `lg` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts both variants expose the same accessible
      control names
- [ ] [AI] **N-19 REFACTOR**: collapse the two selectors onto one generic `<FilterSelect>` taking a
      label, an option list, and an `onChange`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Phase 8 Gate

> All checks below must pass before starting Phase 9. This is a **boundary** phase.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — every scenario AC-1 … AC-37
      except AC-3 and AC-38 now has a `@covers`-annotated step
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
- [ ] [AI] The page is still unlinked — acceptance: `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>`
      prints `0` for both files
- [ ] [AI] `npx nx affected -t typecheck lint` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-8-filters` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-8-filters/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: the page is functionally complete and still unlinked — every behaviour the plan
> promised works at a direct URL. Safe to stop. To resume: `npx nx run ayokoding-www:test:quick`.

---

## Phase 9: Manual Behavioural Verification and Static UI Quality Gate

> Non-boundary phase — commits to the Phase 9-10 branch and opens no PR of its own.
>
> Evidence obligations follow the
> [Evidence Capture Convention](../../../repo-governance/development/quality/evidence-capture.md):
> screenshots to `<EV>` named by phase, locale, and breakpoint; every supported locale exercised.

- [ ] [AI] Provision the Phase 9-10 unit's worktree from the latest `origin/main` — this is the
      unit's first phase, before its boundary at Phase 10:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-9-10-verify-reveal-retest origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-9-10-verify-reveal-retest
rev-parse --show-toplevel` prints the worktree path

### Manual UI verification (Playwright MCP) — all locales × all breakpoints

- [ ] [AI] **M-1**: confirm the supported locale set by reading
      `apps/ayokoding-www/src/features/i18n/core/config.ts` — acceptance: the locale list is recorded
      here in this checklist (expected `en`, `id`; if the file lists more, all are covered below)
- [ ] [AI] **M-2**: start the dev server: `npx nx dev ayokoding-www` — acceptance:
      `curl -s -o /dev/null -w '%{http_code}' http://localhost:3101/en/tools/ai-benchmark` prints `200`
- [ ] [AI] **M-3**: for **each** locale × **each** breakpoint (375 / 768 / 1280 px), navigate to the
      locale-prefixed URL via `browser_navigate` + `browser_resize`
      — acceptance: all six combinations render without layout overflow
- [ ] [AI] **M-4**: inspect the DOM via `browser_snapshot` at each combination — acceptance:
      `html[lang]` matches the locale and no raw translation key appears in the rendered text
- [ ] [AI] **M-5**: exercise the interactive flows via `browser_click` — apply a harness filter, apply
      a class filter, apply a combination matching nothing, then clear — acceptance: each transition
      updates the URL and both charts and the table narrow together
- [ ] [AI] **M-6**: check `browser_console_messages` at each combination — acceptance: **zero** errors
      per locale
- [ ] [AI] **M-7**: check `browser_network_requests` — acceptance: no request to any external
      benchmark or pricing host (the dataset is static; an outbound fetch would be a defect)
- [ ] [AI] **M-8**: capture one screenshot per locale per breakpoint via `browser_take_screenshot` to
      `<EV>phase-9-ai-benchmark-<locale>-<breakpoint>px.png`
      — acceptance: six files exist under `<EV>`
- [ ] [AI] **M-9**: capture two extra screenshots proving the dark theme renders the band tokens
      correctly, at `<EV>phase-9-ai-benchmark-<locale>-1280px-dark.png`
      — acceptance: two files exist under `<EV>`
- [ ] [AI] **M-10**: reference every captured screenshot in this checklist via
      `![description](./evidence/<filename>)` and note the console and network status per locale
      — acceptance: every file under `<EV>` matching `phase-9-*` is referenced at least once in
      `<PLAN>delivery.md`

### AC-38 — live-page contrast assertion

- [ ] [AI] **M-11 RED**: append AC-38 to `<SPECS>ai-benchmark.feature` and bind it in
      `<ESTEPS>ai-benchmark.steps.ts`, reading **computed styles** from the live page in each theme
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails
  - _Gherkin (binds) → AC-38 "Band colours meet contrast in both themes"_

    ```gherkin
    Scenario Outline: Band colours meet contrast in both themes
      Given the page is rendered in the "<theme>" theme
      When the computed styles of the band tokens are read from the live page
      Then every band token meets the WCAG AA contrast ratio against its background

      Examples:
        | theme |
        | light |
        | dark  |
    ```

- [ ] [AI] **M-12 GREEN**: adjust any band token that fails the live contrast check, re-recording
      `<EV>phase-1-band-contrast.md` — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: AC-38 passes for both themes
  - jsdom cannot resolve `oklch()` custom properties through a cascade, which is why this assertion
    lives in e2e and not in a unit test.

### Static UI quality gate

- [ ] [AI] **M-13**: run the
      [ui-quality-gate workflow](../../../repo-governance/workflows/ui/ui-quality-gate.md) at
      `mode: strict` with `scope: apps/ayokoding-www/src/features/ai-benchmark/` — acceptance:
      terminates with zero findings on two consecutive validations
- [ ] [AI] **M-14**: fix every CRITICAL, HIGH and MEDIUM finding the gate reports, re-running until it
      terminates clean — acceptance: the gate's final report lists zero findings at strict mode

### Phase 9 Gate

> All checks below must pass before starting Phase 10. **Non-boundary** — commit to the unit branch
> and open no PR.

- [ ] [AI] Six locale × breakpoint screenshots plus two dark-theme screenshots exist under `<EV>` and
      are referenced from this file
- [ ] [AI] Zero console errors recorded for every locale × breakpoint combination
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 with AC-38 passing in both themes
- [ ] [AI] The ui-quality-gate workflow terminated with zero findings at `strict`
- [ ] [AI] `npx nx run ayokoding-www:test:quick` exits 0
- [ ] [AI] Commit per the [Commit Guidelines](#commit-guidelines) to
      `ayokoding-www-tools-ai-benchmark/phase-9-10-verify-reveal-retest` — no push, no PR yet

> **Pause Safety**: the unlinked page is verified across every locale and breakpoint with committed
> evidence, and the static UI gate is clean. Nothing is public yet. Safe to stop. To resume:
> re-run `npx nx run ayokoding-www:test:quick`.

---

## Phase 10: Reveal and Rule-15 Three-Tester Retest

> **This phase removes the link gate** (see
> [tech-docs §Feature gating](./tech-docs.md#feature-gating)). The reveal runs **before** the retest
> so the three live-site testers evaluate the shipped navigation path rather than a direct-URL-only
> page.

### Reveal — link-gate removal

- [ ] [AI] **R-1 RED**: append AC-3 to `<SPECS>tools-index.feature` and bind it in both
      `<USTEPS>tools-index.steps.tsx` and `<ESTEPS>tools-index.steps.ts`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-3 "The AI benchmark entry shows a description distinct from its link text"_

    ```gherkin
    Scenario: The AI benchmark entry shows a description distinct from its link text
      Given I am on the tools index page
      When the AI benchmark entry renders
      Then the AI benchmark entry shows a description distinct from its link text
    ```

- [ ] [AI] **R-2 GREEN**: add the AI benchmark `<li>` to `<TOOLSIDX>` — a `<Link>` to
      `./tools/ai-benchmark` reading `t(locale, "toolsPageAiBenchLink")` plus a
      `data-testid="tool-desc-ai-benchmark"` paragraph reading `t(locale, "toolsPageAiBenchDesc")`,
      mirroring the existing calculator entry; add both keys to **both** locales in `<I18N>`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-3 passes
- [ ] [AI] **R-3**: add the footer Tools-column link to `<FOOTER>`, mirroring the existing
      `/${locale}/tools/cost-of-living-calculator` entry
      — acceptance: `grep -c "tools/ai-benchmark" <FOOTER>` prints `1`. Falsifiable both ways: with
      the link absent it prints `0`.
- [ ] [AI] **R-4**: confirm the gate is fully removed — acceptance:
      `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>` prints a non-zero count for **both** files,
      inverting the Phase 5–8 gate check exactly
- [ ] [AI] **R-5 REFACTOR**: confirm no other tool-listing surface was missed — acceptance:
      `grep -rn "cost-of-living-calculator" apps/ayokoding-www/src` lists no navigation surface that
      lacks a sibling `ai-benchmark` entry, excluding the calculator's own feature folder and its tests

### Rule-15 three-tester retest

- [ ] [AI] **RT-1**: run the three live-site testers — the
      [web-ux-test-fixing-planning workflow](../../../repo-governance/workflows/web/web-ux-test-fixing-planning.md)'s
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester` — against the running
      target across **all** supported locales, entering via site navigation rather than a direct URL
      — acceptance: EWT-###, UWT-###, DWT-### findings and any SG-### spec gaps are recorded
- [ ] [AI] **RT-2**: append each finding below as a new unchecked, source-attributed checkbox under
      **Rule-15 retest follow-ups** — acceptance: every reported finding has a corresponding
      checkbox carrying its id
- [ ] [AI] **RT-3**: append each SG-### spec gap into `<SPECS>ai-benchmark.feature` as a new scenario
      with its step implementation, or record a written triage rationale
      — acceptance: `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
- [ ] [AI] **RT-4**: fix **every** rule-15 EWT/UWT/DWT defect finding before archival. Deferral
      requires explicit user permission and is allowed only when the fix is genuinely impossible;
      SG-### spec-gap proposals and USS-### suggestions may be triaged or deferred with a written
      rationale — acceptance: every EWT/UWT/DWT checkbox below is ticked

#### Rule-15 retest follow-ups

<!-- Findings are appended here by step RT-2 during execution. Every EWT/UWT/DWT defect finding must
     be ticked before Plan Archival. -->

- [ ] [AI] _(placeholder — replaced by the actual findings at RT-2; if the retest genuinely reports
      no defect finding, replace this line with `No rule-15 defect findings — <one-line reason>`)_

### Phase 10 Gate

> All checks below must pass before starting Phase 11. This is a **boundary** phase for the Phase
> 9-10 unit.

- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [ ] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — every scenario AC-1 … AC-38
      has a `@covers`-annotated step
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
- [ ] [AI] The link gate is removed — `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>` prints a
      non-zero count for both files
- [ ] [AI] Every rule-15 EWT/UWT/DWT defect finding under **Rule-15 retest follow-ups** is ticked, or
      the section records the explicit no-findings line
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-9-10-verify-reveal-retest` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-9-10-verify-reveal-retest/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: the page is public, linked from both navigation surfaces, verified across every
> locale and breakpoint, and clean under all three live-site testers. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:quick`.

---

## Phase 11: Knowledge Capture

> _Triage every surviving `<PLAN>learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._
>
> Non-boundary phase — commits to the Phase 11-12 branch and opens no PR of its own.

- [ ] [AI] Provision the Phase 11-12 unit's worktree from the latest `origin/main` — this is the
      unit's first phase, before its boundary at Phase 12:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-11-12-capture-archival origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-11-12-capture-archival
rev-parse --show-toplevel` prints the worktree path
- [ ] [AI] Apply the litmus test to every `<PLAN>learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `<PLAN>learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content
      (Terraform, k3s, Proxmox, real hostnames or inventories) stays in `ose-infra` only and is NEVER
      cross-routed into `ose-public`/`ose-primer`; public-governance content may propagate via the
      existing parity loop — acceptance: no infra-private content appears in this repo's routed output
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix — non-code homes may land inline (small edit) or as a `plans/backlog/` follow-up (large);
      code homes (`apps/`, `libs/`, tests) are **ALWAYS** filed as a separate `plans/backlog/<slug>/`
      plan and **NEVER** landed inline
      — acceptance: every `<PLAN>learnings.md` entry records its terminal routing state
- [ ] [AI] Specifically consider routing the three method learnings this plan is most likely to
      surface, if they held during execution: the DD-5a normalization defect (coverage
      renormalization plus identity normalization systematically rewards narrow reporting), the
      DD-20a anchor-subset degeneracy, and the marker-first idempotence guard in `<GEN>`
      — acceptance: each is either routed with a named home or discarded with a reason
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `<PLAN>learnings.md`:
      `No generalizable learnings — <one-line reason>` — acceptance: `learnings.md` is never silently
      empty

### Phase 11 Gate

> All checks below must pass before Plan Archival. **Non-boundary** — commit to the unit branch and
> open no PR.

- [ ] [AI] Every `<PLAN>learnings.md` entry is in a terminal state (routed inline, filed as backlog,
      or discarded with reason), or the file records the explicit "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own commits or PR
- [ ] [AI] Commit per the [Commit Guidelines](#commit-guidelines) to
      `ayokoding-www-tools-ai-benchmark/phase-11-12-capture-archival` — no push, no PR yet

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly recorded as empty); no future
> process depends on querying it later. Safe to stop. To resume: re-read `<PLAN>learnings.md` and
> confirm every entry is terminal.

---

## Phase 12: Plan Archival

> This is a **boundary** phase for the Phase 11-12 unit and the last change-producing phase.

### Plan Archival

- [ ] [AI] Verify ALL delivery checklist items above are ticked
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state (routed inline, filed as a `plans/backlog/` plan, or discarded with reason) or
      the file records the explicit `No generalizable learnings — <reason>` escape; both the
      secret/sensitivity gate and the repo-relevance gate were applied to every surviving entry
- [ ] [AI] Verify ALL quality gates pass (local + CI) — acceptance:
      `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` exits 0 and the latest `main` CI
      run concludes `success`
- [ ] [AI] Verify ALL manual assertions pass with committed evidence in `<EV>` — six locale ×
      breakpoint screenshots plus two dark-theme screenshots, all referenced from this file
- [ ] [AI] Verify ALL supported locales were exercised in UI verification, not just the default
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires
      explicit user permission and is allowed only when the fix is genuinely impossible; SG-###
      proposals and USS-### suggestions may be triaged or deferred with written rationale
- [ ] [AI] Rule-16 API exploratory retest — **not applicable**: this plan adds no REST or GraphQL
      endpoint. Record the exemption here rather than leaving the check absent.
- [ ] [AI] Verify the feature gate is removed and no gate residue remains — acceptance:
      `grep -rn "link gate\|link-gate" apps/ayokoding-www/src` prints nothing
- [ ] [AI] Rename and move:
      `git mv plans/in-progress/ayokoding-www-tools-ai-benchmark/ plans/done/YYYY-MM-DD__ayokoding-www-tools-ai-benchmark/`
      using **today's** date as the completion date, not the creation date — acceptance: the folder
      exists under `plans/done/` and the `evidence/` and `assets/` subfolders moved with it
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with its completion date
- [ ] [AI] Update any other README that references this plan — acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0 and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      exits 0
- [ ] [AI] Commit the archival: `chore(plans): move ayokoding-www-tools-ai-benchmark to done`

### Phase 12 Gate

> All checks below must pass before the plan is considered complete.

- [ ] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      exits 0 — no link anywhere in the repo points at the old `plans/in-progress/` path
- [ ] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` exits 0
- [ ] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-11-12-capture-archival` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-11-12-capture-archival/`
- [ ] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)
- [ ] [AI] Verify every unit's worktree was removed at its own boundary gate — none deferred to plan
      end. Unit 9's own worktree (`ayokoding-www-tools-ai-benchmark-phase-11-12-capture-archival`) was
      already removed by the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      step above; this is the final confirmation across all nine units, not a fresh removal:
      `git worktree list | grep -c ayokoding-www-tools-ai-benchmark` prints `0`

> **Pause Safety**: the plan is archived under `plans/done/`, every link resolves, and `main` is
> green. The plan is complete. To resume verification: re-run the two rhino-cli validators above.
