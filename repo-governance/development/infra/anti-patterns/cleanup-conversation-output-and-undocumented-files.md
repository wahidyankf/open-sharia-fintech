---
description: Covers the never-cleaning-temp-files, conversation-only-output, and undocumented-long-lived-temp-file anti-patterns.
when_to_use: Use when a checker agent is about to report findings only in conversation, or when temporary files are piling up without cleanup or documentation.
---

# Anti-Patterns in Temp File Cleanup, Checker Output, and Documentation

## Anti-Pattern 8: Never Cleaning Temporary Files

**Problem**: Accumulating thousands of old temporary files.

**Bad Example:**

```bash
# Never clean up
ls generated-reports/ | wc -l
# Output: 5,847 files (most months old!)
```

**Solution:**

```bash
# Periodic cleanup
find generated-reports/ -name "*.md" -mtime +30 -exec mv {} archive/ \;
find local-tmp/ -mtime +7 -delete
```

**Rationale:**

- Directory bloat slows file system
- Hard to find recent reports
- Wastes disk space
- Regular cleanup maintains hygiene

## Anti-Pattern 9: Conversation-Only Output

**Problem**: Checker outputs findings in conversation without writing report file.

**Bad Example:**

```markdown
## Agent: docs-checker

Validation complete! Found 15 issues:

1. Missing alt text in image
2. Broken link to /docs/guide
   ...
   (No file written - findings lost during context compaction!)
```

**Solution:**

```bash
# Write findings to report file
REPORT="local-tmp/docs/docs__${UUID}__${TIMESTAMP}__audit.md"
echo "# Validation Report" > "$REPORT"
echo "## Issues Found" >> "$REPORT"
echo "1. Missing alt text in image" >> "$REPORT"
# ... continue writing to file
```

**Rationale:**

- Conversation findings lost during compaction
- No audit trail
- Can't pass to fixer agents
- Report files persist regardless of context

## Anti-Pattern 10: Undocumented Long-Lived Temporary Files

**Problem**: Mysterious temporary files with no explanation.

**Bad Example:**

```bash
# What are these files?
local-tmp/cache-v3.bin
local-tmp/data-final-2025.json
local-tmp/temp-backup-v2.tar.gz
```

**Solution:**

```bash
# local-tmp/cache/README.md
# API Response Cache
#
# Contains cached API responses for development.
# Regenerated if older than 1 hour.
# Safe to delete - recreated as needed.
```

**Rationale:**

- Purpose unclear without documentation
- New team members don't know if safe to delete
- Retention policies unknown
- Documentation prevents confusion
