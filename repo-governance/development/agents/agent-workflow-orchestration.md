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

- [Principles Implemented/Respected](./agent-workflow-orchestration/principles-implemented-respected.md) — principle list.
- [Conventions Implemented/Respected](./agent-workflow-orchestration/conventions-implemented-respected.md) — sibling conventions.
- [When to Plan](./agent-workflow-orchestration/when-to-plan.md) — plan format, re-planning.
- [Delegated Agent Strategy](./agent-workflow-orchestration/delegated-agent-strategy.md) — when to delegate.

## Operating Budgets

- [Authoring and Propagating Repository Rules](./agent-workflow-orchestration/operating-budgets-authoring-repository-rules.md) — rule propagation.
- [Parallelism Budget](./agent-workflow-orchestration/operating-budgets-parallelism-budget.md) — concurrency cap.
- [DAG-First Orchestration and Background-Slot Preference](./agent-workflow-orchestration/operating-budgets-dag-first-and-background-slot.md) — sequencing.
- [Harness Capability Gating](./agent-workflow-orchestration/operating-budgets-harness-capability-gating.md) — capability checks.
- [The PR Is the Independent Merge Point](./agent-workflow-orchestration/operating-budgets-pr-independent-merge-point.md) — worktree isolation.
- [The PR Is the Independent Merge Point (Continued)](./agent-workflow-orchestration/operating-budgets-pr-independent-merge-point-continued.md) — per-repo scope.
- [CI and GitHub Actions Monitoring Cadence](./agent-workflow-orchestration/operating-budgets-ci-monitoring-cadence.md) — polling cadence.

## Verification and Bug Fixing

- [Verification Before Done](./agent-workflow-orchestration/verification-before-done.md) — pre-completion checks.
- [Autonomous Bug Fixing](./agent-workflow-orchestration/autonomous-bug-fixing.md) — expected behavior, CI failures.
- [Demand Elegance (Balanced)](./agent-workflow-orchestration/demand-elegance-balanced.md) — polish standard.

## Self-Improvement and Task Management

- [Self-Improvement Loop](./agent-workflow-orchestration/self-improvement-loop.md) — lessons file.
- [Task Management](./agent-workflow-orchestration/task-management.md) — planning, tracking, granular items.
- [Continuation-State Integrity](./agent-workflow-orchestration/continuation-state-integrity.md) — preserves active user-established rule decisions across compaction and handoff.
- [Anti-Patterns](./agent-workflow-orchestration/anti-patterns.md) — orchestration mistakes.
- [References](./agent-workflow-orchestration/references.md) — related conventions.
