---
title: "Execution Mode"
description: Preferred and fallback execution modes for the CI quality gate.
when_to_use: Use when starting the CI quality gate, to decide between Agent Delegation and Manual Orchestration.
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `ci-checker` and `ci-fixer` via the Agent tool
with `subagent_type` (see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.
