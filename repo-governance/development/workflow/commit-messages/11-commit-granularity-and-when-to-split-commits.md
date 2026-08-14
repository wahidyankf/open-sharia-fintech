---
title: "Commit Granularity and When to Split Commits"
description: Why splitting work into logical commits matters, and the five situations that call for separate commits.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when deciding whether a set of changes should be split into multiple commits.
---

# Commit Granularity and When to Split Commits

When making changes to the codebase, it's essential to split your work into multiple logical commits rather than creating one large commit with many unrelated changes. This practice improves code review, makes git history more navigable, and enables easier debugging with tools like `git bisect`.

## When to Split Commits

Split your work into multiple commits when:

**Different commit types** - Changes that fall under different conventional commit types should be separate commits:

```
PASS: Good:
1. feat(agents): add docs-link-checker agent
2. docs(agents): update agent index with new agent

FAIL: Bad:
1. feat(agents): add docs-link-checker agent and update agent index
```

**Creating vs updating** - Creating new files and updating references to them should be separate commits:

```
PASS: Good:
1. feat(auth): add user authentication module
2. refactor(api): integrate authentication module

FAIL: Bad:
1. feat(auth): add user authentication module and integrate it
```

**Renaming vs updating references** - Renaming files and updating all references should be separate commits:

```
PASS: Good:
1. refactor(agents): rename agents for consistency
2. docs(agents): update all references to renamed agents

FAIL: Bad:
1. refactor(agents): rename agents and update all references
```

**Different domains** - Changes to different parts of the codebase should be separate commits:

```
PASS: Good:
1. feat(api): add user endpoint
2. docs: document user API
3. test(api): add user endpoint tests

FAIL: Bad:
1. feat(api): add user endpoint with docs and tests
```

**Independent changes** - Changes that could be reviewed or reverted separately should be separate commits:

```
PASS: Good:
1. fix(validation): handle empty strings correctly
2. perf(db): optimize user query
3. docs: update API reference

FAIL: Bad:
1. fix: various improvements to validation, database, and docs
```
