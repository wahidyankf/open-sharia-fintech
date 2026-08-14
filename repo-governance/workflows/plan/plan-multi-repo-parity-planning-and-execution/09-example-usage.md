---
title: "Example Usage"
description: Two worked examples of invoking the composite — all three repos in default order, and a two-repo run with custom order.
when_to_use: Use when constructing an invocation of this workflow or explaining its behavior with a concrete example.
---

# Example Usage

## Default: All Three Repos, Plan Then Execute

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: standardize markdown
       gates across ose-public, ose-primer, and ose-private"
```

The orchestrator surveys the three repos, builds and grills the deviation matrix, researches and
re-grills, authors and gates three plans, pushes them to each repo's `origin main`, grills the
execution specifics, then executes each plan in its repo's designated worktree (synced to
`origin/main`) one repo at a time — archiving each plan, repairing sibling links, and prompting
before each worktree deletion.

## Two Repos, Custom Order

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: align agent catalogs
       repos: ose-public, ose-private"
```

Plans and executes only the two listed repos; the pre-execution grill confirms which runs first.
