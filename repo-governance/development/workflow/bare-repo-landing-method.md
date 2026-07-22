---
title: "Bare-Repo Base-Worktree Landing Method"
description: Defines the base-worktree procedure for landing changes into a repository with no primary checkout, including the mandatory topology verification, the seven-step landing sequence, the topology-keyed terminal reconcile that closes the silent local-main lag defect, the one-landing-path-per-unit-of-work rule, and advisory guidance for parking long-lived WIP
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - bare-repo
  - safety
created: 2026-07-21
---

# Bare-Repo Base-Worktree Landing Method

This document defines the **bare-repo git-ops method**: the procedure for landing changes into a
repository that has no primary checkout, and for closing the silent lag that a landing performed from
a side worktree can leave behind in local `main`. Two repositories in this project's ecosystem —
`ose-primer` and `ose-infra` — are bare (`core.bare=true`) today; any repository that later adopts the
same shape needs the identical procedure.

## Principles Implemented/Respected

This procedure implements/respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: the method
  is a fixed, ordered sequence rather than an improvised set of commands chosen per instance — every
  step exists because skipping it has produced an observed failure.
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: the terminal
  reconcile step closes the actual cause of the local-`main`-lag defect (a push that never updates the
  pushing checkout's own branch), rather than treating the symptom — a stale local `main` — as
  unavoidable.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  topology is verified with a named command before any mutation, never assumed from a repository's
  name or from memory of what it was last time.

## Conventions Implemented/Respected

This procedure implements/respects the following conventions:

- **[No Destructive Git Operations Convention](./no-destructive-git-operations.md)**: every step below
  uses a non-destructive equivalent — `git worktree remove` without `--force`, `git merge --ff-only`
  in place of a reset, `git fetch origin main:main` in place of a forced ref overwrite.
- **[Worktree and Artifact Cleanup Convention](./worktree-and-artifact-cleanup.md)**: the method's
  worktree-removal step feeds directly into that convention's mandatory plan-end cleanup gate; this
  document does not restate the five pre-removal checks there, it precedes them.
- **[Worktree Toolchain Initialization](./worktree-setup.md)**: the worktree this method creates needs
  the same two-step `npm install` / `npm run doctor -- --fix` initialization as any other worktree in
  this repository.

## When This Applies

Use this method whenever either condition holds:

- The target repository has **no primary checkout** — a bare repository (`core.bare=true`), which
  today means `ose-primer` or `ose-infra`. Every mutation there must flow through a linked worktree,
  because there is no other tree to work in.
- A landing is performed **from a side worktree rather than from the branch's own checkout**, even in
  a non-bare repository such as `ose-public`. The side worktree's push reaches the remote branch, but
  nothing about that push touches the local `main` sitting in the repository's own primary checkout —
  the same lag this method exists to close.

## Verify Topology First

Ask "is this repository bare, or does it have a work tree?" before doing anything else. Two checks
answer it, with different provenance, and one command is forbidden for this question entirely.

### Primary / human check — `git worktree list`

```console
$ git worktree list
/Users/wkf/ose-projects/ose-primer  (bare)
```

The `(bare)` marker on the entry for the repository's common directory is **upstream-prescribed**:
`git-worktree(1)` §LIST OUTPUT FORMAT documents this exact output shape. Read this first, and read it
with your own eyes when a human is present — it is the least interpretation-dependent signal
available.

### Scriptable form — the `core.bare` read

```bash
git config --file "$(git rev-parse --git-common-dir)/config" core.bare
```

This form is **derived from documented mechanics, not upstream-prescribed** — git does not publish it
as a bareness API. `git-worktree(1)` documents where `core.bare` lives (the common config file) and
which worktree it governs (the main worktree only); reading it as a bareness test is a defensible
inference from that documentation, not a quotation of it. Label the form this way wherever it appears,
so a later reader does not mistake a derived recipe for a prescribed one.

### The forbidden command — never `git rev-parse --is-bare-repository`

`git rev-parse --is-bare-repository` must never be used to answer "is this repository bare." This is
**documented scoping semantics, to be worked around by asking the right question** — the command
answers a narrower, different question correctly: "is _this checkout_ bare." `git-worktree(1)`
§CONFIGURATION FILE states that when `core.bare` lives in the common config file, "they will be
applied to the main worktree only." A linked worktree is by design never bare, so
`--is-bare-repository` returns `false` from inside one even when the repository's main worktree is
bare — exactly as documented, not as an anomaly.

One source in general circulation gets this wrong by omission:
<https://www.gitworktree.org/troubleshooting/must-be-run-in-work-tree> recommends
`git rev-parse --is-bare-repository` as a general bareness diagnostic without addressing the
linked-worktree scoping caveat above. Treat it as a **known-bad counter-source** for this specific
question, not as a corroborating reference.

## The Method, As Numbered Steps

1. **Verify topology first** (see [Verify Topology First](#verify-topology-first) above).
2. `git fetch origin` — refresh remote-tracking refs before creating anything from them.
3. `git worktree add <path> origin/main` — create a linked worktree at the verified, up-to-date tip.
4. **Re-apply the delta and commit** inside that worktree, exactly as any other worktree-based change.
5. **Run local quality gates** in the worktree — typecheck, lint, `test:quick`, `specs:coverage`, and
   the markdown gates where the change touches markdown.
6. `git push origin HEAD:main` — push the worktree's branch tip directly onto the remote `main` ref.
   This is the **direct-push** landing path. When the unit of work instead lands through a branch and
   a pull request, this step becomes the PR's own push-and-merge, and step 7 needs the branch cleanup
   below before it runs.
7. `git worktree remove <path>` — remove the worktree non-destructively, never with `--force` and
   never `rm -rf`, per the
   [No Destructive Git Operations Convention](./no-destructive-git-operations.md). If step 6 was a
   branch-and-pull-request landing rather than a direct push, delete the merged remote branch
   **before** running this step — see
   [Remote-Branch Cleanup in a Bare Repository](#remote-branch-cleanup-in-a-bare-repository). This
   step's worktree removal is exactly what triggers the ordering trap that section closes.
8. **Reconcile local `main`** — the step most often missing in practice. See
   [Terminal Reconcile](#terminal-reconcile) for the exact command, keyed by topology.

## Terminal Reconcile

Step 8 above is not optional, and its command depends on whether the repository being reconciled has
a work tree at all.

| Topology            | Reconcile command                                  | Why this form                                                                                                                                                                                                                                                                         |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bare (no work tree) | `git fetch origin main:main`                       | Requires no work tree to run. `git-fetch(1)` fast-forward-checks the destination ref by default and refuses a non-fast-forward update unless the refspec carries a leading `+` — the same safety property `--ff-only` provides, delivered by a command a bare repository can execute. |
| Has a work tree     | `git fetch` then `git merge --ff-only origin/main` | `git-merge(1)` documents `--ff-only`: resolve the merge as a fast-forward when possible, and **refuse to merge and exit with a non-zero status** when it is not. This remains git's own idiom wherever a work tree exists, and is unchanged by this document.                         |

### Why `merge --ff-only` cannot run in the bare siblings

```console
$ git -C ose-primer worktree list
/Users/wkf/ose-projects/ose-primer  (bare)

$ git -C ose-primer merge --ff-only origin/main
fatal: this operation must be run in a work tree

$ git -C ose-primer status --porcelain
fatal: this operation must be run in a work tree

$ git -C ose-primer fetch origin main:main
```

Unlike the two commands above, this one exits `0` with no error — the point of this example.

**What it prints depends on whether the shell is RTK-wrapped**, so read the transcript accordingly.
Under plain `git`, a `fetch` that finds nothing new (the ref is already at that tip) prints nothing
at all, which is why no output line is shown above. Under this repo's RTK wrapper — where a hook
rewrites every `git` invocation to `rtk git` — the same command instead prints a filtered summary
line such as `ok fetched (1 new refs)`, and it prints that line **unconditionally**, including on a
genuine no-op. To see the underlying `From <url> … -> FETCH_HEAD` form, run it through
`rtk proxy git fetch …`.

Do not treat an `ok fetched` line in a transcript as fabricated evidence: it is the literal RTK
output an agent sees in this repo. See the worked example below for the same command against a ref
that genuinely has new commits to pull.

`git merge` requires a work tree unconditionally; a bare repository has none. The refspec fetch form
is the only one of the two idioms that runs in both topologies, which is why the table above keys on
topology rather than offering one universal command.

### Worked example — the 2026-07-21 sibling drift

Both `ose-primer` and `ose-infra` were found in exactly the state this method exists to close, on the
same day this document was written:

```console
$ git -C ose-primer rev-list --left-right --count origin/main...main
2 0
$ git -C ose-infra rev-list --left-right --count origin/main...main
2 0
```

Local `main` was **two commits behind** `origin/main` in both repositories. Neither repository's own
history was wrong — the commits had genuinely reached `origin/main` through prior side-worktree
landings — but no command in either landing had ever touched the repository's own `main` ref, because
a push from a linked worktree updates only the remote and that worktree's own branch, never a
same-named local branch sitting elsewhere. The bare-repo reconcile closed the gap in both:

```console
$ git -C ose-primer fetch origin main:main
72640e287..53d9081b7  main       -> main
$ git -C ose-primer rev-list --left-right --count origin/main...main
0 0

$ git -C ose-infra fetch origin main:main
fe4a0a66e..f6ecdcc0b  main       -> main
$ git -C ose-infra rev-list --left-right --count origin/main...main
0 0
```

No command failed and nothing warned during the original landings — the lag was entirely silent, which
is exactly why step 8 is a fixed part of the numbered method rather than a step performed only when
something looks wrong.

### Measure after fetching, never before

`git rev-list --left-right --count origin/main...main` compares two **local** refs: `main` and the
remote-tracking ref `refs/remotes/origin/main`. It performs no network access. Run before any fetch,
it therefore reports the relationship between two refs that may both be equally stale, and the
answer it gives is `0 0` — indistinguishable from a genuinely reconciled repository.

That false clean is not hypothetical. Immediately after a merge landed on the remote, this sequence
was observed in a bare sibling:

```console
$ git -C ose-infra rev-list --left-right --count origin/main...main
0 0

$ git -C ose-infra fetch origin
$ git -C ose-infra rev-list --left-right --count origin/main...main
1 0

$ git -C ose-infra fetch origin main:main
$ git -C ose-infra rev-list --left-right --count origin/main...main
0 0
```

The first reading and the last are byte-identical, and only one of them means what it appears to
mean. **Always refresh the remote-tracking ref before measuring** — either with a preceding
`git fetch origin`, or by reading the count only after the reconcile command itself has run. (This
transcript demonstrates the false-clean problem, not the claim below on its own: the plain
`git fetch origin` shown above already refreshed `origin/main` before `git fetch origin main:main`
ran, so the final `0 0` here is equally consistent with `main:main` having updated only `main` — the
ref that was actually behind — and leaving the already-current `origin/main` untouched.)

Separately, as a documented git behavior rather than something this transcript isolates:
`git fetch origin main:main` does update both `main` and `refs/remotes/origin/main` — but the
`origin/main` half is git's **opportunistic remote-tracking update**, which fires only when the
remote's standard `remote.origin.fetch` refspec is configured, as it is for every repository this
document addresses. That update is not intrinsic to the `main:main` refspec itself: a bare repository
cloned without that standard refspec (for example, a plain `git clone --bare`) has no `origin/main`
ref at all. There, the fetch still **succeeds** — it updates `main` and prints an ordinary update
line — and it is the measurement afterwards that fails loudly, with
`fatal: ambiguous argument 'origin/main...main'`. That failure is the good case: it is the one shape
of this problem that cannot pass silently. Treat any left-right count taken before a fetch as no
evidence at all.

## Remote-Branch Cleanup in a Bare Repository

When a unit of work lands through a branch and a pull request rather than through this document's
direct `git push origin HEAD:main`, the merged remote branch still has to be deleted. In a bare
repository the obvious command does not work, and the reason has nothing to do with the branch:

```console
$ git -C ose-primer push origin --delete <branch>
NX  Command failed: git diff --name-only --no-renames --relative HEAD .
fatal: this operation must be run in a work tree
husky - pre-push script failed (code 1)
error: failed to push some refs
```

The `pre-push` hook runs `nx affected`, which shells out to a work-tree operation. A bare repository
has none, so **every** push originating from it fails — including a pure ref deletion that carries
no content and could not fail a quality gate even in principle.

Two routes work. Either delete the branch **from inside the linked worktree, before removing it**,
while a work tree still exists for the hook to run in; or delete the ref through the forge's API
after the worktree is gone:

```console
gh api -X DELETE /repos/<owner>/<repo>/git/refs/heads/<branch>
```

That API call is the same path `gh pr merge --delete-branch` takes natively, so no hook is bypassed
and nothing is force-pushed. Note the ordering trap: this document's own step order removes the
worktree before cleanup would typically happen, which leaves the bare repository — the one actor
that cannot push — as the only one remaining.

**`--no-verify` is not the sanctioned answer here.** It is the obvious workaround, and the
[Git Push Safety Convention](./git-push-safety.md) requires explicit per-instance user approval for
it. A rule that is unexecutable as written pushes its reader toward exactly the escape hatch that
needs permission; both routes above avoid that.

## Reading a File From Another Repository

This method is frequently used to propagate a change across sibling repositories, which means
reading a file out of one repository while standing in another. Address it by **git ref, never by
working-tree path**, and fetch immediately before the read:

```console
git -C <other-repo> fetch origin
git -C <other-repo> show origin/main:<path>
```

A working-tree path such as `<other-repo>/<path>` resolves against whatever that checkout happens to
contain right now. On a shared machine that is not a safe assumption: another session may have left
its local `main` behind `origin/main` — the very defect this document exists to close — in which case
the file may be stale, or may not exist at all. The ref form fixes exactly that problem: it does not
depend on a working tree being reconciled at all, and it is the only form that works when the source
repository is bare and has no working tree to path into.

What the ref form does **not** fix is staleness of the remote-tracking ref itself. `origin/main` —
`refs/remotes/origin/main` — is a purely local ref, the same class of ref
[Measure after fetching, never before](#measure-after-fetching-never-before) above warns about:
`git show origin/main:<path>` performs no network access, so it returns whatever `<other-repo>` last
fetched, silently, with no error if that content is stale or the change is entirely missing from it.
The drift is not always the direction that section's example shows, either — it can just as easily be
that another session pushed to the shared remote and `<other-repo>`'s own `origin/main` has not caught
up yet, rather than `<other-repo>`'s local `main` lagging behind its own `origin/main`. Treat this read
under the same discipline as that section's `rev-list` measurement: **always fetch in `<other-repo>`
immediately before the `show`**, as the two-line recipe above does, never rely on a ref that was
fetched at some earlier, unknown time. This is why the read across sibling repositories for a
byte-identity check must be a fetch-then-show pair, not the `show` alone.

## One Landing Path Per Unit Of Work

Choose exactly one landing path for a given unit of work: through the worktree described above — step
6's direct push, or its branch-and-pull-request variant — **or** through an already-reconciled local
`main`. **Never both.** Applying the same delta through both paths produces a duplicate, stale-base
commit — the second landing carries a parent that the first landing's push has already superseded, and
the two histories then diverge instead of one simply following the other.

The duplicate-commit failure is the sharper-edged sibling of the silent-lag defect the worked example
above shows: that example left local `main` two commits behind with no divergence, because nothing
was re-landed against the stale base. Re-landing against a stale base is what turns a merely-behind
`main` into a **diverged** one, which the topology-keyed reconcile above cannot repair with a
fast-forward — recovery then requires the kind of manual, per-instance judgment this method exists to
make unnecessary.

## Long-Lived WIP Belongs on a Branch, Not in the Index

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
[No Destructive Git Operations Convention](./no-destructive-git-operations.md) forbids exactly that
class of action. A guard built to protect long-lived WIP that instead stashes it out from under its
owner is not a safeguard.

## Why There Is No Guard

No automated guard enforces the terminal reconcile step, and this section states why, so a future
reader does not propose one without first reading this.

Git ships **no `post-push` client hook**. The full enumerated hook list in `githooks(5)` has no entry
by that name. The nearest primitive, `pre-push`, fires **before** the transfer completes and therefore
cannot observe the state a push leaves behind. Background maintenance does not fill the gap either:
`git maintenance`'s `prefetch` task writes to a separate `refs/prefetch/*` namespace and never updates
`refs/remotes/origin/*`, so no maintenance task would trigger a guard even if one existed to trigger.

The consequence is direct: any future lag guard is necessarily a **wrapper script, never a hook** —
there is no git-native extension point this defect can attach to. If such a guard is ever built, it
has a documented starting primitive: `git status --porcelain=v2 --branch` emits a `# branch.ab` line
showing ahead/behind counts, but it does not run in a bare repository. A portable detector would
instead use `git rev-list --left-right --count origin/main...main`, the same command this document
uses throughout to show the defect and its resolution.

## Related Documentation

- [No Destructive Git Operations Convention](./no-destructive-git-operations.md) — the safety
  guarantees this method's every step is built to satisfy; that convention links back here as the
  procedure it supplies those guarantees to.
- [Worktree and Artifact Cleanup Convention](./worktree-and-artifact-cleanup.md) — the teardown gate
  that governs everything after this method's `git worktree remove` step.
- [Git Push Safety Convention](./git-push-safety.md) — the remote-side companion covering force-push
  and hook-bypass approval; this method's `git push origin HEAD:main` step is an ordinary,
  non-force push and does not require that approval.
- [Worktree Toolchain Initialization](./worktree-setup.md) — the mandatory two-step init this method's
  worktree requires before step 4 can run.
- [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md) — the worktree-agnostic
  execution rule this method's topology check refines.
