---
title: "Example Usage"
description: Walks through four invocation examples (default, extended iterations, from backlog, quick validation) and one full iteration trace.
when_to_use: Use when learning how to invoke plan execution with different arguments, or tracing a typical execute-validate cycle.
---

# Example Usage

## Execute Plan with Default Settings

```
User: "Execute plan plans/in-progress/new-feature/plan.md"
```

The calling context orchestrates directly and invokes specialized agents via the Agent tool (default max 10 iterations):

- Read delivery checklist and materialize 1:1 Task list in the calling context
- Delegate each item to the appropriate specialized agent (e.g., `swe-typescript-dev`)
- Tick checkboxes progressively as each item completes (Atomic Sync Ritual)
- Validate implementation by invoking `plan-execution-checker` delegated agent
- Iterate until zero findings and all deliverables complete
- Move plan folder to plans/done/ on success

## Execute with Extended Iterations

```
User: "Execute plan plans/in-progress/complex-migration/plan.md with max-iterations=15"
```

The AI will invoke agents with extended iteration limit:

- Allow up to 15 execute-validate cycles for complex plans
- Suitable for large migrations or multi-phase implementations

## Execute Plan from Backlog

```
User: "Execute plan plans/backlog/future-feature/plan.md"
```

The AI runs Step 0 first, on the local `main` checkout, before any implementation begins:

- `git mv plans/backlog/future-feature/ plans/in-progress/future-feature/`
- Commit the move and push directly to `origin main`
- Only then resolve `plan-path` to `plans/in-progress/future-feature/plan.md` and continue with
  Step 1 (enter the work branch) onward
- Implement plan requirements via orchestrated specialized agents
- Won't move to done until zero findings achieved
- Plan archived to plans/done/ only on complete success

Execution never runs directly out of `plans/backlog/` — the promotion commit+push is a mandatory
precondition, not an optional courtesy.

## Quick Validation Only

```
User: "Execute plan plans/in-progress/new-feature/plan.md with max-iterations=1"
```

The AI will invoke agents for a single cycle:

- Single execute-validate cycle
- Reports findings without further iteration
- Useful for quick validation pass

## Iteration Example

Typical execution flow:

```
Step 1: Load checklist — 12 items across 3 phases, 12 tasks created

Step 2: Execute all items sequentially
  Phase 1 (Infrastructure):
    Item 1 → swe-typescript-dev → checkbox ticked
    Item 2 → swe-typescript-dev → checkbox ticked
    Item 3 → docs-maker              → checkbox ticked
  Phase 2 (Implementation):
    Item 4 → swe-typescript-dev → checkbox ticked
    Item 5 → swe-e2e-dev   → checkbox ticked
    Item 6 → swe-rust-dev       → checkbox ticked
    ...and so on without stopping between phases

Step 3: Validate → 4 findings (quality issues, missing tests)

Step 5: Address findings
  Finding 1 → swe-typescript-dev → resolved
  Finding 2 → swe-e2e-dev   → resolved
  Finding 3 → docs-maker               → resolved
  Finding 4 → swe-typescript-dev → resolved

Step 6: Re-validate → 0 findings

Result: SUCCESS → Plan moved to plans/done/
```
