---
description: Why uncleaned worktree artifacts harm a shared machine — disk, ref namespace, and stale-state ambiguity.
when_to_use: Use when justifying why cleanup is mandatory rather than optional on a shared machine.
---

# Why This Is a Gate

On a shared machine, uncleaned artifacts are not a tidiness issue — they accumulate against a resource
everyone is using.

- **Disk.** Each worktree is a full checkout. A multi-phase plan is capped at **one worktree per
  repository**, reused across every delivery unit that repo produces — several such plans in flight
  still fill a disk that CI runners, builds, and every other agent share, which is exactly why the cap
  exists (see [Plans Organization Convention §Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
- **The ref namespace.** Removing a worktree leaves its branch behind. A plan that cleans worktrees but
  not refs still leaves stale local and remote branches on every repo it touched, and those
  accumulate permanently.
- **Stale state.** An idle worktree is indistinguishable, by path alone, from an active one. Every
  worktree left behind makes the next actor's "is this safe to remove?" judgment harder.
