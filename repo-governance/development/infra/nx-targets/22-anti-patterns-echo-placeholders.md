---
title: "Anti-Patterns — Echo Placeholders"
description: Clarifies that echo placeholders for test:unit/test:integration/test:e2e are required, not an anti-pattern -- omitting the mandatory-six is.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when deciding whether a project without real integration or E2E tests still needs the target declared.
---

# Anti-Patterns — Echo Placeholders

## Echo Placeholders vs. Omitted Targets

`test:unit: echo "no unit tests"`, `test:integration: echo "no integration tests"`, and
`test:e2e: echo "no e2e tests"` declared as mandatory placeholder targets are **required** — they are
**not anti-patterns**. The anti-pattern is _omitting_ the mandatory-six targets entirely. Echo
placeholders enable `nx affected -t test:unit` (and similar) to run workspace-wide without
special-casing any project.

The `build` no-op rule still stands: do not add a no-op `build` to interpreted-language projects that
have no compile step. Only the three test targets (`test:unit`, `test:integration`, `test:e2e`) and
`typecheck` use echo placeholders as the required pattern when the real implementation does not apply.
