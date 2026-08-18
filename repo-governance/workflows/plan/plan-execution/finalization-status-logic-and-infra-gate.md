---
title: "Finalization and Archival — Status Logic, Infra-Execution Gate, and Direct-Push Archival"
description: Defines the pass/partial/fail branching logic, the Infra-Execution Gate precondition, and the direct-push archival steps.
when_to_use: Use when determining final plan status, or verifying a pending infra-apply step before archiving a plan.
---

**Logic**:

- If status is `pass` (zero findings):

  **Infra-Execution Gate (precondition before archival)**: Before running `git mv`, check whether the plan's delivery checklist contains any infrastructure-apply step — `terraform apply`, `terraform destroy`, a live Ansible converge (`ansible-playbook` against real hosts), or any equivalent state-changing infra operation per the [Step 0 policy note](./enter-worktree-preconditions-and-work-branch.md). If any such step is present but has NOT been verified-executed from the primary checkout (i.e., its checkbox remains unticked, or its implementation notes show it was deferred rather than genuinely run and confirmed), the workflow MUST NOT archive. Instead:
  1. Set status to `partial`.
  2. Leave the plan in `plans/in-progress/`.
  3. Retain the worktree.
  4. Surface to the user the exact infra step(s) that remain unexecuted, quoting the checkbox text and acceptance criterion verbatim.
  5. Stop. Do not proceed to any archival step.

  Zero validation findings alone is NOT sufficient for archival when an infra-apply step is still pending — the apply must be genuinely performed and its acceptance criterion verified (the provisioned resource exists and the target service responds), not merely reviewed or deferred. Only when all infra-apply steps in the delivery checklist are confirmed executed from the primary checkout may archival proceed.

  When the gate passes, proceed with archival. The remaining steps branch by the delivery mode
  resolved in Step 0.

  **`worktree-to-origin-main` / `main-to-origin-main` (direct-push modes)** — archival lands as a
  direct commit pushed to `origin main`, matching the default flow:
  1. Move entire plan folder from current location to `plans/done/`:

     ```bash
     git mv plans/in-progress/plan-name/ plans/done/YYYY-MM-DD__plan-name/
     ```

  2. **Update `plans/in-progress/README.md`** — remove the plan entry from the list
  3. **Update `plans/done/README.md`** — add the plan entry with completion date and brief summary:

     ```markdown
     - [Plan Name](./YYYY-MM-DD__plan-name/) — Brief description. Completed YYYY-MM-DD.
     ```

  4. **Update any other READMEs** that reference this plan (e.g., `plans/README.md`, project READMEs that link to the plan)
  5. **Search for orphaned references** to the old `plans/in-progress/[plan-name]` path and fix them
  6. **Commit the archival**:

     ```
     chore(plans): move [plan-identifier] to done
     ```
