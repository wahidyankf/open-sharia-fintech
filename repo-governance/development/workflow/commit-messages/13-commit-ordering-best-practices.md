---
title: "Commit Ordering Best Practices"
description: How to order a sequence of related commits — create before update, refactor before fix, and a natural type progression.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when a change requires multiple commits and you need to decide what order to make them in.
---

# Commit Ordering Best Practices

When you have multiple commits, order them logically:

1. **Create before update** - Create new files before updating references to them
2. **Refactor before fix** - Refactor code before fixing bugs in the refactored code
3. **Type progression** - Follow a natural flow: `feat` → `refactor` → `docs` → `test` → `fix`

**Example of good commit ordering:**

```
1. feat(agents): add docs-link-checker agent          # Create new file
2. refactor(agents): rename agents for consistency    # Rename existing files
3. docs(agents): update all references to renamed agents  # Update references
4. fix(docs): align frontmatter date                  # Fix issues discovered
```
