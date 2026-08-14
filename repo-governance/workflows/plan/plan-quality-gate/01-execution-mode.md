---
title: "Execution Mode — Plan Quality Gate"
description: Describes the agent-delegation and manual-orchestration execution modes for plan-quality-gate, and when each is used.
when_to_use: Use when deciding whether to invoke plan-checker/plan-fixer via the Agent tool or fall back to manual orchestration.
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `plan-checker` and `plan-fixer` via the Agent
tool with `subagent_type` (see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).
The calling root owns every user interaction; delegated specialists return decision envelopes.

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem, making it
the preferred approach when these agents exist as defined delegated agent types.

**How to Execute**:

```
User: "Run plan quality gate workflow for plans/backlog/my-plan/"
```

The AI will:

1. Invoke `plan-checker` via the Agent tool (reads plan files, writes audit report)
2. Invoke `plan-fixer` via the Agent tool (reads audit, applies fixes, writes fix report)
3. Resolve any `## User Decisions Required` envelope through root-owned `grill-me`, then resume or
   reinvoke the fixer
4. Iterate until zero findings achieved
5. Show git status with modified files
6. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run plan quality gate workflow for plans/backlog/my-plan/ in manual mode"
```

The AI executes checker and fixer logic directly using Read/Write/Edit tools in the main
context — use this when agent delegation is unavailable.

**When to use**:

- After creating new project plans
- Before starting plan execution
- When updating existing plans with new requirements
- Periodically to ensure plan quality and accuracy
