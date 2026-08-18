---
title: "Key Differences from Documentation and Creating Plans"
description: Contrasts plans/ against docs/ across location, purpose, and lifecycle, then walks through the seven steps of creating a new plan.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding whether new content belongs in plans/ or docs/, or when starting to author a new plan.
---

# Key Differences from Documentation and Creating Plans

## Key Differences from Documentation

Plans differ from `docs/` in several important ways:

| Aspect           | Plans (`plans/`)                      | Documentation (`docs/`)              |
| ---------------- | ------------------------------------- | ------------------------------------ |
| **Location**     | Root-level `plans/` folder            | Root-level `docs/` folder            |
| **Purpose**      | Temporary project planning            | Permanent documentation              |
| **File Naming**  | Kebab-case by purpose                 | Kebab-case describing content        |
| **Lifecycle**    | Move between in-progress/backlog/done | Evolve and update in place           |
| **Audience**     | Project team, stakeholders            | All users, contributors, maintainers |
| **Longevity**    | Temporary (archived in done/)         | Permanent (evolves over time)        |
| **Organization** | By project and status                 | By Diátaxis category                 |

## Creating Plans

1. **Start with an idea**: Capture the idea as a two-pager in `plans/ideas/<slug>.md` (see [Ideas Folder (Two-Pagers)](./ideas-folder-overview-rationale-and-file-layout.md#ideas-folder-two-pagers))
2. **Formalize when ready**: Promote the two-pager to a full plan folder in `backlog/` when it is ripe
3. **Follow naming convention**: Use `[project-identifier]/` format (no date prefix in `backlog/`)
4. **Choose structure**: Default to the five-document multi-file layout (`README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`). Collapse to single-file only when all four exception criteria in the Structure Decision section are met simultaneously.
5. **Resolve design decisions via structured grilling**: Before writing plan content, resolve all
   open design decisions using the
   [Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md) — structured
   multiple-choice questions with 2-4 concrete options, explicit trade-offs, and exactly one Recommended
   option. Never ask open-ended "what approach?" questions without offering structured options.
6. **Create content**: Write overview, requirements, tech docs, and delivery sections
7. **Update index**: Add plan to `backlog/README.md`
