---
title: "Parallel-by-Default — Standards 1-2: Parallel Unless Dependent, and the N+1 Model"
description: The default execution model (parallel unless dependent) and the adjustable N+1 concurrency model, including why the default is 3 and the adjustment rule
category: explanation
subcategory: development
tags:
  - parallelism
  - concurrency
  - performance
  - ai-agents
  - efficiency
created: 2026-06-23
when_to_use: Use when deciding whether to run work serially or in parallel, and how many concurrent units are allowed.
---

# Standards 1-2: Parallel Unless Dependent, and the N+1 Model

## Standard 1 — Parallel Unless Dependent

The default execution model is **parallel**. An agent MUST run multiple independent units of work in the same turn rather than issuing them one at a time when:

- The outputs of the units do not depend on each other
- All inputs needed to launch the units are already known

The burden of proof is on serialization: an agent that runs independent work serially must have an explicit reason (dependency, ordering constraint, tool conflict). Absence of a reason means parallel.

## Standard 2 — The N+1 Model (One Adjustable N)

No more than **N** independent units of work run simultaneously at any point, where **N defaults to 3**. Counting the always-active main thread as the `+1`, this yields **N+1 concurrently active units in total** — four at the default. After a unit completes, a new one may start immediately to refill the slot: N governs the instantaneous maximum, not the batch total.

**One N, not two.** This model replaces an older asymmetry that set a cap of three for tool-call batching but a stricter cap of two for background subagents. Both collapse into the single adjustable N. Background Agent-tool spawns are a **specialization** of this norm, not an exception to it — the [Subagent Orchestration Convention](../../agents/subagent-orchestration.md) owns their extra mechanics (polling, stuck detection, relaunch) while using the same N.

**Why the default is 3**: N=3 is chosen specifically to **bound token/compute-budget burn** — parallelism has real cost, since each concurrent unit independently spends tokens and API quota against the vendor's per-minute limit. Fewer than three under-uses available throughput; more risks rate-limit cascades and budget overrun. Assume the machine is **shared** — other agents, engineers, and processes run concurrently against the same disk, git object store, and CI runners — so the safe N is bounded by what that machine can absorb alongside everyone else.

**Adjustment rule**: N is adjustable per-plan and **along the way**. Raising it requires all three of genuinely independent work, machine capacity, and budget headroom; **lowering it is required** under budget, runner, or disk pressure. A plan declares its chosen N in its `## Parallelization Model` section. The agent MUST NOT silently self-promote beyond the declared N based on its own assessment of available headroom.
