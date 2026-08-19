---
title: "Iron Rules (Non-Negotiable) — Rules 6-11"
description: "States the remaining six non-negotiable execution rules: CI verification, thematic commits, manual assertions, progress streaming, resume reconciliation, and the file-touch ledger."
when_to_use: Use when checking execution against rules 6-11 of the hard, non-negotiable rules governing every execution step.
---

# Iron Rules (Non-Negotiable) — Rules 6-11

**Continues** [Iron Rules (Non-Negotiable) — Rules 1-5](./iron-rules-1-5.md).

1. **Post-Push CI Verification**: After every push, monitor ALL GitHub Actions workflows triggered by that push. Fix ALL failures (including preexisting). Do NOT proceed until CI is fully green.
2. **Thematic Commits**: Group related changes. Split different concerns. Follow Conventional Commits. Preexisting fixes get their own commits.
3. **Manual Behavioral Assertions**: After quality gates pass, use Playwright MCP for web UI verification and curl for API verification. Fix any broken behavior before proceeding.
4. **Progress Streaming (Observability)**: The live Task list is the user's monitoring window — keep it fresh in real time. Never run silent for more than one checkbox. After each phase completes, emit a one-line user-visible status: phase name, items ticked / total, files changed, any preexisting fixes.
5. **Resume Reconciliation (Disk Is Truth)**: When starting or re-entering execution, read delivery.md first. Rebuild the Task list from disk state. If in-memory tasks disagree with disk checkboxes, delete them and rebuild. Never trust in-memory state over disk.
6. **File-Touch Ledger — Survives Compaction**: These repos are edited constantly by other agents, engineers, and background processes, in other worktrees and on local `main`, while your plan runs. Keep an append-only record of every path you create, modify, delete, or move, and **reproduce it in full in every compaction, summary, and handoff** — it is a required section, never droppable detail. Before staging, reconcile it against `git status --porcelain` in both directions: anything in the tree but not on your ledger is another actor's in-flight work and stays untouched and unstaged — unless it trips the bounded read-only diagnosis obligation (large foreign set, unchanged since a prior deferral, or blocking a gate), in which case identify it before deferring again; anything on your ledger but missing from the tree means your change was overwritten — stop and find out why. `git status` is the union of everyone's work, never a report of yours. Without a ledger, assume NOTHING in the tree is yours: reconstruct from your transcript, or ask. A `.claude/` edit legitimately pulls generated `.opencode/`, `.codex/`, and `.agents/` mirrors into the same commit — those are yours, belong on the ledger, and MUST ship in that same commit, never a follow-up sync commit. See [File-Touch Discipline](../../../development/practice/file-touch-discipline.md).
