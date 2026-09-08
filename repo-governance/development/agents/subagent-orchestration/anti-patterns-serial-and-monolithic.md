---
description: "Covers running background work serially and assigning monolithic chunks to a single agent."
when_to_use: Use when reviewing whether work was needlessly serialized or a chunk was too large for one agent.
---

# Anti-Patterns — Running Serially and Monolithic Chunks

## Running Background Work Serially

**Problem**: The main agent runs background subagents one at a time — waiting for the first to finish before launching the second — even when independent units of work are ready simultaneously.

**Why it fails**: Serial execution wastes available throughput. If the units are independent and a background slot is free, holding it empty multiplies elapsed time for no benefit.

**Fix**: Keep all background slots full up to the declared **N** (the N+1 model: 1 main thread + N background agents, **default N=3**). When a slot frees and independent work is waiting, launch immediately. Never split dependent work merely to fill a slot, and never self-promote beyond the declared N.

## Monolithic Chunks Assigned to Single Agents

**Problem**: The main agent assigns 20 or 30 examples to a single background agent to minimize spawning overhead.

**Why it fails**: Large chunks produce long-running agents that either exhaust their output-token budget mid-way (causing the stuck condition) or require the main agent to wait a long time before observing any output. When they stall, the entire chunk must restart.

**Fix**: Target 3–10 minute runtime per agent. Size chunks empirically for each agent type.
