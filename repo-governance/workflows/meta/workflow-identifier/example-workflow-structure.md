---
title: "Example Workflow Structure"
description: A worked, simplified example of a full multi-step content-validation workflow document, frontmatter through Termination Criteria.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when you want a complete worked example to model a new workflow document on, rather than the bare template.
---

# Example Workflow Structure

Here's a simplified example of a multi-step validation workflow:

```markdown
---
name: content-validation
goal: Validate content quality and apply fixes
termination: Content passes all quality checks
inputs:
  - name: content-type
    type: enum
    values: [docs, ayokoding, ose, readme]
    required: true
  - name: scope
    type: string
    required: true
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold"
    required: false
    default: strict
outputs:
  - name: validation-status
    type: enum
    values: [pass, partial, fail]
---

# Content Validation Workflow

**Purpose**: Validate and fix content quality iteratively until zero findings achieved.

**When to use**: After creating or updating content.

## Execution Mode

**Preferred Mode**: Agent Delegation — invoke `{input.content-type}-checker` and
`{input.content-type}-fixer` via the Agent tool with `subagent_type` when these
agents exist as defined delegated agent types.

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.
```

User: "Run content validation workflow for [scope] in [mode] mode"

```

The AI invokes specialized agents via the Agent tool. If agents are unavailable as
delegated agent types, it falls back to executing workflow logic directly.

## Steps

### 1. Validate Content (Sequential)

**Agent**: `{input.content-type}-checker`

- Validate content in scope
- Generate audit report in generated-reports/

### 2. Apply Fixes (Sequential)

**Agent**: `{input.content-type}-fixer`

- Read audit report from step 1
- Apply fixes based on mode level
- Generate fix report

### 3. Iteration Control (Sequential)

- Re-validate content
- If zero threshold-level findings: Success
- If findings remain and under max-iterations: Loop to step 2

## Termination Criteria

- PASS: Success: Zero threshold-level findings (based on mode)
- Partial: Findings remain after max-iterations
- FAIL: Failure: Technical errors
```
