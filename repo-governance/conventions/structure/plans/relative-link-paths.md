---
title: "Relative Link Paths in Plan Files"
description: Explains the three-level ../../../ relative-path depth for links from a plan file to repo-root directories, with the one-level-shallower exception for two-pagers.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing a relative link from inside a plan folder or a two-pager to a repo-root file.
---

# Relative Link Paths in Plan Files

Plan files sit three directory levels deep from the repository root: `plans/` → `in-progress/` (or `backlog/` or `done/`) → `[identifier]/` (backlog and in-progress) or `YYYY-MM-DD__identifier/` (done). Any markdown file inside a plan folder must use `../../../` to reach root-level directories such as `repo-governance/`, `docs/`, `apps/`, or `libs/`.

## Correct Path Depth

| Target from a plan file                          | Correct prefix |
| ------------------------------------------------ | -------------- |
| `repo-governance/conventions/structure/plans.md` | `../../../`    |
| `docs/how-to/organize-work.md`                   | `../../../`    |
| `apps/organiclever-be/README.md`                 | `../../../`    |
| Sibling file in the same plan folder             | `./`           |

**Two-pagers are one level shallower.** A two-pager lives directly at `plans/ideas/<slug>.md`
(two levels deep, not three like a `plans/<stage>/<slug>/` plan file), so it reaches
`repo-governance/...` with `../../` — not `../../../`. Sibling two-pagers and the folder README
resolve with `./`.

## Example

A plan at `plans/in-progress/my-feature/README.md` links to the AI Agents Convention:

```markdown
<!-- PASS: Three levels up to reach repo root, then down into repo-governance/ -->

[AI Agents Convention](../../../repo-governance/development/agents/ai-agents.md)
```

```markdown
<!-- FAIL: Only two levels up — resolves to plans/repo-governance/ (does not exist) -->

[AI Agents Convention](../../repo-governance/development/agents/ai-agents.md)
```

## Why Three Levels

The plan subfolder adds a third level of nesting that `docs/` files at two levels deep (e.g., `repo-governance/conventions/structure/plans.md`) do not have. Forgetting this extra level produces a path that points into the `plans/` directory tree instead of the repository root.

Use the verification tip from the [Linking Convention](../../formatting/linking.md#verification-tip): start at the plan file's location, count each `../` as one directory up, and confirm you reach the repo root before descending into the target directory.
