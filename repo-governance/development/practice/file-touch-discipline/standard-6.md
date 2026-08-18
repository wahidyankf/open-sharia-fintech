---
title: "File-Touch Discipline — Standard 6: Reconciling Before Commit"
description: Comparing the ledger against the working tree in both directions before staging, and the bounded read-only diagnosis obligation for large foreign change sets
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
when_to_use: Use immediately before staging or committing any change, and whenever a foreign change set looks unusually large or persistent.
---

# Standard 6: Reconciling Before Commit

## Standard 6 — Reconcile Ledger Against Tree Before Any Commit

Immediately before staging, run `git status --porcelain` and compare it against the ledger. The
comparison has two directions and both matter:

- **In the tree but not on your ledger** → another actor's work. Leave it untouched and unstaged.
  Do not investigate it by modifying it. This deferral is valid only while a plausible actor exists —
  see the diagnosis obligation below.
- **On your ledger but not in the tree** → your change is gone. Something reverted, overwrote, or
  checked out over it. Stop and find out what before proceeding; this is evidence of a concurrent
  actor operating on your paths.

State the delta explicitly rather than resolving it silently. A surprise in either direction is a
signal about the shared machine, not noise to be smoothed over.

**Bounded read-only diagnosis obligation.** Deferring to foreign tree state is not an unconditional
pass. Run a read-only identification pass and report a verdict — live work, or drift — before
deferring again, when any of these hold: the foreign set exceeds roughly 50 paths, it is unchanged
from a state a prior session already deferred to, or it blocks a gate you must pass. Permitted
commands are strictly read-only and never touch the foreign paths themselves: `git reflog`,
`git rev-list --left-right --count <ref>...<ref>`, `git diff --cached --stat`, and
`git ls-files --others`. If the pass finds the state is stale ref-advance drift rather than live work
(see [Bare-Repo Landing Method](../../workflow/bare-repo-landing-method/terminal-reconcile.md#terminal-reconcile)),
say so explicitly and escalate — do not keep deferring to it silently across sessions.
