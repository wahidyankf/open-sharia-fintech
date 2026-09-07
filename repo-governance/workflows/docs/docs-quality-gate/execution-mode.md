---
description: "Describes Agent Delegation (preferred, invoking docs-checker/docs-tutorial-checker/docs-link-checker/docs-fixer/docs-tutorial-fixer) versus Manual Orchestration (fallback), and how a user invokes each."
when_to_use: "Use when deciding whether to run this workflow via delegated agents or manual tool orchestration."
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `docs-checker`, `docs-tutorial-checker`,
`docs-link-checker`, `docs-fixer`, and `docs-tutorial-fixer` via the Agent tool
with `subagent_type` (see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem, making it
the preferred approach when these agents exist as defined delegated agent types.

**How to Execute**:

```
User: "Run documentation quality gate workflow for docs/tutorials/"
```

The AI will:

1. Invoke `docs-checker`, `docs-tutorial-checker`, and `docs-link-checker` via the Agent tool in parallel (validate, write audits)
2. Invoke `docs-fixer` and `docs-tutorial-fixer` via the Agent tool in sequence (read audits, apply fixes, write fix reports)
3. Iterate until zero findings achieved across all three validators
4. Show git status with modified files
5. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run documentation quality gate workflow for docs/tutorials/ in manual mode"
```

The AI executes checker and fixer logic directly using Read/Write/Edit tools in the main
context — use this when agent delegation is unavailable.
