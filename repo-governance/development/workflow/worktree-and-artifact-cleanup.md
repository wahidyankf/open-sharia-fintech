---
title: "Worktree and Artifact Cleanup Convention"
description: Mandatory plan-end gate requiring a plan to remove the worktrees, branches, and build artifacts it created — self-scoped, verified idle, and never touching shared caches other sessions depend on
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
---

# Worktree and Artifact Cleanup Convention

A plan that creates worktrees, branches, and build output must remove them when it finishes. This is
the **teardown** half of the worktree lifecycle; provisioning and toolchain initialization are covered
separately.

Cleanup is a **mandatory plan-end gate**, not a courtesy. It is also the one gate most likely to cause
harm if executed carelessly, because every action it takes is a deletion. The whole convention exists
to make that combination safe: delete thoroughly, delete only what is yours, and verify before each
removal.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Every
  action this gate takes is a deletion, and deletions are irreversible. The convention requires
  positively identifying ownership and idleness before each removal rather than sweeping broadly.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: A
  plan cleans up what it can positively account for having created — never what merely looks stale.
  Shared caches other sessions depend on are out of scope by rule, not by judgement call.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Cleanup is
  a fixed plan-end gate with a short, ordered checklist rather than a heuristic sweep, so its blast
  radius stays legible.

## Conventions Implemented/Respected

- **[No Destructive Git Operations Convention](./no-destructive-git-operations.md)**: The companion
  convention forbids the blunt removals (recursive clean, force delete, hard reset) that a careless
  cleanup would otherwise reach for; this gate prescribes the self-scoped, verified alternative.

- **[Worktree Toolchain Initialization](./worktree-setup.md)**: The provisioning half of the same
  worktree lifecycle. This convention is its teardown counterpart.

- **[Worktree Path Convention](../../conventions/structure/worktree-path.md)**: Cleanup depends on
  worktrees living at the conventional `worktrees/<name>/` path so ownership is determinable.

## Why This Is a Gate

On a shared machine, uncleaned artifacts are not a tidiness issue — they accumulate against a resource
everyone is using.

- **Disk.** Each worktree is a full checkout. A multi-phase plan under the 1-PR ↔ 1-worktree mapping
  creates one per phase per repo; several such plans in flight fill a disk that CI runners, builds,
  and every other agent share.
- **The ref namespace.** Removing a worktree leaves its branch behind. A plan that cleans worktrees but
  not refs still leaves stale local and remote branches on every repo it touched, and those
  accumulate permanently.
- **Stale state.** An idle worktree is indistinguishable, by path alone, from an active one. Every
  worktree left behind makes the next actor's "is this safe to remove?" judgment harder.

## The Three Artifact Classes

A complete cleanup covers all three. Stopping after the first is the common failure.

1. **Worktrees** — the working directories this plan created.
2. **Branches** — local and remote, merged-only. See [Branch Cleanup](#branch-cleanup).
3. **Build output** — `target/`, `dist/`, `.next/`, and build caches produced **inside this plan's own
   worktrees**.

## Hard Safety Rules

These bound every action the gate takes.

- **Self-created only.** Delete only what this plan created. Anything else requires positive evidence
  it is idle — not merely the absence of evidence that it is busy.
- **Verify not in use before deleting.** Check, then delete. When in doubt, leave it. An artifact left
  behind costs disk; an artifact wrongly deleted costs someone else's work.
- **Never delete a shared cache.** In particular, the **shared cargo `target/` directory** — the
  symlinked shared build output introduced by the
  [`rust-cargo-target-dir-sharing`](../../../plans/done/2026-07-19__rust-cargo-target-dir-sharing/)
  plan — is depended on by concurrent builds in every other worktree. Removing it breaks them. The
  same reasoning applies to any shared cache: if another session can be relying on it, it is out of
  scope for a plan-scoped cleanup.
- **Cleanup is itself non-destructive to others.** The gate may not use any operation that a
  concurrent actor could be harmed by. It removes; it never force-removes, rewrites, or prunes shared
  state.

## Mandatory Pre-Removal Checks

Run all five before any `git worktree remove`. Each is grounded in an observed incident, not a
hypothetical.

**1. Test merge state with `gh pr list`, never with ancestry.**

```bash
gh pr list --head <branch> --state all --json number,state,mergedAt
```

PRs in these repos are **squash**-merged, which replays the branch as one new commit. The branch's own
commits therefore never become ancestors of `main`, and `git merge-base --is-ancestor` reports
NOT-MERGED for **every** merged branch. Observed live: four worktree branches all reported NOT-MERGED
by ancestry while `gh` showed their PRs merged. Ancestry is not a conservative approximation here — it
is wrong in the direction that blocks correct cleanup, and it would be wrong in the dangerous
direction if anyone inverted it.

**2. Read the worktree's dirty diff before removing it.**

```bash
git -C <worktree> status --porcelain
```

A merged PR proves the _branch_ landed, not that the _working tree_ is empty. Archival record-keeping
in particular is written last — after the merge — and is easily left uncommitted. Observed live: a
worktree held its plan's two terminal archival checkboxes, ticked with real commit SHAs and a merge
timestamp, that existed **nowhere else**; every merge-state signal said "safe to delete". Recover such
content first, or discard it explicitly with a stated reason. Never discard it silently.

**3. Check for unpushed commits — work that exists nowhere but this machine.**

```bash
git -C <worktree> log origin/<branch>..<branch>
```

Any output is a commit that has never left this disk. Unlike checks 1 and 2, there is no remote copy
to fall back on: if the worktree goes, so does the commit.

**4. Always use non-force `git worktree remove`.**

Never `rm -rf` a worktree — that leaves orphaned administrative state behind. The non-force command
refuses on a dirty worktree, which is the backstop for when checks 1-3 were skipped or rushed.
Preserving that backstop is the entire reason force is forbidden here.

**5. Never remove a worktree this plan did not create** without positive evidence it is idle. On a
shared machine, another session's live work is indistinguishable from stale state by path alone.
Observed live: of 11 worktrees across three repos, one held five dirty files belonging to active work
and was correctly left in place.

## Branch Cleanup

Removing a worktree leaves its branch behind. Under the 1-PR ↔ 1-worktree mapping, a multi-phase plan
accumulates one branch per phase per repo — so a plan that cleans worktrees but not refs still leaves
stale local and remote branches on every repo it touched. Run this after each worktree removal.

**Delete only branches this plan created**, and only after the branch's PR is confirmed MERGED by the
same `gh pr list --head <branch> --state all --json number,state,mergedAt` test used in check 1.
Ancestry tests are useless here for the same squash-merge reason.

**Local deletion uses `git branch -d`** — never `git branch -D`. The merged-check that `-d` retains is
the point: it refuses on an unmerged branch, which is the intended backstop. If `-d` refuses on a
branch whose PR reports MERGED, that is the **squash-merge shape, not lost work** — confirm the
content landed with `git log origin/main..<branch>`, then delete with an explicit stated reason. Do
not reflexively reach for `-D`; force-deletion is on the forbidden-operations list precisely because
it silences the signal you would want in the case where the content genuinely had not landed.

**Remote deletion uses `git push origin --delete <branch>`**, only after the PR is MERGED, and only
for branches this plan pushed. **Never delete `main`, and never delete an environment branch.** Which
branches those are is **repo-specific**: `ose-public` defines `prod-*` and `stag-*`; `ose-primer` and
`ose-infra` currently define none, so the rule is vacuously satisfied there. Confirm each repo's own
set with `git branch -a` rather than assuming this pattern is universal — a plan that hardcodes one
repo's environment-branch shape will eventually run against a repo that does not match it.

**Jurisdiction note.** `git push origin --delete` is remote-ref deletion, not history-rewriting
force-push. It sits deliberately **outside** the per-instance-approval gate that covers
`--force` / `--force-with-lease` / hook bypass, and is instead safety-gated by **this convention's
own** merged-check requirement above. This convention is the single authority for remote branch
deletion; the local-side forbidden-operations table and the remote-side force-push convention both
defer here.

**Run `git worktree prune`** after removals so administrative worktree metadata does not accumulate.
It touches only already-removed entries and is safe alongside other sessions.

**Never `gc` or `prune` the object store** as part of cleanup. History maintenance is a serialization
point on a shared machine, and carries a documented corruption risk when another process is writing
concurrently. It stays out of the cleanup gate entirely.

## Build-Artifact Cleanup

Purge only the build output produced **inside this plan's own worktrees** — `target/`, `dist/`,
`.next/`, and build caches — after verifying non-use.

Explicitly **skip** the shared cargo `target/` and every other shared cache, and run **no** `git gc`
or `git prune` on the object store. History maintenance is a serialization point on a shared machine
and stays out of the cleanup gate entirely.

## Related Documentation

- [Worktree Toolchain Initialization](./worktree-setup.md) — the **setup** half of the same lifecycle.
  That convention provisions a worktree and converges its toolchain; this one tears it down. A plan
  touches both, at opposite ends.
- [Temporary Files Convention](../infra/temporary-files.md) — the build-artifact and temporary-file
  taxonomy this convention's third artifact class removes (`generated-reports/`, `local-temp/`, and
  build output).
- [No Destructive Git Operations Convention](./no-destructive-git-operations.md) — the forbidden-op
  set that bounds what this gate may do. `git branch -D`, `rm -rf` of a worktree, forced worktree
  removal, and object-store pruning are all forbidden there, which is why this convention prescribes
  `-d`, non-force removal, and no `gc`.
- [Git Push Safety Convention](./git-push-safety.md) — the remote-side companion. Note the boundary
  set out in the Jurisdiction note above: remote **branch deletion** is gated here by the merged-check,
  not there by the force-push approval gate.
- [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md) — the DAG model
  in which cleanup is the **terminal node**, depending on every delivery node so it cannot remove an
  artifact that in-flight work still needs.
