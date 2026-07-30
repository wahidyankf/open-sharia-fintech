# Delivery Checklist: Audit `reuseExistingServer` Across `*-e2e` Playwright Configs

**Delivery Mode**: `worktree-to-pr` (the repo default). One delivery unit, one PR.

> **Legend** — `[AI]` = agent-executable step. `[HUMAN]` = requires a human decision or credential
> this repo's agents may not exercise. No `[HUMAN]` step is anticipated for this plan — recorded
> for completeness per the legend convention.

## Worktree

Worktree path: `worktrees/audit-e2e-reuse-existing-server-config/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree audit-e2e-reuse-existing-server-config
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

## Phase 1: CI Runner Persistence Investigation

- [ ] [AI] Determine whether each of the six configs' CI runners are ephemeral-per-job or
      shared/persistent (checking workflow YAML runner labels against this repo's self-hosted vs.
      GitHub-hosted runner usage)
- [ ] [AI] Record the availability/persistence matrix per config, with the evidence used for each
      verdict

### Phase 1 Gate

- [ ] [AI] Every one of the six configs has a recorded, evidenced ephemeral-or-persistent verdict

> **Pause Safety**: this plan is Backlog (not started) — no work has begun, so there is nothing to
> resume. Promotion to `in-progress/` re-reads this `README.md` from the top.

## Phase 2: Remedy Selection and Application

- [ ] [AI] Based on Phase 1's verdicts, choose the remedy per config: a `!process.env.CI` gate
      (matching `organiclever-app-web-e2e`), a documentation caveat, or both
- [ ] [AI] Apply the chosen remedy to each of the six configs
- [ ] [AI] Decide whether an automated guard (checker rule or comment convention) is warranted and,
      if so, add it

### Phase 2 Gate

- [ ] [AI] Every one of the six configs matches its chosen remedy; no config is left
      unconditionally hardcoded `true` without a documented, evidenced reason

> **Pause Safety**: work is only underway once Phase 1 completes; a partial Phase 2 leaves the
> matrix from Phase 1 as the resumption point.

## Quality Gates

Local: `npx nx affected -t typecheck lint test:quick` for every touched `*-e2e` project exits 0.
CI: the same targets green on the PR's own CI run before merge, per this repo's standard PR Merge
Protocol.

## Verification

The plan is complete when all six configs have a recorded, evidenced ephemeral-or-persistent
verdict and a remedy applied consistent with that verdict, and (if added) the automated guard
passes against the current repo state.

## Phase 3: Knowledge Capture and Plan Archival

- [ ] [AI] Triage `learnings.md` per the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
      — route or discard every entry, or record the explicit "none" escape
- [ ] [AI] Move the plan folder to
      `plans/done/YYYY-MM-DD__audit-e2e-reuse-existing-server-config/` per the Plans Organization
      Convention's `done/` prefix
- [ ] [AI] Update the moved `README.md`'s Status line to "done — archived YYYY-MM-DD"

### Phase 3 Gate

- [ ] [AI] Every `learnings.md` entry reaches a terminal state (routed inline, filed as backlog, or
      discarded) — or the plan carries the explicit `No generalizable learnings — <reason>` escape
- [ ] [AI] Plan folder moved to `plans/done/YYYY-MM-DD__audit-e2e-reuse-existing-server-config/`
- [ ] [AI] Draft PR opened (covers Phases 1-3 commits), 3-cycle PR-Review Maker→Fixer loop run, all
      5 hardened merge preconditions hold, `[AI]`-merged to `main`

> **Pause Safety**: `learnings.md` is fully triaged and the plan folder is moved to `plans/done/`.
> Safe to stop indefinitely before the PR opens — nothing else depends on this plan. To resume (if
> interrupted after the PR opened but before it merged): check the PR's review-cycle and CI status,
> then finish the merge.
