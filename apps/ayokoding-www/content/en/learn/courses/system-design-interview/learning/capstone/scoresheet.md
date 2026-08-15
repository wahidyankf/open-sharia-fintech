---
title: "Capstone Scoresheet"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 4
---

Score the walkthrough—or your own recording—from 1 to 4 and write one evidence sentence for each.

| Rubric axis                      | Score | Evidence                                                                             |
| -------------------------------- | ----: | ------------------------------------------------------------------------------------ |
| Scoping and requirements         |     4 | Names core behavior, exclusions, and product constraints before components.          |
| Estimation                       |     3 | Uses explicit illustrative volume and peak assumptions; retention needs validation.  |
| Breadth of high-level design     |     4 | Shows API, state, scheduled work, worker, provider, and status path.                 |
| Targeted depth                   |     4 | Deep-dives idempotency and ambiguous timeouts, then returns to the full flow.        |
| Communication and round control  |     4 | Opens with a plan and closes with a validation sequence.                             |
| Trade-off reasoning              |     4 | States cost and benefit for durable work and conservative retry behavior.            |
| Reliability and failure behavior |     4 | Covers provider slowness, bounded retries, reconciliation, and graceful degradation. |
| Observability and operability    |     4 | Names lag, throughput, error, and duplicate-suppression signals.                     |
| Senior/staff judgment            |     3 | Names cohort rollout, ownership, and cost; organization boundary needs more detail.  |

## Self-review prompts

- Did every major component earn its place from a requirement?
- Did I name what I do not know rather than invent a fact?
- Could a listener identify my bottleneck and two trade-offs without rereading the diagram?
- Did I state a reversible next step?
