---
title: "Related Documentation"
description: Links to plan-takeover-execution.md, plan-execution.md, Knowledge Capture, and the Agent Workflow Orchestration Convention.
when_to_use: Use when navigating from this workflow to the read-side workflow it feeds, or to the conventions its rules mirror.
---

# Related Documentation

- [Plan Takeover Execution](../plan-takeover-execution.md) — the read-side workflow this one's output
  feeds into; owns discovery, reconciliation, and takeover once a handover (or none) is found.
- [Plan Execution](../plan-execution.md) — the workflow a resumed plan ultimately continues in, once
  `plan-takeover-execution.md` has adopted its worktree.
- [Knowledge Capture](../../../development/quality/knowledge-capture.md) — the entry-shape convention this
  workflow's gotcha-capture step mirrors, and the destination for a gotcha that turns out to be durable
  rather than session-specific.
- [Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration.md) —
  the same-machine assumption `local-tmp/handovers/` depends on.
