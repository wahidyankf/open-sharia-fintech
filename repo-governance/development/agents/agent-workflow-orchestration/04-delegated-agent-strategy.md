---
title: "Delegated Agent Strategy"
description: "Defines when to use delegated (sub)agents, the rules for delegating, and when not to delegate."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when deciding whether to hand a piece of work off to a delegated agent.
---

# Delegated Agent Strategy

Use delegated agents to keep the main context window focused and clean.

## When to Use Delegated Agents

Offload work to delegated agents when:

- **Research and exploration**: Reading many files to understand a codebase section, gathering facts before a decision
- **Parallel analysis**: Multiple independent questions can be answered simultaneously
- **Complex subtasks**: A subtask is large enough to have its own plan

## Delegated Agent Rules

- **One task per delegated agent**: Each delegated agent has a single, focused responsibility. Do not bundle multiple concerns into one delegated agent
- **Use fork skills for structured delegation**: When the task fits a known skill pattern, prefer fork skills over ad hoc delegated agent invocation
- **Return summarized results**: Delegated agents return findings, not raw dumps. The main conversation receives what it needs to make decisions, not everything the delegated agent read

## When Not to Use Delegated Agents

Do not spawn a delegated agent for simple reads or lookups that take one or two tool calls. The overhead is not worth it for small operations.
