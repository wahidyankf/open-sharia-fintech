---
title: "Standard 5 — Status-Update Cadence (Continued)"
description: "Continues Standard 5 with the rationale for the split, how it refines prior guidance, and worked examples."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when justifying why the status-update cadence differs from the stuck-detection polling cadence.
---

# Standard 5 — Status-Update Cadence (Continued)

## Rationale for the Split

CI state changes fast and a failure blocks delivery immediately, so it earns the tighter 3-minute cadence — the user needs to know quickly if a check goes red. Generic background work (subagent batches, refactors, doc sweeps) moves more slowly and rarely turns urgent between one poll and the next, so a more frequent update would be pure noise.

## Refines, Does Not Replace, the Prior Guidance

This Standard replaces the previously vague "every 3-5 minutes, not faster" guidance by **assigning** the two ends of that range to specific kinds of work — 3 minutes for CI-related batches, 5 minutes for generic batches — rather than leaving the choice open to judgment call. It is a refinement, not a contradiction: both values sit inside the old range.

## Examples

```
PASS: CI-related batch → report at 3-min intervals while polling CI status every 2 min
PASS: Generic subagent batch (no CI items) → report at 5-min intervals
PASS: Mixed batch (one CI item, three generic items) → report at 3-min intervals
FAIL: Agents in flight for 20 minutes with no status update to the user
FAIL: Main agent posts a status update every 30 seconds → excessive chatter
FAIL: Mixed CI+generic batch reported at 5-min intervals → CI item's tighter cadence ignored
```
