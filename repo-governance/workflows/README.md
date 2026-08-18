---
title: "Workflows"
description: Orchestrated multi-step processes that compose agents, procedures, and/or other workflows to achieve specific goals
when_to_use: Use when routing to the workflow that orchestrates a specific multi-step task, or when deciding whether a task should become a new workflow.
category: explanation
subcategory: workflows
tags:
  - index
  - workflows
  - orchestration
  - agents
created: 2026-01-04
---

# Workflows Index

**Purpose**: Repeatable paths for work that needs more than one careful step. A workflow makes the goal, evidence, and stopping point clear so a delivery can stay understandable as it grows.

**Layer**: 5th layer in repository hierarchy. Workflows are to Agents what Agents are to Tools — a composition layer; a workflow step can itself be another workflow. See [Repository Governance Architecture](../repository-governance-architecture.md) for the full model.

```
Layer 0: Vision (WHY WE EXIST)     → Foundational purpose
Layer 1: Principles (WHY)          → Foundational values
Layer 2: Conventions (WHAT)        → Documentation rules
Layer 3: Development (HOW)         → Software practices
Layer 4: AI Agents (WHO)           → Atomic task executors
Layer 5: Workflows (WHEN)          → Multi-step processes ← YOU ARE HERE
```

## Using Workflows

```
User: "Run [workflow-name] workflow for [scope] in [mode] mode"
```

Workflows support two execution modes and a standard set of input parameters (`mode`, `max-concurrency`, `min-iterations`/`max-iterations`) — see Workflow Meta Documentation below for the full Agent Delegation vs. Manual Orchestration convention.

## Workflow Directories

- [API Workflows](api/README.md) — Orchestrated processes for live REST and GraphQL API quality validation and remediation. Use when routing to a workflow that exercises a running REST or GraphQL API against its contract and specs.
- [AyoKoding Web Workflows](ayokoding-web/README.md) — Workflows for keeping AyoKoding learning content accurate, useful, and well structured. Use when routing to a workflow that validates a specific AyoKoding tutorial type's quality.
- [CI Workflows](ci/README.md) — Workflows for checking that repository CI setup follows its documented standards. Use when routing to a workflow that validates or fixes CI/CD standards compliance.
- [Content Workflows](content/README.md) — Workflows for creating, converting, and validating content in various formats. Use when routing to a workflow that converts a source document to Markdown or validates conversion fidelity.
- [Documentation Workflows](docs/README.md) — Workflows for checking that reader-facing documentation remains accurate and navigable. Use when routing to a workflow that validates docs/ content quality or its style-guide separation.
- [Infrastructure Workflows](infra/README.md) — Workflows for development environment and infrastructure setup. Use when routing to a workflow that sets up or verifies a development environment's toolchains.
- [Workflow Meta Documentation](meta/README.md) — Reference material for designing workflows that are understandable and reusable. Use when routing to reference material about how workflows are structured or executed.
- [Plan Workflows](plan/README.md) — Orchestrated workflows for plan creation, quality validation, and execution — from idea to archived delivery. Use when routing to a workflow that authors, validates, executes, or takes over a project plan.
- [PR Review Workflows](pr/README.md) — Orchestrated workflows for reviewing and finishing off pull requests before merge. Use when routing to a workflow that runs the specialist review cycle against an open pull request.
- [Repository Workflows](repo/README.md) — Orchestrated repository-level governance workflows — rules consistency, harness compatibility, and dependency bump planning. Use when routing to a workflow that validates repository-level rules, harness compatibility, or dependency posture.
- [Specs Workflows](specs/README.md) — Workflows for checking that specifications remain coherent, complete, and actionable. Use when routing to a workflow that validates specs/ structural completeness, accuracy, or cross-spec coherence.
- [UI Workflows](ui/README.md) — Orchestrated processes for UI component quality validation and remediation. Use when routing to a workflow that audits or fixes UI component quality.
- [Web Workflows](web/README.md) — Orchestrated workflows that test a live running website and turn the findings into a fix plan. Use when routing to a workflow that tests a live running site and turns findings into a fix plan.

All `*-quality-gate` workflows follow the check-fix Workflow Pattern (see Workflow Meta Documentation above) which fixes every finding and iterates until zero remain.

## Naming

Workflow filenames are ordinary lowercase kebab-case, per [File Naming](../conventions/structure/file-naming.md). Most end in a token naming the workflow's shape; the table below is a **descriptive** vocabulary, not a mandate. The type-suffix rule that once bound this tree, and the validator that enforced it, were withdrawn — see [Withdrawn Rules](../conventions/structure/file-naming.md#withdrawn-rules). A workflow whose shape is not in the table needs no new token and no exception.

| Type           | Semantics                                                                                       | Example                         |
| -------------- | ----------------------------------------------------------------------------------------------- | ------------------------------- |
| `quality-gate` | Iterative maker → checker → fixer loop until zero findings                                      | `ci-quality-gate`               |
| `execution`    | Executes a defined procedure or plan against inputs                                             | `plan-execution`                |
| `setup`        | One-time environment or resource provisioning                                                   | `development-environment-setup` |
| `planning`     | Surveys/analyzes state and produces a plan as its terminal deliverable                          | `repo-dependency-bump-planning` |
| `grooming`     | Recurring sweep/reorganization over existing state; no zero-findings convergence or plan output | `plan-ideas-grooming`           |

**Workflow vs Plans**: a plan is strategic (WHAT to build), free-form, human-authored, and archived once delivered; a workflow is tactical (HOW to build), structured Markdown with YAML, and executed repeatedly. Plans can reference workflows; workflows can be generated from plan checklists.

## Related Documentation

- [Workflow Meta Documentation](meta/README.md) — How workflows are structured and executed
- [Maker-Checker-Fixer Pattern](../development/pattern/maker-checker-fixer.md) — Core workflow pattern
- [Plans Organization](../conventions/structure/plans.md) — How plans relate to workflows
- [Repository Governance Architecture](../repository-governance-architecture.md) — Complete six-layer model
