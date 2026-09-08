---
description: The first three ledger standards - open before the first mutation, append at the moment of mutation with a reason, and never reconstruct the ledger from the working tree
when_to_use: Use when starting a session that will mutate files, or when deciding what to write for each ledger entry.
---

# Standards 1-3: Opening and Building the Ledger

## Standard 1 — Open the Ledger Before the First Mutation

Before the first file is written, the agent MUST begin an explicit record of files it touches. Not
after the first edit, and not at commit time. A ledger begun late is a ledger with an unknown gap at
the front, and there is no way to tell how large that gap is.

## Standard 2 — Append at the Moment of the Mutation, With the Reason

Each entry records **the path**, **what was done to it** (created / modified / deleted / moved), and
**why** — a short phrase tying it to the task at hand. The reason is what makes the ledger auditable
later by someone who is not you.

The ledger is **append-only within a session**. Entries are never removed, because "I touched this
and then reverted it" is itself information a later reader needs.

## Standard 3 — Never Reconstruct the Ledger From the Working Tree

The ledger is built from **what you did**, never from what the tree shows. `git status`,
`git diff`, and `git stash list` all report the union of every actor's work and cannot distinguish
authorship. Deriving your ledger from them re-introduces exactly the error the ledger prevents, while
producing the _feeling_ of having verified something.

Legitimate sources for reconstruction, in order of preference: your own recorded ledger; your
session transcript; the harness task list. Not the tree.
