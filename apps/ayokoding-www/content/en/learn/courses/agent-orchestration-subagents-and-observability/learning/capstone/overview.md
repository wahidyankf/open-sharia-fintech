---
title: "Capstone: Observable Orchestrated Agent"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

Build a local orchestrator that delegates bounded work through one sequential chain and one parallel
fan-out, aggregates summaries, and handles a partial failure. Add lifecycle hooks, a terminal
interaction model with an approval boundary, trace spans, structured logs, cost and latency metrics,
and a local regression-eval signal.

## Acceptance criteria

- Each subagent returns a bounded summary; parent state excludes exploration detail.
- The orchestrator records sequential and parallel work, including a handled worker failure.
- Hooks and terminal interaction expose lifecycle and approval decisions without changing the core.
- A run produces a complete trace tree and compact metrics summary.
- A local eval signal detects a planted regression; deeper eval construction is forward-linked.
