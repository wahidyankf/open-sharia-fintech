---
title: "Plan Workflows"
description: "Orchestrated workflows for plan creation, quality validation, and execution — from idea to archived delivery."
when_to_use: Use when routing to a workflow that authors, validates, executes, or takes over a project plan.
category: explanation
subcategory: workflows
tags: []
created: 2026-05-12
---

# Plan Workflows

Use these workflows to turn an idea into a well-grounded, checkable delivery plan, then carry it through execution without losing the evidence behind each decision.

## Purpose

These workflows define **WHEN and HOW to establish, validate, and execute plans**. The
plan-establishment workflow orchestrates the full prompt-to-pushed-plan lifecycle (repo
exploration → grill → research → plan-maker → quality gate → push). The plan-quality-gate
workflow orchestrates `plan-checker` and `plan-fixer` for authoring-time validation. The
plan-execution workflow is orchestrated directly by the calling context (which delegates
per-item work to specialized agents) and invokes `plan-execution-checker` for independent
validation at the end.

## Scope

**✅ Workflows Here:**

- Plan quality validation
- Plan execution tracking
- Iterative plan improvement
- Multi-agent orchestration for plans/
- Check-fix-verify and execution cycles

**❌ Not Included:**

- Content quality validation (that's docs/)
- ayokoding-web content validation (that's ayokoding-web/)
- Single-agent operations (use agents directly)

## Workflows

- [plan-planning](./plan-planning.md) — Orchestrates a user prompt through repo exploration, two grill sessions, optional web research, plan-maker delegation, structural review, and the plan-quality-gate into a pushed, validated plan. Use when a user describes a new behavior, pattern, or convention to adopt and needs it turned into a validated, execution-ready plan in plans/in-progress/ or plans/backlog/.
- [plan-idea-promotion-planning](./plan-idea-promotion-planning.md) — Promotes one ripe two-pager idea brief into a mature-core backlog plan, gated, researched, and retired atomically. Use when a two-pager in plans/ideas/ has matured and should become a scheduled backlog plan.
- [plan-handover-execution](./plan-handover-execution.md) — Writes a structured handover document capturing an in-progress plan's state for the next agent, session, or human. Use when stepping away from an in-progress plan and prior session context would otherwise be lost.
- [plan-takeover-execution](./plan-takeover-execution.md) — Discovers, reconciles, and takes over a plan's in-flight state across repos before handing off to plan-execution.md. Use before plan-execution.md when the plan might already be worked somewhere; skip for a brand-new plan.
- [plan-execution](./plan-execution.md) — Executes a project plan end-to-end — orchestration, delegation, quality gates, iteration, archival — split into per-topic children. Use when executing a plan, or looking up one step (worktree entry, a quality gate, finalization) of that execution.
- [multi-plans-execution](./multi-plans-execution.md) — Schedules several ready plans together via a dependency DAG and bounded parallelism. Use when two or more gated plans should run together, not one at a time.
- [plan-multi-repo-parity-planning](./plan-multi-repo-parity-planning.md) — Authors aligned-but-divergent plans across sibling repos, grilling every deviation to a decision. Use when a change spans sibling repos and drift between them must not be silent.
- [plan-multi-repo-parity-planning-and-execution](./plan-multi-repo-parity-planning-and-execution.md) — End-to-end composite that plans then executes a cross-repo parity objective in one run. Use when a cross-repo objective should be planned AND delivered in one continuous run.
- [plan-quality-gate](./plan-quality-gate.md) — Iteratively runs plan-checker and plan-fixer against a plan's documents until zero threshold-level findings are confirmed on two consecutive checks, or max-iterations is reached. Use before starting plan execution, after creating or updating a plan, or periodically to re-validate plan completeness and technical accuracy.
- [plan-ideas-grooming](./plan-ideas-grooming.md) — Sweeps plans/ideas/ across repos, deduplicating, classifying into Eisenhower quadrants, and correcting cross-repo residency. Use when a repo's plans/ideas/ exceeds 60 files or 90 days have passed since the last grooming run.

## Orchestration Model Shared by These Workflows

Every workflow in this directory fans out under the **N+1 model** — `1 main thread + N background
agents = N+1 total`, default **N=3**, with the main thread kept vacant as orchestrator. Ordering is
**DAG-first**: a plan's `## Parallelization Model` declares which nodes are independent, independent
nodes fan out up to N, and dependent nodes serialize — sequence is not dependency. Delivery is
**1-PR↔1-branch↔1-delivery-unit**: each independent node gets its own branch and PR, opened and
merged at that unit's **delivery boundary** rather than at every phase or batched at plan end, with
cleanup as the DAG's terminal node. The **worktree** is a coarser unit — capped at one per repository
per plan and reused across every node landing in that repo, per
[Plans Organization Convention §Worktree Cap](../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Plans Organization Convention](../../conventions/structure/plans.md) - Plan structure standards
- [Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md) - The N+1 model, DAG-first ordering, and background-slot preference these workflows inherit
- [No Destructive Git Operations](../../development/workflow/no-destructive-git-operations.md) - Forbidden operations on the shared machine and the non-destructive equivalent for each
- [Worktree and Artifact Cleanup](../../development/workflow/worktree-and-artifact-cleanup.md) - The plan-end cleanup gate across worktrees, branches, and build output
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model
- [Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md) - Every
  grill question must present 2-4 concrete options; open-ended questions are forbidden
