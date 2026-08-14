# Plan Archival and Worktree Usage Verification

## 1. Verify Plan Archival and README Updates (Step 5d — MANDATORY)

After verifying manual assertions (Step 5c), verify that the plan was properly archived.

### What to Validate

1. **Plan Moved to done/**
   - Verify the plan folder exists in `plans/done/` (not in `plans/in-progress/` or `plans/backlog/`)
   - If plan is still in `in-progress/`: CRITICAL finding
   - Use `git log` to confirm `git mv` was used (preserves history)

2. **in-progress README Updated**
   - Read `plans/in-progress/README.md`. Verify the plan entry has been REMOVED.
   - If the plan entry still exists: HIGH finding

3. **done README Updated**
   - Read `plans/done/README.md`. Verify the plan entry has been ADDED with completion date.
   - If the plan entry is missing: HIGH finding

4. **No Orphaned References**
   - Search for references to the old `plans/in-progress/[plan-name]` path across the repo
   - If any broken references exist: MEDIUM finding per reference

5. **Archival Commit Exists**
   - Check git log for a commit with pattern `chore(plans): move * to done`
   - If no archival commit: MEDIUM finding

### Finding Severity

- Plan not moved to done/: **CRITICAL**
- in-progress README not updated: **HIGH**
- done README not updated: **HIGH**
- Orphaned references: **MEDIUM** per reference
- Missing archival commit: **MEDIUM**

## 2. Verify Worktree Was Used (Step 5e — MANDATORY)

After verifying archival (Step 5d), verify that execution actually happened inside the declared
worktree per the
[plan-execution Step 0 gate](../../../../repo-governance/workflows/plan/plan-execution/14-enter-worktree-preconditions-and-work-branch.md#0-enter-the-designated-worktree-sequential-hard-gate).
The plan-execution workflow refuses to start without a worktree — it navigates to the declared
worktree (provisioning it from the latest `origin/main` when missing) and syncs it with `origin/main`
before implementing. This step independently confirms the gate held.

### What to Validate

1. **Plan declares a `## Worktree` section**
   - Multi-file plan: `delivery.md` contains `## Worktree`. Single-file plan: `README.md` contains
     it.
   - Missing: **HIGH** finding (the executor should have refused to start; if it ran, that itself is
     a CRITICAL workflow violation).

2. **Declared worktree path matches the convention**
   - Path follows `worktrees/<plan-identifier>/` where `<plan-identifier>` matches the folder name
     minus the date prefix.
   - Wrong format: **HIGH** finding (counts as a `## Worktree` section misuse).

3. **Git history evidence the work happened in the worktree**
   - Commits authored during the plan execution window should show authorship from the worktree
     branch (`<plan-identifier>`) before merging to `main`, OR commit messages should reference the
     worktree.
   - When the publish path was direct-to-main (no worktree branch trace), confirm the commits cluster
     within the plan-execution timeframe and reference the plan identifier.
   - No worktree evidence at all: **MEDIUM** finding (could be a legitimate fast-forward; flag for
     manual review).

4. **Freshness sync was performed (Step 0 freshness gate)**
   - Look for execution-log or delivery-notes evidence that the worktree was synced with
     `origin/main` before implementation began (e.g., the `Worktree gate: passed (… up to date with
origin/main)` line, or a recorded `git merge --ff-only origin/main` / `git rebase origin/main`
     step).
   - No sync evidence: **MEDIUM** finding (the gate may have run unrecorded; flag for manual review).

5. **Worktree cleanup was offered after archival (prompted, never silent)**
   - On `pass` with the archival commit pushed: either (a) the worktree `worktrees/<plan-identifier>/`
     no longer exists (user approved deletion), or (b) a recorded user decline exists (e.g., the
     `Worktree retained at worktrees/<plan-identifier>/ per user choice.` line in the execution log or
     delivery notes).
   - Worktree still present with NO recorded prompt/decline: **MEDIUM** finding (cleanup step skipped
     — worktrees accumulate).
   - Worktree deleted with NO recorded user confirmation: **HIGH** finding (deletion without explicit
     user approval violates the prompted-cleanup rule).

6. **Worktree cap held during execution** (enforces
   [Worktree Cap](../../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule))
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
