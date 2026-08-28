---
title: "Operating Budgets — Parallelism Budget"
description: "Defines the parallelism budget for how many concurrent work streams an orchestrating agent may run."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when deciding how many parallel work streams to run at once.
---

# Operating Budgets — Parallelism Budget

Parallelize aggressively — prefer running independent work concurrently over serially, and try to keep the parallel budget fully used whenever independent work is available.

The budget follows the **N+1 model**: `1 main thread + N background agents = N+1 total`. `N` counts concurrent background operations — background delegated agents spawned via the Agent tool, and equivalent token-spending background tasks. The main thread is the `+1`; its own work is not one of the `N`. The **default is `N = 3`**, yielding four concurrently active agents in total.

**Why the default is 3.** N=3 is chosen specifically to **bound token/compute-budget burn** — parallelism is not free, and each background agent independently spends tokens and API quota. Raising N is a **deliberate, justified** act requiring all three of: genuinely independent work available, machine capacity to absorb it, and budget headroom. Lowering N is **required** under budget, runner, or disk pressure.

**Adjustable, never self-promoted.** N may be raised per-plan and **along the way** as conditions change, and a plan declares its chosen N in its `## Parallelization Model` section. An agent MUST NOT silently self-promote beyond the declared N — raising it is an explicit decision, recorded, not an inference an agent draws from its own sense of available headroom.

**Same-machine assumption.** Treat the repository as **very active**: assume other AI agents, software engineers, and background processes are running **simultaneously on the same physical machine**, sharing its disk, its git object store, its worktrees, and its self-hosted CI runners. The N you can safely run is bounded by what that shared machine can absorb alongside everyone else's work, not by what this session alone could drive.

**Cross-repository heavy-work schedule.** When one plan spans repositories, run worktree
provisioning, toolchain convergence, builds, and validation in one repository at a time by default.
N remains the cap for other independent work; it does not authorize cross-repository heavy overlap.
An exception requires a concrete operational need recorded in the plan and confirmed machine, disk,
runner, and risk controls.

The detailed background-batch mechanics (sequencing, stuck detection, relaunch) live in the [Subagent Orchestration Convention](../subagent-orchestration.md), which specializes the same N.
