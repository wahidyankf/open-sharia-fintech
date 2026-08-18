---
title: "Anti-Patterns — Open-Ended Poll Loops and Going Silent"
description: "Covers delegating an open-ended poll loop inside a long chunk and going silent while background agents run."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when reviewing whether an orchestrator delegated a poll loop it should have owned, or went quiet during a long run.
---

# Anti-Patterns — Open-Ended Poll Loops and Going Silent

## Delegating an Open-Ended Poll Loop Inside a Long Chunk

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

## Going Silent While Background Agents Run

**Problem**: The main agent launches a background batch and posts no status update to the user until the batch completes, regardless of how long that takes.

**Why it fails**: A batch running longer than the applicable interval (3 minutes for CI-related work, 5 minutes for generic work) with no visible update looks identical to the main agent stalling. The user has no way to distinguish "still working" from "stuck" without asking.

**Fix**: Post a status update at the interval matched to the kind of work in flight — every 3 minutes when any CI-related item is in flight (mixed batches take the tighter cadence), every 5 minutes for purely generic work (see Standard 5).
