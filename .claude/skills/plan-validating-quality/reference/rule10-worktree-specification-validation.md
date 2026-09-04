# Rule 10: Worktree Specification Validation (Step 5d — MANDATORY)

After Step 5c, verify the plan declares its mode-resolved work location. All plans need a
`## Worktree` section: worktree modes declare a path; main modes declare the primary-checkout
`not applicable` form. Apply prospectively regardless of size.

**What to validate** (items 2–5 apply only to worktree modes; for a main mode, verify those
worktree artifacts are absent):

1. **`## Worktree` section exists** — multi-file plans: top-level section in `delivery.md` before any
   phase heading in `delivery.md`. Missing: **HIGH**
   (plan-execution Step 0 hard gate refuses to start).
2. **Worktree-mode path format** — `worktrees/<plan-identifier>/` where the identifier matches the plan-folder
   identifier (folder name minus the `YYYY-MM-DD__` prefix). Wrong format or identifier mismatch:
   **HIGH**.
3. **Worktree-mode provisioning command present** — the `claude --worktree <plan-identifier>` command shown verbatim
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
6. **Mode-specific record** — for a worktree mode, `## Worktree` contains a Provisioned Worktree
   Identity with the declared repository-relative `worktrees/<plan-identifier>/` route, initial branch,
   creator, and UTC creation time, plus a Delivery Branch Inventory whose initial branch entry is
   `provisioned`/`active` and proves the creation command and timestamp. A real absolute, home,
   tool-prefix, drive, UNC, or other machine-specific path in that identity is **HIGH**. Missing
   identity, inventory, or initial proof: **HIGH**. An inventory that omits a
   plan-created/current branch, leaves an active entry at cleanup, or lacks a merged-PR reviewed-head
   SHA for a `*-to-pr` delivery: **HIGH**. Scan the complete committed `delivery.md`: any real
   absolute, home, tool-prefix, drive, UNC, or other machine-specific local path is **HIGH**, even
   outside the identity section. The sole authoring-worktree exception passes authoring
   review only when the plan records `Provisioning status: pending`, names the different active
   authoring worktree, cites the user's explicit stay-in-worktree constraint, and explains its
   dependency on unlanded work there. It must omit rather than fake identity/inventory and must make
   Step 0 provisioning a blocking first outcome. Missing evidence or any implementation while
   pending: **HIGH**. For a main mode, require `Worktree: not applicable` plus the mode and primary
   checkout rationale; any worktree identity or provisioning command is **HIGH**.

7. **Archival cleanup steps** — for a worktree mode, the plan's archival section or phase — the
   `### Plan Archival` section, or the phase that performs archival — contains a step
   classifying every `Delivery Branch Inventory` entry, a worktree-removal step, and a
   branch-cleanup step routing to
   [Branch Cleanup](../../../../repo-governance/development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md).
   Missing any: **MEDIUM** — the obligation already binds at plan-execution
   finalization, so the defect is that the plan does not show it, not that it is unbound. Never
   fires for a main mode, which provisions none, or a plan folder with no `delivery.md`.

**Finding severity**: missing section: **HIGH**. Wrong format/identifier mismatch: **HIGH**. Missing
provisioning command: **MEDIUM**. Missing cross-reference: **LOW**. More than one distinct worktree
path for this repository: **HIGH**. Machine-specific worktree identity path: **HIGH**.
Missing/incomplete identity or inventory outside the documented authoring exception: **HIGH**.
Machine-specific local path anywhere in committed `delivery.md`: **HIGH**.
Missing a worktree-mode archival cleanup step: **MEDIUM**.
