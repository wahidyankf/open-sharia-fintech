---
title: "The Fundamental Principle: MOVE, NOT DELETE"
description: "The core rule: condensed content is moved, never deleted."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use before condensing or trimming any file with substantive content."
---

# The Fundamental Principle: MOVE, NOT DELETE

**CRITICAL REQUIREMENT:** All condensation must preserve content by moving it to convention or development documents. Zero content loss is non-negotiable.

## Why This Matters

**Problem:** Simply deleting content to reduce file size causes:

- Loss of valuable knowledge and context
- Need to recreate documentation later
- Inconsistent coverage across repository
- Erosion of institutional knowledge

**Solution:** Offload content to appropriate convention or development documents where it becomes:

- Permanent, comprehensive reference
- Source of truth for the topic
- Discoverable through index files
- Maintainable in one canonical location

## Content Offload vs Content Deletion

**PASS: Content Offload (CORRECT):**

```markdown
Before (AGENTS.md - 500 lines on file naming):

## File Naming Convention

Files must use lowercase kebab-case basenames with a standard extension...

[... 500 lines of detailed examples, rules, edge cases ...]

After (AGENTS.md - 3 lines):

## File Naming Convention

Files use lowercase kebab-case basenames (e.g., `file-naming.md`), with directory hierarchy encoding the category. See [File Naming Convention](../../conventions/structure/file-naming.md) for complete details.

Result: Content preserved in file-naming.md (comprehensive)
```

**FAIL: Content Deletion (WRONG):**

```markdown
Before (AGENTS.md - 500 lines):

## File Naming Convention

[... 500 lines of detailed guidance ...]

After (AGENTS.md - 0 lines):

[Section completely removed]

Result: Knowledge lost, need to recreate later
```
