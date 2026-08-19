# Workflow Structure

### YAML Frontmatter (Required)

```yaml
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
    description: Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total)
    required: false
    default: 3
outputs:
  - name: output-name
    type: string | number | boolean | file | file-list | enum
    description: What this output contains
    pattern: file-pattern (for file/file-list types)
---
```

**Critical YAML Syntax**: Values containing colons (`:`) must be quoted.

✅ **Good**:

```yaml
description: "Workflow name: detailed description here"
parameter: "key: value pairs"
```

❌ **Bad** (breaks YAML parsing):

```yaml
description: Workflow name: detailed description
```

### Workflow Content

````markdown
# Workflow Name

## Purpose

What this workflow accomplishes and when to use it.

## Agents Involved

- **agent-name-1**: Role and responsibility
- **agent-name-2**: Role and responsibility

## Input Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| param1    | string | Yes      | -       | Purpose     |
| param2    | number | No       | 5       | Purpose     |

## Execution Phases

### Phase 1: Name (Sequential)

1. Run agent-name-1 with parameters
2. Wait for completion
3. Run agent-name-2 with results from agent-name-1

### Phase 2: Name (Parallel)

Run in parallel:

- agent-name-3
- agent-name-4

Wait for all to complete before proceeding.

### Phase 3: Name (Conditional)

If condition A:

- Run agent-name-5
  Else:
- Run agent-name-6

## Success Criteria

```gherkin
Given [precondition]
When [workflow executed]
Then [expected outcome]
And [additional verification]
```
````

## Example Usage

Concrete example showing how to invoke workflow.

## Related Workflows

- workflow-name-1 - When to use together
- workflow-name-2 - Alternative approach
