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
