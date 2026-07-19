---
title: "Artifact: Loading an Agent Skill Instead of Improvising"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 75
---

> A packaged SKILL.md followed step by step instead of an improvised procedure --
> exercises co-20.

```markdown
---
name: project-lint-format
description: Runs this project's lint and format pipeline in the correct order before any commit.
---

# Project Lint & Format

## Steps

1. Run `npm run lint:md:fix` to auto-fix markdown violations.
2. Run the language-specific formatter for any changed source file (`gofmt`, `rustfmt`, or
   the project's configured formatter).
3. Re-run the linter in check-only mode; if it reports zero violations, the pipeline is
   complete. If it reports violations the auto-fixers could not resolve, stop and report
   them -- do not attempt ad hoc fixes outside this sequence.
```

**Session transcript** (skill loaded):

```text
[agent] loads skill: project-lint-format
[agent] step 1: npm run lint:md:fix -- 3 files auto-fixed
[agent] step 2: gofmt -w changed_file.go -- reformatted
[agent] step 3: lint check-only -- 0 violations remaining
[agent] pipeline complete, following the skill's documented step order
```
