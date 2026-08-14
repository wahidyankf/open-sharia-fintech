---
title: "Model Selection Guidelines"
description: "Summarizes the model-tier decision tree for choosing which model an agent should use."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding which model tier a new or existing agent should declare.
---

# Model Selection Guidelines

For complete model selection standards, see the [Model Selection Convention](../model-selection.md).

**Three tiers**:

- **Planning-grade** (default): Omit the `model` field. For creative reasoning, code generation, architectural decisions, and nuanced content creation (creative makers, language developers). Omitting `model` is budget-adaptive: the agent inherits the session's active model tier. Do NOT add a concrete model name — that overrides budget-adaptive behavior. See [model-selection.md](../model-selection.md) for the full design rationale.
- **Execution-grade** (`model: sonnet`): For rule-based validation, applying validated fixes, template-driven output, and structured pattern-following tasks (checkers, fixers, structured makers, swe-e2e-dev).
- **Fast** (`model: haiku`): For purely mechanical tasks with no reasoning required -- URL validation, deployment scripts, deterministic file operations, simple command execution (deployers, link checkers, docs-file-manager).

```binding-example
Concrete model identifiers per platform:
  Planning-grade (omit model field) — budget-adaptive inheritance
  Execution-grade:  model: sonnet   (Claude Code)
  Fast:             model: haiku    (Claude Code)
```

## Model Selection Decision Tree

```
Start: Choosing Agent Model
    │
    ├─ Does the task require creative reasoning, code generation,
    │   architectural decisions, or nuanced content creation?
    │   │
    │   ├─ Yes → Planning-grade (omit model field)
    │   │
    │   └─ No → Does the task require applying rules, validating
    │            against checklists, or following structured procedures?
    │            │
    │            ├─ Yes → Execution-grade (model: sonnet)
    │            │
    │            └─ No → Is the task purely mechanical with
    │                     no reasoning required?
    │                     │
    │                     ├─ Yes → Fast (model: haiku)
    │                     │
    │                     └─ No → Default to Execution-grade
    │                              (safer than fast for
    │                               ambiguous cases)
```

**Important**: Every agent MUST include a Model Selection Justification block explaining why the chosen tier is appropriate. See [Model Selection Convention](../model-selection.md) for full requirements.
