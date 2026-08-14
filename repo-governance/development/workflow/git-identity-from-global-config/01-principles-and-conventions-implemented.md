---
title: "Principles and Conventions Implemented"
description: The principles and companion convention the Git Identity From Global Config Convention implements and respects.
category: explanation
subcategory: development
tags:
  - git
  - identity
  - commits
  - security
  - reproducibility
created: 2026-05-19
when_to_use: Use when tracing why per-repo git identity overrides are prohibited back to the principles and conventions this rule respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Global git config is a deliberate, visible identity declaration that applies consistently
  across all projects. A per-repo override is an implicit, local mutation that silently
  overrides the developer's stated identity without any warning at commit time.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Commits
  attributed to an unintended identity are a symptom of a per-repo override existing in
  `.git/config`. Removing the override at the root eliminates the class of problem entirely,
  rather than rewriting history after the fact.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**:
  A developer's identity must resolve consistently regardless of which subrepo they are
  working in. Implicit per-repo overrides break that consistency.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  A pre-commit hook enforces the rule automatically on every commit attempt, removing any
  dependency on manual audit of `.git/config` files.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../../quality/code.md)**: Identity enforcement is implemented as a
  Husky pre-commit hook, consistent with the automated quality gate pattern used across the
  repository.
