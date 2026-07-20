---
title: "No Destructive Git Operations Convention"
description: Forbids local destructive and irreversible git operations that can discard a concurrent actor's uncommitted work on a shared machine, and prescribes the non-destructive equivalent for each
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - worktree
  - parallelism
created: 2026-07-20
---

# No Destructive Git Operations Convention

This convention governs **local** git operations that destroy data or rewrite shared state. Its
companion, the [Git Push Safety Convention](./git-push-safety.md), owns the **remote** side —
force-push and hook-bypass approval. Together they cover both directions; neither is sufficient alone.

## The Same-Machine Assumption

Assume the repository is **very active** and that other AI agents, software engineers, and background
processes are working **simultaneously on the same physical machine** — sharing its disk, its git
object database, its refs, its worktrees, and its self-hosted CI runners.

That assumption is what makes these operations dangerous rather than merely blunt. A hard reset in a
solo checkout costs you your own uncommitted work. The same command on a shared machine can discard
work that belongs to someone who never consented to the operation and has no way to recover it — git
keeps no undo history for changes that were never committed.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Every
  operation listed below is irreversible or rewrites state others depend on. The convention prefers
  reversible moves and requires a deliberate, per-instance decision before an irreversible one.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Reaching for a
  hard reset, a force delete, or a recursive clean is nearly always a symptom — a diverged branch, a
  failing gate, a confused working tree. The convention redirects to the cause instead of normalizing
  the destructive shortcut.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  "Nobody else is working right now" is an implicit assumption an agent cannot verify. The convention
  replaces it with explicit scoping: operate on paths and worktrees you can positively account for.

## Conventions Implemented/Respected

- **[Git Push Safety Convention](./git-push-safety.md)**: The remote-side companion. Force-push and
  hook-bypass operations require explicit, fresh, per-instance user approval there; this convention
  applies the same standard to local destruction.

- **[Worktree Toolchain Initialization](./worktree-setup.md)**: Establishes the worktree as the unit
  of isolation. This convention states what must never be done to a worktree that is not your own.

## Forbidden Operations

Forbidden without explicit per-instance approval. Grouped by what they destroy.

| Operation                                                          | What it destroys                                                | Use instead                                                 |
| ------------------------------------------------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------- |
| `git push --force` (bare)                                          | Others' commits on the remote tip                               | `--force-with-lease=<ref>:<expect>` + `--force-if-includes` |
| `git push --force-with-lease` (bare, no expected value)            | Same, when the local fetch is stale                             | The explicit `=<ref>:<expect>` form                         |
| `git rebase` / `git commit --amend` of **published** commits       | Downstream contributors' history                                | `git revert` (a new inverse commit)                         |
| `git filter-repo` / `git filter-branch`                            | All history, for everyone                                       | Scoped revert; coordinate out-of-band                       |
| `git reset --hard`                                                 | Uncommitted work, irrecoverably                                 | `git stash push` (keep, never drop), or commit first        |
| `git clean -fd` / `-fdx`                                           | Untracked files recursively, including ignored build output     | `git clean -n` to preview; delete named paths               |
| `git stash drop` / `git stash clear`                               | Stash entries, which then become prunable                       | Leave entries; they cost nothing                            |
| `git branch -D`                                                    | A branch, skipping the merged-check                             | `git branch -d` (merged-check retained)                     |
| `git reflog expire --expire=now --all` + `git gc --prune=now`      | The recovery path itself, plus concurrent-write corruption risk | Let git's automatic maintenance run                         |
| `git worktree remove --force --force`                              | Another actor's working tree and its uncommitted contents       | Non-force `git worktree remove`                             |
| `rm -rf <worktree>`                                                | The worktree, leaving orphaned administrative state behind      | `git worktree remove`; `git worktree repair` if moved       |
| `git checkout -- <path>` / `git restore <path>` over unstaged work | Unstaged edits at those paths                                   | Commit or stash first, then restore                         |

Two behaviors deserve their own statement because they are easy to misread as safe:

- **Bare `--force-with-lease` is not the safe form.** The lease is checked against whatever the local
  ref says, so a stale fetch can satisfy it. Per
  [git-push(1)](https://git-scm.com/docs/git-push), supplying the option without an expected value
  "interacts very badly with anything that implicitly runs `git fetch` … this is trivially defeated if
  some background process is updating refs in the background" — precisely the shared-machine case.
- **`--prune=now` is documented as corruption-risking under concurrency.** Per
  [git-gc(1)](https://git-scm.com/docs/git-gc), running gc concurrently with another process "may
  corrupt the repository if the other process later adds a reference to the deleted object."

## Cross-Worktree Facts

Git already enforces much of this. State the mechanics so agents cooperate with the tool rather than
fighting it.

- The **object database and `refs/*` are shared** across all worktrees; **`HEAD` and the index are
  per-worktree**. Concurrent checkouts of _different_ branches therefore do not collide by design —
  isolation is real, and does not need to be manufactured.
- Git **already refuses** to check out a branch that is active in another worktree. Note the exact
  mechanism: bare `-f` / `--force` does **not** bypass this guard, but a dedicated
  `--ignore-other-worktrees` flag exists that does. **Do not pass it.**
- Because the object store and refs are shared, `gc`, aggressive pruning, and forced worktree removal
  can affect state another worktree depends on **even though the working trees are isolated**.

## Whole-Tree Staging Is Forbidden

Stage **explicit paths only**. On a shared machine another actor's uncommitted work, scratch files,
and half-finished edits sit in the same tree. A whole-tree stage sweeps them into _your_ commit —
both a correctness bug (your commit now contains changes you did not author and cannot defend in
review) and a disclosure risk (it is how an unrelated credential-adjacent or scratch file gets
committed by accident, into a history that is permanent).

The rule is therefore stated as a **shape**, not as one flag spelling. Blocking `-A` alone would just
redirect the habit to the next spelling. All of the following are forbidden without explicit
per-instance approval:

- `git add -A` and its long form `git add --all`
- `git add .` — and any bare-directory add that pulls in paths you did not author
- `git add -u` / `--update` across the whole tree
- `git commit -a` / `--all`, which stages every tracked modification implicitly
- any wrapper, alias, or agent shortcut whose net effect is "stage everything"

**Required instead:**

1. Run `git status --porcelain` **first** and read every line.
2. Stage only the paths you can account for: `git add <path> [<path>...]`. Anything you cannot
   account for belongs to another actor and stays unstaged.
3. In a sibling repo or another worktree, use the `-C <worktree>` form —
   `git -C <worktree> add <path>` — so the operation cannot leak into the wrong tree.

The cost is a few named paths. The failure it prevents is committing someone else's work, or a
secret, into a history that cannot be rewritten without coordinating with everyone who has pulled it.

## No Corner-Cutting — Root-Cause Orientation Is Binding

Under parallel execution the cheapest way to make a gate go green is to weaken the gate. When a gate,
test, lint, type-check, or CI job fails, **fix the cause, never the signal**.

Forbidden without explicit per-instance approval **and** a written reason recorded in the plan:

- bypassing hooks (`--no-verify`) or skipping a declared quality gate
- deleting, skipping, `.only`-narrowing, or loosening a failing test instead of fixing the code
- weakening an acceptance criterion, threshold, or lint rule so a failing check passes
- ticking a delivery checkbox without the evidence its acceptance criterion demands
- suppressing an error — a broad catch, an ignore-comment, a silenced warning — in place of a fix
- deferring a discovered preexisting failure instead of fixing it in-scope

A blocker that genuinely cannot be root-caused within scope is **escalated and recorded** — named in
the plan, with what was tried and why it is out of scope — never silently worked around. Escalating is
a legitimate outcome; quietly routing around is not.

The distinction that matters: each item above makes the _report_ green without making the _system_
correct. A suppressed error still fires in production; a narrowed test still leaves the untested path
broken; an unticked-but-ticked checkbox transfers a false completion signal to whoever reads the plan
next. On a shared machine that false signal is what another actor builds on.

## Prefer Additive, Own-Worktree Operations

Two habits prevent most of the above from ever arising:

- **Additive over destructive.** A new commit that reverses a change is recoverable; a rewrite that
  erases it is not. When both reach the same end state, take the one that leaves a trail.
- **Your own worktree only.** Operate within the worktree this unit of work created. Acting on a
  worktree you did not create requires positive evidence it is idle — not the absence of evidence
  that it is busy.

Before a long unattended run, `git worktree lock --reason=<why>` makes the intent legible to whoever
looks next. Before any bulk delete, `-n` / `--dry-run` costs nothing.

## Related Documentation

- [Git Push Safety Convention](./git-push-safety.md) — the remote-side companion (force-push,
  hook bypass, per-instance approval)
- [Worktree Toolchain Initialization](./worktree-setup.md) — worktree provisioning and setup
- [Commit Message Convention](./commit-messages.md) — Conventional Commits format
- [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md) — the N+1
  model and the same-machine assumption this convention protects
