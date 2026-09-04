---
title: "Best Practices: File Organization and Progressive Reporting"
description: Covers best practices for organizing temporary files, naming reports consistently, writing reports progressively during execution, and generating real UUIDs and timestamps instead of placeholders.
category: explanation
subcategory: development
tags: [infrastructure, best-practices, temporary-files, reporting]
created: 2026-05-12
when_to_use: Use when setting up temporary file locations, naming a new report file, deciding when to write report content, or generating UUIDs/timestamps for a report.
---

# Best Practices: File Organization and Progressive Reporting

## Practice 1: Use Designated Temporary Directories

**Principle**: All temporary files go in `generated-reports/` (human-requested artifacts) or
`local-tmp/<agent-family>/` (agent working state), never repository root.

**Good Example:**

```bash
# Validation report
local-tmp/docs/docs__a1b2c3__2025-12-14--20-45__audit.md

# Scratch work
local-tmp/draft-analysis.txt
```

**Bad Example:**

```bash
# Scattered temporary files (DO NOT DO THIS)
temp-report.md
validation-output.txt
analysis-2025-12-14.json
```

**Rationale:**

- Clear organization prevents clutter
- Easy cleanup (both gitignored)
- Predictable file locations
- Separates temporary from permanent content

## Practice 2: Follow Standardized Report Naming

**Principle**: Use 4-part pattern: `{agent-family}__{uuid-chain}__{timestamp}__{type}.md`

**Good Example:**

```bash
# Generate UUID and timestamp
UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")

# Create report
REPORT="local-tmp/docs/docs__${UUID}__${TIMESTAMP}__audit.md"
```

**Bad Example:**

```bash
# Placeholder values (DO NOT DO THIS)
REPORT="local-tmp/docs/docs__abc123__2025-12-14--00-00__audit.md"
```

**Rationale:**

- Unique UUIDs prevent file collisions
- Accurate timestamps enable chronological sorting
- Standardized pattern aids automation
- Audit trail for all validation runs

## Practice 3: Write Reports Progressively

**Principle**: Update report files continuously during execution, not at the end.

**Good Example:**

```bash
# Initialize report immediately
echo "# Audit Report" > "$REPORT"
echo "**Status**: In Progress" >> "$REPORT"

# Write findings as discovered
for file in $FILES; do
  result=$(validate "$file")
  echo "## $file" >> "$REPORT"
  echo "Result: $result" >> "$REPORT"
done

# Update final status
sed -i 's/In Progress/Complete/' "$REPORT"
```

**Bad Example:**

```bash
# Buffer in memory (DO NOT DO THIS)
findings=""
for file in $FILES; do
  findings+="$(validate "$file")\n"
done

# Write at end (lost if context compacted!)
echo "$findings" > "$REPORT"
```

**Rationale:**

- Survives context compaction during long audits
- Provides real-time progress visibility
- Enables debugging of incomplete runs
- Critical for AI agent reliability

## Practice 4: Generate Real UUIDs and Timestamps

**Principle**: Execute bash commands for actual values, never use placeholders.

**Good Example:**

```bash
# Generate real UUID
UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
# Example output: a1b2c3

# Generate current timestamp
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")
# Example output: 2025-12-14--16-43
```

**Bad Example:**

```bash
# Placeholder values (DO NOT DO THIS)
UUID="abc123"
TIMESTAMP="2025-12-14--00-00"
```

**Rationale:**

- Unique UUIDs prevent parallel execution collisions
- Accurate timestamps enable audit trails
- Debugging requires real creation times
- Placeholders defeat the purpose of tracking
