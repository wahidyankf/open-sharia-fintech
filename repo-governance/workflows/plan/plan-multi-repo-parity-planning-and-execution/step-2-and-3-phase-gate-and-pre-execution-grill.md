---
description: The hard-gate check that every plan is execution-ready, followed by the third (pre-execution) grill on order, failure policy, and worktree cleanup.
when_to_use: Use before starting the execution phase, to verify readiness and record the operational decisions that govern it.
---

# Step 2 — Phase Gate: Plans Ready for Execution (Hard Gate)

Before any execution, verify for EVERY target repo:

1. The plan folder exists at `plans/in-progress/<objective-slug>/` with the mature core and exactly
   one reader-led technical form.
2. The plan received a `PASS` verdict from plan-quality-gate.
3. The planning-phase commits are on that repo's `origin main` (`git fetch origin && git log
origin/main --oneline -5` shows the plan delivery commits).
4. The plan declares its `## Worktree` section per
   [Plans Organization Convention §Worktree Specification](../../../conventions/structure/plans/worktree-specification.md#worktree-specification).

**If any check fails for any repo**: STOP. Surface the failing repo and check. Do not execute a
subset silently — the invoker decides whether to fix and re-gate or abandon.

**Output**: All plans verified execution-ready.

## Step 3 — Pre-Execution Grill (Third Grill, Hard Gate)

The composite grills three times: the planning phase's matrix grill and post-research grill, then
this pre-execution grill. Invoke the `grill-me` skill per the
[Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md) — every
question presents 2-4 concrete options with trade-offs and exactly one **(Recommended)**; one
question per message; interactive multiple-choice tool when available.

**Mandatory questions** (plus any opened by the answers):

1. **Execution DAG**: which plan nodes are initially ready, and which cross-repository edges are
   required? Options must be grounded in the deviation matrix. Portable public-to-private and Rhino
   propagation keep the public source node ahead of its private consumer **(Recommended)**; a
   repo-specific node with no such edge may enter the ready set immediately. Do not turn a preferred
   review order into a dependency or serialize a whole repository when only one node is constrained.
2. **Failure policy**: if any node ends `partial`/`fail`, do we stop new scheduling across the
   composite **(Recommended)** or continue only independent ready nodes and report at the end?
3. **Unresolved design decisions**: per plan-execution's pre-execution requirement, stress-test
   any decision the plans left open — one question per open decision, options from the plan's
   tech-docs.
4. **`[HUMAN]` step availability**: the delivery checklists may contain `[HUMAN]` gates; is the
   invoker available to confirm them during this run, or should execution stop at the first
   `[HUMAN]` item and resume later?
5. **Worktree cleanup evidence**: confirm each plan has a Provisioned Worktree Identity recording
   its repository-relative route, branch, and creator. After delivery, the executor resolves that
   route against the selected repository and removes only the reconciled worktree
   when replacement proof, the terminal audit in `{final-report}`, final `pass`, clean/idle, and
   no-unpushed checks all pass. A failed terminal or safety check retains it, reopens execution, and
   escalates. This is not a preference or confirmation gate.
6. **Cross-repository parity identity**: confirm every plan carries the same objective slug and
   worktree basename, and that corresponding short-lived branch names match. Probe ownership and
   stop on an unavailable or silently divergent identity before execution mutation.

**Hard gate**: execution does not begin while any question is unresolved. On invoker abandonment,
terminate with status `fail` — the gated plans remain in `plans/in-progress/` for a later
standalone plan-execution run.

**Output**: Confirmed execution DAG, failure policy, and resolved open decisions.
