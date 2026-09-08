---
description: "States why this convention defines standards for orchestrating background subagents."
when_to_use: Use when explaining why a background-agent orchestration rule exists.
---

# Purpose

When a main agent uses the Agent tool to spawn multiple subagents in background (`run_in_background: true`), it operates with incomplete information about each subagent's progress. Two failure modes are common:

1. **Rate-limit collisions**: Each subagent has its own context window and tool-call stream. Running too many simultaneously saturates the the model vendor per-minute API quota, causing retries, degraded throughput, or hard failures.

2. **Stuck agents**: A subagent occasionally stalls — usually because its output-token budget is exhausted mid-plan. The agent "completes" but its output file is sparse or ends with a planning sentence (e.g., "Now writing section...") rather than finished content. Without polling, the main agent waits indefinitely.

This convention codifies two interlocking standards that address both failure modes.
