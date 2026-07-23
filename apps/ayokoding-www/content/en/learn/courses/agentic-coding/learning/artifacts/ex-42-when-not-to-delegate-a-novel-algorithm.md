---
title: "Artifact: Abandoned Delegation of a Novel Scheduling Algorithm"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 82
---

> An attempted delegation of a genuinely novel scheduling algorithm, abandoned in favor of
> hand-writing it, with the rationale recorded -- exercises co-22.

```text
[Prompt given]: "Design an algorithm assigning delivery drivers to pickups
across 3 depots, minimizing total driver idle time, where a driver can serve
any depot but switching depots costs a fixed 20-minute penalty."

[Agent's proposal]: a greedy nearest-idle-driver assignment, presented
confidently with a claimed near-optimal result on the stated constraints.

[Hand-check on a small 4-driver / 6-pickup case]:
  Greedy assignment total idle time:        146 minutes
  Five-minute hand-computed alternative:     98 minutes
  -- the greedy approach is not "near-optimal" on even this small case; it is
  clearly beaten by a schedule found by hand in under five minutes.
```

**Decision**: abandon delegation, hand-write the assignment for the actual production scale
instead of continuing to iterate with the agent on this constraint.

**Written rationale, as recorded**: "Declined delegation: this is a genuinely novel multi-depot
constraint with no known standard algorithm to check the agent's greedy approach against. The
agent's proposed greedy assignment produced a demonstrably worse schedule than a five-minute
hand-computed alternative on a small test case -- meaning even its confidently-stated
near-optimality claim was wrong. Because there is no existing correct implementation to diff
against and the real search space is too large to hand-verify at production scale, delegating this
core logic would trade away the only thing that makes verification possible here: my own
understanding of why any accepted schedule is even approximately correct. Writing it by hand
instead, at a scale small enough to reason about directly."

**Verify**: the written rationale explicitly names why delegation was declined -- no algorithm
exists to check the proposal against, and the proposal already failed a small, hand-verifiable
case -- satisfying ex-42's rule that a written rationale records why delegation was declined.
