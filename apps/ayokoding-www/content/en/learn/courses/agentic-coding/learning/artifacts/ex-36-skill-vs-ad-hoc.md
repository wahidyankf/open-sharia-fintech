---
title: "Artifact: Skill-Loaded vs. Ad Hoc -- the Repeatability Test"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 76
---

> The same task run twice with a skill loaded and twice ad hoc -- exercises co-20.

**Attempt 1, skill loaded** (`project-lint-format`):

```text
[agent] loads skill: project-lint-format
[agent] step 1: npm run lint:md:fix
[agent] step 2: gofmt -w changed_file.go
[agent] step 3: lint check-only -- 0 violations
```

**Attempt 2, skill loaded, same task, different session**:

```text
[agent] loads skill: project-lint-format
[agent] step 1: npm run lint:md:fix
[agent] step 2: gofmt -w changed_file.go
[agent] step 3: lint check-only -- 0 violations
```

**Attempt A, ad hoc, no skill loaded**:

```text
[agent] runs gofmt -w changed_file.go first
[agent] then runs npm run lint:md:fix
[agent] does not re-run the linter in check-only mode afterward -- assumes the auto-fixers
        were sufficient
```

**Attempt B, ad hoc, no skill loaded, same task, different session**:

```text
[agent] runs npm run lint:md:fix
[agent] skips the language-specific formatter entirely -- judges the diff "close enough"
[agent] runs the linter in check-only mode, reports 1 remaining violation, stops
```
