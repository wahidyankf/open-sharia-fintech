---
description: The three eligible artifact classes cleanup covers while retaining diagnostics and shared state.
when_to_use: Use when checking that a cleanup covers all three artifact classes, not just the first.
---

# The Three Artifact Classes

A complete cleanup covers all three. Stopping after the first is the common failure.

1. **Worktrees** — the working directories this plan created.
2. **Branches** — plan-created local and remote branches with delivery and no-unpushed proof. See
   [Branch Cleanup](./branch-cleanup.md#branch-cleanup).
3. **Regenerable build output** — `target/`, `dist/`, `.next/`, and plan-local build caches produced
   **inside this plan's own worktrees**, excluding diagnostics and shared caches.
