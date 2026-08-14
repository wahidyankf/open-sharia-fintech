---
title: "Justification Requirement"
description: "States the requirement that every agent include a Model Selection Justification block explaining its tier choice."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when writing or reviewing an agent's Model Selection Justification block.
---

# Justification Requirement

Every agent MUST include a **Model Selection Justification** block in its markdown body explaining why the chosen tier is appropriate. This block appears near the top of the agent file, after the frontmatter metadata section.

**Format**:

```markdown
**Model Selection Justification**: This agent uses `model: sonnet` because it requires:

- [Capability 1] to [accomplish task aspect]
- [Capability 2] to [accomplish task aspect]
```

**Examples**:

For a checker agent:

> **Model Selection Justification**: This agent uses `model: sonnet` because it requires:
>
> - Systematic rule application to validate content against defined checklists
> - Structured report generation following the audit report template
> - Pattern recognition to identify convention violations across files

For a developer agent (omit model field — inherits opus):

> **Model Selection Justification**: This agent uses inherited `model: opus` (omit model field) because it requires:
>
> - Advanced reasoning to generate idiomatic code across language paradigms
> - Multi-step problem decomposition for complex refactoring tasks
> - Creative synthesis to design APIs and data models

For a deployer agent:

> **Model Selection Justification**: This agent uses `model: haiku` because it requires:
>
> - Execution of predefined git and deployment commands
> - No analytical reasoning beyond following a fixed procedure
