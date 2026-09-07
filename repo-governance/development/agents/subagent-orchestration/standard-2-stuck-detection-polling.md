---
description: "Covers the polling mechanism, stuck threshold, and recovery procedure for detecting a stuck background agent."
when_to_use: Use when a background agent has been running for a while and you need to check whether it is stuck.
---

# Standard 2 — 3-Minute Stuck-Detection Polling

When subagents run in background (`run_in_background: true`), the main agent MUST poll every **3 minutes** to verify no agent has stalled.

## Polling Mechanism

The poll inspects **target file mtime and size** — the output file each subagent is producing. The main agent reads file metadata (not file contents) to check for progress.

**MUST NOT read transcript files**: The Agent tool writes a transcript to a temp path (e.g., `/private/tmp/...output`). Reading this file via shell overflows the main agent's context window, per harness convention. Transcript files are off-limits for polling. Use only the known output file path that the subagent was instructed to write.

## Stuck Threshold

A subagent is considered **stuck** when either of these conditions holds:

- The output file mtime has not changed for **30 minutes or more** since the last observed change (or since launch if never observed to change)
- No task-notification completion signal has arrived within approximately **3× the runtime of peer agents** that completed successfully in the same batch

The 30-minute mtime threshold is empirically grounded: healthy subagents update their output file within 3–10 minutes of launch when chunk size is appropriate. A 30-minute gap with no mtime change reliably distinguishes stalled from slow.

## Recovery Procedure

When a stuck agent is detected:

1. Call `TaskStop` with the agent's `agentId` (obtained from the Agent-tool spawn response)
2. Relaunch the same agent with the same prompt and output path
3. Log the relaunch in the batch tracking state (e.g., `local-tmp/todo.md`) so the main agent can detect if the same agent stalls a second time
4. If a relaunched agent stalls again, reduce the chunk size and relaunch with narrower scope

**Why relaunch works**: The stuck condition is almost always caused by output-token-budget exhaustion during the agent's internal planning phase. The agent consumes its token budget reasoning about structure before generating output, leaving little budget for the actual content. Relaunch starts fresh with full token budget; the agent typically completes normally because it encounters fewer planning branches on a familiar task.
