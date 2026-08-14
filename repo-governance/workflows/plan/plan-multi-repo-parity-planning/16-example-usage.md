---
title: "Example Usage"
description: Three worked examples — default worktree-to-pr, direct push with backlog stage, and a two-repo subset.
when_to_use: Use when constructing an invocation of this workflow or explaining its behavior with a concrete example.
---

# Example Usage

## Default: All Three Repos, worktree-to-pr, in-progress

```
User: "Run plan-multi-repo-parity-planning for objective: standardize markdown gates across
       ose-public, ose-primer, and ose-private"
```

The orchestrator surveys each repo, builds the deviation matrix, grills the invoker (Step 3),
optionally delegates research to `web-researcher` (Step 4), grills again post-research
(Step 5), authors three plans (one per repo) in `plans/in-progress/standardize-markdown-gates/`,
gates each plan, and opens a draft PR per repo rather than pushing directly to `origin main` —
the repo-wide `worktree-to-pr` default.

## Direct push with backlog stage

```
User: "Run plan-multi-repo-parity-planning for objective: align agent catalogs
       mode: worktree-to-origin-main stage: backlog"
```

Creates three backlog plans at `plans/backlog/align-agent-catalogs/`, gates
each, and pushes each plan directly to its repo's `origin main` via worktrees instead of opening
a PR. Useful when the invoker wants to skip the formal review step for low-risk plan documents.

## Subset of Two Repos

```
User: "Run plan-multi-repo-parity-planning for objective: add specs:coverage gate
       repos: ose-public, ose-primer"
```

Surveys only `ose-public` and `ose-primer`, builds a two-column deviation matrix, grills the
invoker, authors two plans, and delivers both. `ose-private` is excluded from this run.
