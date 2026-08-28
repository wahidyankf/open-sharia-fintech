---
title: "Hard Safety Rules"
description: The rules bounding every action the cleanup gate takes — self-created only, verify before deleting, never touch shared caches.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use when deciding whether a specific cleanup action is in-scope for a plan to perform.
---

# Hard Safety Rules

These bound every action the gate takes.

- **Self-created only.** Delete only what this plan created. Anything else requires positive evidence
  it is idle — not merely the absence of evidence that it is busy.
- **Verify not in use before deleting.** Check, then delete. When in doubt, leave it. An artifact left
  behind costs disk; an artifact wrongly deleted costs someone else's work.
- **Never delete a shared cache.** In particular, the **shared cargo `target/` directory** — the
  symlinked shared build output introduced by the
  [`rust-cargo-target-dir-sharing`](../../../../plans/done/2026-07-19__rust-cargo-target-dir-sharing/)
  plan — is depended on by concurrent builds in every other worktree. Removing it breaks them. The
  same reasoning applies to any shared cache: if another session can be relying on it, it is out of
  scope for a plan-scoped cleanup. This binds **agents**, and it is not contradicted by the ambient
  sweeper described in the [Build-Artifact Sweeper Convention](../../infra/build-artifact-sweeper.md),
  which may remove the same shared cache on its own schedule. A cache you must not delete can still
  disappear; that is the environment, not a rule violation by another actor.
- **Preserve diagnostic evidence.** Logs, traces, crash dumps, coverage output used to explain a
  failure, and any other non-regenerable evidence stay in place or move to an explicitly recorded
  evidence location before cleanup. An active, `partial`, or `fail` run retains its artifacts; a
  desire to reclaim disk never outranks diagnosis or resumption.
- **Cleanup is itself non-destructive to others.** The gate may not use any operation that a
  concurrent actor could be harmed by. It removes; it never force-removes, rewrites, or prunes shared
  state.
