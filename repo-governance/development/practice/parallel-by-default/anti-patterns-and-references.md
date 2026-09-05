---
title: "Parallel-by-Default — Anti-Patterns and References"
description: Four common failure patterns (serial reads, serial searches, self-promoting the cap, parallelizing dependent work) plus links to related principles, practices, and agents
category: explanation
subcategory: development
tags:
  - parallelism
  - concurrency
  - performance
  - ai-agents
  - efficiency
created: 2026-06-23
when_to_use: Use when reviewing your own execution pattern for one of these four failure modes, or to find related documentation.
---

# Anti-Patterns and References

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

- [Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md) - Bounded, pre-decided constraints over reactive improvisation
- [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md) - One declared agent cap, with child-resource admission owned by one scheduler
- [Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md) - Automated parallel execution over manually sequenced round-trips
- [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) - Documented constants, not inferred limits

**Related Practices:**

- [Subagent Orchestration Convention](../../agents/subagent-orchestration.md) - Concrete specialization of this norm for background Agent-tool spawns, using the same N (N+1 including the main thread); owns polling, stuck detection, and relaunch mechanics
- [Agent Workflow Orchestration Convention](../../agents/agent-workflow-orchestration.md) - Broader agent task management strategy of which parallel-by-default is one component; states the N+1 parallelism budget and the same-machine assumption that bounds N

**Agents:**

- `repo-rules-checker` - Validates convention compliance
- `repo-rules-maker` - Creates and updates conventions
