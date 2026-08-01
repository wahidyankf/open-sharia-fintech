---
title: "File-Touch Discipline"
description: Every actor keeps a deliberate, append-only record of the files it touched, carries that record intact across context compaction, and treats every file not on the record as another actor's in-flight work
category: explanation
subcategory: development
tags:
  - git
  - safety
  - concurrency
  - ai-agents
  - compaction
  - discipline
created: 2026-08-01
---

# File-Touch Discipline

Keep a deliberate record of every file you touched. Carry it across context compaction. Treat every
file **not** on it as someone else's work in flight.

These repositories are **very active**. AI agents, software engineers, and background processes edit
them constantly and simultaneously — in worktrees, on feature branches, and on local `main`. At any
moment the working tree holds a mixture of your changes and theirs, and nothing in the tree itself
tells you which is which.

The [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md) already
says to stage "only the paths you can account for". This practice defines what **accounting for a
path** actually requires, because an instruction to act only on what you can account for is empty
until the accounting exists.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  "I think I edited that one" is implicit state held in a context window that shrinks, summarizes,
  and eventually drops it. The ledger makes authorship explicit and durable. This is the principle
  the practice exists to serve.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Recording
  a file at the moment you touch it costs one line. Reconstructing authorship afterwards — across a
  tree several actors have written to — ranges from expensive to impossible, and the failure is
  silent when you get it wrong.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: The root cause of
  committing another actor's work is not a careless git flag. It is an unmaintained record of
  authorship, which makes every downstream staging decision a guess. Blocking the flag treats the
  symptom; maintaining the record removes the cause.

## Conventions Implemented/Respected

- **[No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md)**: That
  convention owns the prohibitions — which verbs must never run, and the whole-tree-staging ban. This
  practice supplies the precondition those prohibitions depend on. The two are complementary and
  neither is sufficient alone: knowing that `git add -A` is forbidden does not tell you which paths
  to name instead.

- **[Task List Discipline](./task-list-discipline.md)**: The structural sibling. Both maintain an
  append-only session artifact that must survive compaction; one tracks _what you intend to do_, the
  other _what you have already touched_. An agent that keeps one and not the other is half-recoverable.

- **[Worktree and Artifact Cleanup](../workflow/worktree-and-artifact-cleanup.md)**: Cleanup is the
  single most dangerous moment for this failure, because it is the moment an agent deliberately
  removes things. The ledger is what distinguishes _your_ artifact from _theirs_.

- **[File Naming Convention](../../conventions/structure/file-naming.md)** and
  **[Content Quality Principles](../../conventions/writing/quality.md)**: This document follows both.

## Purpose

Three failure modes, each observed in this repository family rather than hypothesized.

1. **Compaction amnesia.** An agent edits eleven files, its context is compacted, and the summary
   preserves the _conclusions_ while dropping the _inventory_. The agent resumes, runs
   `git status`, sees fourteen modified files, and reasonably infers all fourteen are its own. Three
   belonged to a human who had a branch open in another worktree. This is the failure this practice
   exists for: the record is precisely the kind of detail summarization discards, because it reads
   like bookkeeping rather than substance.

2. **Misattributed dirty state.** `git status` reports the **union of every actor's work** in that
   tree. It is not, and has never been, a report of what you did. Treating it as one is the single
   most common route into the failure — and it feels like verification, which is what makes it
   dangerous.

3. **Tidying.** An agent notices a file that looks stray, unrelated, or half-finished and "cleans it
   up" — reverts it, deletes it, stashes it, or reformats it in passing. It was another actor's
   in-flight work. Uncommitted changes have no undo history; git cannot recover what was never
   committed.

## Scope

### What This Practice Covers

- **Every session, in every OSE repository** — `ose-public`, `ose-primer`, `ose-private`,
  `beaver-nest` — and in every location within them: worktrees, feature branches, and local `main`.
- **Every mutating operation**, not only git verbs: `Write`, `Edit`, file creation, `rm`, `mv`,
  formatter and codemod runs, generator output, and every git command that alters the working tree,
  the index, or the stash.
- **Delegated work.** A subagent's mutations belong on a ledger too — see Standard 7.

### What This Practice Does NOT Cover

- Read-only work. Reading, grepping, and browsing touch nothing and need no ledger.

Generated files are **not** exempt. A file a tool regenerates on your behalf is a file you touched,
one level removed — see Standard 9.

## Standards

### Standard 1 — Open the Ledger Before the First Mutation

Before the first file is written, the agent MUST begin an explicit record of files it touches. Not
after the first edit, and not at commit time. A ledger begun late is a ledger with an unknown gap at
the front, and there is no way to tell how large that gap is.

### Standard 2 — Append at the Moment of the Mutation, With the Reason

Each entry records **the path**, **what was done to it** (created / modified / deleted / moved), and
**why** — a short phrase tying it to the task at hand. The reason is what makes the ledger auditable
later by someone who is not you.

The ledger is **append-only within a session**. Entries are never removed, because "I touched this
and then reverted it" is itself information a later reader needs.

### Standard 3 — Never Reconstruct the Ledger From the Working Tree

The ledger is built from **what you did**, never from what the tree shows. `git status`,
`git diff`, and `git stash list` all report the union of every actor's work and cannot distinguish
authorship. Deriving your ledger from them re-introduces exactly the error the ledger prevents, while
producing the _feeling_ of having verified something.

Legitimate sources for reconstruction, in order of preference: your own recorded ledger; your
session transcript; the harness task list. Not the tree.

### Standard 4 — Carry the Ledger Through Compaction

**Any context compaction, summary, or handoff MUST reproduce the ledger in full.** It is not
droppable detail, and it is not compressible into "edited several governance files" — a summary at
that resolution is indistinguishable from having no ledger at all, because it cannot answer the only
question the ledger is for: _is this specific path mine?_

This applies identically to a summary written for a human, a handoff to another agent, and an
automatic context compaction. When writing any of them, the file inventory is a required section.

For long autonomous runs, materialize the ledger outside the context window — in the active plan's
`delivery.md`, or a scratch file under `local-temp/` — so that no summarization step can lose it.

### Standard 5 — Absent a Ledger, Nothing Is Yours

If the ledger did not survive — a fresh session, a compaction that dropped it, an interrupted
handoff — the agent is in **degraded mode** and MUST act accordingly:

1. Attempt reconstruction from the session transcript, which records the actual tool calls made.
2. Until reconstruction succeeds, treat **every** modified or untracked path in the tree as foreign.
3. Perform no staging, committing, reverting, stashing, cleaning, or deletion of any path whose
   authorship you cannot positively establish.
4. If reconstruction is impossible and the work must proceed, say so explicitly to the user and ask
   which paths are yours. Asking costs a turn; guessing can cost someone their afternoon.

The default is **deny**. Absence of evidence that a file is someone else's is not evidence that it is
yours.

### Standard 6 — Reconcile Ledger Against Tree Before Any Commit

Immediately before staging, run `git status --porcelain` and compare it against the ledger. The
comparison has two directions and both matter:

- **In the tree but not on your ledger** → another actor's work. Leave it untouched and unstaged.
  Do not investigate it by modifying it.
- **On your ledger but not in the tree** → your change is gone. Something reverted, overwrote, or
  checked out over it. Stop and find out what before proceeding; this is evidence of a concurrent
  actor operating on your paths.

State the delta explicitly rather than resolving it silently. A surprise in either direction is a
signal about the shared machine, not noise to be smoothed over.

### Standard 7 — The Ledger Is Scoped to a (Repository, Worktree) Pair

A ledger is valid for exactly one working tree in one repository. The same relative path in a
different worktree is a **different file** with a different authorship history.

Work spanning several repositories or worktrees keeps **one ledger per tree**, never a merged list.
Delegated agents each keep their own and return it as part of their result; the orchestrator merges
the returned ledgers explicitly and never assumes a subagent touched only what it was asked to touch.

### Standard 8 — Foreign Files Are Left Exactly As Found

A file that is not on your ledger gets **no action at all**: not staged, not reverted, not stashed,
not cleaned, not deleted, not reformatted, not "fixed while I was in there", not `git add`-ed
because it looked related.

This holds even when the file appears stray, broken, or obviously wrong. A file that looks abandoned
is frequently a colleague's work in progress, and a formatter run across a tree you do not own
produces a diff that is genuinely painful to disentangle.

If a foreign file is genuinely blocking your work, **say so and stop** — report the path, say why it
blocks you, and let the user decide. That is a two-line report against an unrecoverable loss.

### Standard 9 — Generated Mirrors Belong on the Ledger and in the Same Commit

`.claude/` is the **only** hand-authored harness surface. `.opencode/`, `.cursor/`, and `.amazonq/`
are generated from it mechanically. Editing one agent definition therefore modifies **four** files,
three of which you never opened — and all four are yours.

rhino-cli provides the generators, and this repository already automates them:

| Command                                     | npm wrapper                           | What it does                                                    |
| ------------------------------------------- | ------------------------------------- | --------------------------------------------------------------- |
| `rhino-cli harness bindings generate`       | `npm run generate:bindings`           | Regenerates every mirror from `.claude/`                        |
| `... generate --harness opencode`           | `npm run sync:agents`, `sync:skills`  | Regenerates one harness only                                    |
| `... generate --harness opencode --dry-run` | `npm run sync:dry-run`                | Previews without writing                                        |
| `rhino-cli harness sync validate`           | `npm run validate:sync`               | Fails on mirror drift, and on a stale `.opencode/skill*` mirror |
| `rhino-cli harness claude validate`         | `npm run validate:claude`             | Validates the `.claude/` sources themselves                     |
| `rhino-cli harness bindings validate`       | `npm run harness:bindings-validation` | Byte-parity guard against the emitter output                    |

**Pre-commit Step 3 runs `harness bindings generate` and auto-stages the result**, so in the normal
path the mirrors are committed for you. The obligations are therefore about the paths where that
automation does _not_ protect you:

1. **Put the mirrors on your ledger.** Auto-staged is not the same as unaccounted-for. When you edit
   `.claude/agents/foo.md`, three mirror paths enter your commit; they are yours, and Standard 6's
   reconcile must expect them rather than be surprised by them.
2. **Source and mirror land in the same commit — always.** Never split them into a follow-up "sync"
   commit. Any commit where a source and its mirror disagree is a broken tree for whoever checks out
   that SHA, and it makes the byte-parity guard fail for a reason unrelated to their own work.
3. **Never bypass the hook that generates them.** `--no-verify` skips Step 3, producing exactly that
   broken state. This is already forbidden by the
   [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md); the
   mirror drift is one of the concrete costs.
4. **Verify rather than assume.** `npm run validate:sync` is the check. Run it after any `.claude/`
   edit that you did not commit through the standard hook path — notably in bare-repo worktrees and
   any scripted commit.
5. **Never hand-edit a mirror.** An edit to `.opencode/`, `.cursor/`, or `.amazonq/` is overwritten
   by the next generate, silently. Fix the `.claude/` source and regenerate.

The same reasoning covers every other generated artifact — lockfiles, coverage manifests, emitted
spec stubs. Record the generating command, and let its declared outputs ride in the same commit.

## Anti-Patterns

### Post-Compaction Blanket Staging

**Problem**: After a compaction, the agent runs `git status`, sees a set of modified files, concludes
"this is my work from before the summary", and stages all of it.

**Why it fails**: The compaction dropped the inventory but not the confidence. The tree contains
other actors' changes and the agent has no way to tell — the inference feels sound and is unfalsifiable
from inside the tree.

**Fix**: Standard 4 keeps the inventory alive through the compaction. If it was already lost,
Standard 5 governs: degraded mode, default deny.

---

### Reconstructing Authorship From the Diff

**Problem**: The agent reads `git diff` and decides which hunks look like its own work based on style,
subject matter, or plausibility.

**Why it fails**: Two agents working from the same conventions in the same repository produce changes
that look identical in style and subject. Plausibility is not authorship, and the method fails most
often precisely where the repository is most active.

**Fix**: Standard 3 — the ledger comes from what you did, never from what the tree shows.

---

### Tidying the Tree

**Problem**: The agent encounters an untracked scratch file, a stray edit, or a half-finished change
and cleans it up in passing as a courtesy.

**Why it fails**: Uncommitted work has no recovery path. The courtesy is unrecoverable when wrong,
and the actor who lost the work usually discovers it much later, with no way to trace what happened.

**Fix**: Standard 8 — no action on foreign paths. Report and stop if genuinely blocked.

---

### Trusting a Clean-Looking Worktree

**Problem**: The PR merged, so the agent assumes the worktree is spent and removes it.

**Why it fails**: A merged PR says nothing about uncommitted files still sitting in that worktree —
evidence, notes, or a colleague's follow-up work that was never part of the PR.

**Fix**: Read the dirty state before removal, reconcile it against the ledger (Standard 6), and
recover anything foreign before the worktree is destroyed.

---

### The Ledger as Vague Prose

**Problem**: The record reads "updated the governance docs and synced the bindings."

**Why it fails**: It cannot answer the one question the ledger exists to answer — _is this specific
path mine?_ A ledger that does not resolve to paths is decoration.

**Fix**: Standard 2 — one entry per path, with the operation and the reason.

---

### The Orphan Sync Commit

**Problem**: The agent commits its `.claude/` edit, notices the regenerated mirrors afterwards, and
commits them separately as "chore: sync bindings".

**Why it fails**: The intermediate commit is a tree where a source and its generated mirror disagree.
Anyone who checks out that SHA — a bisect, a CI job, a colleague — gets an inconsistent harness
configuration, and the byte-parity guard fails there for reasons unrelated to their own work.

**Fix**: Standard 9 — source and mirror in one commit. The pre-commit hook already stages them
together; do not defeat it by committing narrowly and reconciling later.

---

### Hand-Editing a Generated Mirror

**Problem**: The agent needs a change in `.opencode/agents/foo.md` and edits that file directly.

**Why it fails**: The next `harness bindings generate` — which pre-commit runs automatically —
overwrites it silently. The change disappears with no error, and the time is spent twice.

**Fix**: Standard 9 — `.claude/` is the only hand-authored harness surface. Edit the source,
regenerate, and let the mirrors follow.

## For AI Agents

1. **Open the ledger before the first mutation** — not at commit time.
2. **Append every path as you touch it**, with the operation and a one-phrase reason.
3. **Reproduce the ledger in full in every summary, compaction, and handoff** — it is a required
   section, never droppable detail.
4. **Never derive the ledger from `git status` or `git diff`** — those are the union of all actors.
5. **Reconcile ledger against tree before staging**, and state the delta in both directions.
6. **Stage explicit paths only**, per the
   [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md).
7. **Leave foreign paths untouched** — report and stop rather than resolving them yourself.
8. **Without a ledger, assume nothing is yours** — reconstruct from the transcript, or ask.
9. **Count generated mirrors as yours** — a `.claude/` edit produces `.opencode/`, `.cursor/`, and
   `.amazonq/` changes that belong on your ledger and in the same commit; regenerate with
   `npm run generate:bindings`, verify with `npm run validate:sync`, and never hand-edit a mirror.

## Related Documentation

- [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md) — the
  prohibitions this practice supplies the precondition for, including the whole-tree-staging ban
- [Task List Discipline](./task-list-discipline.md) — the structural sibling; the same
  append-and-survive-compaction shape applied to intended work
- [Worktree and Artifact Cleanup](../workflow/worktree-and-artifact-cleanup.md) — cleanup is where
  this failure is most costly
- [Subagent Orchestration Convention](../agents/subagent-orchestration.md) — delegated agents each
  return their own ledger
- [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md) — the
  same-machine assumption this practice operationalizes
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — the
  governing principle
