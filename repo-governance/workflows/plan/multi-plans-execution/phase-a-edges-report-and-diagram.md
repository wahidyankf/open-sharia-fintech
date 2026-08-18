---
title: "Phase A — Load Plans and Build the Dependency DAG (Edges, Report, and Diagram)"
description: Covers A4-A7 — inter-plan edges, resource-sets, and the DAG report.
when_to_use: Use when computing ordering edges or reading the DAG report.
---

# Phase A — Load Plans and Build the Dependency DAG (Edges, Report, and Diagram)

Continued from
[Phase A — Scope and Nodes](./phase-a-scope-and-nodes.md).

**A4. Add intra-plan edges (ordering within a plan).** Within a single plan, nodes are ordered by:
(a) the worktree-enter / setup step first; (b) TDD ordering — a phase's `RED` → `GREEN` → `REFACTOR`
sub-steps are strictly sequential; (c) phase gates — a phase's gate node depends on all nodes in that
phase, and the next phase depends on the gate; (d) the archival node last. The default is
**sequential within a plan** unless the plan's own text explicitly marks two phases/steps as
independent. This preserves every per-plan Iron Rule (TDD, one-`in_progress`-per-plan, atomic sync).

**A5. Compute each node's resource-set (conservative).** From the checkbox's named file paths and
the plan's `tech-docs.md` File-Impact Analysis, derive the set of resources the node touches: file
paths / globs, Nx project names, the target repo(s), and a **byte-identity flag** if any path falls
under the `apps/rhino-cli/**` [byte-identity boundary](../../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary).
When a node's footprint is ambiguous, treat it as touching its whole plan's declared file-impact
set — **safety-first: uncertain nodes are treated as conflicting, never as disjoint.**

**A6. Add inter-plan edges (Hybrid ordering).**

1. **Explicit `Depends-on:` wins.** If a plan's `README.md` declares `Depends-on: [<plan-id>, …]`,
   that whole plan is serialized after every named dependency (all of the dependency's nodes precede
   any of this plan's nodes). Explicit declarations are authoritative and never overridden by
   inference.
2. **Inference fills the gaps.** For any pair of plans with no explicit relationship, infer edges
   from **resource overlap**: two nodes whose resource-sets intersect (same file/glob, same Nx
   project, or both carry the byte-identity flag on `apps/rhino-cli/**`) **conflict** and must not run
   concurrently — the scheduler serializes them (the later-scheduled one waits). Nodes with disjoint
   resource-sets are **parallelizable**. Two plans that both touch `apps/rhino-cli/**` are always
   serialized at least at their overlapping nodes, because byte-identical propagation across
   `ose-public`/`ose-private` cannot tolerate two concurrent divergent edits.
3. **Cycle check.** If explicit `Depends-on` declarations form a cycle, stop and report — a cyclic
   plan graph is a planning error, not something to schedule around.

**A7. Emit the DAG / parallelizability report** to
`generated-reports/multi-plans-execution__<uuid>__<timestamp>__dag.md`: the node list per plan, the
intra- and inter-plan edges, each node's resource-set, and — explicitly — which nodes are marked
**PARALLELIZABLE** vs **SEQUENTIAL** and why. If `mode: plan-only`, STOP here and hand the report to
the caller for review.

```mermaid
flowchart TD
  subgraph Legend
    L1[SEQUENTIAL edge]:::seq
    L2[PARALLELIZABLE nodes]:::par
  end
  A0[planA P0 worktree] --> A1[planA P1 RED]:::seq
  A1 --> A2[planA P1 GREEN]:::seq
  B0[planB P0 worktree]:::par --> B1[planB P1 impl]:::par
  A2 -->|shares rhino-cli| C1[planC rhino step waits]:::seq
  classDef seq fill:#0072B2,stroke:#001f3f,color:#ffffff
  classDef par fill:#009E73,stroke:#003b2b,color:#ffffff
```

> **Pause Safety**: safe to stop after Phase A. Nothing has been executed; only the schedule exists.
