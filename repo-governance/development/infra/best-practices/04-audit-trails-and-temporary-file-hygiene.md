---
title: "Best Practices: Audit Trails and Temporary File Hygiene"
description: Covers best practices for pairing audit and fix reports with matching identifiers, periodically cleaning up temporary files, and documenting the purpose of long-lived temporary files.
category: explanation
subcategory: development
tags: [infrastructure, best-practices, temporary-files, audit-trail]
created: 2026-05-12
when_to_use: Use when generating a fix report that follows an audit, scheduling cleanup of temporary files, or documenting why a temporary file or directory exists.
---

# Best Practices: Audit Trails and Temporary File Hygiene

## Practice 8: Pair Audit and Fix Reports with Same UUID and Timestamp

**Principle**: Fixer reports use same UUID-chain and timestamp as source audit.

**Good Example:**

```bash
# Audit report
AUDIT="generated-reports/docs__a1b2c3__2025-12-14--20-45__audit.md"

# Fix report (same UUID and timestamp)
FIX="generated-reports/docs__a1b2c3__2025-12-14--20-45__fix.md"
```

**Bad Example:**

```bash
# Fix report with new timestamp (DO NOT DO THIS)
FIX="generated-reports/docs__d4e5f6__2025-12-14--21-00__fix.md"
# Can't match to source audit!
```

**Rationale:**

- Clear audit-fix traceability
- Enables exact report matching
- Supports debugging and review
- Maintains complete audit trail

## Practice 9: Clean Up Temporary Files Periodically

**Principle**: Remove old temporary files to prevent accumulation.

**Good Example:**

```bash
# Archive old reports (>30 days)
find generated-reports/ -name "*.md" -mtime +30 -exec mv {} archive/ \;

# Clean scratch files (>7 days)
find local-tmp/ -mtime +7 -delete
```

**Bad Example:**

```bash
# Never clean up (thousands of old files accumulate)
```

**Rationale:**

- Prevents directory bloat
- Faster file system operations
- Easier to find recent reports
- Maintains workspace hygiene

## Practice 10: Document Temporary File Purposes

**Principle**: Add README or comments explaining long-lived temporary files.

**Good Example:**

```bash
# local-tmp/cache/README.md
# Performance Cache
#
# This directory contains cached API responses for development.
# Files are regenerated automatically if older than 1 hour.
# Safe to delete - will be recreated as needed.
```

**Bad Example:**

```bash
# Mysterious temporary files with no explanation
local-tmp/data-2025.json
local-tmp/cache-v3.bin
local-tmp/temp-final-v2.txt
```

**Rationale:**

- Clear purpose reduces confusion
- Easier onboarding for new team members
- Prevents accidental deletion of important data
- Documents retention policies
