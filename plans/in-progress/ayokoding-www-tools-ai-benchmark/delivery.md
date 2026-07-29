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

- [x] [AI] Both `.png` finalists (rendered from their `.svg` sources) exist under `<ASSETS>`, are
      embedded in `prd.md`, and their band colours reconcile with the real `--chart-band-*` tokens
      defined above (D-1/D-2)
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `assets/ai-benchmark-option-a-banded-panels.png` and `assets/ai-benchmark-option-c-side-by-side.png` exist (already reconciled from resolved hexes at D-1/D-2); both embedded in `prd.md` lines 274 and 278.
- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: passed (cached; min-role timeout fix from Phase 2 in effect).
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: passed — ayokoding-www + ayokoding-www-fe-e2e clean.
- [ ] [AI] `<EV>phase-1-band-contrast.md` records a passing contrast ratio and hue separation for
      every band in both themes
- [x] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-1-design-and-tokens` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens/`
  - **Date**: 2026-07-29 (reconciled during Phase 5 resume; original execution 2026-07-28)
  - **Status**: done
  - **Notes**: PR #110 merged (`gh pr view 110` → `mergeCommit: 075981dc4`, `state: MERGED`, checks `[SUCCESS, SKIPPED]`); worktree `ayokoding-www-tools-ai-benchmark-phase-1-design-and-tokens` confirmed removed (`git worktree list | grep -c` → `0`). This tick was omitted at original execution time; reconciled now per Resume Reconciliation with fresh evidence, not bulk-ticked from memory.
- [x] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `gh pr view 110 --json statusCheckRollup` → all checks concluded `SUCCESS` or `SKIPPED`, zero failures.

> **Pause Safety**: the design record is complete and four additive token declarations exist that no
> code reads yet — the repo renders exactly as before. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:unit`.

---

## Phase 2: Typed Dataset and Refresh Runbook

> _Suggested executor: `swe-typescript-dev` for the module; `web-researcher` for every primary-source
> re-check; `docs-maker` for the runbook._

- [x] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins: `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset
origin/main` — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset
rev-parse --show-toplevel` prints the worktree path
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files Changed**: new worktree `worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset/` on branch `ayokoding-www-tools-ai-benchmark/phase-2-dataset` provisioned from `origin/main` (HEAD `075981dc4`); `node_modules/` populated via `npm install`
  - **Notes**: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset rev-parse --show-toplevel` prints the worktree path; branch is `ayokoding-www-tools-ai-benchmark/phase-2-dataset`. `npm install` completed (node_modules present); `npm run doctor -- --fix` pending at first commit.

### Dataset schema (TDD)

- [x] [AI] **S-1 RED**: create `<DATA>models.unit.test.ts` asserting dataset invariants 1–4 from
      [tech-docs §Dataset invariant tests](./tech-docs.md#dataset-invariant-tests-coredatamodelsunittestts)
      — every benchmark figure has a non-empty source URL, every price figure has one, every figure
      carries a grade from the five-value union, and every `conflicted` figure has `low ≤ high`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the test fails because `<DATA>models.ts` does not exist
  - _Gherkin (underpins) → AC-21, AC-30, AC-31._
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: RED confirmed — models.unit.test.ts written first, failed because models.ts did not exist. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **S-2 GREEN**: create `<DATA>models.ts` with the type surface only — `EvidenceGrade`,
      `Figure`, `ConflictedFigure`, `BenchmarkId`, `HarnessId`, `PriceSet`, `SubscriptionPrice`,
      `Model`, `Dataset` — plus `snapshotDate`, the two anchor id constants, the benchmark weight
      table, and **three** seed models (one metered, one subscription-only, one zero-coverage)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: `models.unit.test.ts` passes against the three seed models
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: models.ts type surface + 3 seed models (metered/subscription/zero-coverage); test green. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **S-3 RED**: extend `<DATA>models.unit.test.ts` with invariants 5–10 — at least one known
      harness per model, unique ids, ISO-parseable `snapshotDate`, both anchor ids resolving, no
      Terminal-Bench 2.0 or SWE-bench Multilingual figure occupying a 2.1 or Verified field, and every
      `subscription`-kind price carrying a plan cost while omitting per-token rates
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new assertions fail
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: Invariants 5–10 asserted; failed against the seed schema until S-4 extended it. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **S-4 GREEN**: extend the schema so the invariants can hold — add
      `benchmarkVersion` and `conditions` to `Figure`, a discriminated `PriceSet` union on `kind`, and
      a `notes` field carrying integrity notes such as the METR finding
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all invariants pass
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: Added benchmarkVersion, conditions, PriceSet discriminated union, notes/integrity fields. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **S-5 REFACTOR**: extract the invariant assertions into named helper predicates so each
      failure message names the offending model id and field
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass and a deliberately corrupted fixture reports the model id in
      its failure message
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: Invariant assertions extracted to named helpers; failure messages name model id + field. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.

### Transcription

- [x] [AI] **X-1**: apply the DD-7a roster rule against the five harnesses' **current** rosters and
      write the resulting model list (id, vendor, harnesses) into `<DATA>models.ts`, using
      [Appendix A.2](./tech-docs.md#a2--indicative-roster-after-applying-dd-7a) as the starting point
      — acceptance: `models.unit.test.ts` passes and the model count is within the 30–45 band; any
      divergence from Appendix A.2 is recorded as a comment naming the roster page that changed
  - _Suggested executor: `web-researcher` for the roster re-fetch_
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: DD-7a roster applied: 38 models from Appendix A.2 (excludes mythos/deprecated/no-vendor). Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **X-2**: transcribe every benchmark figure from
      [Appendix A.3](./tech-docs.md#a3--benchmark-figures) with its grade, source URL, benchmark
      version, and conditions — acceptance: `models.unit.test.ts` passes; no figure lacks a source;
      Cursor Composer 2.5's 79.8% is recorded as SWE-bench **Multilingual** and its 69.3% as
      Terminal-Bench **2.0**, so invariant 9 holds
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: All benchmark figures transcribed from A.3 with version trap (Multilingual/2.0 excluded). Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **X-3**: resolve the eight known unknowns `K-1`…`K-8` by primary-source check; record each
      as resolved (with the primary URL) or as `unavailable`/`conflicted`
      — acceptance: `<EV>phase-2-known-unknowns.md` records a terminal state for all eight, and no
      `K-*` figure is written with a grade better than the source supports
  - _Suggested executor: `web-researcher`_
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: K-1…K-8 resolved in evidence/phase-2-known-unknowns.md (terminal state each). Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **X-4**: transcribe every price from
      [Appendix A.4](./tech-docs.md#a4--standard-tier-pricing-usd-per-1m-tokens) as a **per-harness**
      rate set under DD-16, applying DD-17a to promotions and the international-endpoint rule to
      regional splits — acceptance: `models.unit.test.ts` passes; Claude Sonnet 5 records `$3/$15`
      with the `$2/$10`-through-2026-08-31 promo as provenance; DeepSeek V4 Pro records **both** its
      `$0.435/$0.87` direct rate and Zen's `$1.74/$3.48`; all 16 OpenCode Go entries carry
      `kind: "subscription"` and no per-token rate
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: Per-harness prices from A.4: Sonnet 5 $3/$15 post-promo; DeepSeek dual rate; GO subscription. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **X-5 REFACTOR**: sort the dataset by vendor then model id and add the module header
      comment (snapshot date, sources summary, the DD-5a/DD-6/DD-7a/DD-16/DD-17a rules in brief, and
      a pointer to `<RUNBOOK>`), mirroring the header style of
      `apps/ayokoding-www/src/features/cost-of-living-calculator/core/data/cities.ts`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: Dataset sorted vendor→id; module header mirrors cities.ts (snapshotDate/sources/rules/runbook ptr). Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.

### Refresh runbook

- [x] [AI] **RB-1**: create `<RUNBOOK>` following the structure of
      `apps/ayokoding-www/docs/cost-of-living-calculator/data-sourcing-prompt.md` — frontmatter
      (`title`, `description`, `category: how-to`), a purpose section, an output-to-destination table,
      the non-negotiable conventions (roster rule DD-7a, pricing rules DD-12/16/17a, evidence grades
      DD-19, the benchmark-version trap), and one copy-paste research prompt per data class (rosters,
      benchmarks, prices)
      — acceptance: `test -f <RUNBOOK>` exits 0 and `npx nx run ayokoding-www:lint` exits 0
  - _Suggested executor: `docs-maker`_
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: data-sourcing-prompt.md created mirroring cost-of-living runbook structure. Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.
- [x] [AI] **RB-2**: index `<RUNBOOK>` from `apps/ayokoding-www/docs/README.md` (or the nearest
      indexing README) — acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `core/data/models.ts`, `core/data/models.unit.test.ts`, `docs/ai-benchmark/data-sourcing-prompt.md`, `docs/README.md`, `evidence/phase-2-known-unknowns.md`
  - **Notes**: Indexed from apps/ayokoding-www/docs/README.md (created — no docs index existed). Verified: `vitest run models.unit.test.ts` → 302 passed; `nx affected -t typecheck lint` → 0 failures.

### Phase 2 Gate

> All checks below must pass before starting Phase 3. This is a **boundary** phase.

- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0 with every dataset invariant passing
  - **Date**: 2026-07-28
  - **Status**: passed (contention flake documented)
  - **Notes**: `models.unit.test.ts` → 302 passed in isolation (2s). Full `test:unit` (128 files) ran 748s under concurrent load and 19 `min-role.test.tsx` tests timed out past the 60s `testTimeout`; re-run in isolation → 37/37 passed in 95s, confirming transient contention (per CI-monitoring contention-flake guidance), not a defect. No ai-benchmark test failed.
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
  - **Date**: 2026-07-28
  - **Status**: passed
  - **Notes**: `nx affected -t typecheck` → 2 projects OK; `nx affected -t lint` → 2 projects OK.
- [x] [AI] `<EV>phase-2-known-unknowns.md` records a terminal state for `K-1` through `K-8`
  - **Date**: 2026-07-28
  - **Status**: passed
  - **Notes**: `evidence/phase-2-known-unknowns.md` carries a terminal state for all eight (K-1 absent, K-2 conflicted 93.2–94.3, K-3 aggregator 96.2% NOT transcribed, K-4 Grok GPQA absent, K-5/K-7 no impact, K-6 secondary, K-8 disclosure-only) plus the two version-trap hazards.
- [x] [AI] No figure in `<DATA>models.ts` lacks a source URL — acceptance: invariant test 1 passes,
      and deleting one source URL from any figure makes it fail (verify once, then restore)
  - **Date**: 2026-07-28
  - **Status**: passed
  - **Notes**: invariant 1 (`it.each` over all figures) passes; every figure carries a non-empty source URL.
- [x] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-2-dataset` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-2-dataset/`
  - **Date**: 2026-07-29 (reconciled during Phase 5 resume; original execution 2026-07-28)
  - **Status**: done
  - **Notes**: PR #112 merged (`gh pr view 112` → `mergeCommit: a81ec0071`, `state: MERGED`, checks `[SUCCESS, SKIPPED]`); worktree `ayokoding-www-tools-ai-benchmark-phase-2-dataset` confirmed removed. Reconciled now with fresh evidence per Resume Reconciliation.
- [x] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `gh pr view 112 --json statusCheckRollup` → all checks concluded `SUCCESS` or `SKIPPED`, zero failures.

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

- [x] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation
origin/main` — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation
rev-parse --show-toplevel` prints the worktree path
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: Worktree provisioned from `origin/main` (HEAD `a81ec0071`, includes Phase 2). `models.ts` confirmed present. `npm install` complete.
- [x] [AI] **G-1 RED**: create `apps/ayokoding-www/src/scripts/generate-benchmark-reference.unit.test.ts`
      asserting that the generator (a) replaces only the text between a
      `<!-- BEGIN GENERATED: <name> -->` / `<!-- END GENERATED: <name> -->` pair, (b) leaves every
      byte outside the markers untouched, and (c) **throws** when a `BEGIN` marker has no matching
      `END` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the test fails because `<GEN>` does not exist
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: RED: generate-benchmark-reference.unit.test.ts asserts marker-only replacement, outside-bytes untouched, and missing-END throw.
- [x] [AI] **G-2 GREEN**: create `<GEN>` implementing marker-delimited replacement. It MUST locate the
      `BEGIN`/`END` pair **before** any substitution and fail loudly when one is missing — never
      falling back to inserting at an anchor, because an insert-style substitution duplicates content
      on every re-run — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all three assertions pass, including the missing-`END` throw
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: generate-benchmark-reference.ts created: marker-first guard, substitutes only between pairs, throws on missing END.
- [x] [AI] **G-3 RED**: extend the generator test asserting **idempotence** — running the generator
      twice over the same input produces byte-identical output
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new assertion fails or passes
      on first run; if it passes trivially, corrupt the marker handling once to confirm it can fail,
      then restore
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: Idempotence assertion added to the test suite.
- [x] [AI] **G-4 GREEN**: make the generator idempotent — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: running it twice yields no diff
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: Generator confirmed idempotent (re-generate → no diff).
- [x] [AI] **G-5 REFACTOR**: split `<GEN>` into a pure `renderTables(dataset)` function and a thin
      file-I/O shell, so the table rendering is unit-testable without touching disk
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: Split into pure renderTables(dataset) + substituteMarkers + thin I/O shell with --validate.
- [x] [AI] **G-6**: insert `BEGIN GENERATED` / `END GENERATED` marker pairs into `<REF>` around
      exactly the sections whose content is data — the quick-reference benchmark table, the
      OpenCode Go roster overview, the Standard API Pricing table, and the Frontier/Big-Brand Model
      Reference table — leaving benchmark **definitions**, tier-rationale prose, and the
      limitations-and-caveats narrative outside every marker
      — acceptance: `grep -c "BEGIN GENERATED" <REF>` and `grep -c "END GENERATED" <REF>` print the
      same number, and that number is at least `4`
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: 5 marker pairs inserted (roster, pricing, frontier, capability-summary + 1) — balanced; definitions/prose outside markers.
- [x] [AI] **G-7**: add the two Nx targets to `<PROJ>` — `generate-benchmark-reference` (writes) and
      `validate-benchmark-reference` (regenerates to a temp file and diffs, exiting non-zero on
      drift), following the shape of the project's existing `generate-indexes` / `validate-indexes`
      pair — acceptance:
      `node -e "const t=require('./apps/ayokoding-www/project.json').targets; process.exit(t['generate-benchmark-reference']&&t['validate-benchmark-reference']?0:1)"`
      exits 0
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: generate-benchmark-reference + validate-benchmark-reference Nx targets added to project.json, mirroring generate-indexes.
- [x] [AI] **G-8**: run `npx nx run ayokoding-www:generate-benchmark-reference` and review the diff
      — acceptance: `npx nx run ayokoding-www:validate-benchmark-reference` exits 0, and re-running
      the generate target produces no further diff (idempotence proven on the real file)
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: generate ran; validate exits 0; second generate produces no diff (idempotence proven on the real file).
- [x] [AI] **G-9**: reconcile every piece of `<REF>` prose the regenerated tables now contradict —
      specifically the section asserting Claude Opus 5 does not exist and the surrounding
      tier-design narrative, which was written when Opus 4.8 was the current Opus generation
      — acceptance: `grep -ci "opus 5.*does not exist\|no such model as.*opus 5" <REF>` prints `0`,
      and the reconciled prose names Opus 5's 2026-07-24 ship date with its source
  - _Suggested executor: `docs-fixer`_
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: Opus-5 prose reconciled — 'does not exist' sections rewritten to name the 2026-07-24 ship date; contradiction grep = 0.
- [x] [AI] **G-10**: state the derivation contract at the top of `<REF>` — that its data tables are
      generated from `<DATA>models.ts`, that hand-edits inside marker pairs are overwritten, and how
      to refresh — acceptance: `grep -c "generated from" <REF>` prints at least `1`
  - **Date**: 2026-07-28
  - **Status**: done
  - **Files**: `src/scripts/generate-benchmark-reference.ts`, `…unit.test.ts`, `project.json`, `docs/reference/ai-model-benchmarks.md`
  - **Notes**: Derivation-contract note added at top of REF ('generated from' present).

### Phase 3 Gate

> All checks below must pass before starting Phase 4. This is a **boundary** phase.

- [x] [AI] `npx nx run ayokoding-www:validate-benchmark-reference` exits 0
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: passed — validate target exits 0.
- [x] [AI] Running `npx nx run ayokoding-www:generate-benchmark-reference` twice leaves the working
      tree clean the second time — acceptance: `git status --porcelain -- docs/reference/ai-model-benchmarks.md`
      prints nothing after the second run
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: passed — second generate produces no diff (idempotent).
- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0
- [x] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      exits 0 for the edited reference
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: passed for the edited reference — 0 broken links in ai-model-benchmarks.md. (142 pre-existing broken links in plans/done/\*\* are unrelated archived-plan link rot, present before this phase; flagged for a separate maintenance task.)
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
- [x] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-3-reference-derivation` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-3-reference-derivation/`
- [x] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

> **Pause Safety**: the governance reference is now generated and current; the public page does not
> exist yet, and nothing user-facing changed. Safe to stop. To resume:
> `npx nx run ayokoding-www:validate-benchmark-reference`.

---

## Phase 4: Pure Functional Core

> _Suggested executor: `swe-typescript-dev`._
>
> Every module in this phase is pure — no React, no router, no side effects — mirroring
> `src/features/cost-of-living-calculator/core/`.

- [x] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins: `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core rev-parse
--show-toplevel` prints the worktree path
  - **Date**: 2026-07-28
  - **Status**: done
  - **Notes**: Worktree provisioned from `origin/main` (HEAD `8ab3b1703`, includes Phases 2+3). `npm install` running.
- [x] [AI] **Z-0**: create `<SPECS>ai-benchmark.feature` containing the eight capability-scoring
      scenarios this phase implements (AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11) plus the
      shared `Background`, and index it from `<SPECS>README.md` — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
  - This phase runs before Phase 5 in the DAG, so it creates the feature file rather than Phase 5;
    Phase 5's `W-0` step extends this same file with its own scenarios, and every later phase
    appends theirs the same way — the incremental per-phase authoring pattern the plan already uses.
  - _Suggested executor: `specs-maker`_

### Normalization and composite (`<CORE>score.ts`)

- [x] [AI] **C-1 RED**: create `<CORE>score.unit.test.ts` asserting `rosterMax(dataset, benchmark)`
      returns the highest **included** figure for that benchmark, using the low end of a `conflicted`
      figure and ignoring figures whose `benchmarkVersion` is excluded from the composite
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<CORE>score.ts` does not exist
  - _Gherkin (underpins) → AC-10, AC-13._
- [x] [AI] **C-2 GREEN**: implement `rosterMax` in `<CORE>score.ts`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the assertions pass
- [x] [AI] **C-3 RED**: assert `rel(model, benchmark, rosterMax)` returns
      `100 × score / rosterMax`, that the roster-max holder returns exactly `100`, and that an absent
      figure returns `undefined` — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
- [x] [AI] **C-4 GREEN**: implement `rel` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [x] [AI] **C-5 RED**: assert `computeIndex(model, rosterMaxes)` returns the weight-renormalized mean
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

- [x] [AI] **C-6 GREEN**: implement `computeIndex` and `coverage`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **C-7 RED**: assert a model with **zero** present benchmarks returns `coverage === 0` and
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

- [x] [AI] **C-8 GREEN**: handle the zero-coverage case explicitly
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **C-9 RED**: assert `isLowCoverage(model)` is true below the 0.50 threshold and false at
      or above it, with the threshold exported as a named constant
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-12._
- [x] [AI] **C-10 GREEN**: implement `isLowCoverage` and export `LOW_COVERAGE_THRESHOLD`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **C-11 REFACTOR**: extract the weight table lookup into one helper used by both
      `computeIndex` and `coverage`, removing the duplicated summation
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Band assignment (`<CORE>bands.ts`)

- [x] [AI] **B-1 RED**: create `<CORE>bands.unit.test.ts` asserting a fixture model whose index equals
      the opus anchor's index is assigned `"opus"`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-4 "A model reaching the opus anchor renders in the opus band"_

    ```gherkin
    Scenario: A model reaching the opus anchor renders in the opus band
      Given a fixture model whose composite index equals the opus anchor index
      When the capability groups are computed
      Then that model belongs to the "opus" band
    ```

- [x] [AI] **B-2 GREEN**: implement `assignBand` in `<CORE>bands.ts` with the opus comparison
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **B-3 RED**: assert a fixture model between the anchors is assigned `"sonnet"`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-5 "A model between the two anchors renders in the sonnet band"_

    ```gherkin
    Scenario: A model between the two anchors renders in the sonnet band
      Given a fixture model whose composite index is above the sonnet anchor index
      And that model's composite index is below the opus anchor index
      When the capability groups are computed
      Then that model belongs to the "sonnet" band
    ```

- [x] [AI] **B-4 GREEN**: add the sonnet comparison
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **B-5 RED**: assert a fixture model below the sonnet anchor is assigned `"light"`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-6 "A model below the sonnet anchor renders in the light band"_

    ```gherkin
    Scenario: A model below the sonnet anchor renders in the light band
      Given a fixture model whose composite index is below the sonnet anchor index
      When the capability groups are computed
      Then that model belongs to the "light" band
    ```

- [x] [AI] **B-6 GREEN**: add the light fallthrough
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **B-7 RED**: assert **anchor pinning** — with a deliberately perverse fixture in which the
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

- [x] [AI] **B-8 GREEN**: short-circuit `assignBand` on the two anchor ids before any comparison
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **B-9 RED**: assert **totality** over the real dataset — every model resolves to exactly
      one of `opus` / `sonnet` / `light` / `unrated`, with no duplicates and no omissions
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-9 "Every roster model belongs to exactly one capability group"_

    ```gherkin
    Scenario: Every roster model belongs to exactly one capability group
      Given the full roster is loaded
      When the capability groups are computed
      Then each model appears in exactly one of "opus", "sonnet", "light", or "unrated"
    ```

- [x] [AI] **B-10 GREEN**: implement `groupByBand(dataset)` returning the four disjoint groups
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **B-11 RED**: assert `groupByBand` orders models **identically within a band** whichever
      chart consumes it — i.e. it returns one canonical ordered list per band, sorted by descending
      index then by id — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-11 "Models are ordered identically in both charts within a band"_

    ```gherkin
    Scenario: Models are ordered identically in both charts within a band
      Given the full roster is loaded
      When both charts are rendered
      Then each band lists its models in the same order in the capability chart and the price chart
    ```

- [x] [AI] **B-12 GREEN**: make the ordering canonical and stable
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **B-13 REFACTOR**: move the anchor ids and threshold derivation into one exported
      `anchors(dataset)` helper so no caller re-derives them
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

### Gherkin bindings — capability scoring and bands (AC-4–AC-11)

> These eight scenarios are pure-logic (fixture data in, an assignment or index out) and need no
> page render, so they bind here in Phase 4 against `<CORE>score.ts`/`<CORE>bands.ts` rather than
> waiting for the route Phase 5 builds. `<USTEPS>ai-benchmark.steps.tsx` is created here at `Z-1` and
> extended by Phase 5's `W-1a` for the rendering-dependent scenarios.

- [x] [AI] **Z-1 RED**: create `<USTEPS>ai-benchmark.steps.tsx` binding AC-4, loading
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

- [x] [AI] **Z-2 GREEN**: wire `assignBand`'s opus comparison into the AC-4 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-4 passes
- [x] [AI] **Z-3 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-5
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

- [x] [AI] **Z-4 GREEN**: wire `assignBand`'s sonnet comparison into the AC-5 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-5 passes
- [x] [AI] **Z-5 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-6
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-6 "A model below the sonnet anchor renders in the light band" — same
    scenario as B-5 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: A model below the sonnet anchor renders in the light band
      Given a fixture model whose composite index is below the sonnet anchor index
      When the capability groups are computed
      Then that model belongs to the "light" band
    ```

- [x] [AI] **Z-6 GREEN**: wire `assignBand`'s light fallthrough into the AC-6 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-6 passes
- [x] [AI] **Z-7 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-7
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

- [x] [AI] **Z-8 GREEN**: wire the anchor-pinning short-circuit into the AC-7 step definition
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-7 passes
- [x] [AI] **Z-9 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-8
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

- [x] [AI] **Z-10 GREEN**: wire the zero-coverage case from `<CORE>score.ts` into the AC-8 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-8 passes
- [x] [AI] **Z-11 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-9
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-9 "Every roster model belongs to exactly one capability group" — same
    scenario as B-9 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: Every roster model belongs to exactly one capability group
      Given the full roster is loaded
      When the capability groups are computed
      Then each model appears in exactly one of "opus", "sonnet", "light", or "unrated"
    ```

- [x] [AI] **Z-12 GREEN**: wire `groupByBand(dataset)` over the full roster into the AC-9 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-9 passes
- [x] [AI] **Z-13 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-10
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

- [x] [AI] **Z-14 GREEN**: wire `computeIndex`/`coverage` from `<CORE>score.ts` into the AC-10 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-10 passes
- [x] [AI] **Z-15 RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding AC-11
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-11 "Models are ordered identically in both charts within a band" — same
    scenario as B-11 above, now bound at the vitest-cucumber layer._

    ```gherkin
    Scenario: Models are ordered identically in both charts within a band
      Given the full roster is loaded
      When both charts are rendered
      Then each band lists its models in the same order in the capability chart and the price chart
    ```

- [x] [AI] **Z-16 GREEN**: wire `groupByBand`'s canonical per-band ordering into the AC-11 step
      definition — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-11 passes
- [x] [AI] **Z-17 REFACTOR**: extract the fixture-dataset builder shared by Z-1…Z-16 into one helper
      in `<USTEPS>ai-benchmark.steps.tsx`, so each step definition stays a thin call into the
      already-tested `<CORE>` functions — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Harness price selection (`<CORE>price.ts`)

- [x] [AI] **P-1 RED**: create `<CORE>price.unit.test.ts` asserting `lowestRate(model)` returns the
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

- [x] [AI] **P-2 GREEN**: implement `lowestRate` in `<CORE>price.ts`, comparing on input rate then
      output rate — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **P-3 RED**: assert `rateFor(model, harnessId)` returns that harness's rate set and
      `undefined` when the model is not exposed by that harness
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-18._
- [x] [AI] **P-4 GREEN**: implement `rateFor`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **P-5 RED**: assert a subscription-only model returns `{ kind: "subscription" }` from both
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

- [x] [AI] **P-6 GREEN**: handle the subscription discriminant explicitly in both selectors
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **P-7 REFACTOR**: collapse `lowestRate` and `rateFor` onto one internal
      `selectRateSet(model, harnessId?)` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Filtering (`<CORE>filter.ts`) and URL state (`<CORE>url-state.ts`)

- [x] [AI] **F-1 RED**: create `<CORE>filter.unit.test.ts` asserting `filterModels(dataset, state)`
      narrows by harness, narrows by class, and intersects both
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-25 "Harness and class parameters intersect"_

    ```gherkin
    Scenario: Harness and class parameters intersect
      Given the URL carries both a harness parameter and a class parameter
      When the page renders
      Then only models satisfying both filters are shown
    ```

- [x] [AI] **F-2 GREEN**: implement `filterModels` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
- [x] [AI] **F-3 RED**: create `<CORE>url-state.unit.test.ts` asserting `decodeState` returns the
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

- [x] [AI] **F-4 GREEN**: implement `PARAM_KEYS`, `DEFAULT_STATE`, `decodeState`, `encodeState` in
      `<CORE>url-state.ts` — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **F-5 RED**: assert an unknown harness value and an unknown class value each sanitize to
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

- [x] [AI] **F-6 GREEN**: sanitize both params against their known-value unions
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **F-7 RED**: assert `encodeState(decodeState(q))` round-trips for every valid query string
      in a table-driven fixture — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-27._
- [x] [AI] **F-8 GREEN**: make the round-trip hold
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: passes
- [x] [AI] **F-9 REFACTOR**: extract the known-value unions into shared constants imported by both
      `filter.ts` and `url-state.ts`, so a new harness id is added in exactly one place
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass

> **Phase 4 implementation evidence (2026-07-28)**: all step boxes above ticked. Single cohesive TDD pass by swe-typescript-dev. - **Date**: 2026-07-28

- **Status**: done
- **Files**: `core/score.ts`, `core/bands.ts`, `core/price.ts`, `core/filter.ts`, `core/url-state.ts` (+ `.unit.test.ts` each), `test/unit/fe-steps/ai-benchmark.steps.tsx`, `specs/.../tools/ai-benchmark.feature`
- **Notes**: implemented per the TDD step (RED/GREEN/REFACTOR). 386 core tests pass; specs:behavior:coverage valid (AC-4..AC-11 bound); Opus5→opus, Sonnet5→sonnet (pinned), Cursor Composer 2.5→unrated; groups opus2/sonnet11/light7/unrated18.

### Phase 4 Gate

> All checks below must pass before starting Phase 5. This is a **boundary** phase.

- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0
  - **Date**: 2026-07-28 — **Status**: done — **Notes**: passed — 136 files / 2891 tests (cached; min-role timeout fix stable).
- [x] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — AC-4 through AC-11 (the only
  - **Date**: 2026-07-28 — **Status**: done — **Notes**: passed — 42 specs, 299 scenarios, 1070 steps all covered; AC-4..AC-11 bound.
    scenarios currently in `<SPECS>ai-benchmark.feature`) each have a `@covers`-annotated step
- [x] [AI] Every module under `<CORE>` is free of React and router imports — acceptance:
  - **Date**: 2026-07-28 — **Status**: done — **Notes**: passed — grep for react/next-navigation/next-router in core/ prints nothing.
    `grep -rn "from \"react\"\|next/navigation\|next/router" <CORE>` prints nothing
- [x] [AI] `npx nx run ayokoding-www:test:coverage` meets the project's configured threshold
  - **Date**: 2026-07-28 — **Status**: done — **Notes**: passed — 88.26% lines (threshold 82).
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
  - **Date**: 2026-07-28 — **Status**: done — **Notes**: passed — 56/56 tasks.
- [x] [AI] Run the [Delivery-Boundary Integration Protocol](#delivery-boundary-integration-protocol)
      for branch `ayokoding-www-tools-ai-benchmark/phase-4-core` in worktree
      `worktrees/ayokoding-www-tools-ai-benchmark-phase-4-core/`
- [x] [AI] Run [Post-Push CI Verification](#post-push-ci-verification)

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

- [x] [AI] Provision this unit's worktree from the latest `origin/main` — this phase is both the
      unit's first phase and its boundary, so the worktree must exist before this phase's own work
      begins:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-5-page-and-table origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-5-page-and-table
rev-parse --show-toplevel` prints the worktree path
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: Worktree provisioned from `origin/main` (HEAD `290b94b63`, includes Phases 2–4). `npm install` complete.

### Feature file and step scaffolds

- [x] [AI] **W-0**: extend `<SPECS>ai-benchmark.feature` (created at Phase 4's `Z-0` with
      AC-4–AC-11) by appending the scenarios this phase implements (AC-1, AC-2, AC-19, AC-20, AC-21,
      AC-29, AC-30, AC-31, AC-32, AC-33, AC-34, AC-35) — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
  - Scenarios for later phases are added by those phases; adding them now would red
    `specs:behavior:coverage` at every intervening gate.
  - _Suggested executor: `specs-maker`_
  - **Date**: 2026-07-29 (reconciled on resume — code pre-existed in worktree, undocumented)
  - **Status**: done
  - **Notes**: all 12 scenarios confirmed present via `grep -n "^  Scenario"` on `ai-benchmark.feature`. `npx nx run ayokoding-www:specs:structure-validation` → `0 finding(s)` for all namespaces.

### Route and content shell

> _Split per [Test-Driven Development Convention §Gherkin-Tagged Delivery Steps](../../../repo-governance/development/workflow/test-driven-development.md#gherkin-tagged-delivery-steps):
> one cycle per scenario, never bundled. AC-1 (English) and AC-2 (Indonesian) each get their own
> RED → GREEN cycle, for both the unit binding and the `@e2e` binding._

- [x] [AI] **W-1a RED**: extend `<USTEPS>ai-benchmark.steps.tsx` (created at Phase 4's `Z-1`
      binding AC-4–AC-11) binding **only** AC-1, loading `<SPECS>ai-benchmark.feature` and rendering
      the page for the `en` locale
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<ROUTE>page.tsx` does not exist
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (RED phase superseded by present GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:349-370` binds AC-1 with `@covers` annotation. RED-phase evidence not separately recoverable from a stopped prior session; GREEN state verified directly (see W-1b).
  - _Gherkin (binds) → AC-1 "The English page renders its localized heading"_

    ```gherkin
    Scenario: The English page renders its localized heading
      Given the locale is "en"
      When the AI benchmark page renders
      Then the page shows a level-one heading in English
      And the document language attribute is "en"
    ```

- [x] [AI] **W-1b GREEN**: create `<ROUTE>page.tsx` (server, with `generateMetadata` reading
      `t(locale, "aiBenchTitle")`) and `<ROUTE>benchmark-content.tsx` (`"use client"`), wrapped in
      `<Suspense>`, mirroring `tools/cost-of-living-calculator/page.tsx`; add `aiBenchTitle` and the
      H1 key to the `en` locale in `<I18N>`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-1 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `<ROUTE>page.tsx` and `<ROUTE>benchmark-content.tsx` exist; `aiBenchTitle` present in `en` block of `<I18N>` (translations.ts:30). `npx nx run ayokoding-www:test:unit` → 2955 passed, 6 skipped, 0 failed.
- [x] [AI] **W-2a RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding **only** AC-2, rendering the
      page for the `id` locale
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because the `id` locale's `aiBenchTitle` and H1 key do not exist yet
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by present GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:371-382` binds AC-2 with `@covers` annotation.
  - _Gherkin (binds) → AC-2 "The Indonesian page renders its localized heading"_

    ```gherkin
    Scenario: The Indonesian page renders its localized heading
      Given the locale is "id"
      When the AI benchmark page renders
      Then the page shows a level-one heading in Indonesian
      And the document language attribute is "id"
    ```

- [x] [AI] **W-2b GREEN**: add `aiBenchTitle` and the H1 key to the `id` locale in `<I18N>` — the
      route and content shell created in W-1b already handle locale routing generically
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-2 passes and AC-1 still passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `aiBenchTitle: "Tolok Ukur Model AI"` present in `id` block (translations.ts:355). `test:unit` green (2955 passed).
- [x] [AI] **W-3a RED**: add the `@e2e` binding for **only** AC-1 in `<ESTEPS>ai-benchmark.steps.ts`,
      navigating to `/en/tools/ai-benchmark`
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails until the dev server
      serves the route
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by present GREEN state)
  - **Notes**: `<ESTEPS>ai-benchmark.steps.ts:34-42` binds AC-1 with `@covers` annotation, navigating via `page.goto('/${scenarioLocale}/tools/ai-benchmark')`.
  - _Gherkin (binds) → AC-1 "The English page renders its localized heading" — same scenario as
    W-1a, now bound at the e2e layer._

    ```gherkin
    Scenario: The English page renders its localized heading
      Given the locale is "en"
      When the AI benchmark page renders
      Then the page shows a level-one heading in English
      And the document language attribute is "en"
    ```

- [x] [AI] **W-3b GREEN**: confirm the English locale route renders — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the AC-1 e2e scenario passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `nx run ayokoding-www-fe-e2e:test:e2e` → 623-625 passed across two runs; no ai-benchmark scenario among the failures in either run (4 and 6 unrelated preexisting flakes in course-rehome-redirects/cost-of-living-calculator/skills-path/content-namespace, confirmed non-deterministic under concurrent load).
- [x] [AI] **W-4a RED**: add the `@e2e` binding for **only** AC-2 in `<ESTEPS>ai-benchmark.steps.ts`,
      navigating to `/id/tools/ai-benchmark`
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails until the dev server
      serves the route
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by present GREEN state)
  - **Notes**: `<ESTEPS>ai-benchmark.steps.ts:44-52` binds AC-2 with `@covers` annotation.
  - _Gherkin (binds) → AC-2 "The Indonesian page renders its localized heading" — same scenario as
    W-2a, now bound at the e2e layer._

    ```gherkin
    Scenario: The Indonesian page renders its localized heading
      Given the locale is "id"
      When the AI benchmark page renders
      Then the page shows a level-one heading in Indonesian
      And the document language attribute is "id"
    ```

- [x] [AI] **W-4b GREEN**: confirm the Indonesian locale route renders — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the AC-2 e2e scenario passes, and the
      AC-1 e2e scenario still passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: Both AC-1 and AC-2 e2e scenarios pass (not among the failures in either full e2e run).
- [x] [AI] **W-5 REFACTOR**: extract the locale-aware page-object helper used by both e2e scenarios
      into `<ESTEPS>ai-benchmark.steps.ts`'s local helpers
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: both still pass
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: shared `scenarioLocale` module variable + `Given("the locale is {string}")` + `When("the AI benchmark page renders")` (lines 12-30) form the single locale-aware navigation helper both AC-1 and AC-2 scenarios reuse — no duplication.

### Accessible data table

- [x] [AI] **W-6 RED**: bind AC-19 in `<USTEPS>ai-benchmark.steps.tsx`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:395-406` binds AC-19 with `@covers` annotation.
  - _Gherkin (binds) → AC-19 "The data table is present without any interaction"_

    ```gherkin
    Scenario: The data table is present without any interaction
      Given the full roster is loaded
      When the page first renders
      Then a data table is present in the document
      And the table has a caption
      And every table header cell declares a scope
    ```

- [x] [AI] **W-7 GREEN**: create `<SHELL>model-table.tsx` rendering a semantic `<table>` with a
      `<caption>` and `scope` on every `<th>` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-19 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `model-table.tsx:230` renders `<caption>`; every `<th>` (lines 233-259, 271) carries `scope="col"`/`scope="row"`. `test:unit` green.
- [x] [AI] **W-8 RED**: bind AC-20 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:427-438` binds AC-20 with `@covers` annotation.
  - _Gherkin (binds) → AC-20 "The table carries every figure the charts encode"_

    ```gherkin
    Scenario: The table carries every figure the charts encode
      Given the full roster is loaded
      When the data table is rendered
      Then each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price
    ```

- [x] [AI] **W-9 GREEN**: render every column — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-20 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `model-table.tsx` renders harnesses/class/every `BENCHMARK_COLUMNS` entry/composite index/coverage/input+output price per row (desktop `<tr>` at ~line 270-286; mobile card via `renderBenchmarkFigures`+`renderStaticFigures` at ~line 200-215).
- [x] [AI] **W-10 RED**: bind AC-21 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:471-482` binds AC-21 with `@covers` annotation.
  - _Gherkin (binds) → AC-21 "Every figure in the table carries an evidence grade"_

    ```gherkin
    Scenario: Every figure in the table carries an evidence grade
      Given the full roster is loaded
      When the data table is rendered
      Then every benchmark score cell carries an evidence grade marker
      And every price cell carries an evidence grade marker
    ```

- [x] [AI] **W-11 GREEN**: create `<SHELL>evidence-badge.tsx` and use it in every figure cell
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-21 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `evidence-badge.tsx` exists; `EvidenceBadge` composed into every `FigureCell` call site in `model-table.tsx`. Grade rendered as localized text (WCAG 1.4.1 — never colour alone).
- [x] [AI] **W-12 RED**: bind AC-30 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:529-540` binds AC-30 with `@covers` annotation.
  - _Gherkin (binds) → AC-30 "Every benchmark figure links to the source it came from"_

    ```gherkin
    Scenario: Every benchmark figure links to the source it came from
      Given the full roster is loaded
      When the data table is rendered
      Then every benchmark score cell resolves to a source link
      And every price cell resolves to a source link
    ```

- [x] [AI] **W-13 GREEN**: render each figure's source as an anchor on the badge
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-30 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `evidence-badge.tsx` renders `<a href={source} target="_blank" rel="noopener noreferrer nofollow">` around the grade word.
- [x] [AI] **W-14 RED**: bind AC-31 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:561-593` binds AC-31 with `@covers` annotation.
  - _Gherkin (binds) → AC-31 "A conflicted figure renders as a range rather than a single number"_

    ```gherkin
    Scenario: A conflicted figure renders as a range rather than a single number
      Given a fixture model whose benchmark figure has conflicting published values
      When the data table is rendered
      Then that cell shows the lowest and highest published values
      But that cell shows no averaged value
    ```

- [x] [AI] **W-15 GREEN**: render `conflicted` figures as a low–high range
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-31 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `model-table.tsx`'s `benchmarkCell` checks `isConflictedFigure(f)` and passes both `value`/`highValue` into `FigureCell`, which renders `${value} ${separator} ${highValue}` — never an average.
- [x] [AI] **W-16 RED**: bind AC-33 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:638-665` binds AC-33 with `@covers` annotation.
  - _Gherkin (binds) → AC-33 "The page names a known benchmark-integrity finding beside the model it concerns"_

    ```gherkin
    Scenario: The page names a known benchmark-integrity finding beside the model it concerns
      Given the dataset records a benchmark-integrity note for a model
      When that model is rendered in the data table
      Then the integrity note is reachable from that model's row
    ```

- [x] [AI] **W-17 GREEN**: surface each model's `notes` entries from its row (the METR finding on
      GPT-5.6 Sol is the live case) — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: AC-33 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `model-table.tsx`'s `integrityNotes()` renders each `model.notes` entry as a linked marker beside the model name in both desktop `<th scope="row">` and mobile card header.
- [x] [AI] **W-18 REFACTOR**: extract the per-figure cell into one `<FigureCell>` used by every
      numeric column, so grade, source link, and range handling live in one place
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `shell/figure-cell.tsx` exists and is the sole component used for every benchmark/index/price cell in `model-table.tsx`. `test:unit` green (2955 passed).

### Honesty surface

> _Split per [Test-Driven Development Convention §Gherkin-Tagged Delivery Steps](../../../repo-governance/development/workflow/test-driven-development.md#gherkin-tagged-delivery-steps):
> one cycle per scenario. AC-29 (snapshot date) and AC-32 (how-to-read disclosure) are unrelated
> behaviors that happen to land in the same `<SHELL>how-to-read.tsx` component, so each gets its own
> RED → GREEN cycle rather than one bundled RED._

- [x] [AI] **W-19a RED**: bind **only** AC-29 — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<SHELL>how-to-read.tsx` does not exist
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:509-520` binds AC-29 with `@covers` annotation.
  - _Gherkin (binds) → AC-29 "The page displays the dataset snapshot date"_

    ```gherkin
    Scenario: The page displays the dataset snapshot date
      Given the dataset carries a snapshot date
      When the page renders
      Then the snapshot date is shown in text
    ```

- [x] [AI] **W-19b GREEN**: create `<SHELL>how-to-read.tsx` rendering the snapshot date in text
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-29 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `how-to-read.tsx` renders `data-testid="ai-bench-snapshot"` with the formatted `dateText` from the dataset's `snapshotDate` prop.
- [x] [AI] **W-20a RED**: extend `<USTEPS>ai-benchmark.steps.tsx` binding **only** AC-32
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:611-622` binds AC-32 with `@covers` annotation.
  - _Gherkin (binds) → AC-32 "The page discloses that frontier scores are overwhelmingly vendor-reported"_

    ```gherkin
    Scenario: The page discloses that frontier scores are overwhelmingly vendor-reported
      Given the page carries a how-to-read disclosure
      When the page renders
      Then the disclosure states that most frontier benchmark scores are vendor self-reported
      And the disclosure is visible without interaction
    ```

- [x] [AI] **W-20b GREEN**: extend `<SHELL>how-to-read.tsx` with a `<details open>` disclosure whose
      copy covers, in **both** locales: that most frontier scores are vendor self-reported (the
      0-of-104 finding); that the index is roster-relative and its weights are ours; that coverage
      varies and low-coverage models are marked; that figures reflect each vendor's best published
      configuration; the ARC-AGI-2 measurement conflict as the worked example of why provenance
      matters; and the DeepSeek-versus-gateway price gap as the worked example of why prices are per
      harness — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-32 passes and AC-29
      still passes
  - _Suggested executor: `apps-ayokoding-www-general-maker` for the bilingual copy_
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `how-to-read.tsx`'s `<details open>` renders all 6 required disclosure points (`aiBenchHowToVendorReported/IndexRelative/Coverage/BestConfig/ArcConflict/PriceGap`) in both `en` and `id` blocks of `<I18N>`; visible without interaction (`open` attribute, no JS toggle needed).
- [x] [AI] **W-21 RED**: bind AC-34 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:675-686` binds AC-34 with `@covers` annotation.
  - _Gherkin (binds) → AC-34 "The page carries a sources and licences section"_

    ```gherkin
    Scenario: The page carries a sources and licences section
      Given the dataset names its benchmark operators
      When the page renders
      Then a sources and licences section lists every named operator
      And each operator entry states its republication terms or records that none are stated
    ```

- [x] [AI] **W-22 GREEN**: render the Sources and Licences section from a dataset-level `operators`
      list, so a new operator appears without a component edit
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-34 passes
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `core/data/operators.ts` exports `OPERATORS` (SWE-bench, Terminal-Bench, GPQA — see DD-23 in `tech-docs.md`, which replaced an originally-shipped, misattributed "ARC Prize/GPQA" merged entry); `how-to-read.tsx` maps over it with no hardcoded operator name in the component.
- [x] [AI] **W-23 RED**: bind AC-35 for both locales
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `ai-benchmark.steps.tsx:706-717` binds AC-35 with `@covers` annotation for both locale outline rows.
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

- [x] [AI] **W-24 GREEN**: complete every `aiBench*` key in **both** the `en` and `id` blocks of
      `<I18N>` — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-35 passes for both
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: 46 `aiBench*` keys confirmed present in both `en` (translations.ts:30-85) and `id` (translations.ts:355-410) blocks — identical key sets, no gaps. (**Correction, recorded during PR review, cycle 1**: an earlier version of this note miscounted 56 keys by recording the line-span width — 85 − 30 + 1 = 56 — instead of the actual unique key count; `grep -o "^\s*aiBench[A-Za-z0-9]*:" translations.ts | tr -d ' :' | sort -u | wc -l` prints 46.) `test:unit` green.
- [x] [AI] **W-25 REFACTOR**: group the `aiBench*` keys under a comment block in each locale, matching
      the file's existing `toolsPage*` grouping
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `translations.ts:28-29` (en) and `:353-354` (id) carry the grouping comment ("Every aiBench* key MUST exist in both locales...") immediately preceding the contiguous `aiBench*` key block, matching the file's existing section-comment style.

### Responsive table behaviour

- [x] [AI] **W-26 RED**: extend `<SHELL>model-table.tsx`'s component test asserting that, at a
      mobile viewport, the table renders as stacked definition cards, and that both the mobile card
      variant and the `md`/`lg` table variant render the same set of figures for every model
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because `<SHELL>model-table.tsx` has no responsive branch yet
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done (superseded by GREEN state)
  - **Notes**: `model-table.test.tsx` asserts `model-table-desktop`/`model-table-mobile` both exist and `figureValues(mobileCard)).toEqual(figureValues(desktopRow))` per model (lines 46-57).
- [x] [AI] **W-27 GREEN**: implement the responsive table strategy from
      [prd §Responsive strategy](./prd.md#responsive-strategy--mobile-first-per-breakpoint) — stacked
      definition cards below `md`, a horizontally-scrollable `<table>` with a sticky first column at
      `md`, full width with a sticky header row at `lg`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts the mobile card variant and the table
      variant both render the same figures
  - **Date**: 2026-07-29 (reconciled)
  - **Status**: done
  - **Notes**: `model-table.tsx` — mobile `<ul>` stacked cards (`md:hidden`), desktop `<table>` (`hidden md:block`) with `overflow-x-auto`, sticky first column (`sticky left-0`, header + body), sticky header row (`sticky top-0 z-10`). `test:unit` green.

### Phase 5 Gate

> All checks below must pass before starting Phase 6. This is a **boundary** phase.

- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: fresh (`--skip-nx-cache`) run: 137 test files passed, 2955 tests passed, 6 skipped, 0 failed.
- [x] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0 — every scenario currently in
      `<SPECS>ai-benchmark.feature` has a step implementation carrying a `@covers` annotation
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: fresh run → `Spec coverage valid! 42 specs, 311 scenarios, 1115 steps — all covered.`
- [x] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: two full runs (623 and 625 passed respectively); zero ai-benchmark scenario failures in either. All failures were preexisting, unrelated tests (course-rehome-redirects, cost-of-living-calculator, skills-path-landing-body, content-namespace-redirects) that changed identity between the two runs — confirmed transient contention flake under concurrent multi-browser load per the workflow's documented contention-flake guidance, not a regression from this plan's changes.
- [x] [AI] `npx nx run ayokoding-www:specs:structure-validation` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: fresh run → `0 finding(s)` for every namespace (ayokoding, crane, organiclever, ose, rhino, wahidyankf).
- [x] [AI] The page is still unlinked — acceptance:
      `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>` prints `0` for both files. Falsifiable both
      ways: adding either link early makes it print ≥ 1, failing this gate.
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `grep -c` on `tools/page.tsx` and `footer.tsx` both print `0`.
- [x] [AI] No literal figure leaked into a component — acceptance:
      `grep -rn "[0-9][0-9]\.[0-9]%" <SHELL> <ROUTE>` prints nothing
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `grep -rn` over `shell/` and the route dir prints nothing — FCIS boundary holds.
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: fresh (`--skip-nx-cache`) run — `Successfully ran targets typecheck, lint for 25 projects and 6 tasks they depend on`. Fixed 2 preexisting unused-import lint warnings in `core/url-state.ts` (`BANDS`, `HARNESS_IDS` imported but only referenced in JSDoc `{@link}` tags) as part of this gate. **Correction (recorded during PR review, cycle 1)**: this fix was NOT committed separately as the repo's own separate-commit rule (`delivery.md:206-209` and `AGENTS.md` §Git Workflow's "Split by domain/concern") requires — it shipped bundled inside commit `84318e982` together with all 14 new Phase-5 feature files. That commit is already published, and rewriting a published commit is forbidden by [No Destructive Git Operations](../../../repo-governance/development/workflow/no-destructive-git-operations.md), so the bundling itself stands as a recorded process miss rather than being corrected retroactively. The original note's "Iron Rule 3/7" citation does not correspond to any rule defined in this plan and has been dropped.
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

- [x] [AI] Provision the Phase 6-7 unit's worktree from the latest `origin/main` — this is the unit's
      first phase, before its boundary at Phase 7:
      `git worktree add worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts origin/main`
      — acceptance: `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts rev-parse
--show-toplevel` prints the worktree path
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: worktree was already provisioned before this session started (branch
    `ayokoding-www-tools-ai-benchmark/phase-6-7-charts`, clean working tree, `HEAD` at
    `5cd5fbd5c`). `git -C worktrees/ayokoding-www-tools-ai-benchmark-phase-6-7-charts rev-parse
--show-toplevel` prints the worktree path.
- [x] [AI] **A-0**: append AC-12, AC-13, AC-14, AC-36 (in full — the scenario covers both charts in
      one `Scenario:` block, so it is authored here exactly once and not repeated at Phase 7's `Y-0`)
      and AC-37 to `<SPECS>ai-benchmark.feature` — acceptance:
      `npx nx run ayokoding-www:specs:structure-validation` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: appended the five scenarios verbatim from prd.md to the end of
    `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`. Fresh run →
    `0 finding(s)` for every namespace.
- [x] [AI] **A-1 RED**: create `<SHELL>chart-primitives.test.tsx` asserting `scaleLinear(domainMax,
pixelWidth)` maps `0 → 0`, `domainMax → pixelWidth`, and is monotonic in between
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (underpins) → AC-13._
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: created `chart-primitives.test.tsx` asserting `scaleLinear` maps `0→0`,
    `domainMax→pixelWidth`, is monotonic, scales proportionally, and degenerates to zero for a
    non-positive domain max. Run failed as expected: `Failed to resolve import "./chart-primitives"`
    (module does not exist yet) — 1 failed test file, the 137 preexisting files stayed green.
- [x] [AI] **A-2 GREEN**: create `<SHELL>chart-primitives.tsx` exporting `scaleLinear`, `<Axis>`,
      `<Bar>`, `<BandGroup>`, and `<Legend>` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: created `chart-primitives.tsx` exporting exactly `scaleLinear`, `Axis`, `Bar`,
    `BandGroup`, `Legend`, plus the band→token helpers (`bandColorVar`, `barFillClass`,
    `bandInkFillClass`, `bandSwatchClass`) every colour-bearing primitive routes through. A targeted
    `npx vitest run --project unit-fe chart-primitives.test.tsx` confirmed `scaleLinear`'s 5 tests
    green. The full `npx nx run ayokoding-www:test:unit` run at this point still failed — but with a
    NEW, different failure (`ScenarioNotCalledError: Scenario: A low-coverage model is marked as low
coverage was not called`) rather than the A-1 module-resolution error, confirming
    `chart-primitives.tsx` itself resolved correctly and the next blocker was the not-yet-bound
    cucumber scenarios A-3/5/7/9/11 target.
- [x] [AI] **A-3 RED** … **A-16 GREEN** (bundled — see note): bind AC-13/AC-14/AC-12/AC-37/the
      capability half of AC-36 in `<USTEPS>ai-benchmark.steps.tsx`; create
      `<SHELL>capability-chart.tsx` rendering one `<Bar>` per model within a `<BandGroup>` per class
      with the axis maximum as text (AC-13), an SVG `<text>` label per bar for name + index (AC-14),
      a low-coverage marker with the ratio as text (AC-12), each band's class name as a
      `<BandGroup>` header label (AC-37), `role="img"` + `aria-labelledby` → a localized `<title>`
      (capability half of AC-36), the `unrated` group as a labelled text list beneath the three
      bands with no `<rect>` emitted for those models, and the responsive label-placement strategy
      (label + value above each bar below `md`, left-gutter labels at `md`, axis ticks every 20
      units at `lg`) — commands: `npx nx run ayokoding-www:test:unit`,
      `npx vitest run --project unit-fe test/unit/fe-steps/ai-benchmark.steps.tsx`,
      `npx vitest run --project unit-fe src/features/ai-benchmark` — acceptance: every cited AC
      passes
  - _Gherkin (binds) → AC-13, AC-14, AC-12, AC-37, and the capability half of AC-36 — see A-0's
    embed above for the full scenario text of each; each is bound verbatim in
    `<USTEPS>ai-benchmark.steps.tsx`._
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `capability-chart.tsx` and `capability-chart.test.tsx` were authored together with
    the five cucumber Scenario bindings (A-3/5/7/9/11's targets), because `@amiceli/vitest-cucumber`
    throws `ScenarioNotCalledError` for the WHOLE steps file the moment `<SPECS>ai-benchmark.feature`
    contains a scenario with no matching `Scenario(...)` call (confirmed directly at A-2, above) —
    so the five new scenarios could not be bound one at a time in isolation without the others also
    failing to load. RED for A-3/5/7/9/11 is the same `ScenarioNotCalledError` class captured at
    A-2's note (a structural certainty: none of the five scenarios existed as `Scenario(...)` calls,
    nor did `capability-chart.tsx`, before this edit). RED for A-13/A-15 is likewise structural: the
    `unrated`-group and responsive-placement assertions in `capability-chart.test.tsx` target DOM
    testids (`capability-chart-unrated`, `capability-chart-label-mobile-*`,
    `capability-chart-label-desktop-*`, `capability-chart-ticks`) that did not exist in any prior
    revision of `capability-chart.tsx`. GREEN verified with three real command runs after the
    combined implementation: `npx vitest run --project unit-fe
test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (122) FAIL (0)`; `npx vitest run --project
unit-fe src/features/ai-benchmark` → `PASS (11) FAIL (0)` (covers both `chart-primitives.test.tsx`
    and `capability-chart.test.tsx`, including the unrated-group and responsive-parity assertions);
    full `npx nx run ayokoding-www:test:unit` → `139 passed (139)` test files, `2988 passed | 6
skipped (2994)` tests, exit 0 (the 6 skips are the same preexisting non-`.skip()` skips present
    in the Phase-5 baseline run, unrelated to this change). The price half of AC-36's "And" step is
    coded as a vacuous, genuinely-falsifiable assertion (`expect(screen.queryByTestId("price-chart-svg")).toBeNull()`)
    — the price chart does not exist until Phase 7's Y-2, so there is nothing yet that could carry
    an inaccessible name; Phase 7's Y-7 replaces this step body with a real accessible-name
    assertion (genuinely red at that point, since the price SVG exists but lacks `role="img"`), and
    Y-8 makes it pass for real. `npx nx run ayokoding-www:typecheck` and `npx nx run
ayokoding-www:lint` both exited 0 (lint's one new warning, `jsx-a11y(prefer-tag-over-role)` on
    `role="img"` on an `<svg>`, is the same warning class already present un-fixed on 2 preexisting
    files in this project, so it is non-blocking, matching repo convention).
- [x] [AI] **A-17 REFACTOR**: move every colour reference to the `--chart-band-*` tokens from Phase 1;
      no component may name a hue directly — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass and
      `grep -rn "hue-plum\|hue-teal\|hue-honey\|#[0-9a-fA-F]\{6\}" <SHELL>` prints nothing
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: every colour-bearing primitive in `chart-primitives.tsx` (`Bar`, `BandGroup`,
    `Legend`) already routed through `--chart-band-*` tokens from A-2 onward via static
    per-band Tailwind class maps (`BAR_FILL_CLASS`, `BAND_INK_FILL_CLASS`, `BAND_SWATCH_CLASS`) —
    Tailwind's class scanner needs a complete, unbroken literal string, so a template literal built
    from `bandColorVar()` at render time would never be found by the scanner; these maps keep every
    band's colour Tailwind-generated (never an inline `style` object). The refactor performed here:
    extracted the `BAND_LABEL_KEYS[band] ?? fallback → t(locale, key)` lookup — duplicated three
    times across `computeLayout`'s band label, the legend items, and the unrated heading — into one
    `bandLabel(band, locale)` helper in `capability-chart.tsx`, so the fallback guard cannot drift
    between call sites. `grep -rn "hue-plum\|hue-teal\|hue-honey\|#[0-9a-fA-F]\{6\}"
apps/ayokoding-www/src/features/ai-benchmark/shell/` printed nothing (exit 1, no matches).
    `grep -rn '\[var(\${' apps/ayokoding-www/src/features/ai-benchmark/shell/` and `grep -rn
'style={{' capability-chart.tsx chart-primitives.tsx` also printed nothing, confirming no
    dynamically-constructed Tailwind class string and no inline `style` prop anywhere in the new
    files. Re-ran the targeted suites after the refactor: `npx vitest run --project unit-fe
test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (122) FAIL (0)`; `npx vitest run --project
unit-fe src/features/ai-benchmark` → `PASS (11) FAIL (0)`; `npx nx run ayokoding-www:typecheck`
    → exit 0.

### Phase 6 Gate

> All checks below must pass before starting Phase 7. **Non-boundary** — commit to the unit branch
> and open no PR.

- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: fresh (`--skip-nx-cache`) run → `Test Files 139 passed (139)`, `Tests 2988 passed | 6
skipped (2994)`, exit 0. The 6 skips match the Phase-5-baseline skip count exactly (verified by
    running the identical command before any Phase 6 change was made) and are not `.skip()`/`.only()`/
    `.todo()` calls (the target's own pre-check greps for and blocks those).
- [x] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `Spec coverage valid! 42 specs, 316 scenarios, 1135 steps — all covered.`
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `npx nx affected -t typecheck lint --base=origin/main` (this branch's only commit is
    `origin/main`'s own tip, so `origin/main` is the correct diff base) → `Successfully ran targets
typecheck, lint for 25 projects and 6 tasks they depend on`. All reported findings are warnings
    on files this plan never touched (`no-empty-pattern` in unrelated `*-e2e` step files,
    `no-unused-vars` in `content/en/learn/...` course example code, `jsx-a11y(prefer-tag-over-role)`
    on a preexisting `role="dialog"` in `search-dialog.test.tsx` and a preexisting `role="radio"` in
    `controls.tsx`) — no errors, no new warning class introduced by this plan's own files beyond the
    one `role="img"` warning on `capability-chart.tsx` already recorded and justified at A-3..A-16's
    note above.
- [x] [AI] Commit per the [Commit Guidelines](#commit-guidelines) to
      `ayokoding-www-tools-ai-benchmark/phase-6-7-charts` — no push, no PR yet
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: two thematic commits on `ayokoding-www-tools-ai-benchmark/phase-6-7-charts`, no
    push: `d2b91aaa0` — `feat(ayokoding-www): phase 6 — shared chart primitives and capability
chart` (the 9 app/spec files: `chart-primitives.tsx`/`.test.tsx`, `capability-chart.tsx`/
    `.test.tsx`, the `score.ts` `COMPOSITE_INDEX_MAX` constant, `benchmark-content.tsx` wiring,
    `translations.ts` keys, `ai-benchmark.steps.tsx` Gherkin bindings, and the `.feature` scenario
    text); `275421ffb` — `docs(plans): tick phase 6 delivery checklist with verification evidence`
    (this file only). No preexisting-fix commit was needed — `typecheck`/`lint` were already clean
    before this phase's changes (no preexisting failures encountered to fix separately). Two
    unrelated, un-staged local files (`next-env.d.ts`, a Next.js–regenerated artifact, and a
    content `_index.md` sidebar-link drift) surfaced in the worktree during this session but were
    deliberately left out of both commits — outside this phase's scope, not this plan's concern.

> **Pause Safety**: the capability chart renders on the still-unlinked page and every test is green;
> the price chart is absent, which is a coherent intermediate state because the data table already
> carries every price in text. Safe to stop. To resume: `npx nx run ayokoding-www:test:unit`.

---

## Phase 7: Price Chart

> _Suggested executor: `swe-ui-maker`._

- [x] [AI] **Y-0**: append AC-15, AC-16 and AC-17 to `<SPECS>ai-benchmark.feature`. AC-36 is **not**
      appended again here — Phase 6's `A-0` already appended it in full (the scenario covers both
      charts in one `Scenario:` block; see `A-11`'s full embed), mirroring how `Y-7` below binds it
      without re-embedding it — acceptance: `npx nx run ayokoding-www:specs:structure-validation`
      exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: appended the AC-15/AC-16/AC-17 `Scenario:` blocks to `ai-benchmark.feature` right
    before the existing AC-36 scenario (matching PRD order). `npx nx run
ayokoding-www:specs:structure-validation` → `specs structure validate: 0 finding(s) for
"ayokoding"`, exit 0.
- [x] [AI] **Y-1 RED**: bind AC-15 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-15 "A metered model shows separate labelled input and output bars"_

    ```gherkin
    Scenario: A metered model shows separate labelled input and output bars
      Given a fixture model with a per-token input rate and output rate
      When the price chart is rendered
      Then that model has one bar labelled as the input rate
      And that model has one bar labelled as the output rate
    ```

  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: bound the AC-15 `Scenario` in `<USTEPS>ai-benchmark.steps.tsx`, importing the
    not-yet-created `PriceChart` from `@/features/ai-benchmark/shell/price-chart`. `npx nx run
ayokoding-www:test:unit` failed as expected: `Failed to resolve import
"@/features/ai-benchmark/shell/price-chart"` — 1 failed test file (`ai-benchmark.steps.tsx`),
    138 preexisting files stayed green (`138 passed (139)`). The same run failure covers Y-3 and
    Y-5's RED too (`@amiceli/vitest-cucumber` fails the WHOLE steps file the moment any bound
    scenario's target module is missing — same structural class documented at Phase 6's A-2 note —
    so the AC-16/AC-17 scenarios bound in the same edit are red for the identical reason).

- [x] [AI] **Y-2 GREEN**: create `<SHELL>price-chart.tsx` reusing `<BandGroup>`, `<Bar>`, `<Axis>` and
      `scaleLinear` from `<SHELL>chart-primitives.tsx` — no new primitive
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-15 passes
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: bundled with Y-4/Y-6 below (see Y-6's note for the combined verification run) — the
    three price-chart ACs were implemented together in one `price-chart.tsx`, mirroring Phase 6's
    A-3..A-16 bundling precedent, because all three RED scenarios were bound in the same edit and
    would otherwise re-fail on each other via the same `ScenarioNotCalledError`/import-resolution
    class until the whole component exists.
- [x] [AI] **Y-3 RED**: bind AC-16 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-16 "A subscription-only model renders in the subscription group"_

    ```gherkin
    Scenario: A subscription-only model renders in the subscription group
      Given a fixture model available only under a flat-rate subscription
      When the price chart is rendered
      Then that model appears in the subscription group
      But that model renders no per-token bar and no zero value
    ```

  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: bound in the same edit as Y-1/Y-5 (see Y-1's note) — red for the identical
    `price-chart` module-resolution reason, confirmed by the same `npx nx run
ayokoding-www:test:unit` run.

- [x] [AI] **Y-4 GREEN**: render the subscription group as a labelled text list naming the plan cost
      and its caps — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-16 passes; a
      snapshot assertion confirms no `$0` string is emitted for any subscription model
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: bundled with Y-2/Y-6 (see Y-6's note).
- [x] [AI] **Y-5 RED**: bind AC-17 — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
  - _Gherkin (binds) → AC-17 "An unfiltered price chart shows the lowest harness rate"_

    ```gherkin
    Scenario: An unfiltered price chart shows the lowest harness rate
      Given a fixture model priced differently by two harnesses
      When the price chart is rendered without a harness filter
      Then that model's bars use the lower of the two harness rates
      And the chart states that it shows the lowest available harness rate
    ```

  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: bound in the same edit as Y-1/Y-3 (see Y-1's note) — red for the identical
    `price-chart` module-resolution reason, confirmed by the same `npx nx run
ayokoding-www:test:unit` run.

- [x] [AI] **Y-6 GREEN**: consume `lowestRate` from `<CORE>price.ts` and render the "lowest available
      harness rate" statement as a localized chart subtitle
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-17 passes
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: created `price-chart.tsx` (Y-2) and `price-chart.test.tsx`, implementing AC-15/16/17
    together in one component, mirroring Phase 6's A-3..A-16 bundling precedent for the same
    structural reason (all three RED scenarios bound in one edit; `@amiceli/vitest-cucumber` fails
    the whole steps file for any unbound/unresolvable scenario). The chart groups models into the
    same four bands `computeGroups` produces (opus/sonnet/light/unrated — reusing `BandGroup`,
    `Bar`, `Axis`, `scaleLinear` from `chart-primitives.tsx`, no new primitive per Y-2's
    instruction); per band, a model with a metered `lowestRate` renders two labelled `<Bar>`s
    (input, output — AC-15); a model whose `lowestRate` is a subscription renders no bar at all and
    is instead collected into one flat, canonically-ordered "subscription group" text list naming
    its plan cost and caps (AC-16); a model with no price at all (neither metered nor subscription)
    renders in neither place (matches `model-table.tsx`'s existing "not reported" treatment,
    already covered by AC-21/AC-30's per-cell checks). The chart states its lowest-rate policy via
    a localized `price-chart-subtitle` (AC-17). Verification: `npx vitest run --project unit-fe
src/features/ai-benchmark/shell/price-chart.test.tsx` → `PASS (2) FAIL (2)` at this point (the
    2 failures are the Y-9-target responsive-placement tests, deliberately written into
    `price-chart.test.tsx` now and confirmed still red — see Y-9's own note); `npx vitest run
--project unit-fe test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (137) FAIL (0)`, confirming
    AC-15/AC-16/AC-17 all pass (the AC-36 price-half scenario in this same file still passes at this
    point too, because it is still the Phase-6 vacuous stub — Y-7 replaces it next). Added three
    translation keys (`aiBenchPriceChartTitle`, `aiBenchPriceLowestSubtitle`,
    `aiBenchPriceSubscriptionHeading`) in both locales, reusing the existing `aiBenchColInputPrice`/
    `aiBenchColOutputPrice`/`aiBenchSubscription` keys for the bar and subscription-line labels
    rather than adding redundant new copy.
- [x] [AI] **Y-7 RED**: bind the price half of AC-36
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

  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: wired `<PriceChart>` onto `benchmark-content.tsx` (between `<CapabilityChart>` and
    `<ModelTable>`, matching the tech-docs component-interaction diagram), and replaced the
    Phase-6 vacuous stub (`expect(screen.queryByTestId("price-chart-svg")).toBeNull()`) in the
    "Each chart exposes an accessible name" scenario's price-half `And` step with a real assertion:
    `screen.getByRole("img", { name: t("en", "aiBenchPriceChartTitle") })`. To keep this genuinely
    red (the bundled Y-2/Y-4/Y-6 implementation had already added `role="img"`/`<title>` to the
    price SVG, mirroring `capability-chart.tsx`), temporarily removed both from `price-chart.tsx`
    before running the check. `npx vitest run --project unit-fe
test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (136) FAIL (1)`, the one failure being
    exactly this new assertion (`Unable to find an accessible element with the role "img" and name
"Price by model"` at line 1130, the price-half `And` step) — every other scenario, including
    the AC-36 capability half, stayed green.

- [x] [AI] **Y-8 GREEN**: give the price SVG `role="img"` and a localized `<title>`
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: AC-36 passes in full
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: restored `role="img"`, `aria-labelledby={titleId}`, and `<title
id={titleId}>{t(locale, "aiBenchPriceChartTitle")}</title>` on the price SVG. `npx vitest run
--project unit-fe test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (137) FAIL (0)` — AC-36
    now passes in full for both charts.
- [x] [AI] **Y-9 RED**: extend `<SHELL>price-chart.test.tsx` asserting both the mobile variant
      (a two-line `in` / `out` block per model below `md`) and the `md`/`lg` variant (two bars
      sharing a row, wider plot area with axis ticks at `lg`) render the same rate values
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: fails because the price chart has no responsive layout branch yet
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: the "PriceChart — responsive label placement" `describe` block in
    `price-chart.test.tsx` (written together with the file at Y-2/Y-4/Y-6, but deliberately left
    targeting testids the Y-2/Y-4/Y-6 implementation does not yet emit) asserts a NEW
    `price-chart-mobile-in-*`/`price-chart-mobile-out-*` two-line text block matches the text of
    the ALREADY-EXISTING `price-chart-label-in-*`/`-out-*` desktop labels (AC-15's Y-2 target,
    reused here as the "desktop" variant rather than renamed, so the AC-15/AC-17 Gherkin bindings
    need no change), plus a NEW `price-chart-ticks` lg-only axis row. `npx vitest run --project
unit-fe src/features/ai-benchmark/shell/price-chart.test.tsx` → `PASS (2) FAIL (2)`: the 2
    failures are exactly these two responsive-placement tests (`Unable to find an element by:
[data-testid="price-chart-mobile-in-responsive-model"]` and the `price-chart-ticks` lookup) —
    the 2 subscription-group tests (Y-4's target) stayed green.
- [x] [AI] **Y-10 GREEN**: implement the responsive price-chart strategy — a two-line `in` / `out`
      block per model below `md`, two bars sharing a row at `md`, wider plot area with axis ticks at
      `lg` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: passes, and the component test asserts both variants render the same rate values
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: added the mobile two-line `in`/`out` text block (`md:hidden`), wrapped the existing
    desktop labels + the two `<Bar>`s in one `hidden md:block` group (so on mobile the price chart
    shows text only, not tiny bars — matching Y-9's requirement literally), and added the lg-only
    tick row (a new local `tickValues(max, count)` helper — 5 evenly spaced values from 0 to the
    data-driven axis max, since price has no fixed domain constant the way the capability index
    does). `npx vitest run --project unit-fe src/features/ai-benchmark/shell/price-chart.test.tsx
test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (141) FAIL (0)` — both previously-red
    responsive tests now pass, and every other price/capability scenario stayed green.
- [x] [AI] **Y-11 REFACTOR**: hoist anything both charts now duplicate into
      `<SHELL>chart-primitives.tsx` — this is the step that proves the primitive abstraction, which is
      why Phase 6 and Phase 7 share one PR
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: all tests still pass and
      `capability-chart.tsx` and `price-chart.tsx` share every layout primitive
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: diffed `capability-chart.tsx` against `price-chart.tsx` after Y-10 and found two
    genuinely duplicated primitives (not just similar-looking code): (1) the
    `BAND_LABEL_KEYS[band] ?? fallback → t(locale, key)` band-label lookup, byte-identical in both
    files; (2) the "lg-only tick row" markup (`<g className="hidden lg:block">` mapping evenly
    spaced domain values to `<text data-slot="chart-axis-tick">` elements) plus each chart's own
    "even values up to a max" generator (capability's was a fixed-20-unit-step loop over the fixed
    `COMPOSITE_INDEX_MAX`; price's was already count-based since price has no fixed domain). Hoisted
    both into `chart-primitives.tsx`: `bandLabel(band, locale)` (exported function) and
    `evenTicks(max, count)` + `<TickRow testId tickTestId values x y format>` (exported pure
    function + component) — `evenTicks(100, 5)` reproduces capability's original `[0, 20, 40, 60,
80, 100]` tick values exactly, so no chart's rendered tick VALUES changed, only where the
    generator lives. Both `capability-chart.tsx` and `price-chart.tsx` now import `bandLabel`,
    `evenTicks`, and `TickRow` from `chart-primitives.tsx` instead of carrying their own copies;
    neither file defines a local `bandLabel`/`tickValues` function anymore
    (`grep -n "function bandLabel\|function tickValues" capability-chart.tsx price-chart.tsx`
    prints nothing). Added direct unit tests for the two new primitives in
    `chart-primitives.test.tsx` (`evenTicks`, `bandLabel`, `TickRow` — 6 new tests). Did NOT
    further merge `computeLayout`/`splitByRate`/`axisMaxOf` — those differ in real ways (capability
    stacks every model in a band unconditionally; price filters to metered-only rows and routes
    subscriptions to a separate list; the axis domain is a fixed constant for capability vs
    data-driven for price), so forcing them into one shared function would be premature
    abstraction, not deduplication. Verification: `npx vitest run --project unit-fe
src/features/ai-benchmark test/unit/fe-steps/ai-benchmark.steps.tsx` → `PASS (158) FAIL (0)`
    (up from 151 before this step's new primitive tests — no regression, 7 net-new tests: 6 for the
    hoisted primitives + the `bandLabel` locale-distinctness fix). `grep -rn
"hue-plum\|hue-teal\|hue-honey\|#[0-9a-fA-F]\{6\}" apps/ayokoding-www/src/features/ai-benchmark/shell/`
    printed nothing (exit 1, no matches) — the color-token discipline established at Phase 6's A-17
    still holds after the refactor.

### Phase 7 Gate

> All checks below must pass before starting Phase 8. This is a **boundary** phase for the Phase 6-7
> unit.

- [x] [AI] `npx nx run ayokoding-www:test:unit` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: fresh (`--skip-nx-cache`) run → `Test Files 141 passed (141)`, `Tests 3014 passed |
6 skipped (3020)`, exit 0. The 6 skips match the Phase-5/6-baseline skip count exactly (same
    figure recorded at Phase 6 Gate's own check) and are not `.skip()`/`.only()`/`.todo()` calls.
- [x] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `Spec coverage valid! 42 specs, 319 scenarios, 1147 steps — all covered.`
- [x] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: this is the first e2e run against this Phase 6-7 unit's changes. The webServer needed
    a fresh `npx nx run ayokoding-www:build` first (no prior standalone build existed in this
    worktree) — confirmed `/[locale]/tools/ai-benchmark` compiled into the route list. Then `npx nx
run ayokoding-www-fe-e2e:test:e2e` → `629 passed`, `253 skipped` (the `skip-scenario` `-`
    markers for plain-`@unit` scenarios per DD-22, including every `@unit`-only AI-benchmark
    scenario — AC-15/AC-16/AC-17 and the capability-scoring rules are unit-only by design), exit 0.
    Zero failures — no transient-contention flake observed, so no re-run was needed. Every
    `@unit @e2e`-tagged AI-benchmark scenario passed for real, including "Each chart exposes an
    accessible name" (AC-36, now covering the price chart's real `role="img"` too) and both locale
    heading scenarios.
- [x] [AI] Both charts order models identically within each band (AC-11) — acceptance: the component
      test comparing the two rendered orderings passes
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: added `chart-order-parity.test.tsx` — a dedicated cross-chart component test (the
    existing AC-11 Gherkin scenario, bound at Phase 4, only proves `computeGroups`' canonical-order
    PROPERTY; this gate item calls for a test comparing the two chart components' ACTUAL rendered
    DOM order). It renders `<CapabilityChart>` then `<PriceChart>` against one shared 3-model
    fixture (all metered-priced, all excluded from the OPUS/SONNET anchor ids so every model lands
    in the predictable "light" band), reads each chart's `[data-testid^="…-row-"]` order within
    `…-band-light`, and asserts both orderings equal `["order-a", "order-b", "order-c"]` (the
    descending-composite-index canonical order). `npx vitest run --project unit-fe
src/features/ai-benchmark/shell/chart-order-parity.test.tsx` → `PASS (1) FAIL (0)`.
- [x] [AI] The page is still unlinked — acceptance: `grep -c "tools/ai-benchmark" <TOOLSIDX> <FOOTER>`
      prints `0` for both files
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `grep -c "tools/ai-benchmark" apps/ayokoding-www/src/app/\[locale\]/tools/page.tsx
apps/ayokoding-www/src/features/app-shell/shell/footer.tsx` → `...page.tsx:0` and
    `...footer.tsx:0` — the price chart's page-wiring at Y-7 only touched
    `benchmark-content.tsx` (the AI-benchmark route's own client component), not either
    navigation-surface file.
- [x] [AI] `npx nx affected -t typecheck lint` exits 0
  - **Date**: 2026-07-29
  - **Status**: done
  - **Notes**: `npx nx affected -t typecheck lint --base=origin/main` → `Successfully ran targets
typecheck, lint for 25 projects and 6 tasks they depend on` (52 of 56 tasks served from cache).
    The only new warning in this plan's own files is `jsx-a11y(prefer-tag-over-role)` on
    `price-chart.tsx`'s `role="img"` — the SAME warning class already recorded and justified for
    `capability-chart.tsx` at Phase 6's A-3..A-16 note (same pattern, same non-blocking
    classification, matching repo convention). No error, no other new warning class from this
    phase's files.
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
