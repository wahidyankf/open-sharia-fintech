# Rule 10: Worktree Specification Validation (Step 5d — MANDATORY)

After Step 5c, verify the plan declares a worktree path. Applies to ALL plans regardless of size —
pure-docs, single-file, trivial plans included.

**What to validate**:

1. **`## Worktree` section exists** — multi-file plans: top-level section in `delivery.md` before any
   phase heading; single-file plans: in `README.md` before `## Delivery Checklist`. Missing: **HIGH**
   (plan-execution Step 0 hard gate refuses to start).
2. **Path format** — `worktrees/<plan-identifier>/` where the identifier matches the plan-folder
   identifier (folder name minus the `YYYY-MM-DD__` prefix). Wrong format or identifier mismatch:
   **HIGH**.
3. **Provisioning command present** — the `claude --worktree <plan-identifier>` command shown verbatim
   as the optional manual pre-provisioning path (plan-execution Step 0 auto-provisions from latest
   `origin/main` by default, but the manual command must still be documented). Missing or wrong:
   **MEDIUM**.
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
   than one distinct path for this repo: **HIGH** — the cap permits exactly one worktree per
   repository per plan, reused across every delivery unit; a second distinct path is a defect even if
   each is individually well-formatted.

**Finding severity**: missing section: **HIGH**. Wrong format/identifier mismatch: **HIGH**. Missing
provisioning command: **MEDIUM**. Missing cross-reference: **LOW**. More than one distinct worktree
path for this repository: **HIGH**.
