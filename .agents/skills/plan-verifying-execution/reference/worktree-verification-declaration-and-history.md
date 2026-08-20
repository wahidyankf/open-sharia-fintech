# Worktree Usage Verification (Step 5e): Declaration and Git History

## 2. Verify Worktree Was Used (Step 5e — MANDATORY)

After verifying archival (Step 5d), verify that execution actually happened inside the declared
worktree per the
[plan-execution Step 0 gate](../../../../repo-governance/workflows/plan/plan-execution/enter-worktree-preconditions-and-work-branch.md#0-enter-the-designated-worktree-sequential-hard-gate).
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
