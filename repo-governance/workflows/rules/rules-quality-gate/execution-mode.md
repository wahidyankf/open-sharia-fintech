---
title: "Execution Mode"
description: How to invoke repo-rules-checker and -fixer via Agent Delegation, the Manual Orchestration fallback, and the six-step execution summary.
when_to_use: Use when starting a repository rules quality gate run and deciding preferred vs. fallback execution mode.
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `repo-rules-checker` and
`repo-rules-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem, making it
the preferred approach when these agents exist as defined delegated agent types.

**How to Execute**:

```
User: "Run repository rules quality gate workflow in normal mode"
```

The AI will:

0. Resolve lifecycle ownership/evidence, then build rhino-cli if missing (`rtk nx build
rhino-cli`) and run the filtered domain preflight (Step 0.5).
1. Invoke `repo-rules-checker` via the Agent tool (reads governance files, writes audit)
2. Invoke `repo-rules-fixer` via the Agent tool (reads audit, applies fixes, writes fix report)
3. Iterate until zero threshold-level domain findings are achieved; report lifecycle status separately
4. Show git status with modified files
5. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run repository rules quality gate workflow in manual mode"
```

The AI executes checker and fixer logic directly using Read/Write/Edit tools in the main
context — use this when agent delegation is unavailable.
