---
description: The two failure modes (unnecessary latency, wasted throughput) that parallel-by-default eliminates, and exactly what work this practice covers and does not cover
when_to_use: Use when deciding whether a specific piece of work falls under this practice's scope.
---

# Purpose and Scope

## Purpose

Two failure modes emerge when agents treat serial execution as the default:

1. **Unnecessary latency**: Reading five independent files one at a time takes five round-trips. Reading them in a single parallel turn takes one. The agent adds latency for every independently-readable file, search, or tool call that waits behind a previous unrelated operation.

2. **Wasted throughput**: Parallel capacity exists. Leaving it idle while independent work queues serially is waste — the kind that compound across every multi-file task and multi-agent batch an agent runs.

This practice eliminates both failure modes by inverting the default: parallel unless dependent.

## Scope

### What This Practice Covers

- Independent Bash/tool calls batched together in a single conversation turn (e.g., reading multiple unrelated files, running multiple independent searches)
- Delegated Agent-tool spawns running in background (covered in detail by [Subagent Orchestration Convention](../../agents/subagent-orchestration.md))
- Any work where sub-units do not depend on each other's output

### Related Boundaries and Exceptions

- Dependent work, where a later step requires an earlier step's result — those stay sequential
- Capacity arithmetic for compute-bearing work: worktree provisioning, toolchain setup, builds,
  and validation enter the [Resource-Aware Development](../resource-aware-development.md)
  boundary, which admits them against shared CPU and memory rather than a per-repository turn.
  Dependency, shared-output, byte-identity, transactional, and documented correctness edges
  still serialize.
- Intra-agent concurrency inside a subagent's own execution (governed by that agent's own behaviour)
- Bash-level pipeline parallelism (e.g., `&` / `wait` in shell scripts)
