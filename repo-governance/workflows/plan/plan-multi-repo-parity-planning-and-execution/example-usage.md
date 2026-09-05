---
title: "Example Usage"
description: Two worked examples of invoking the composite — both parity repos, and a single-repo subset.
when_to_use: Use when constructing an invocation of this workflow or explaining its behaviour with a concrete example.
---

# Example Usage

## Default: Both Parity Repos, Plan Then Execute

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: standardize markdown
       gates across ose-public and ose-private"
```

The orchestrator surveys both repos, builds and grills the deviation matrix, researches and
re-grills, authors and gates one plan per repo, pushes them to each repo's `origin main`, grills the
execution specifics, then executes each plan in its repo's designated worktree (synced to
`origin/main`) one repo at a time — archiving each plan, repairing sibling links, and immediately
removing each eligible exact identity-recorded worktree; failed preconditions retain evidence and
escalate.

## One Repo Only

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: align agent catalogs
       repos: ose-public"
```

Plans and executes only the listed repo; `ose-private` is excluded from this run.
