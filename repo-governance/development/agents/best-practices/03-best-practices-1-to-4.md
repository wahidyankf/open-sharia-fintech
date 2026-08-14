---
title: "Best Practices — Single Responsibility, Minimum Tools, Model Choice, and Descriptions"
description: "Covers Practices 1-4: single responsibility per agent, requesting minimum necessary tool permissions, using the appropriate model for task complexity, and clear actionable descriptions."
category: explanation
subcategory: development
tags:
  - ai-agents
  - best-practices
  - development
  - standards
created: 2025-11-23
when_to_use: Use when authoring a new agent and deciding its responsibility, tool list, model tier, or frontmatter description.
---

# Best Practices — Single Responsibility, Minimum Tools, Model Choice, and Descriptions

## Practice 1: Single Responsibility Per Agent

**Principle**: Each agent should have one clear, focused purpose.

**Good Example:**

```yaml
---
name: docs-checker
description: Validates factual correctness of documentation
tools: [Read, Glob, Grep, WebFetch, WebSearch, Write, Bash]
model: sonnet
---
```

**Bad Example:**

```yaml
---
name: super-agent
description: Checks docs, writes content, deploys apps, manages files
tools: [*]  # Too many responsibilities
---
```

**Rationale:**

- Easier to test and debug
- Clear ownership and accountability
- Reusable across different workflows
- Simpler tool permission model

## Practice 2: Request Minimum Necessary Tool Permissions

**Principle**: Only request tools the agent actually needs.

**Good Example:**

```yaml
---
name: readme-checker
description: Validates README quality standards
tools: [Read, Glob, Grep, Write] # Only what is needed
---
```

**Bad Example:**

```yaml
---
name: readme-checker
description: Validates README quality standards
tools: [Read, Write, Edit, Bash, WebFetch, WebSearch] # Excessive
---
```

**Rationale:**

- Reduces security risk
- Clear what the agent can do
- Faster user approval
- Easier auditing

## Practice 3: Use Appropriate Model for Task Complexity

**Principle**: Match model to task complexity - use fast model for simple tasks, execution-grade for structured tasks, and omit `model` for planning-grade agents.

**Good Example:**

```yaml
# Simple validation task
---
name: link-checker
model: haiku
---
# Structured rule-based task
---
name: plan-checker
model: sonnet
---
# Complex reasoning task — omit model (budget-adaptive)
---
name: plan-maker
model:
---
```

**Rationale:**

- Cost optimization
- Performance optimization
- Clear expectations
- Planning-grade agents omit `model` by design (budget-adaptive — inherits session model). Do not add a concrete planning-tier model identifier. See [model-selection.md](../model-selection.md) for the design rationale.

## Practice 4: Provide Clear, Actionable Descriptions

**Principle**: Agent description should clearly state WHAT the agent does and WHEN to use it.

**Good Example:**

```yaml
---
description: >
  Validates tutorial quality focusing on pedagogical structure,
  narrative flow, visual completeness, and hands-on elements.
  Use when reviewing tutorial documentation.
---
```

**Bad Example:**

```yaml
---
description: Checks stuff
---
```

**Rationale:**

- Users know when to invoke agent
- Clear purpose and scope
- Better discoverability
