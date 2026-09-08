---
description: Every actor keeps a deliberate, append-only record of the files it touched, carries that record intact across context compaction, and treats every file not on the record as another actor's in-flight work
when_to_use: Use whenever you are about to mutate any file in a repository shared with other actors, and always before staging or committing changes.
---

# File-Touch Discipline

Keep a deliberate record of every file you touched. Carry it across context compaction. Treat every
file **not** on it as someone else's work in flight.

These repositories are **very active**: agents, engineers, and background processes edit them
constantly and simultaneously, across worktrees, feature branches, and local `main`. At any moment
the working tree holds a mixture of your changes and theirs, and nothing in the tree itself tells you
which is which. The [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md)
already says to stage "only the paths you can account for" — this practice defines what accounting
for a path actually requires.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: the
  ledger makes authorship explicit and durable instead of relying on a shrinking context window.
- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: recording
  a touch costs one line; reconstructing authorship afterwards ranges from expensive to impossible.
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: the root cause of
  committing another actor's work is an unmaintained record of authorship, not a careless git flag.

## Conventions Implemented/Respected

- **[No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md)**: owns
  the prohibitions; this practice supplies the precondition — which paths to name instead.
- **[Task List Discipline](../practice/task-list-discipline.md)**: the structural sibling — one tracks intended
  work, the other tracks touched work; keeping only one leaves you half-recoverable.
- **[Worktree and Artifact Cleanup](../workflow/worktree-and-artifact-cleanup.md)**: cleanup is the
  most dangerous moment for this failure, since it deliberately removes things.
- **[File Naming Convention](../../conventions/structure/file-naming.md)** and
  **[Content Quality Principles](../../conventions/writing/quality.md)**: this document follows both.

## Contents

- [Purpose and Scope](./file-touch-discipline/purpose-and-scope.md) — the three observed failure modes and what this practice covers.
- [Standards 1-3 — Opening and Building the Ledger](./file-touch-discipline/standards-1-to-3.md) — open before the first mutation, append with reason, never reconstruct from the tree.
- [Standards 4-5 — Carrying and Losing the Ledger](./file-touch-discipline/standards-4-to-5.md) — surviving compaction, and degraded mode when it doesn't.
- [Standard 6 — Reconciling Before Commit](./file-touch-discipline/standard-6.md) — comparing ledger against tree in both directions.
- [Standards 7-8 — Scope and Foreign Files](./file-touch-discipline/standards-7-to-8.md) — one ledger per (repository, worktree) pair; leave foreign files untouched.
- [Standard 9 — Generated Mirrors](./file-touch-discipline/standard-9.md) — mirrors belong on the ledger, in the same commit as their source.
- [Anti-Patterns — Ledger Integrity](./file-touch-discipline/anti-patterns-ledger-integrity.md) — blanket staging, diff-based reconstruction, tidying, trusting a clean worktree.
- [Anti-Patterns — Commit Hygiene](./file-touch-discipline/anti-patterns-commit-hygiene.md) — vague-prose ledgers, orphan sync commits, hand-editing a mirror.
- [Agent Checklist and Related Documentation](./file-touch-discipline/agent-checklist-and-related-docs.md) — nine-point summary and related conventions.
