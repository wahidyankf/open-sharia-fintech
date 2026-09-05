---
title: "File-Touch Discipline — Standards 4-5: Carrying and Losing the Ledger"
description: How the ledger survives context compaction and handoffs, and the degraded-mode default-deny behaviour required when it does not survive
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
when_to_use: Use when writing a compaction summary or handoff, or when resuming a session and the ledger appears to be missing.
---

# Standards 4-5: Carrying and Losing the Ledger

## Standard 4 — Carry the Ledger Through Compaction

**Any context compaction, summary, or handoff MUST reproduce the ledger in full.** It is not
droppable detail, and it is not compressible into "edited several governance files" — a summary at
that resolution is indistinguishable from having no ledger at all, because it cannot answer the only
question the ledger is for: _is this specific path mine?_

This applies identically to a summary written for a human, a handoff to another agent, and an
automatic context compaction. When writing any of them, the file inventory is a required section.

For long autonomous runs, materialize the ledger outside the context window — in the active plan's
`delivery.md`, or a scratch file under `local-tmp/` — so that no summarization step can lose it.

## Standard 5 — Absent a Ledger, Nothing Is Yours

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
