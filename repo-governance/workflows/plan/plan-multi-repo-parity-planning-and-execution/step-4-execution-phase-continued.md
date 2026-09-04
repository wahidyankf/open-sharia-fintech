---
title: "Step 4 — Execution Phase (Continued)"
description: Covers propagation shape, the parity-manifest gate, per-repo delivery shape, and shared-machine safety.
when_to_use: Use when deciding whether to run repos concurrently, or the parity-manifest gate fires.
---

# Step 4 — Execution Phase (Continued)

**Continues from** [Step 4 — Execution Phase](./step-4-execution-phase.md).

**Propagation shape when the invoker opts out of strict whole-repository sequencing**: the repos
form a logical fan-out, not a content-dependency chain — `ose-public` is the source of truth and
`ose-private` its one downstream node. Once `ose-public` reaches `pass`, downstream repos may remain
independent DAG nodes, but their resource-heavy worktree provisioning, toolchain setup, builds, and
validation still run one repository at a time by default. Concurrent cross-repository heavy work
requires a concrete operational need recorded in the plan and confirmed machine, disk, runner, and
risk controls; lightweight independent work may use the N+1 model.

Two constraints override any permitted fan-out and force strict serialization:

- **`apps/rhino-cli` byte-identity** across the parity repos — `ose-public` and
  `ose-private` — a plan touching it propagates one repo at a time, never concurrently
  ([AGENTS.md §Related Repositories](../../../../AGENTS.md#related-repositories)).
- **Any node writing what another node reads** — the general DAG independence test. Sequence is not
  dependency, but a shared write target is.

**Expect the local `parity-manifest` pre-push gate to fire on the very first push, before any
cross-repo work.** Editing a byte-identity-governed file (`apps/rhino-cli/src/`, `Cargo.toml`,
`Cargo.lock`, `project.json`, `LICENSE`, the shared Gherkin tree) invalidates **this repo's own**
recorded checksum the moment the file changes. The gate is a same-repo self-consistency check, not a
cross-repo diff — it is not a signal that propagation is overdue, and it fires identically whether
the other repo is already in sync or untouched. Clear it with
`rhino-cli parity manifest generate`, committed as its own follow-up commit, then push. The
generator refuses to run against unstaged boundary files, so the order is fixed: `git add` the
boundary files you edited, generate, then stage the regenerated manifest.

Regenerating the local manifest **does not discharge the propagation obligation** — the gate's own
error text says so. It unblocks this repo's push and nothing more; the identical change still has to
reach the other parity repo.

**Per-repo delivery shape**: each repo's phases group into natural cohesive **delivery units**.
Under `*-to-pr`, one branch → one PR → one unit, opened and merged at its boundary. Under a
permitted direct mode, one unit reaches one direct integration checkpoint. Never integrate at every
phase or batch ready units at composite end. Each unit leaves `main` immediately safe to deploy;
incomplete behavior is complete-and-inert behind a temporary production-disabled **feature flag**,
with both paths tested and rollout, rollback, and removal recorded. Worktree modes reuse at most one
worktree per repo; main modes use the primary checkout and provision none — see
[Plans Organization Convention §Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).
See [plan-planning §Planning Granularity](../plan-planning/planning-granularity-and-one-branch-rule.md#planning-granularity-and-mode-specific-delivery-mapping).

**Shared-machine safety**: the parity repos share one machine's disk and git object store, and any of
them may be a bare repo driven through worktrees — verify each repo's topology, never assume it. The
**no-destructive-git** rule binds every git action
here — never discard a concurrent actor's uncommitted work, never remove a worktree or branch you
did not create. See
[No Destructive Git Operations](../../../development/workflow/no-destructive-git-operations.md).

**Output per repo**: plan-execution `final-status`, `iterations-completed`, final validation
report.

**On failure**: apply the Step 3 failure policy. Under the default stop policy, terminate the
composite with status `partial` (completed repos stay archived; the failing repo's plan stays in
`plans/in-progress/` with its worktree retained).
