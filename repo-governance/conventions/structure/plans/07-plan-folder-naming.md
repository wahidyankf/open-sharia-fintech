---
title: "Plan Folder Naming"
description: Defines the stage-aware folder naming rules for backlog/, in-progress/, and done/, including the completion-date prefix used only in done/.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when naming or renaming a plan folder as it moves between lifecycle stages.
---

# Plan Folder Naming

Naming differs by lifecycle stage. Each stage has its own rule.

## backlog/ — NO date prefix

```
[project-identifier]/
```

Backlog plans carry no date prefix. A date is added only when the plan is archived to `done/`.

## in-progress/ — NO date prefix

```
[project-identifier]/
```

Active plans carry no date prefix at all. The date is added only when the plan is archived to
`done/`. Moving a plan from `backlog/` to `in-progress/` is a pure move — neither stage carries a date prefix, so no rename is needed.

## done/ — completion date prefix

```
YYYY-MM-DD__[project-identifier]/
```

The date is the day the plan was completed (last git-committed), NOT the creation date. When
archiving from `in-progress/`, add the completion date prefix.

## Naming Rules (all stages)

- **Date Format** (`done/` only): ISO 8601 (`YYYY-MM-DD`)
- **Separator** (`done/` only): Double underscore `__` separates the completion date from the identifier
- **Identifier**: Kebab-case (lowercase with hyphens)
- **No Spaces**: Use hyphens instead of spaces
- **No Special Characters**: Only alphanumeric and hyphens in identifier

## Examples

**Good (backlog/)**:

- `backlog/init-monorepo/`
- `backlog/auth-system/`
- `backlog/payment-integration/`

**Good (in-progress/)**:

- `in-progress/mobile-app-redesign/`
- `in-progress/auth-system/`
- `in-progress/payment-integration/`

**Good (done/)**:

- `done/2025-11-24__init-monorepo/` (completion date)
- `done/2026-01-15__mobile-app-redesign/` (completion date)

**Bad**:

- `backlog/2026-01-15__auth-system/` (date prefix in backlog — WRONG)
- `in-progress/2026-01-15__mobile-app-redesign/` (date prefix in in-progress — WRONG)
- `2025-11-24_init-monorepo/` (single underscore)
- `2025-11-24__Init Monorepo/` (capital letters, spaces)
- `2025-11-24__init_monorepo/` (underscores in identifier)
