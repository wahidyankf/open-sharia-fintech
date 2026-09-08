---
description: How agents generate the 6-character UUID chain, plus scope-based tracking and scope passing.
when_to_use: Use when generating a report filename's UUID chain.
---

# UUID Chain Generation

**UUID Chain Examples**:

- `a1b2c3` - Root execution (no parent)
- `a1b2c3_d4e5f6` - Child of a1b2c3
- `a1b2c3_d4e5f6_g7h8i9` - Grandchild (2 levels deep)

**Full Filename Examples**:

```
local-tmp/repo-rules/repo-rules__a1b2c3__2025-12-14--20-45__audit.md
local-tmp/ayokoding-web-general/ayokoding-web-general__d4e5f6__2025-12-14--15-30__audit.md
local-tmp/ayokoding-web-by-example/ayokoding-web-by-example__a1b2c3_d4e5f6__2025-12-14--15-45__audit.md
local-tmp/ose-web-content/ose-web-content__g7h8i9__2025-12-14--16-00__audit.md
local-tmp/docs/docs__a1b2c3_d4e5f6_g7h8i9__2025-12-15--10-00__audit.md
local-tmp/plan/plan__b2c3d4__2025-12-15--11-30__validation.md
local-tmp/plan-execution/plan-execution__c3d4e5__2025-12-15--14-00__validation.md
```

**Why UUID Chain?**

- **Parallelization**: Unique UUID per execution prevents file collisions when multiple agents run simultaneously
- **Traceability**: Underscore-separated chain shows parent-child execution hierarchy
- **Debugging**: Can trace back from any report to its root execution

## UUID Generation

All checker agents MUST generate a 6-character hexadecimal UUID at startup:

```bash
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
# Example output: a1b2c3
```

**Why 6 characters?**

- 16^6 = 16,777,216 possible combinations
- Collision probability for 1000 parallel executions: ~0.003%
- Short enough for readable filenames, long enough for uniqueness

## Scope-Based Execution Tracking

To enable accurate parent-child hierarchy tracking across concurrent workflow runs, agents use **scope-based tracking files**.

**Tracking File Pattern**: `local-tmp/.execution-chain-{scope}` — at the root, because the chain spans agent families

**Scope Definitions**:

| Workflow/Agent        | Scope           | Tracking File                    |
| --------------------- | --------------- | -------------------------------- |
| rules-checker         | `repo-rules`    | `.execution-chain-repo-rules`    |
| docs-checker          | `docs`          | `.execution-chain-docs`          |
| docs-tutorial-checker | `docs-tutorial` | `.execution-chain-docs-tutorial` |
| readme-checker        | `readme`        | `.execution-chain-readme`        |
| plan-checker          | `plan`          | `.execution-chain-plan`          |
| docs-link-checker     | `docs-link`     | `.execution-chain-docs-link`     |
| ayokoding-web-\* (ts) | `ayokoding`     | `.execution-chain-ayokoding`     |
| ose-web-\*            | `ose`           | `.execution-chain-ose`           |

**Tracking File Format**: `{unix-timestamp} {uuid-chain}`

**Example**: `1703594400 a1b2c3_d4e5f6`

## Scope Passing

When spawning child agents, include `EXECUTION_SCOPE` in the prompt:

```bash
Task(
  subagent_type="docs-checker",
  prompt="Validate documentation. EXECUTION_SCOPE: docs"
)
```
