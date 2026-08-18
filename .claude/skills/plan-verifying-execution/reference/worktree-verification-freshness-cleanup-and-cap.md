# Worktree Usage Verification (Step 5e continued): Freshness, Cleanup, and the Worktree Cap

1. **Freshness sync was performed (Step 0 freshness gate)**
   - Look for execution-log or delivery-notes evidence that the worktree was synced with
     `origin/main` before implementation began (e.g., the `Worktree gate: passed (… up to date with
origin/main)` line, or a recorded `git merge --ff-only origin/main` / `git rebase origin/main`
     step).
   - No sync evidence: **MEDIUM** finding (the gate may have run unrecorded; flag for manual review).

2. **Worktree cleanup was offered after archival (prompted, never silent)**
   - On `pass` with the archival commit pushed: either (a) the worktree `worktrees/<plan-identifier>/`
     no longer exists (user approved deletion), or (b) a recorded user decline exists (e.g., the
     `Worktree retained at worktrees/<plan-identifier>/ per user choice.` line in the execution log or
     delivery notes).
   - Worktree still present with NO recorded prompt/decline: **MEDIUM** finding (cleanup step skipped
     — worktrees accumulate).
   - Worktree deleted with NO recorded user confirmation: **HIGH** finding (deletion without explicit
     user approval violates the prompted-cleanup rule).

3. **Worktree cap held during execution** (enforces
   [Worktree Cap](../../../../repo-governance/conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule))
   - This check runs against the single repository `plan-execution-checker` is invoked in. Inspect
     execution evidence for this repo — implementation-notes/execution-log lines recording
     `git worktree add`, or (when still on disk) `git worktree list --porcelain` combined with
     `git reflog` for the plan's execution window — for how many distinct `git worktree add`
     invocations happened for this repo over the plan's whole run.
   - **More than one distinct `git worktree add` invocation for this repo within one plan: HIGH**
     finding — every delivery unit landed in this repo should have reused the one provisioned
     worktree (branch-switching between units), not provisioned a fresh one per unit.
   - **No worktree-provisioning evidence recoverable** (no execution-log/implementation-notes lines
     recording `git worktree add`, AND the worktree is already gone from disk per this repo's
     [Immediate Cleanup rule](../../../../repo-governance/development/workflow/worktree-and-artifact-cleanup.md),
     so `git worktree list --porcelain` and `git reflog` have nothing left to inspect either):
     **MEDIUM** finding (the cap may have held unrecorded; flag for manual review) — never treat a
     zero-evidence result as equivalent to "one worktree, compliant."

### Finding Severity

- Plan ran without a `## Worktree` section: **CRITICAL** (Step 0 gate breach)
- Wrong worktree-path format in plan: **HIGH**
- Worktree deleted without recorded user confirmation: **HIGH**
- No worktree evidence in git history: **MEDIUM**
- No `origin/main` freshness-sync evidence: **MEDIUM**
- Worktree still present with no recorded cleanup prompt or decline: **MEDIUM**
- More than one `git worktree add` invocation for this repository within one plan: **HIGH**
- No worktree-provisioning evidence recoverable (log lines absent and worktree already cleaned up per
  the Immediate Cleanup rule): **MEDIUM**
