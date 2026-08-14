---
title: "Agent Workflow Orchestration Convention"
description: "Standards for how AI agents plan, execute, verify, and self-improve during multi-step tasks"
category: explanation
subcategory: development
tags:
  - ai-agents
  - workflow
  - orchestration
  - planning
  - verification
  - delegated-agents
created: 2026-03-09
when_to_use: Use when planning, delegating, verifying, or self-improving during a multi-step agent task.
---

# Agent Workflow Orchestration Convention

This document defines how AI agents plan, execute, verify, and improve their work during multi-step tasks. It covers when to enter plan mode, how to use delegated agents, how to manage task state, and how to verify completion before declaring a task done.

## Planning and Delegation

- [Principles Implemented/Respected](./agent-workflow-orchestration/01-principles-implemented-respected.md) — principle list.
- [Conventions Implemented/Respected](./agent-workflow-orchestration/02-conventions-implemented-respected.md) — sibling conventions.
- [When to Plan](./agent-workflow-orchestration/03-when-to-plan.md) — plan format, re-planning.
- [Delegated Agent Strategy](./agent-workflow-orchestration/04-delegated-agent-strategy.md) — when to delegate.

## Operating Budgets

- [Authoring and Propagating Repository Rules](./agent-workflow-orchestration/05-operating-budgets-authoring-repository-rules.md) — rule propagation.
- [Parallelism Budget](./agent-workflow-orchestration/06-operating-budgets-parallelism-budget.md) — concurrency cap.
- [DAG-First Orchestration and Background-Slot Preference](./agent-workflow-orchestration/07-operating-budgets-dag-first-and-background-slot.md) — sequencing.
- [Harness Capability Gating](./agent-workflow-orchestration/08-operating-budgets-harness-capability-gating.md) — capability checks.
- [The PR Is the Independent Merge Point](./agent-workflow-orchestration/09-operating-budgets-pr-independent-merge-point.md) — worktree isolation.
- [The PR Is the Independent Merge Point (Continued)](./agent-workflow-orchestration/10-operating-budgets-pr-independent-merge-point-continued.md) — per-repo scope.
- [CI and GitHub Actions Monitoring Cadence](./agent-workflow-orchestration/11-operating-budgets-ci-monitoring-cadence.md) — polling cadence.

## Verification and Bug Fixing

- [Verification Before Done](./agent-workflow-orchestration/12-verification-before-done.md) — pre-completion checks.
- [Autonomous Bug Fixing](./agent-workflow-orchestration/13-autonomous-bug-fixing.md) — expected behavior, CI failures.
- [Demand Elegance (Balanced)](./agent-workflow-orchestration/14-demand-elegance-balanced.md) — polish standard.

## Self-Improvement and Task Management

- [Self-Improvement Loop](./agent-workflow-orchestration/15-self-improvement-loop.md) — lessons file.
- [Task Management](./agent-workflow-orchestration/16-task-management.md) — planning, tracking, granular items.
- [Anti-Patterns](./agent-workflow-orchestration/17-anti-patterns.md) — orchestration mistakes.
- [References](./agent-workflow-orchestration/18-references.md) — related conventions.
