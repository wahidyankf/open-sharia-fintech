---
title: "Archive Exclusion"
description: "Why plans/done/ and archived/ are excluded from markdown linting."
category: explanation
subcategory: development
tags:
  - markdown
  - linting
  - formatting
  - prettier
  - markdownlint
  - quality
created: 2026-01-17
when_to_use: "Use when deciding whether archived content should be linted."
---

# Archive Exclusion

`plans/done/` and `archived/` are excluded from markdown linting in both
`.markdownlintignore` and `.markdownlint-cli2.jsonc`.

**Rationale**: Archived content is frozen historical record. Internal links in archived plans
legitimately rot over time as files are renamed, moved, or deleted — this is expected and
acceptable behaviour for historical artifacts. Linting frozen content produces false positives
that block active work without improving quality.

**Policy**:

- `plans/done/` — completed plans moved there for historical reference after execution
- `archived/` — any other archived content (retired apps, deprecated docs)

**Active content is still fully linted**: `plans/in-progress/`, `plans/backlog/`, all `docs/`,
`repo-governance/`, and app source files are checked without exception. Only frozen archives
are excluded.

**Configuration**:

```
# .markdownlintignore
plans/done/
archived/

# .markdownlint-cli2.jsonc ignores array
"plans/done/**",
"archived/**",
```
