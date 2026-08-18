---
title: "Workflow Execution Mode Convention"
description: Defines execution modes for workflows — Agent Delegation (preferred) and Manual Orchestration (fallback) — explaining how to use the Agent tool for delegated agent invocation and when to fall back to direct execution
when_to_use: Use when a workflow step needs to invoke an agent or run its logic directly, and you need to decide which execution mode applies and how to execute it correctly.
category: explanation
subcategory: workflows
tags:
  - workflows
  - execution-mode
  - orchestration
  - conventions
created: 2026-01-05
---

# Workflow Execution Mode Convention

This convention defines the execution modes for workflows in this repository: **Agent
Delegation** (preferred, invoke agents via the Agent tool so file changes persist) and **Manual
Orchestration** (fallback, execute workflow logic directly with Read/Write/Edit/Bash tools).
Covers the decision flow, the manual step-by-step pattern, an authoring template, and common
pitfalls below.

## Contents

- [Overview](./execution-modes/overview.md) — the two modes and why they matter.
- [The Core Challenge](./execution-modes/the-core-challenge.md) — why persistence needs a defined mode.
- [Agent Delegation Mode (Preferred)](./execution-modes/agent-delegation-mode.md) — invoking agents via the Agent tool.
- [Manual Orchestration Mode (Fallback)](./execution-modes/manual-orchestration-mode.md) — direct tool execution.
- [Execution Mode Decision Flow](./execution-modes/execution-mode-decision-flow.md) — the decision tree.
- [Manual Mode Execution Pattern](./execution-modes/manual-mode-execution-pattern.md) — the six-step manual procedure.
- [Implementation Example](./execution-modes/implementation-example.md) — the Execution Mode section template.
- [Future Considerations](./execution-modes/future-considerations.md) — potential workflow-runner automation.
- [Tool Usage Rules](./execution-modes/tool-usage-rules.md) — which tools apply per mode.
- [Common Pitfalls](./execution-modes/common-pitfalls.md) — four recurring mistakes and fixes.
- [Principles Implemented/Respected](./execution-modes/principles-implemented-respected.md) — traceability to foundational principles.
- [Related Documentation](./execution-modes/related-documentation.md) — links to composing conventions.
