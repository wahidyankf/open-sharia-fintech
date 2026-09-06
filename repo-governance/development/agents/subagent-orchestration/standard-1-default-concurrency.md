---
title: "Standard 1 — Default Concurrency: N Background Agents (N+1 Total Including Main Thread)"
description: "States the default concurrency cap for background agents plus the main thread."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when deciding how many background agents to run concurrently for a batch of independent work.
---

# Standard 1 — Default Concurrency: N Background Agents (N+1 Total Including Main Thread)

The main agent MUST NOT have more than **N background subagents active simultaneously**, where **N defaults to 3**. The main thread's own execution is the `+1` and does not consume one of the N slots, but it is never idle while background subagents run — it is always one of the concurrently active agents. Counting the main thread, **at most N+1 agents are concurrently active in total** (four at the default N). When independent units of work are ready, background slots should be kept full up to N rather than running them one at a time.

**Applies to**: All Agent-tool spawns, whether background or foreground. Both content-producing makers (e.g., `apps-ayokoding-www-by-example-maker`) and meta-agents (e.g., `rules-maker`) count toward N. Total simultaneous background Agent-tool invocations is the metric, not agent type.

**Background-slot preference**: prefer to fill the background slots up to N and keep the **main thread vacant** — the main thread is the responsive **orchestrator**, background agents are the **workers**. A user who asks a question mid-batch should not have to wait behind the main thread's own long-running work. This preference is **bounded by the DAG**: fan out only genuinely independent nodes. Never split dependent work artificially just to raise slot utilization — a serialized dependent chain running at one slot is correct, not a failure to parallelize.
