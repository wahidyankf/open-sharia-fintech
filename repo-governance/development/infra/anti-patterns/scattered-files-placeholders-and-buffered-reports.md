---
title: "Anti-Patterns in Temporary Files, Placeholder Values, and Buffered Reports"
description: Covers the scattered-temp-files, placeholder-UUID, and in-memory-report-buffering anti-patterns, with bad/good examples for each.
category: explanation
subcategory: development
tags: [anti-patterns, temp-files, uuid, report-generation]
created: 2026-05-12
when_to_use: Use when a script is about to write a temporary file, generate a UUID/timestamp, or buffer audit findings before writing a report.
---

# Anti-Patterns in Temporary Files, Placeholder Values, and Buffered Reports

## Anti-Pattern 1: Scattered Temporary Files

**Problem**: Creating temporary files in repository root or random locations.

**Bad Example:**

```bash
# Temporary files scattered everywhere
temp-report.md
validation-output.txt
/docs/temp-analysis.json
/apps/scratch-notes.txt
```

**Solution:**

```bash
# Organized in designated directories
local-tmp/docs/docs__a1b2c3__2025-12-14--20-45__audit.md
local-tmp/scratch-notes.txt
local-tmp/analysis.json
```

**Rationale:**

- Repository clutter makes navigation hard
- Can't easily find or clean temporary files
- Risk of accidentally committing temporary data
- Designated directories are gitignored

## Anti-Pattern 2: Using Placeholder UUID and Timestamps

**Problem**: Using hardcoded placeholder values instead of generating real UUIDs.

**Bad Example:**

```bash
# Placeholder values (DO NOT DO THIS)
UUID="abc123"
TIMESTAMP="2025-12-14--00-00"
REPORT="local-tmp/docs/docs__${UUID}__${TIMESTAMP}__audit.md"
```

**Solution:**

```bash
# Generate real values
UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")
REPORT="local-tmp/docs/docs__${UUID}__${TIMESTAMP}__audit.md"
```

**Rationale:**

- Placeholder timestamps defeat audit trail purpose
- Same UUID causes file collisions in parallel execution
- Can't sort chronologically with fake timestamps
- Debugging requires real creation times

## Anti-Pattern 3: Buffering Reports in Memory

**Problem**: Collecting findings in memory and writing report only at the end.

**Bad Example:**

```bash
# Buffer findings (DO NOT DO THIS)
findings=""
for file in $FILES; do
  result=$(validate "$file")
  findings+="$result\n"
done

# Write once at end (lost if context compacted!)
echo "$findings" > "$REPORT"
```

**Solution:**

```bash
# Write progressively
echo "# Audit Report" > "$REPORT"
for file in $FILES; do
  result=$(validate "$file")
  echo "## $file" >> "$REPORT"
  echo "Result: $result" >> "$REPORT"
done
```

**Rationale:**

- Findings lost during context compaction
- No progress visibility during long audits
- Can't debug incomplete runs
- Progressive writing ensures persistence
