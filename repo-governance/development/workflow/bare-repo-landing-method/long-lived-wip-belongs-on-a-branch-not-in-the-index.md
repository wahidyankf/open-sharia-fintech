---
description: Advisory (non-enforced) guidance to park long-lived work-in-progress on a refs/heads/wip/* branch instead of leaving it staged.
when_to_use: Use when work-in-progress would otherwise sit staged in a shared index for an extended period instead of on its own branch.
---

# Long-Lived WIP Belongs on a Branch, Not in the Index

This section is advisory prose, not an enforced rule. No checker, hook, wrapper, or tooling subcommand
is proposed for it, here or in any follow-up.

Long-lived work-in-progress should live on an ordinary `refs/heads/wip/*` branch rather than sitting
staged in the shared index of a repository other actors also work in. An ordinary branch under
`refs/heads/wip/` is remote-durable, attributable to whoever created it, diffable against `main` at
any time, and survives the loss of the machine it was created on — properties a purely local staging
area does not have.

Two facts explain why this is advisory rather than automated. First, no tool can see **how long**
content has been staged: `git diff --cached --exit-code` and `git status --porcelain` report state,
not duration. They can tell you that a path is staged, never when it was staged, so distinguishing
"staged five seconds ago" from "staged six weeks ago" would require bespoke tracking this repository
does not maintain. Second, the failure this rule prevents is recoverable, not catastrophic: content
that reached the index via `git add` survives even a `reset --hard` as a dangling blob, and
`git fsck --lost-found` writes such blobs back out within `gc.pruneExpire`'s default retention window
of `2.weeks.ago`.

A related warning belongs here plainly: an automated stash of a foreign actor's staged work is itself
a destructive operation against content that actor never asked to have moved, and the
[No Destructive Git Operations Convention](../no-destructive-git-operations.md) forbids exactly that
class of action. A guard built to protect long-lived WIP that instead stashes it out from under its
owner is not a safeguard.
