---
title: "Enter the Designated Worktree — Locate and Provision"
description: Defines how the orchestrator locates the plan's declared ## Worktree section and navigates to or auto-provisions the worktree.
when_to_use: Use when a plan's worktree does not yet exist and must be provisioned from the latest origin/main, or when locating its declared path.
---

# Enter the Designated Worktree — Locate and Provision

**Continues** [Enter the Designated Worktree — Delivery-Mode Resolution](./enter-worktree-delivery-mode-resolution.md).

**Orchestrator action**:

1. **Locate the `## Worktree` section** in the plan:
   - **Multi-file plans**: in `delivery.md` (top-level `## Worktree` heading, before any phase).
   - **Single-file plans**: in `README.md` (top-level `## Worktree` heading, before `## Delivery Checklist`).
2. **If the section is missing AND the user specified no work branch at invocation**: terminate immediately with status `fail`. Emit a single user-visible line: `Worktree specification missing — add a "## Worktree" section to <delivery.md|README.md> per repo-governance/conventions/structure/plans/29-worktree-specification.md#worktree-specification before re-invoking plan execution.` (If the user specified a work branch — a worktree, `main`, or any existing branch — that selection wins per the precedence above and a missing `## Worktree` section is not a failure; skip provisioning and apply the freshness gate to that branch.)
3. **Parse the declared worktree path** (format: `worktrees/<plan-identifier>/`).
4. **Go to the designated worktree — navigate or provision** (default behavior; no user prompt needed):
   - Check whether the worktree is already registered: `git worktree list --porcelain` from the repo root, and confirm the directory `<repo-root>/worktrees/<plan-identifier>` exists.
   - **If it exists**: make it the execution root. If the current working directory is not already inside it, switch to it (e.g., `cd <repo-root>/worktrees/<plan-identifier>` or the harness's worktree-entry tool). Emit: `Worktree gate: entering existing worktree at worktrees/<plan-identifier>/`.
   - **If it does not exist**: auto-provision it from the latest `origin/main`:
     1. Emit a user-visible line: `Auto-provisioning worktree at worktrees/<plan-identifier>/…`
     2. From the repo root run:

        ```bash
        git fetch origin
        git worktree add -b <plan-identifier>-base worktrees/<plan-identifier> origin/main
        ```

        If the branch `<plan-identifier>-base` already exists (e.g., a prior worktree was removed but its branch kept), reuse it instead: `git worktree add worktrees/<plan-identifier> <plan-identifier>-base`.

     3. If `git worktree add` fails (e.g., path already exists as a stale entry), run `git worktree prune` and retry once; if it still fails, terminate with status `fail` and emit the error output verbatim.
     4. Add the immutable [Provisioned Worktree Identity](../../../conventions/structure/plans/worktree-specification.md#worktree-identity-record) to the plan using the exact path and branch returned by `git worktree add`, the executor identity, and current UTC time. A missing or conflicting record blocks later cleanup.
     5. Run `npm install && npm run doctor -- --fix` in the root repository worktree to initialize the toolchain, per [Worktree Toolchain Initialization](../../../development/workflow/worktree-setup.md).
     6. Emit a user-visible line: `Worktree provisioned at worktrees/<plan-identifier>/ — continuing execution.`
