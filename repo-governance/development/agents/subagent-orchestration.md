---
title: "Subagent Orchestration Convention"
description: Standards for concurrency caps and stuck-detection when a main agent spawns subagents via the Agent tool, capping concurrent background subagents at two (three total including the main agent/thread) to control token burn and avoid Claude API rate-limit hits
category: explanation
subcategory: development
tags:
  - ai-agents
  - orchestration
  - subagents
  - concurrency
  - rate-limits
created: 2026-05-17
---

# Subagent Orchestration Convention

This document defines how a main agent manages subagents it spawns via the Agent tool: how many to run in parallel, how to poll for stuck agents, and what signals distinguish healthy from stalled execution. These standards prevent Claude API per-minute rate-limit failures and ensure stuck agents are detected and relaunched rather than silently starving a batch.

## Principles Implemented/Respected

This practice implements/respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Concurrency caps and polling cadences are deliberate, pre-decided constraints — not reactive responses. The main agent acts from a bounded model rather than spawning speculatively and hoping the API absorbs it.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Stuck detection addresses the root cause (output-token-budget exhaustion during planning, causing silent stall) rather than the symptom (batch never completing). Relaunch restores completion; ignoring a stall compounds delay.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: A fixed default cap (2 background subagents, 3 total including the main thread) with a clearly-described override path is simpler than an adaptive scheduler. Three minutes between polls is a single number to remember. Concrete mtime-based stuck detection requires no additional tooling.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The cap, polling interval, and stuck threshold are explicit constants stated in this document. Agents do not infer limits from context; they apply the values here.

## Conventions Implemented/Respected

This practice respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: This document follows active voice, proper heading hierarchy, and accessible examples throughout.

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: This document uses a lowercase kebab-case filename consistent with repository naming rules.

The following Layer 3 development practice also informs this document:

- **[Agent Workflow Orchestration Convention](./agent-workflow-orchestration.md)**: Subagent orchestration is a specialization of delegated agent strategy. The rules here narrow the delegation model for the case where agents run in background.

## Purpose

When a main agent uses the Agent tool to spawn multiple subagents in background (`run_in_background: true`), it operates with incomplete information about each subagent's progress. Two failure modes are common:

1. **Rate-limit collisions**: Each subagent has its own context window and tool-call stream. Running too many simultaneously saturates the the model vendor per-minute API quota, causing retries, degraded throughput, or hard failures.

2. **Stuck agents**: A subagent occasionally stalls — usually because its output-token budget is exhausted mid-plan. The agent "completes" but its output file is sparse or ends with a planning sentence (e.g., "Now writing section...") rather than finished content. Without polling, the main agent waits indefinitely.

This convention codifies two interlocking standards that address both failure modes.

## Scope

### What This Convention Covers

- Maximum concurrent Agent-tool spawns from a single main agent
- Polling cadence and signals for stuck detection
- How to identify healthy vs. stalled subagent output
- Relaunch procedure when a stuck agent is detected
- Chunk sizing guidance to fit within healthy runtimes
- Per-session override rules

### What This Convention Does NOT Cover

- Subagent internal behavior (covered by [Agent Workflow Orchestration Convention](./agent-workflow-orchestration.md))
- Agent frontmatter or file structure (covered by [AI Agents Convention](./ai-agents.md))
- Workflows that call agents sequentially rather than in background (no special rules needed)
- Bash-based tool parallelism (distinct from Agent-tool spawning)

## Standards

### Standard 1 — Default Concurrency Cap: 2 Background (3 Total Including Main Thread)

The main agent MUST NOT have more than **2 background subagents active simultaneously** at any point, unless the user explicitly raises the cap for a specific session or batch. The main thread's own execution does not count toward this background cap, but it is never idle while background subagents run — it is always one of the concurrently active agents. Counting the main thread, **at most 3 agents are concurrently active in total** (the main thread plus up to 2 background subagents) — never more. When independent units of work are ready, background slots should be kept full up to 2 rather than running them one at a time.

**Applies to**: All Agent-tool spawns, whether background or foreground. Both content-producing makers (e.g., `apps-ayokoding-www-by-example-maker`) and meta-agents (e.g., `repo-rules-maker`) count toward the background cap. Total simultaneous background Agent-tool invocations is the metric, not agent type.

**Rationale**: Each subagent operates its own independent tool-call stream against the Claude API. Running more than 2 background subagents concurrently (3 total including the main thread) risks saturating the per-minute request quota at the model vendor and increases token burn rate, producing rate-limit errors that cascade and slow the entire batch — this is a token-starvation and rate-limit concern, not merely a throughput cap. Two concurrent background subagents, alongside the main thread's own work, deliver meaningful parallel throughput while staying safely below observed saturation thresholds. This cap is the concrete subagent specialization of the broader parallel-by-default working norm — see [Parallel-by-Default Practice](../practice/parallel-by-default.md) for the general principle.

**Sequencing rule**: Launch a new subagent only after a prior one completes (via task-notification message) or after calling `TaskStop` on a stuck agent. Do not pre-queue more than 2 pending background launches at once.

**Override rule**: The user may instruct the main agent to raise the cap temporarily (e.g., "run 3 background agents in parallel this batch"). The override applies for that session or batch only. After the batch completes, the default of 2 background subagents (3 total including the main thread) resumes automatically. The main agent MUST NOT self-promote the cap based on its own assessment of available headroom.

#### Examples

```
PASS: 1 background agent active, a second independent unit is ready → launch the second (keep slots full)
PASS: 2 background agents active → wait for one to complete → launch next
PASS: User says "run 3 background agents at once for this batch" → 3 active during that batch only
FAIL: 3 background agents launched simultaneously without user instruction
FAIL: Main agent raises cap to 3 background agents because "the first two seem fast"
```

### Standard 2 — 3-Minute Stuck-Detection Polling

When subagents run in background (`run_in_background: true`), the main agent MUST poll every **3 minutes** to verify no agent has stalled.

#### Polling Mechanism

The poll inspects **target file mtime and size** — the output file each subagent is producing. The main agent reads file metadata (not file contents) to check for progress.

**MUST NOT read transcript files**: The Agent tool writes a transcript to a temp path (e.g., `/private/tmp/...output`). Reading this file via shell overflows the main agent's context window, per harness convention. Transcript files are off-limits for polling. Use only the known output file path that the subagent was instructed to write.

#### Stuck Threshold

A subagent is considered **stuck** when either of these conditions holds:

- The output file mtime has not changed for **30 minutes or more** since the last observed change (or since launch if never observed to change)
- No task-notification completion signal has arrived within approximately **3× the runtime of peer agents** that completed successfully in the same batch

The 30-minute mtime threshold is empirically grounded: healthy subagents update their output file within 3–10 minutes of launch when chunk size is appropriate. A 30-minute gap with no mtime change reliably distinguishes stalled from slow.

#### Recovery Procedure

When a stuck agent is detected:

1. Call `TaskStop` with the agent's `agentId` (obtained from the Agent-tool spawn response)
2. Relaunch the same agent with the same prompt and output path
3. Log the relaunch in the batch tracking state (e.g., `local-temp/todo.md`) so the main agent can detect if the same agent stalls a second time
4. If a relaunched agent stalls again, reduce the chunk size and relaunch with narrower scope

**Why relaunch works**: The stuck condition is almost always caused by output-token-budget exhaustion during the agent's internal planning phase. The agent consumes its token budget reasoning about structure before generating output, leaving little budget for the actual content. Relaunch starts fresh with full token budget; the agent typically completes normally because it encounters fewer planning branches on a familiar task.

#### Healthy vs. Stuck: Empirical Signal Table

| Signal                                       | Healthy                                    | Stuck                                                      |
| -------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| First mtime change after launch              | Within 3–10 min                            | Never, or after 30+ min                                    |
| Output file size growth                      | Grows steadily across polls                | Flat across multiple polls                                 |
| Task-notification arrival                    | Within 3–10 min after peer agents complete | Absent long after peers complete                           |
| Final output content (post-completion check) | Complete section                           | Ends mid-sentence or with planning text ("Now writing...") |

#### Examples

```
PASS: Poll at 3-min intervals → agent A mtime updated at t+5min → healthy
PASS: t+30min, agent B mtime unchanged → TaskStop(agentB.id) → relaunch → completes
FAIL: Main agent waits indefinitely for task-notification without polling
FAIL: Main agent reads /private/tmp/...output to check progress → context overflow
FAIL: Main agent polls every 30 seconds → excessive tool-call overhead
```

### Standard 3 — Chunk Sizing for Background Agents

Chunk the work assigned to each background subagent so that expected runtime stays within **3–10 minutes per agent**. This keeps the batch observable, limits blast radius if an agent stalls, and fits within healthy output-token budgets.

**Empirical guidance**: 7 examples per chunk (for content-generating agents processing example pages) observed to produce 3–10 minute runtimes with 2 parallel languages (the current background cap). Adjust chunk size down if a category of agent stalls repeatedly; adjust up (cautiously) if completion times are consistently under 2 minutes.

**Rule**: When a relaunched agent stalls a second time on the same chunk, split the chunk in half and relaunch the two halves as sequential (not parallel) agents.

### Standard 4 — Agent ID and Task-Notification Handling

The Agent tool returns an `agentId` for each spawn. The main agent MUST:

- Record each `agentId` alongside the expected output file path in its tracking state
- Use `agentId` with `TaskStop` when stuck detection triggers
- Use `SendMessage` (not file polling) to relay new instructions mid-run if needed

Task-notification messages from the harness signal completion (or kill). These are the primary completion signal. File mtime polling is the secondary stuck-detection signal, not a substitute for task-notifications.

`TaskList` does NOT show spawned Agent IDs. The only source of an Agent ID is the response from the Agent-tool spawn call. The main agent must preserve these IDs in local tracking state (e.g., `local-temp/todo.md`) for the duration of the batch.

## Anti-Patterns

### Launching a Full Batch Without Waiting

**Problem**: The main agent launches all subagents simultaneously to minimize total elapsed time.

**Why it fails**: More than 2 concurrent background agents (3 total including the main thread) saturates the per-minute API quota and increases token burn rate. Rate-limit errors cascade; agents that would have succeeded fast must retry, extending total batch time beyond the sequential baseline.

**Fix**: Cap background agents at 2 (3 total including the main thread). Launch the next agent only after one completes.

### Relying Solely on Task-Notifications for Stuck Detection

**Problem**: The main agent waits for task-notification completion signals and takes no other action.

**Why it fails**: A stuck agent may never emit a completion notification. The batch blocks indefinitely.

**Fix**: Poll file mtime every 3 minutes. Apply the 30-minute stuck threshold. Call `TaskStop` when triggered.

### Reading the Transcript File to Check Progress

**Problem**: The main agent reads the `/private/tmp/...output` transcript file via shell to diagnose a slow agent.

**Why it fails**: The transcript file is large and grows with every tool call. Reading it overflows the main agent's context window, degrading reasoning quality for all subsequent work in the session.

**Fix**: Poll the output file mtime only. If content verification is needed post-completion, read only the relevant sections of the output file.

### Self-Promoting the Concurrency Cap

**Problem**: The main agent raises the cap to 3 or 4 background agents on its own judgment because early agents are completing quickly.

**Why it fails**: Completion speed varies. A batch that starts fast can become rate-limited as all agents hit their tool-intensive middle sections simultaneously. The default cap is set deliberately at 2 background agents (3 total including the main thread) — the optimal balance between parallel throughput and API headroom — to stay safely below the saturation threshold at all batch phases.

**Fix**: The cap is 2 background agents (3 total including the main thread). Only explicit user instruction raises it, and only for a named session or batch.

### Running Background Work Serially

**Problem**: The main agent runs background subagents one at a time — waiting for the first to finish before launching the second — even when two independent units of work are ready simultaneously.

**Why it fails**: Serial execution wastes available throughput. If two units are independent and a second background slot is free, holding it empty doubles elapsed time for no benefit.

**Fix**: Keep all background slots full up to the cap of two. When a slot frees and independent work is waiting, launch immediately.

### Monolithic Chunks Assigned to Single Agents

**Problem**: The main agent assigns 20 or 30 examples to a single background agent to minimize spawning overhead.

**Why it fails**: Large chunks produce long-running agents that either exhaust their output-token budget mid-way (causing the stuck condition) or require the main agent to wait a long time before observing any output. When they stall, the entire chunk must restart.

**Fix**: Target 3–10 minute runtime per agent. Size chunks empirically for each agent type.

### Delegating an Open-Ended Poll Loop Inside a Long Chunk

**Problem**: A background agent's assigned chunk embeds an open-ended wait (e.g., "poll CI every 2
minutes until all checks are terminal") as one step in a longer multi-step sequence (provision →
edit → push → **poll** → review-cycle → flip-ready).

**Why it fails**: The agent's turn can end mid-poll — reporting a task-notification with
`status: completed` even though the wait, and every step after it, never ran. Treating that
notification as "the whole chunk finished" silently skips the remaining steps.

**Fix**: Read the agent's actual reported result, not just the `completed` label, before advancing
downstream tasks. If the result shows an in-progress wait rather than a final outcome, resume the
same agent via `SendMessage` (restating the remaining steps) rather than assuming completion or
spawning a duplicate agent for the same chunk.

**Debounce before resuming**: a single externally-observed "CI is green" snapshot is not proof the
agent's own poll noticed it — the main thread's check and the agent's next poll cycle race each
other, and one green reading can be a transient blip (flaky self-hosted-runner check, a check that
briefly reports success then reruns). Require the terminal state to hold for **two consecutive**
external poll cycles — CI still green, PR review count and `headRefOid` unchanged both times —
before concluding the agent silently stopped and taking over its remaining step (e.g., running the
mechanical `gh pr ready` yourself). Resuming on the first green reading risks duplicating or racing
work the agent is about to do on its own next tick.

## Tooling Reference

| Tool             | Purpose in This Convention                                     |
| ---------------- | -------------------------------------------------------------- |
| `Agent`          | Spawns subagent; returns `agentId`                             |
| `TaskStop`       | Terminates stuck agent by `agentId`                            |
| `SendMessage`    | Sends new instructions to a running agent                      |
| `TaskList`       | Lists TaskCreate tasks — does NOT show Agent IDs               |
| `ScheduleWakeup` | Schedules the main agent's next poll (use 180-second interval) |

**Note**: `ScheduleWakeup(delaySeconds=180)` is the preferred mechanism for 3-minute polling cadence. This is consistent with the pattern established by [CI Monitoring Convention](../workflow/ci-monitoring.md) for other scheduled checks.

## References

**Related Principles:**

- [Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md) - Bounded, pre-decided constraints over reactive improvisation
- [Root Cause Orientation](../../principles/general/root-cause-orientation.md) - Relaunch addresses the actual cause of stuck behavior
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) - Fixed cap and concrete threshold over adaptive scheduling
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) - Documented constants, not inferred limits

**Related Practices:**

- [Agent Workflow Orchestration Convention](./agent-workflow-orchestration.md) - Delegated agent strategy; this convention specializes that model for background spawning
- [AI Agents Convention](./ai-agents.md) - Agent file structure and frontmatter standards
- [CI Monitoring Convention](../workflow/ci-monitoring.md) - `ScheduleWakeup` polling pattern reused here for stuck detection

**Agents:**

- `repo-rules-checker` - Validates convention compliance
- `repo-rules-maker` - Creates and updates conventions
