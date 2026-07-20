---
title: "Parallel-by-Default Practice"
description: When doing work with independent sub-units (tool calls, file reads/edits, searches, or delegated agents), default to running them in parallel rather than serially, capped at three concurrent units of work
category: explanation
subcategory: development
tags:
  - parallelism
  - concurrency
  - performance
  - ai-agents
  - efficiency
created: 2026-06-23
---

# Parallel-by-Default Practice

When independent units of work are ready, run them in parallel. Serial execution of independent work wastes throughput and adds latency with no benefit. The deliberate cap of **three** simultaneous units preserves meaningful speedup while staying below the token-burn and Claude API per-minute rate-limit threshold.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: The declared N is a deliberate, pre-decided constraint — not a reactive limit set after hitting errors, and not a number an agent infers mid-batch from how fast things feel. Acting from a bounded model prevents speculative over-parallelism and the cascading failures it causes.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: One number — three — governs all parallel work. No adaptive scheduling, no per-task caps, no context-dependent arithmetic. A single fixed cap is simple enough to apply consistently without thought.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Running independent tool calls in a single turn, or independent subagents in background, automates what would otherwise require manually sequenced round-trips. Parallel-by-default is the automated form of efficient execution.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The cap and its rationale are stated explicitly in this document. Agents apply the value here — they do not infer limits from context or self-promote based on observed headroom.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: This document follows active voice, proper heading hierarchy, and accessible examples throughout.

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: This document uses a lowercase kebab-case filename consistent with repository naming rules.

## Purpose

Two failure modes emerge when agents treat serial execution as the default:

1. **Unnecessary latency**: Reading five independent files one at a time takes five round-trips. Reading them in a single parallel turn takes one. The agent adds latency for every independently-readable file, search, or tool call that waits behind a previous unrelated operation.

2. **Wasted throughput**: Parallel capacity exists. Leaving it idle while independent work queues serially is waste — the kind that compound across every multi-file task and multi-agent batch an agent runs.

This practice eliminates both failure modes by inverting the default: parallel unless dependent.

## Scope

### What This Practice Covers

- Independent Bash/tool calls batched together in a single conversation turn (e.g., reading multiple unrelated files, running multiple independent searches)
- Delegated Agent-tool spawns running in background (covered in detail by [Subagent Orchestration Convention](../agents/subagent-orchestration.md))
- Any work where sub-units do not depend on each other's output

### What This Practice Does NOT Cover

- Dependent work, where a later step requires an earlier step's result — those stay sequential
- Intra-agent concurrency inside a subagent's own execution (governed by that agent's own behavior)
- Bash-level pipeline parallelism (e.g., `&` / `wait` in shell scripts)

## Standards

### Standard 1 — Parallel Unless Dependent

The default execution model is **parallel**. An agent MUST run multiple independent units of work in the same turn rather than issuing them one at a time when:

- The outputs of the units do not depend on each other
- All inputs needed to launch the units are already known

The burden of proof is on serialization: an agent that runs independent work serially must have an explicit reason (dependency, ordering constraint, tool conflict). Absence of a reason means parallel.

### Standard 2 — The N+1 Model (One Adjustable N)

No more than **N** independent units of work run simultaneously at any point, where **N defaults to 3**. Counting the always-active main thread as the `+1`, this yields **N+1 concurrently active units in total** — four at the default. After a unit completes, a new one may start immediately to refill the slot: N governs the instantaneous maximum, not the batch total.

**One N, not two.** This model replaces an older asymmetry that set a cap of three for tool-call batching but a stricter cap of two for background subagents. Both collapse into the single adjustable N. Background Agent-tool spawns are a **specialization** of this norm, not an exception to it — the [Subagent Orchestration Convention](../agents/subagent-orchestration.md) owns their extra mechanics (polling, stuck detection, relaunch) while using the same N.

**Why the default is 3**: N=3 is chosen specifically to **bound token/compute-budget burn** — parallelism has real cost, since each concurrent unit independently spends tokens and API quota against the vendor's per-minute limit. Fewer than three under-uses available throughput; more risks rate-limit cascades and budget overrun. Assume the machine is **shared** — other agents, engineers, and processes run concurrently against the same disk, git object store, and CI runners — so the safe N is bounded by what that machine can absorb alongside everyone else.

**Adjustment rule**: N is adjustable per-plan and **along the way**. Raising it requires all three of genuinely independent work, machine capacity, and budget headroom; **lowering it is required** under budget, runner, or disk pressure. A plan declares its chosen N in its `## Parallelization Model` section. The agent MUST NOT silently self-promote beyond the declared N based on its own assessment of available headroom.

### Standard 3 — Background-Slot Preference (Keep the Main Thread Vacant)

Prefer to fill the **background** slots up to N and keep the **main thread vacant** and responsive. The main thread is the **orchestrator**; background agents are the **workers**. A user who asks a question mid-batch should not wait behind the main thread's own long-running work.

This preference is **bounded by the DAG** (Standard 4): fan out only genuinely independent nodes. "Maximize background utilization" never justifies artificially splitting dependent work to fill idle slots — a dependent chain running one node at a time is correct, not a failure to parallelize. Independence governs the fan-out; N only caps it.

### Standard 4 — DAG-First Ordering

Every non-trivial task list **and** plan delivery checklist declares an explicit **dependency DAG**: nodes are tasks or checklist items, edges are `blocks` / `blockedBy`. Independent nodes run in parallel up to N; dependent nodes serialize.

The DAG's **independent-node width** is what the orchestrator fans out to — N only caps that width, it never creates it. Establish the DAG _before_ dispatching, not after: two nodes are independent only when neither reads what the other writes, so a shared output file, a shared branch, or an ordering constraint makes them dependent however separable they appear. **Cleanup is the terminal node**, depending on every other node, so it can never remove an artifact something still in flight needs.

Task lists express this via `blocks` / `blockedBy`; `delivery.md` expresses it as phases/steps plus a `## Parallelization Model` section — see the [Plans Organization Convention](../../conventions/structure/plans.md) and the [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md).

## Anti-Patterns

### Serial Execution of Independent Reads

**Problem**: The agent reads five unrelated files one at a time, waiting for each response before issuing the next read.

**Why it fails**: Each read is independent. Five sequential round-trips add latency proportional to the number of files. The batch could complete in one turn with five parallel reads (or two turns at cap-3).

**Fix**: Batch all independent reads into a single turn, up to three at a time.

---

### Serial Execution of Independent Searches

**Problem**: The agent runs three independent grep/glob searches in sequence, waiting for each result before issuing the next.

**Why it fails**: The searches are independent. Running them in parallel reduces total elapsed time to the duration of the slowest single search.

**Fix**: Issue all three searches in the same turn.

---

### Self-Promoting the Cap

**Problem**: The agent raises the parallel limit to five or six because the first few units completed quickly and the API feels responsive.

**Why it fails**: Response latency varies across a batch. Units that start fast can converge on rate-limit boundaries as they all hit their heaviest phases simultaneously. The cap is set to stay safely below saturation at all batch phases, not just the opening ones.

**Fix**: The cap is three. Only explicit user instruction raises it.

---

### Parallelizing Dependent Work

**Problem**: The agent runs step B in parallel with step A even though step B requires step A's output as its input.

**Why it fails**: Step B will read stale or missing data. The result is either a tool error or incorrect output that must be redone.

**Fix**: Identify dependencies before batching. Dependent steps run sequentially. Independent steps run in parallel.

## References

**Related Principles:**

- [Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md) - Bounded, pre-decided constraints over reactive improvisation
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) - One fixed cap over adaptive scheduling
- [Automation Over Manual](../../principles/software-engineering/automation-over-manual.md) - Automated parallel execution over manually sequenced round-trips
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) - Documented constants, not inferred limits

**Related Practices:**

- [Subagent Orchestration Convention](../agents/subagent-orchestration.md) - Concrete specialization of this norm for background Agent-tool spawns, using the same N (N+1 including the main thread); owns polling, stuck detection, and relaunch mechanics
- [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md) - Broader agent task management strategy of which parallel-by-default is one component; states the N+1 parallelism budget and the same-machine assumption that bounds N

**Agents:**

- `repo-rules-checker` - Validates convention compliance
- `repo-rules-maker` - Creates and updates conventions
