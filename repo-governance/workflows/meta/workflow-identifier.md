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

- [Overview](./workflow-identifier/01-overview.md) — what a workflow is.
- [Repository Hierarchy](./workflow-identifier/02-repository-hierarchy.md) — where workflows sit.
- [What Workflows Are](./workflow-identifier/03-what-workflows-are.md) — the seven properties.
- [What Workflows Are NOT](./workflow-identifier/04-what-workflows-are-not.md) — boundary cases.
- [When to Create a Workflow](./workflow-identifier/05-when-to-create-a-workflow.md) — the signals.
- [Workflow Structure](./workflow-identifier/06-workflow-structure.md) — the frontmatter/body template.
- [YAML Syntax Requirements](./workflow-identifier/07-yaml-syntax-requirements.md) — quoting rules.
- [File Naming Convention](./workflow-identifier/08-file-naming-convention.md) — plain kebab-case.
- [Step Execution Patterns](./workflow-identifier/09-step-execution-patterns.md) — sequential/parallel/conditional.
- [State Management](./workflow-identifier/10-state-management.md) — passing data between steps.
- [Human Checkpoints](./workflow-identifier/11-human-checkpoints.md) — pausing for approval.
- [Error Handling](./workflow-identifier/12-error-handling.md) — per-step failure behavior.
- [Validation](./workflow-identifier/13-validation.md) — pre-execution checks.
- [Relationship to Other Layers](./workflow-identifier/14-relationship-to-other-layers.md) — principles through plans.
- [Composability](./workflow-identifier/15-composability.md) — nesting workflows/agents/procedures.
- [\*-check-fix Pattern — Characteristics](./workflow-identifier/16-check-fix-pattern-characteristics.md) — the zero-findings pattern.
- [\*-check-fix Pattern — Standard Structure](./workflow-identifier/17-check-fix-standard-structure.md) — the inputs/outputs block.
- [\*-check-fix Pattern — Required Steps](./workflow-identifier/18-check-fix-required-steps.md) — the five steps.
- [\*-check-fix Pattern — Termination Criteria](./workflow-identifier/19-check-fix-termination-criteria.md) — mandatory pass/partial/fail rules.
- [\*-check-fix Pattern — Consecutive Pass Requirement](./workflow-identifier/20-check-fix-consecutive-pass-requirement.md) — double-zero confirmation.
- [\*-check-fix Pattern — Safety and Strictness](./workflow-identifier/21-check-fix-safety-and-strictness.md) — loop guards and mode levels.
- [\*-check-fix Pattern — Example and Differences](./workflow-identifier/22-check-fix-example-and-differences.md) — canonical example, comparison table.
- [Example Workflow Structure](./workflow-identifier/23-example-workflow-structure.md) — a full worked example.
- [Documentation Requirements](./workflow-identifier/24-documentation-requirements.md) — the required sections.
- [Future Enhancements](./workflow-identifier/25-future-enhancements.md) — not-yet-implemented features.
- [Token Budget Philosophy](./workflow-identifier/26-token-budget-philosophy.md) — don't economize tokens.
- [Principles Implemented/Respected](./workflow-identifier/27-principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./workflow-identifier/28-conventions-implemented-respected.md) — traceability.
- [Related Documentation](./workflow-identifier/29-related-documentation.md) — composing references.
