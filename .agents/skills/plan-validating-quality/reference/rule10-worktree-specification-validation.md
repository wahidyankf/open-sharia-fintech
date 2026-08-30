# Rule 10: Worktree Specification Validation (Step 5d — MANDATORY)

After Step 5c, verify the plan declares a worktree path. Applies to ALL plans regardless of size —
pure-docs and otherwise small formal plans included. Apply prospectively.

**What to validate**:

1. **`## Worktree` section exists** — multi-file plans: top-level section in `delivery.md` before any
   phase heading in `delivery.md`. Missing: **HIGH**
   (plan-execution Step 0 hard gate refuses to start).
2. **Path format** — `worktrees/<plan-identifier>/` where the identifier matches the plan-folder
   identifier (folder name minus the `YYYY-MM-DD__` prefix). Wrong format or identifier mismatch:
   **HIGH**.
3. **Provisioning command present** — the `claude --worktree <plan-identifier>` command shown verbatim
   as the provisioning path the plan was authored inside (plan-execution Step 0 auto-provisions from
   latest `origin/main` only as a backstop, but the command must still be documented). Missing or
   wrong: **MEDIUM**.
4. **Cross-reference** — link to
   [Worktree Path Convention](../../../../repo-governance/conventions/structure/worktree-path.md)
   and/or
   [Plans Organization Convention §Worktree Specification](../../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).
   Missing: **LOW**.
5. **Worktree cap — at most one worktree path per repository** (enforces
   [Worktree Cap](../../../../repo-governance/conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
   Scoped to the single repository `plan-checker` runs in (confirm via `git remote get-url origin` or
   `repo-config.yml`). Collect every worktree path named: the top-level declaration, every `Worktree`
   column value in `### Delivery Boundaries`, and any other `worktrees/<...>/` path mentioned. More
   than one distinct path for this repo: **HIGH** — the cap permits at most one worktree per
   repository per plan, reused across every delivery unit; a second distinct path is a defect even
   if each is individually well-formatted.
6. **Identity record and initialized inventory** — normally, `## Worktree` contains a Provisioned Worktree
   Identity with exact path, initial branch, creator, and UTC creation time, plus a Delivery Branch
   Inventory whose initial branch entry is `provisioned`/`active` and proves the exact creation command
   and timestamp. Missing identity, inventory, or initial proof: **HIGH**. An inventory that omits a
   plan-created/current branch, leaves an active entry at cleanup, or lacks a merged-PR reviewed-head
   SHA for a `*-to-pr` delivery: **HIGH**. The sole authoring-worktree exception passes authoring
   review only when the plan records `Provisioning status: pending`, names the different active
   authoring worktree, cites the user's explicit stay-in-worktree constraint, and explains its
   dependency on unlanded work there. It must omit rather than fake identity/inventory and must make
   Step 0 provisioning a blocking first outcome. Missing evidence or any implementation while
   pending: **HIGH**.

**Finding severity**: missing section: **HIGH**. Wrong format/identifier mismatch: **HIGH**. Missing
provisioning command: **MEDIUM**. Missing cross-reference: **LOW**. More than one distinct worktree
path for this repository: **HIGH**. Missing/incomplete identity or inventory outside the documented
authoring exception: **HIGH**.
