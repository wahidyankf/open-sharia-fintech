---
name: plan-multi-repo-parity-planning-and-execution
title: "plan-multi-repo-parity-planning-and-execution"
description: End-to-end composite that plans then executes a cross-repo parity objective in one run.
when_to_use: Use when a cross-repo objective should be planned AND delivered in one continuous run.
goal: Author aligned-but-deliberately-divergent plans across sibling repositories for a shared objective, then execute every resulting plan to zero-findings completion and archival — one end-to-end orchestration from idea to delivered parity
termination: "Every parity plan passes plan-quality-gate (double-zero), every plan executes to zero findings via plan-execution, every plan is archived to plans/done/ in its repo with all work pushed, and every plan worktree is cleaned up (or retained by explicit user choice)"
inputs:
  - name: objective
    type: string
    description: "The shared topic to standardize or align across repos (e.g., 'standardize markdown gates', 'align agent catalogs')"
    required: true
  - name: repos
    type: string
    description: "Comma-separated target repository names or absolute paths in the parity set"
    required: false
    default: "ose-public, ose-private"
  - name: mode
    type: enum
    values: [main-to-origin-main, worktree-to-origin-main]
    description: "Planning-phase delivery mode passed to plan-multi-repo-parity-planning. worktree-to-pr is NOT supported by this composite — execution cannot start on plans that are awaiting PR review (use the planning workflow alone for that)"
    required: false
    default: worktree-to-origin-main
  - name: gate-mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Mode passed through to plan-quality-gate for each plan"
    required: false
    default: strict
  - name: max-iterations
    type: number
    description: Maximum execute-check cycles per plan during the execution phase (passed to plan-execution)
    required: false
    default: 10
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
  - name: execution-order
    type: string
    description: "Repo execution order for the execution phase; confirmed in the pre-execution grill"
    required: false
    default: "as listed in repos"
outputs:
  - name: plans-created
    type: file-list
    description: One plan folder path per target repo (archived to plans/done/ on success)
  - name: gate-results
    type: string
    description: "plan-quality-gate final status per plan (pass/partial/fail)"
  - name: execution-results
    type: string
    description: "plan-execution final status per repo (pass/partial/fail) with iterations-completed"
  - name: delivery-refs
    type: string
    description: "Commits pushed to each repo's origin main during planning and execution phases"
---

# Plan Multi-Repo Parity Planning and Execution Workflow

Plans then executes a cross-repo parity objective in one run.

## Contents

- [Purpose & Scope](./plan-multi-repo-parity-planning-and-execution/purpose-scope-and-when-to-use.md) — why this exists.
- [Execution Mode & Tasks](./plan-multi-repo-parity-planning-and-execution/execution-mode-and-task-list-contract.md) — orchestration, Task list.
- [Step 1 — Planning](./plan-multi-repo-parity-planning-and-execution/step-1-planning-phase.md) — nested workflow.
- [Steps 2-3 — Gate & Grill](./plan-multi-repo-parity-planning-and-execution/step-2-and-3-phase-gate-and-pre-execution-grill.md) — readiness, third grill.
- [Step 4 — Execution](./plan-multi-repo-parity-planning-and-execution/step-4-execution-phase.md) — plan-execution per repo.
- [Step 4 — Execution (cont.)](./plan-multi-repo-parity-planning-and-execution/step-4-execution-phase-continued.md) — propagation, manifest gate.
- [Step 5 — Finalization](./plan-multi-repo-parity-planning-and-execution/step-5-cross-repo-finalization.md) — sibling links, report.
- [Termination & Grilling](./plan-multi-repo-parity-planning-and-execution/termination-criteria-and-grilling-contract.md) — outcomes, three grills.
- [Example Usage](./plan-multi-repo-parity-planning-and-execution/example-usage.md) — two worked examples.
- [Safety & Related](./plan-multi-repo-parity-planning-and-execution/safety-features-and-related-workflows.md) — guarantees, links.
- [Principles & Conventions](./plan-multi-repo-parity-planning-and-execution/principles-conventions-and-agents.md) — governance, agents.
