---
title: "Enter the Designated Worktree — Secrets, Output, and Rationale"
description: Explains why secret- and state-dependent infra operations must run from the primary checkout, and states the gate's output and rationale.
when_to_use: Use when a delivery checklist item runs terraform apply, a live Ansible converge, or any other state-changing infra operation.
---

# Enter the Designated Worktree — Secrets, Output, and Rationale

**Continues** [Enter the Designated Worktree — Freshness Gate](./enter-worktree-freshness-gate.md).

**Secret/State-Dependent Infrastructure Operations Run from the Primary Checkout**

A worktree provisioned from `origin/main` contains no gitignored secrets or local infrastructure state. Credential files (`.env` and similar) and any local-backend infrastructure-state file (for example a Terraform state file) are gitignored and exist only in the primary checkout. Because of this, secret- or state-dependent infrastructure operations — `terraform apply`, a live Ansible converge (`ansible-playbook` against real hosts), or any equivalent state-changing infra operation — MUST run from the primary checkout as `[HUMAN]` / operator steps, never from the plan's worktree. Running `terraform apply` from a worktree that has no state causes Terraform to see an empty state and attempt to recreate the entire managed estate; copying state into a worktree creates split-brain, with two checkouts mutating real infrastructure against divergent state copies. Keeping these operations in the primary checkout keeps all secret-bearing, state-changing work in a single location.

Mark such steps `[HUMAN]` in the delivery checklist (per [Plans Organization Convention §Executor Tagging](../../../conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)) and instruct the operator to run them from the primary checkout where the secrets and state reside.

**Output**: Execution running inside the designated worktree, up to date with the latest `origin/main` (provisioned if needed).

**Why this is a hard gate**: A missing `## Worktree` section is a hard-fail **only when the user has not specified a work branch at invocation** — in that case there is no declared path to provision, so the plan is incomplete and must be fixed by the author before execution can proceed. A CWD mismatch, by contrast, is recoverable: the executor knows the target path and navigates to or provisions the worktree automatically. Running outside a worktree without a declared path would pollute the main checkout with in-flight work, break the parallel-safety guarantee, and risk dirty-gitlink hazards in any subrepo context. The freshness sync is equally mandatory: implementing against a stale base invites merge conflicts at push time and validates the plan against code that no longer matches `origin/main`.
