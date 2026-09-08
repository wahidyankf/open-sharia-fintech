---
description: "Describes Agent Delegation (preferred, invoking docs-software-engineering-separation-checker/fixer) versus Manual Orchestration (fallback), and how a user invokes each."
when_to_use: "Use when deciding whether to run this workflow via delegated agents or manual tool orchestration."
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `docs-software-engineering-separation-checker`
and `docs-software-engineering-separation-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem, making it
the preferred approach when these agents exist as defined delegated agent types.

**How to Execute**:

```
User: "Run docs software engineering separation quality gate workflow"
```

The AI will:

1. Invoke `docs-software-engineering-separation-checker` via the Agent tool (reads files, writes audit)
2. Invoke `docs-software-engineering-separation-fixer` via the Agent tool (reads audit, applies fixes, writes fix report)
3. Iterate until zero findings achieved
4. Show git status with modified files
5. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run docs software engineering separation quality gate workflow in manual mode"
```

The AI executes checker and fixer logic directly using Read/Write/Edit tools in the main
context — use this when agent delegation is unavailable.
