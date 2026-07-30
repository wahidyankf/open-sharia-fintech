# Delivery Checklist: Vitest Glob-Coverage Guard

**Delivery Mode**: `worktree-to-pr` (the repo default). One delivery unit, one PR.

> **Legend** — `[AI]` = agent-executable step. `[HUMAN]` = requires a human decision or credential
> this repo's agents may not exercise. No `[HUMAN]` step is anticipated for this plan — recorded
> for completeness per the legend convention.

## Worktree

Worktree path: `worktrees/vitest-glob-coverage-guard/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree vitest-glob-coverage-guard
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

## Phase 1: Investigation and Guard Design

- [ ] [AI] Confirm scope: enumerate every `apps/*`/`libs/*` project with a `vitest.config.ts` (or
      equivalent) exposing named `include` globs
- [ ] [AI] Decide the guard's home (new script + Nx target vs. an existing checker agent
      enhancement) and its failure mode (CI-blocking vs. checker-report)
- [ ] [AI] Prototype the guard against the current repo state and confirm it reproduces the
      EWT-003 zero-coverage condition when replayed against the pre-fix glob

### Phase 1 Gate

- [ ] [AI] The guard, run against the current repo, reports zero uncovered test files
- [ ] [AI] The guard, run against a synthetic reintroduction of the EWT-003 glob gap, reports
      exactly that file as uncovered

> **Pause Safety**: this plan is Backlog (not started) — no work has begun, so there is nothing to
> resume. Promotion to `in-progress/` re-reads this README from the top.

## Quality Gates

Local: `npx nx affected -t typecheck lint test:quick` (once the guard lands as code) exits 0.
CI: the same targets green on the PR's own CI run before merge, per this repo's standard PR Merge
Protocol.

## Verification

The plan is complete when the guard exists, is wired into an Nx target or checker agent, passes
against the current repo (zero uncovered test files), and demonstrably fails against a
reintroduced glob-coverage gap (verified by the synthetic-reintroduction check in the Phase 1
Gate above).

## Phase 2: Knowledge Capture and Plan Archival

- [ ] [AI] Triage `learnings.md` per the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
      — route or discard every entry, or record the explicit "none" escape
- [ ] [AI] Move the plan folder to `plans/done/YYYY-MM-DD__vitest-glob-coverage-guard/` per the
      Plans Organization Convention's `done/` prefix
- [ ] [AI] Update the moved `README.md`'s Status line to "done — archived YYYY-MM-DD"

### Phase 2 Gate

- [ ] [AI] Every `learnings.md` entry reaches a terminal state (routed inline, filed as backlog, or
      discarded) — or the plan carries the explicit `No generalizable learnings — <reason>` escape
- [ ] [AI] Plan folder moved to `plans/done/YYYY-MM-DD__vitest-glob-coverage-guard/`
- [ ] [AI] Draft PR opened (covers Phases 1-2 commits), 3-cycle PR-Review Maker→Fixer loop run, all
      5 hardened merge preconditions hold, `[AI]`-merged to `main`

> **Pause Safety**: `learnings.md` is fully triaged and the plan folder is moved to `plans/done/`.
> Safe to stop indefinitely before the PR opens — nothing else depends on this plan. To resume (if
> interrupted after the PR opened but before it merged): check the PR's review-cycle and CI status,
> then finish the merge.
