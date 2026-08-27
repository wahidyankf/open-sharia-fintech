---
title: "Atomic Commits"
description: What makes a commit atomic — self-contained, functional, single-purpose, and reversible — with a worked example.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when checking whether a commit is atomic before finalizing it.
---

# Atomic Commits

Each commit should be **atomic** - meaning:

- **Self-contained**: The commit includes everything needed for the change
- **Functional**: The codebase builds and runs after the commit
- **Single purpose**: The commit has one clear, well-defined purpose
- **Reversible**: The commit can be reverted without breaking other changes

Atomicity follows the purpose, not the file type. Required tests, docs, specs, references,
migration rollback, and generated mirrors complete the purpose and stay in the same commit. Choose
the fewest commits satisfying these properties after the user authorizes the named change set.

**Example of atomic commits:**

```
PASS: Good (atomic):
1. feat(db): add user index on email field
   - Includes migration file
   - Includes rollback script
   - Updates schema documentation
   - All related to ONE database change

FAIL: Bad (not atomic):
1. feat(db): add user index
   - Only adds migration, missing rollback
   - Builds fail until next commit
```
