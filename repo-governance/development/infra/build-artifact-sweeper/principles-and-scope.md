---
title: "Principles, Conventions, and Sweep Scope"
description: Enumerates the principles and conventions the build-artifact sweeper implements, and defines exactly what it may remove and what it never touches
category: explanation
subcategory: development
tags:
  - build-artifacts
  - environment
  - ai-agents
  - infrastructure
  - cleanup
created: 2026-08-05
when_to_use: Use when you need to know why the sweeper exists, which conventions govern its scope, or whether a specific missing file falls inside or outside what it removes.
---

# Principles, Conventions, and Sweep Scope

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: The
  correct response to a vanished artifact is one cheap, reversible action — rebuild — not an
  investigation. Knowing the environment's behaviour in advance is what makes that judgement
  available at the moment of surprise.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: The sweeper **is**
  the root cause of a missing-artifact failure. Naming it here prevents the far more expensive
  failure mode: an agent tracing a phantom defect through code that was never wrong.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: Everything
  the sweeper removes is reproducible from committed sources by a documented command. That is
  precisely why it is safe to remove, and why regeneration is a complete fix.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: One
  environmental fact with a fixed response, rather than per-agent heuristics for distinguishing
  "suspiciously missing" from "legitimately missing".

## Conventions Implemented/Respected

- **[No Machine-Specific Information in Commits](../../quality/no-machine-specific-commits.md)**: This
  convention deliberately records **no** scheduler label, script path, username, or cadence. Those
  are host-specific details that would both violate that rule and drift out of date. Agents depend on
  the sweeper's _behaviour_, never on its mechanism.

- **[Temporary Files Convention](../temporary-files.md)**: Draws the boundary between what the sweeper
  removes (regenerable build output) and the agent-owned temporary directories it does not.

- **[Worktree and Artifact Cleanup Convention](../../workflow/worktree-and-artifact-cleanup.md)**: The
  plan-end gate governing what **agents** delete. This convention governs what the **environment**
  deletes. See
  [Reconciliation](./reconciliation-and-related-documentation.md#reconciliation-with-neighbouring-rules) —
  the two do not conflict.

- **[Worktree Toolchain Initialization](../../workflow/worktree-setup.md)**: The provisioning commands a
  swept worktree is restored with.

## What the Sweeper May Remove

Three classes, all gitignored and all regenerable:

1. **Build output** — `target/`, `dist/`, `.next/`, `out/`, `coverage/`, and equivalents in any
   worktree or the primary checkout.
2. **Tool caches** — `.nx/cache`, `node_modules/.cache`, and equivalents.
3. **The shared cargo `target/`** — the symlinked shared Rust build directory used across worktrees.
   It is swept like any other cache, notwithstanding the agent-facing rule that no agent may delete
   it.

## What the Sweeper Never Touches

This boundary is what makes the response protocol safe. The sweeper does not remove:

- tracked files, or uncommitted edits to tracked files
- `.env*` files
- `generated-reports/` and `local-tmp/`
- worktree directories themselves, or any git ref or the object store

**Anything missing outside the three removable classes is not the sweeper.** Investigate it normally —
and never assume a sweep explains lost work.
