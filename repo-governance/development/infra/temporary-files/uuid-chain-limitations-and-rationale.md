---
description: The concurrency limitation, backward compatibility for old filenames, and why the scheme is mandatory.
when_to_use: Use when parsing an old-format report filename.
---

# UUID Chain Generation — Limitations, Compatibility, and Rationale

Continues [UUID Chain Generation — Startup and Tracking](./uuid-chain-startup-and-tracking.md).

## Documented Limitation

> **Edge case:** If the same workflow with the same scope runs concurrently (e.g., two ayokoding by-example validations simultaneously), parent tracking may be imperfect within that scope. This is expected behaviour for concurrent operations on the same resource. The unique UUID still ensures no file collisions.

## Backward Compatibility

Fixer agents MUST handle both old (3-part) and new (4-part) filename formats:

```bash
BASENAME=$(basename "$AUDIT_FILE" .md)
PART_COUNT=$(echo "$BASENAME" | awk -F'__' '{print NF}')

if [ "$PART_COUNT" -eq 3 ]; then
  # Old format: agent__timestamp__type
  AGENT=$(echo "$BASENAME" | awk -F'__' '{print $1}')
  TIMESTAMP=$(echo "$BASENAME" | awk -F'__' '{print $2}')
  TYPE=$(echo "$BASENAME" | awk -F'__' '{print $3}')
  UUID_CHAIN=""
elif [ "$PART_COUNT" -eq 4 ]; then
  # New format: agent__uuid__timestamp__type
  AGENT=$(echo "$BASENAME" | awk -F'__' '{print $1}')
  UUID_CHAIN=$(echo "$BASENAME" | awk -F'__' '{print $2}')
  TIMESTAMP=$(echo "$BASENAME" | awk -F'__' '{print $3}')
  TYPE=$(echo "$BASENAME" | awk -F'__' '{print $4}')
fi
```

## Why This is Mandatory

**Consistency**: Standardized report location and naming across all checker families

**Traceability**: Timestamps enable chronological tracking of validation runs

**Integration**: Fixer agents expect audit reports in `local-tmp/<agent-family>/` following this naming pattern

**Documentation**: Audit trail for all validation activities

**NO conversation-only output**: Reports must be persisted for review, comparison, and fixer integration
