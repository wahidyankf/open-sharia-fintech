---
title: "Purpose, Scope, and Relationship to plan-takeover-execution.md"
description: What a handover captures, when (not) to write one, and how this write-side workflow relates to plan-takeover-execution.md's read side.
when_to_use: Use when deciding whether a handover is warranted, or clarifying how this workflow's output feeds the takeover workflow.
---

# Purpose, Scope, and Relationship to plan-takeover-execution.md

**Purpose**: Capture the state of an in-progress, multi-session, possibly-multi-repo plan into one
document before stepping away from it, so the next agent or session — which starts with none of this
session's context — can resume from fact rather than from re-discovery or guesswork.

**When to use**:

- Ending a session with plan work still in progress, whether by choice, a context/compaction boundary,
  or the user explicitly asking for a handover.
- Before an intentional pause the user has directed (e.g., "pause this phase"), so the pause carries
  forward its own reasoning instead of reading as an unexplained stop next time someone opens the plan.
- Any time a plan's execution is about to move to a different agent, a different session, or a
  different person, and prior context would otherwise be lost.

**When NOT to use**:

- The plan is fully complete — route it through Phase 9/10 (Knowledge Capture, Archival) instead; a
  finished plan needs an archive entry, not a resume document.
- The plan never started — there is no state to hand over; a fresh `plan-takeover-execution.md` run
  on a never-touched plan is already a no-op discovery, per that workflow's own "When NOT to use".

## Relationship to plan-takeover-execution.md (write side / read side)

This workflow is the **write-side counterpart** to
[`plan-takeover-execution.md`](../plan-takeover-execution.md)'s **read side**: that workflow's Phase
A0.5 checks `local-tmp/handovers/` for a document this workflow produces, using it as a fast, informal
lead that narrows and accelerates the git/`gh` ground-truth probes Phase A2 still runs in full — a
handover document is a hint, never a substitute for verification, since it can go stale the moment
another actor touches the same plan. Nothing here duplicates that workflow's discovery logic; this
workflow only produces the artifact it consumes.
