---
name: plan-handover-execution
title: "plan-handover-execution"
description: Writes a structured handover document capturing an in-progress plan's state for the next agent, session, or human.
when_to_use: Use when stepping away from an in-progress plan and prior session context would otherwise be lost.
goal: Given an in-progress plan and the current session's execution state, write a structured handover document capturing enough context for a different agent, session, or human to resume the plan without re-discovering already-known state or re-learning the same gotchas
termination: The handover document is written to local-tmp/handovers/, is non-empty, names the plan-identifier and current per-repo state, and its path has been reported back
inputs:
  - name: plan-path
    type: string
    description: Path to the plan folder (in plans/backlog/, plans/in-progress/, or plans/done/) in the current repo, or a bare plan-identifier slug.
    required: true
  - name: date
    type: string
    description: "ISO date (YYYY-MM-DD) to stamp the handover filename with. Defaults to the current date."
    required: false
outputs:
  - name: handover-doc
    type: file
    pattern: local-tmp/handovers/*__*-implementation.md
    default: local-tmp/handovers/<date>__<plan-identifier>-implementation.md
    description: The written handover document. Default filename/folder is `local-tmp/handovers/<date>__<plan-identifier>-implementation.md` — the exact same default `plan-takeover-execution.md`'s Phase A0.5 looks up (see its frontmatter `inputs`/discovery-path note); keep both in sync if this default ever changes.
---

# Plan Handover Execution Workflow

Captures an in-progress, multi-session, possibly-multi-repo plan's state into one document before
stepping away, so the next agent or session can resume from fact rather than re-discovery.

## Agent References

No specialist owns the handover itself. When the resumed plan reaches final verification, use
[plan-execution-checker](../../../.claude/agents/plan/plan-execution-checker.md).

## Contents

- [Purpose, Scope, and Relationship](./plan-handover-execution/purpose-scope-and-relationship.md) — when (not) to use it; ties to plan-takeover-execution.md.
- [Why This Exists](./plan-handover-execution/why-this-exists.md) — the two kinds of knowledge delivery.md misses.
- [Required Document Structure](./plan-handover-execution/required-document-structure.md) — the literal template, section by section.
- [Notes and Execution Mode](./plan-handover-execution/notes-and-execution-mode.md) — load-bearing sections; who writes it.
- [Steps](./plan-handover-execution/steps.md) — the seven steps to write a handover.

## Related Documentation

- [Plan Takeover Execution](./plan-takeover-execution.md) — the read-side workflow this one's output
  feeds into; owns discovery, reconciliation, and takeover once a handover (or none) is found.
- [Plan Execution](./plan-execution.md) — the workflow a resumed plan ultimately continues in, once
  `plan-takeover-execution.md` has adopted its worktree.
- [Knowledge Capture](../../development/quality/knowledge-capture.md) — the entry-shape convention this
  workflow's gotcha-capture step mirrors, and the destination for a gotcha that turns out to be durable
  rather than session-specific.
- [Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md) —
  the same-machine assumption `local-tmp/handovers/` depends on.
