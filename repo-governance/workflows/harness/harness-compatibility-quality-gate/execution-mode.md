---
description: How to invoke harness-compatibility-checker and -fixer via Agent Delegation, with the Manual Orchestration fallback and how each is triggered.
when_to_use: Use when starting a harness compatibility quality gate run and deciding preferred vs. fallback execution mode.
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `harness-compatibility-checker` and
`harness-compatibility-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem,
making it the preferred approach when these agents exist as defined delegated agent types.

**How to Execute**:

```
User: "Run repo harness compatibility quality gate workflow"
```

The orchestrator will:

1. Resolve delegated registry IDs and lifecycle evidence, then invoke
   `harness-compatibility-checker` via the Agent tool (runs unowned semantic parity in Phase 0,
   then delegates per-harness web research to
   `web-researcher` in Phase 1, writes a combined drift audit report)
2. Invoke `harness-compatibility-fixer` via the Agent tool (reads audit, applies fixes
   to parity drift, catalog rows, binding files, and specs as needed)
3. Iterate until zero domain findings are achieved on two consecutive validations; lifecycle
   evidence is reported separately and never rerun here
4. Show git status with modified files
5. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run repo harness compatibility quality gate workflow in manual mode"
```

The orchestrator executes checker and fixer logic directly using Read/Write/Edit tools in
the main context — use this when agent delegation is unavailable.
