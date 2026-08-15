---
title: "Orchestration and Background Work"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Theme B covers source Examples 13–24 with credential-free standard-library simulations.

### Example 13: Build a Sequential Pipeline

**Brief explanation**: Each agent step consumes the previous step's result.

**Code**: Run `python3 code/ex-13-sequential-pipeline/example.py`.

**Expected observation**: Three ordered stages produce one final value.

**Key takeaway**: Dependencies require sequence.

**Why it matters**: Parallelizing dependent work creates invalid inputs.

### Example 14: Run a Parallel Fan-Out

**Brief explanation**: Independent workers can run concurrently before a join.

**Code**: Run `python3 code/ex-14-parallel-fanout/example.py`.

**Expected observation**: Three results arrive from one gather call.

**Key takeaway**: Parallelism is for independent work.

**Why it matters**: Fan-out reduces waiting when no dependency exists.

### Example 15: Aggregate Parallel Results

**Brief explanation**: An orchestrator merges independently returned summaries into a coherent result.

**Code**: Run `python3 code/ex-15-aggregate-parallel-results/example.py`.

**Expected observation**: Named worker values become one mapping.

**Key takeaway**: Aggregation must preserve source identity.

**Why it matters**: Unattributed results cannot be reviewed or retried safely.

### Example 16: Use a Hierarchical Orchestrator

**Brief explanation**: A coordinator plans, dispatches workers, and collects their summaries.

**Code**: Run `python3 code/ex-16-hierarchical-orchestrator/example.py`.

**Expected observation**: The trace is `plan`, `dispatch`, then `collect`.

**Key takeaway**: Hierarchy separates coordination from execution.

**Why it matters**: A worker should not need the whole system plan.

### Example 17: Poll a Background Task

**Brief explanation**: A long operation can progress separately while the main interaction remains active.

**Code**: Run `python3 code/ex-17-background-task/example.py`.

**Expected observation**: The task changes from pending to done.

**Key takeaway**: Background work needs explicit lifecycle state.

**Why it matters**: A responsive parent must observe work without blocking on it.

### Example 18: Recover from a Worker Failure

**Brief explanation**: A failed worker becomes a partial result rather than a whole-run collapse.

**Code**: Run `python3 code/ex-18-orchestration-failure-recovery/example.py`.

**Expected observation**: One value and one error appear in the result.

**Key takeaway**: Orchestrators own partial-failure policy.

**Why it matters**: Multi-worker systems always need a failure path.

### Example 19: Cap Concurrent Subagents

**Brief explanation**: A semaphore bounds how many workers may hold shared capacity.

**Code**: Run `python3 code/ex-19-concurrency-cap/example.py`.

**Expected observation**: The observed maximum is two.

**Key takeaway**: Fan-out must be admission-controlled.

**Why it matters**: Unlimited concurrency increases cost and overload risk.

### Example 20: Compare Orchestration Shapes

**Brief explanation**: A local flow record contrasts sequential, parallel, and hierarchical patterns.

**Code**: Run `python3 code/ex-20-orchestration-diagram/example.py`.

**Expected observation**: All three shapes are named.

**Key takeaway**: Structure follows dependency and ownership.

**Why it matters**: Pattern choice affects failure and latency behavior.

### Example 21: Map-Reduce over Files

**Brief explanation**: Per-file workers map local summaries, then a reducer combines them.

**Code**: Run `python3 code/ex-21-map-reduce-over-files/example.py`.

**Expected observation**: Every fixture file appears in the reduction.

**Key takeaway**: Fan-out needs an explicit reduction step.

**Why it matters**: A list of worker results is not yet a useful parent answer.

### Example 22: Apply Retry and Fallback Policy

**Brief explanation**: A bounded retry precedes a deterministic fallback.

**Code**: Run `python3 code/ex-22-retry-and-fallback-policy/example.py`.

**Expected observation**: The failed first attempt returns the fallback.

**Key takeaway**: Recovery policy must be finite and inspectable.

**Why it matters**: Endless retries turn transient faults into runaway cost.

### Example 23: Report Orchestration Cost

**Brief explanation**: A run reports cost and latency across its coordinated workers.

**Code**: Run `python3 code/ex-23-orchestration-cost-report/example.py`.

**Expected observation**: The report totals local cost and latency fields.

**Key takeaway**: Coordination has an operational price.

**Why it matters**: Metrics reveal when a single agent is the better design.

### Example 24: Contrast Single and Multi-Agent Work

**Brief explanation**: A small task can be cheaper inline than after orchestration overhead.

**Code**: Run `python3 code/ex-24-single-vs-multi-agent-contrast/example.py`.

**Expected observation**: The single-agent cost is lower for the fixture task.

**Key takeaway**: Multi-agent design is conditional, not default.

**Why it matters**: Complexity must earn its keep.
