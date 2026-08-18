---
title: "Execution Mode"
description: Preferred and fallback execution modes for the UI quality gate, and example invocations.
when_to_use: Use when starting the UI quality gate, to decide between Agent Delegation and Manual Orchestration.
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `swe-ui-checker` and `swe-ui-fixer` via the Agent tool with `subagent_type` (see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using Read/Write/Edit tools when Agent Delegation is unavailable.

**How to Execute**:

```
User: "Run UI quality gate workflow for libs/web-ui/"
User: "Run UI quality gate for apps/organiclever-app-web/src/components/ui/"
```
