---
description: The standard Inputs and Outputs body sections every *-check-fix workflow uses — mode, max-concurrency, min-iterations, max-iterations, and their outputs.
when_to_use: Use when authoring the Inputs and Outputs sections for a new *-check-fix workflow.
---

# \*-check-fix Workflow Pattern — Standard Structure

All \*-check-fix workflows follow this pattern:

```markdown
## Inputs

- **`mode`** (enum: lax, normal, strict, ocd, optional, default `strict`) — Quality threshold
  (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels).
- **`max-concurrency`** (number, optional, default `3`) — Background agents run concurrently — the
  N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent
  work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk
  pressure. Never self-promoted beyond the declared value.
- **`min-iterations`** (number, optional) — Minimum check-fix cycles before allowing zero-finding
  termination.
- **`max-iterations`** (number, optional, default `7`) — Maximum check-fix cycles to prevent
  infinite loops.

## Outputs

- **`final-status`** (enum: pass, partial, fail)
- **`iterations-completed`** (number)
- **`final-report`** (file)
```
