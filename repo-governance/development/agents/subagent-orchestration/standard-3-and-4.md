---
title: "Standard 3 and Standard 4 — Chunk Sizing and Task-Notification Handling"
description: "Defines Standard 3 (chunk sizing for background agents) and Standard 4 (agent ID and task-notification handling)."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when sizing a chunk of work for a background agent, or handling its task-notification and agent ID.
---

# Standard 3 and Standard 4 — Chunk Sizing and Task-Notification Handling

## Standard 3 — Chunk Sizing for Background Agents

Chunk the work assigned to each background subagent so that expected runtime stays within **3–10 minutes per agent**. This keeps the batch observable, limits blast radius if an agent stalls, and fits within healthy output-token budgets.

**Empirical guidance**: 7 examples per chunk (for content-generating agents processing example pages) observed to produce 3–10 minute runtimes with 2 parallel languages (the current background cap). Adjust chunk size down if a category of agent stalls repeatedly; adjust up (cautiously) if completion times are consistently under 2 minutes.

**Rule**: When a relaunched agent stalls a second time on the same chunk, split the chunk in half and relaunch the two halves as sequential (not parallel) agents.

## Standard 4 — Agent ID and Task-Notification Handling

The Agent tool returns an `agentId` for each spawn. The main agent MUST:

- Record each `agentId` alongside the expected output file path in its tracking state
- Use `agentId` with `TaskStop` when stuck detection triggers
- Use `SendMessage` (not file polling) to relay new instructions mid-run if needed

Task-notification messages from the harness signal completion (or kill). These are the primary completion signal. File mtime polling is the secondary stuck-detection signal, not a substitute for task-notifications.

`TaskList` does NOT show spawned Agent IDs. The only source of an Agent ID is the response from the Agent-tool spawn call. The main agent must preserve these IDs in local tracking state (e.g., `local-tmp/todo.md`) for the duration of the batch.
