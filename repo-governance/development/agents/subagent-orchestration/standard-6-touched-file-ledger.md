---
title: "Standard 6 — Every Subagent Returns Its Touched-File Ledger"
description: "Defines the requirement that every subagent report the full list of files it touched."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when a subagent finishes a task and reports its results back to the orchestrator.
---

# Standard 6 — Every Subagent Returns Its Touched-File Ledger

A background subagent mutates files in a tree the orchestrator is not watching, and its context dies
when it returns. Whatever it touched and did not report is unattributable from that moment on.

Every subagent that can write MUST therefore return, as part of its result, the list of paths it
created, modified, deleted, or moved — see
[File-Touch Discipline](../../practice/file-touch-discipline.md).

The orchestrator's obligations on receipt:

- **Merge the returned ledgers explicitly** into its own. Do not assume a subagent touched only what
  its prompt named — agents legitimately touch more (a regenerated binding mirror, an index entry,
  a companion test) and illegitimately touch more when a prompt was ambiguous.
- **Treat a missing ledger as unknown, not empty.** A subagent that returned no file list has not
  told you it changed nothing; re-derive from its transcript before staging anything it may have hit.
- **Never resolve a conflict between two subagents' ledgers by picking one.** Two agents reporting
  the same path means they raced on it; read the file before committing it.

Under the N+1 model several agents write concurrently to the same shared disk, which is precisely the
condition that makes `git status` useless for attribution: it shows the union of all of them plus
whatever a human is doing in another worktree.
