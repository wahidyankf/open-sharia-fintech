---
title: "Workflow Structure"
description: The structured Markdown-with-YAML-frontmatter template every workflow document follows, showing the full frontmatter and body skeleton.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when authoring a new workflow file and needing the canonical frontmatter and section skeleton to copy.
---

# Workflow Structure

All workflows use **structured Markdown with YAML frontmatter**:

```markdown
---
name: workflow-identifier
goal: What this workflow achieves
termination: Success/failure criteria
inputs:
  - name: input-name
    type: string | number | boolean | file | file-list | enum
    description: What this input is for
    required: true | false
    default: value (if not required)
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: output-name
    type: string | number | boolean | file | file-list | enum
    description: What this output contains
    pattern: file-pattern (for file/file-list types)
---

# Workflow Name

**Purpose**: One-sentence description of what this workflow does.

**When to use**: Specific scenarios where this workflow applies.

## Steps

### 1. Step Name (Execution Mode)

Execution modes: Sequential | Parallel | Conditional

Description of what this step does.

**Agent**: `agent-name` _(use for agent steps)_
**Workflow**: `category/workflow-name` _(use for nested workflow steps)_
**Procedure**: description of manual/scripted step _(use for procedure steps)_

- **Args**: Key-value pairs or references to inputs/previous outputs
- **Output**: What this step produces
- **Depends on**: Previous step(s) that must complete first (if sequential)
- **Condition**: When this step runs (if conditional)

**Success criteria**: What defines success for this step.
**On failure**: What happens if this step fails.

## Termination Criteria

- PASS: **Success**: Conditions for successful completion
- **Partial**: Conditions for partial success
- FAIL: **Failure**: Conditions for failure

## Example Usage

Concrete examples of how to invoke this workflow.

## Related Workflows

Links to workflows that compose with this one.

## Notes

Additional context, limitations, or important considerations.
```
