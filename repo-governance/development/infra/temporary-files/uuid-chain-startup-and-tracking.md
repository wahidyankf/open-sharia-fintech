---
title: "UUID Chain Generation — Startup and Tracking"
description: The startup logic that builds the UUID chain, the write-tracking rule, and concurrency isolation.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when implementing a checker/fixer agent's startup logic.
---

# UUID Chain Generation — Startup and Tracking

Continues [UUID Chain Generation](./uuid-chain-generation.md).

## Agent Startup Logic

All checker agents MUST implement this startup logic:

```bash
# 1. Generate own UUID (6 hex chars)
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)

# 2. Determine scope (from prompt or default to agent-family)
# If EXECUTION_SCOPE found in prompt, use it; otherwise use agent-family
SCOPE="${EXECUTION_SCOPE:-${AGENT_FAMILY}}"

# 3. Read parent chain from scope-specific tracking file
CHAIN_FILE="local-tmp/.execution-chain-${SCOPE}"
if [ -f "$CHAIN_FILE" ]; then
  read PARENT_TIME PARENT_CHAIN < "$CHAIN_FILE"
  CURRENT_TIME=$(date +%s)
  TIME_DIFF=$((CURRENT_TIME - PARENT_TIME))

  if [ $TIME_DIFF -lt 300 ]; then
    # Recent parent, append to chain
    UUID_CHAIN="${PARENT_CHAIN}_${MY_UUID}"
  else
    # Stale parent (>300 seconds / 5 minutes), treat as root
    UUID_CHAIN="${MY_UUID}"
  fi
else
  # No tracking file, we're root
  UUID_CHAIN="${MY_UUID}"
fi

# 4. Generate timestamp
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")

# 5. Create report filename
mkdir -p "local-tmp/${AGENT_FAMILY}"
REPORT_FILE="local-tmp/${AGENT_FAMILY}/${AGENT_FAMILY}__${UUID_CHAIN}__${TIMESTAMP}__audit.md"

# 6. Write tracking file ONLY if about to spawn children
# Most checker/fixer agents skip this step (they don't spawn children)
```

## Write Tracking File Rule

**CRITICAL**: Only write to `.execution-chain-{scope}` when **about to spawn child agents**.

- PASS: Workflows write before spawning checkers
- PASS: Orchestrating agents write before spawning sub-agents
- FAIL: Checker agents do NOT write (they don't spawn children)
- FAIL: Fixer agents do NOT write (they don't spawn children)

This prevents race conditions when multiple children run in parallel.

## Concurrent Workflow Isolation

Scope-based tracking enables correct parent tracking for concurrent workflows:

```
T0: ayokoding-workflow writes .execution-chain-ayokoding = "aaa111"
T1: ose-workflow writes .execution-chain-ose = "bbb222"
T2: ayokoding-checker reads .execution-chain-ayokoding → "aaa111"
T3: ose-checker reads .execution-chain-ose → "bbb222"
```

Each workflow scope is isolated, preventing cross-contamination.

Continued in [UUID Chain Generation — Limitations, Compatibility, and Rationale](./uuid-chain-limitations-and-rationale.md).
