---
title: "State Management"
description: How workflows pass data between steps using {input.name}, {stepN.outputs.name}, {stepN.status}, and {stepN.user-approved} references.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when a workflow step needs to reference a prior step's output or an input value.
---

# State Management

Workflows pass data between steps using references:

- `{input.name}` - References workflow input
- `{stepN.outputs.name}` - References output from step N
- `{stepN.status}` - References status of step N (success/failure/partial)
- `{stepN.user-approved}` - References user decision from checkpoint

**Example**:

```yaml
inputs:
  - name: scope
    type: string
    required: true
```

```markdown
**Agent**: `docs-checker`

- **Args**: `scope: {input.scope}`
```
