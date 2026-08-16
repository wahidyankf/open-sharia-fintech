---
name: plan-multi-repo-parity-planning
title: "plan-multi-repo-parity-planning"
description: Authors aligned-but-divergent plans across sibling repos, grilling every deviation to a decision.
when_to_use: Use when a change spans sibling repos and drift between them must not be silent.
goal: Author aligned-but-deliberately-divergent plans across multiple sibling repositories for a shared objective, with every cross-repo deviation grilled, decided, and durably documented
termination: "One plan per target repo exists, each passes plan-quality-gate (double-zero), every deviation-matrix cell carries a recorded decision, research findings are incorporated or skipped with justification, and delivery completed per the selected mode"
inputs:
  - name: objective
    type: string
    description: "The shared topic to standardize or align across repos (e.g., 'standardize markdown gates', 'align agent catalogs')"
    required: true
  - name: repos
    type: string
    description: "Comma-separated target repository names or absolute paths in the parity set (e.g., 'ose-public, ose-private')"
    required: false
    default: "ose-public, ose-private"
  - name: mode
    type: enum
    values: [main-to-origin-main, worktree-to-origin-main, worktree-to-pr]
    description: "Where plans are authored and how they are delivered (see Modes section)"
    required: false
    default: worktree-to-pr
  - name: stage
    type: enum
    values: [in-progress, backlog]
    description: "Plan stage folder in each target repo"
    required: false
    default: in-progress
  - name: gate-mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Mode passed through to plan-quality-gate for each plan"
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: plans-created
    type: file-list
    description: One plan folder path per target repo
  - name: deviation-matrix
    type: file
    description: "Cross-repo decision matrix (every gap mapped to an align/deviate decision with justification), embedded in each plan's tech-docs.md and mirrored in each repo's explanation rationale doc"
  - name: gate-results
    type: string
    description: "plan-quality-gate final status per plan (pass/partial/fail)"
  - name: delivery-refs
    type: string
    description: "Commits pushed to origin main (main-push modes) or PR URLs (worktree-to-pr)"
---

# Plan Multi-Repo Parity Planning Workflow

Authors one plan per sibling repo, grilling every cross-repo gap first.

## Contents

- [Purpose & Scope](./plan-multi-repo-parity-planning/01-purpose-scope-and-when-to-use.md) — why this exists.
- [Execution Mode](./plan-multi-repo-parity-planning/02-execution-mode.md) — orchestrator steps.
- [Propagation & Safety](./plan-multi-repo-parity-planning/03-propagation-delivery-and-machine-safety.md) — fan-out, PR shape.
- [Invocation & Modes](./plan-multi-repo-parity-planning/04-invocation-point-and-modes-overview.md) — anchor repo, direct-push modes.
- [`worktree-to-pr` Default](./plan-multi-repo-parity-planning/05-modes-worktree-to-pr-default.md) — default mode.
- [Delivery Mode Relationship](./plan-multi-repo-parity-planning/06-relationship-to-delivery-mode.md) — vs. plan's own mode.
- [Step 1 — Survey](./plan-multi-repo-parity-planning/07-step-1-parity-set-survey.md) — state inventory.
- [Step 2 — Matrix](./plan-multi-repo-parity-planning/08-step-2-gap-and-deviation-matrix.md) — deviation matrix.
- [Step 3 — Grill](./plan-multi-repo-parity-planning/09-step-3-first-grill.md) — resolve every row.
- [Step 3 — Meta-Questions](./plan-multi-repo-parity-planning/10-step-3-first-grill-meta-questions.md) — mandatory asks.
- [Steps 4-5 — Research & Grill](./plan-multi-repo-parity-planning/11-step-4-and-5-research-and-second-grill.md) — validate direction.
- [Step 6 — Authoring](./plan-multi-repo-parity-planning/12-step-6-plan-authoring.md) — plan-maker handoff.
- [Step 6 — Required Contents](./plan-multi-repo-parity-planning/13-step-6-plan-authoring-required-contents.md) — matrix, links.
- [Steps 7-8 — Gate & Delivery](./plan-multi-repo-parity-planning/14-step-7-and-8-quality-gate-and-delivery.md) — gate, deliver.
- [Termination & Grilling](./plan-multi-repo-parity-planning/15-termination-criteria-and-grilling-contract.md) — outcomes.
- [Example Usage](./plan-multi-repo-parity-planning/16-example-usage.md) — worked runs.
- [Safety & Related](./plan-multi-repo-parity-planning/17-safety-features-and-related-workflows.md) — guarantees, links.
- [Principles & Conventions](./plan-multi-repo-parity-planning/18-principles-and-conventions.md) — governance.
