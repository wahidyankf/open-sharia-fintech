---
title: "Execution Mode Decision Flow"
description: A decision tree for choosing Agent Delegation vs. Manual Orchestration for a given workflow step.
category: explanation
subcategory: workflows
tags:
  - workflows
  - execution-mode
  - orchestration
created: 2026-01-05
when_to_use: Use when deciding, step by step, which execution mode applies to a specific workflow step reference.
---

# Execution Mode Decision Flow

```
What does the workflow step reference?
├── Named agent → Agent exists as defined subagent_type in .claude/agents/?
│   ├── YES → Use Agent Delegation (preferred)
│   └── NO  → Use Manual Orchestration (fallback)
├── Nested workflow → Execute that workflow (recursively apply this decision flow)
└── Procedure → Use Manual Orchestration (follow procedure steps directly)
```
