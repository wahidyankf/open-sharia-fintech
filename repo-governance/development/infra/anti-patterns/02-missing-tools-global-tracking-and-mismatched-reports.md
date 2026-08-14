---
title: "Anti-Patterns in Checker Tooling, Execution Tracking, and Report Pairing"
description: Covers the missing-tools, global-execution-tracking, and mismatched-audit/fix-report anti-patterns for checker and fixer agents.
category: explanation
subcategory: development
tags: [anti-patterns, checker-agents, execution-tracking, audit-trail]
created: 2026-05-12
when_to_use: Use when defining a checker agent's tool list, an execution-tracking file, or pairing a fixer report with its source audit.
---

# Anti-Patterns in Checker Tooling, Execution Tracking, and Report Pairing

## Anti-Pattern 4: Missing Write or Bash Tools

**Problem**: Checker agent lacks required tools for report generation.

**Bad Example:**

```yaml
---
name: docs-checker
description: Validates documentation
tools: [Read, Glob, Grep] # MISSING Write and Bash!
---
```

**Solution:**

```yaml
---
name: docs-checker
description: Validates documentation
tools: [Read, Glob, Grep, Write, Bash]
---
```

**Rationale:**

- Write tool creates report files
- Bash tool generates UTC+7 timestamps
- Mandatory for all checker agents
- Consistent tool permissions across agents

## Anti-Pattern 5: Global Execution Tracking

**Problem**: Using single global tracking file for all workflows.

**Bad Example:**

```bash
# Global tracking file (causes race conditions)
CHAIN_FILE="generated-reports/.execution-chain"
# All workflows share same file!
```

**Solution:**

```bash
# Scope-based tracking files
SCOPE="${EXECUTION_SCOPE:-docs}"
CHAIN_FILE="generated-reports/.execution-chain-${SCOPE}"
```

**Rationale:**

- Concurrent workflows overwrite each other's data
- Parent tracking breaks across scopes
- Race conditions in parallel execution
- Scope isolation prevents contamination

## Anti-Pattern 6: Mismatched Audit and Fix Reports

**Problem**: Fixer uses different UUID or timestamp than source audit.

**Bad Example:**

```bash
# Audit report
AUDIT="generated-reports/docs__a1b2c3__2025-12-14--20-45__audit.md"

# Fix report with NEW UUID and timestamp (DO NOT DO THIS)
FIX="generated-reports/docs__d4e5f6__2025-12-14--21-00__fix.md"
```

**Solution:**

```bash
# Extract UUID and timestamp from audit filename
BASENAME=$(basename "$AUDIT" .md)
UUID=$(echo "$BASENAME" | awk -F'__' '{print $2}')
TIMESTAMP=$(echo "$BASENAME" | awk -F'__' '{print $3}')

# Fix report uses SAME UUID and timestamp
FIX="generated-reports/docs__${UUID}__${TIMESTAMP}__fix.md"
```

**Rationale:**

- Can't match fix report to source audit
- Breaks audit trail
- Complicates debugging
- Same UUID+timestamp enables exact pairing
