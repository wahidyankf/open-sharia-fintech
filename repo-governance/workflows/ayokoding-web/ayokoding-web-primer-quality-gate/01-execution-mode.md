---
title: "Execution Mode"
description: Describes the Agent Delegation (preferred) and Manual Orchestration (fallback) execution modes for the Primer quality gate, and how to invoke each.
when_to_use: Use when deciding whether to run this quality gate via Agent tool delegation or manually with Read/Write/Edit tools, or when looking up the exact invocation syntax.
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `apps-ayokoding-www-primer-checker` and
`apps-ayokoding-www-primer-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem, making it
the preferred approach when these agents exist as defined delegated agent types. Note: this
workflow includes a manual user review step (step 3) — agent delegation applies to the checker and
fixer steps, not the human decision point.

**How to Execute**:

```
User: "Run ayokoding-web primer quality gate workflow for just-enough-go/learning/"
```

The AI will:

1. Invoke `apps-ayokoding-www-primer-checker` via the Agent tool (validates primer, writes audit)
2. User reviews audit report and decides on fixes (manual decision point)
3. Invoke `apps-ayokoding-www-primer-fixer` via the Agent tool (reads audit, applies fixes, writes
   fix report)
4. Iterate until EXCELLENT status achieved (zero findings, 75-85 examples, verified scope
   discipline)
5. Show git status with modified files
6. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run ayokoding-web primer quality gate workflow for just-enough-go/learning/ in manual mode"
```

The AI executes checker and fixer logic directly using Read/Write/Edit tools in the main context —
use this when agent delegation is unavailable.
