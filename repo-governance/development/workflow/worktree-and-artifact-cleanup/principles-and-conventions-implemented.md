---
description: The principles and companion conventions the worktree and artifact cleanup gate implements and respects.
when_to_use: Use when tracing why the worktree and artifact cleanup gate exists back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Every
  action this gate takes is a deletion, and deletions are irreversible. The convention requires
  positively identifying ownership and idleness before each removal rather than sweeping broadly.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: A
  plan cleans up what it can positively account for having created — never what merely looks stale.
  Shared caches other sessions depend on are out of scope by rule, not by judgement call.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Cleanup is
  a fixed post-merge gate with a short, ordered checklist rather than a heuristic sweep, so its blast
  radius stays legible.

## Conventions Implemented/Respected

- **[No Destructive Git Operations Convention](../no-destructive-git-operations.md)**: The companion
  convention forbids the blunt removals (recursive clean, force delete, hard reset) that a careless
  cleanup would otherwise reach for; this gate prescribes the self-scoped, verified alternative.

- **[Worktree Toolchain Initialization](../worktree-setup.md)**: The provisioning half of the same
  worktree lifecycle. This convention is its teardown counterpart.

- **[Worktree Path Convention](../../../conventions/structure/worktree-path.md)**: Cleanup depends on
  worktrees living at the conventional `worktrees/<name>/` path so ownership is determinable.
