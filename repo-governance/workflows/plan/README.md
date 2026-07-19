---
title: "Plan Workflows"
description: "Orchestrated workflows for plan creation, quality validation, and execution — from idea to archived delivery."
category: explanation
subcategory: workflows
tags: []
created: 2026-05-12
---

# Plan Workflows

Orchestrated workflows for project planning quality validation and systematic execution.

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

- [Plan Planning](./plan-planning.md) - Orchestrate the full prompt-to-pushed-plan
  lifecycle: repo exploration → grill → web research → grill → plan-maker → plan-quality-gate →
  push. Use when turning a behavioral prompt into a production-ready plan.
- [Plan Execution](./plan-execution.md) - Execute plan tasks systematically with validation and completion tracking; orchestrated directly by the calling context, validated by `plan-execution-checker`
- [Multi-Plans Execution](./multi-plans-execution.md) - Execute several plans together — named as an explicit list or a set-selector (`all-in-progress` / `all-backlog` / `all`, optionally minus an `except` list) resolved to a frozen set: build a dependency DAG (explicit `Depends-on` wins, resource-overlap inference fills gaps), materialize one very-granular union Task list, and run a bounded ready-queue scheduler (default 3 parallel nodes, overridable) that drives each plan through its full `plan-execution` lifecycle; failure quarantines a plan without cascading to independent ones
- [Plan Multi-Repo Parity Planning](./plan-multi-repo-parity-planning.md) - Author aligned-but-deliberately-divergent plans across multiple sibling repositories for a shared objective: survey → deviation matrix → first grill (hard gate) → web research → second grill → author → gate → deliver. Every cross-repo deviation reaches a recorded decision before authoring begins
- [Plan Multi-Repo Parity Planning and Execution](./plan-multi-repo-parity-planning-and-execution.md) - End-to-end composite: run the full parity planning workflow (both grills included), then a third pre-execution grill, then plan-execution per repo for every resulting plan — flattened granular Task list kept 1:1 with each delivery.md, archival, sibling-link repair, and prompted worktree cleanup
- [Plan Quality Gate](./plan-quality-gate.md) - Validate plan completeness and accuracy, apply fixes iteratively until ZERO findings using plan-checker and plan-fixer

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Plans Organization Convention](../../conventions/structure/plans.md) - Plan structure standards
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model
- [Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md) - Every
  grill question must present 2-4 concrete options; open-ended questions are forbidden
