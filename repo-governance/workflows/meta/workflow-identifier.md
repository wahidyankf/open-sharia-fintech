---
title: "Workflow Pattern Convention"
description: Standards for creating orchestrated multi-step processes that compose agents, procedures, and/or other workflows
when_to_use: Use when defining, structuring, or validating a new workflow document, or when deciding whether a task should become a workflow at all.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
  - conventions
created: 2025-12-23
---

# Workflow Pattern Convention

Workflows are **composed multi-step processes** that orchestrate agents, procedures, and/or
other workflows to achieve specific goals with clear termination criteria — the fifth layer in
the repository's governance hierarchy. Covers what workflows are (and aren't), the frontmatter
and body structure, step execution patterns, state/error handling, composability, the
`*-check-fix` pattern, and a worked example below.

## Contents

- [Overview](./workflow-identifier/overview.md) — what a workflow is.
- [Repository Hierarchy](./workflow-identifier/repository-hierarchy.md) — where workflows sit.
- [What Workflows Are](./workflow-identifier/what-workflows-are.md) — the seven properties.
- [What Workflows Are NOT](./workflow-identifier/what-workflows-are-not.md) — boundary cases.
- [When to Create a Workflow](./workflow-identifier/when-to-create-a-workflow.md) — the signals.
- [Workflow Structure](./workflow-identifier/workflow-structure.md) — the frontmatter/body template.
- [YAML Syntax Requirements](./workflow-identifier/yaml-syntax-requirements.md) — quoting rules.
- [File Naming Convention](./workflow-identifier/file-naming-convention.md) — plain kebab-case.
- [Step Execution Patterns](./workflow-identifier/step-execution-patterns.md) — sequential/parallel/conditional.
- [State Management](./workflow-identifier/state-management.md) — passing data between steps.
- [Human Checkpoints](./workflow-identifier/human-checkpoints.md) — pausing for approval.
- [Error Handling](./workflow-identifier/error-handling.md) — per-step failure behaviour.
- [Validation](./workflow-identifier/validation.md) — pre-execution checks.
- [Relationship to Other Layers](./workflow-identifier/relationship-to-other-layers.md) — principles through plans.
- [Composability](./workflow-identifier/composability.md) — nesting workflows/agents/procedures.
- [Governance Gate Class](./workflow-identifier/governance-gate-class.md) — the second gate class and how to choose.
- [\*-check-fix Pattern — Characteristics](./workflow-identifier/check-fix-pattern-characteristics.md) — the zero-findings pattern.
- [\*-check-fix Pattern — Standard Structure](./workflow-identifier/check-fix-standard-structure.md) — the inputs/outputs block.
- [\*-check-fix Pattern — Required Steps](./workflow-identifier/check-fix-required-steps.md) — the five steps.
- [\*-check-fix Pattern — Termination Criteria](./workflow-identifier/check-fix-termination-criteria.md) — mandatory pass/partial/fail rules.
- [\*-check-fix Pattern — Consecutive Pass Requirement](./workflow-identifier/check-fix-consecutive-pass-requirement.md) — double-zero confirmation.
- [\*-check-fix Pattern — Safety and Strictness](./workflow-identifier/check-fix-safety-and-strictness.md) — loop guards and mode levels.
- [\*-check-fix Pattern — Example and Differences](./workflow-identifier/check-fix-example-and-differences.md) — canonical example, comparison table.
- [\*-quality-gate Lifecycle Validation Ownership](./workflow-identifier/check-fix-lifecycle-validation-ownership.md) — registry-owned check delegation.
- [Example Workflow Structure](./workflow-identifier/example-workflow-structure.md) — a full worked example.
- [Documentation Requirements](./workflow-identifier/documentation-requirements.md) — the required sections.
- [Future Enhancements](./workflow-identifier/future-enhancements.md) — not-yet-implemented features.
- [Token Budget Philosophy](./workflow-identifier/token-budget-philosophy.md) — don't economize tokens.
- [Principles Implemented/Respected](./workflow-identifier/principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./workflow-identifier/conventions-implemented-respected.md) — traceability.
- [Related Documentation](./workflow-identifier/related-documentation.md) — composing references.
