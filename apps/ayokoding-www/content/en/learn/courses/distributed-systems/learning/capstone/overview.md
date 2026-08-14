---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Build a local, simulated replicated key-value store with explicit AP-leaning quorum/read-repair and
CP leader-elected modes. Inject loss, delay, and a partition; write assertions for the different
promises each mode makes.

## Build sequence

1. Add vector-clock metadata and tests for causal versus concurrent writes.
2. Add a quorum store and read repair; demonstrate `R + W > N` and a sub-quorum stale read.
3. Add a term-scoped leader-election and log-replication model; demonstrate one leader per term.
4. Partition the simulated network and assert CP blocking versus AP local availability followed by convergence.

## Acceptance criteria

- The clock classification distinguishes causality from concurrency.
- Quorum behavior is stated and tested, including its stale-read counterexample.
- The leader model rejects stale authority and converges followers after healing.
- The partition test demonstrates the advertised behavior without claiming production equivalence.
