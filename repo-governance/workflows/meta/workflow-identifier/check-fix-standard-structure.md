---
title: "*-check-fix Workflow Pattern — Standard Structure"
description: The standard inputs/outputs YAML block every *-check-fix workflow uses — mode, max-concurrency, min-iterations, max-iterations, and their outputs.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when authoring the frontmatter inputs/outputs block for a new *-check-fix workflow.
---

# \*-check-fix Workflow Pattern — Standard Structure

All \*-check-fix workflows follow this pattern:

```yaml
inputs:
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
  - name: min-iterations
    type: number
    description: Minimum check-fix cycles before allowing zero-finding termination
    required: false
  - name: max-iterations
    type: number
    description: Maximum check-fix cycles to prevent infinite loops
    required: false
    default: 7

outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
  - name: iterations-completed
    type: number
  - name: final-report
    type: file
```
