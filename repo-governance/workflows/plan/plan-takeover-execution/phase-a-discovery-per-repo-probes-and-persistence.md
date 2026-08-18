---
title: "Phase A — Discover Every Trace of This Plan: Per-Repo Probes and Persistence"
description: Covers Phase A steps A2 and A3 — the ordered six-item per-repo probe list, and persisting raw findings to the takeover-report as they're gathered.
when_to_use: Use when running the ordered per-repo discovery probes, or when deciding what to log to the takeover-report during discovery.
---

# Phase A — Discover Every Trace of This Plan: Per-Repo Probes and Persistence (Sequential per Repo, Hard Gate)

**Continued from** [Phase A — Plan-Identifier and Repo Set](./phase-a-discovery-plan-identifier-and-repo-set.md).

**A2. Per repo, in this order, log every hit verbatim** — never summarize a hit away as "probably
stale" at discovery time; that judgment belongs to Phase B, with evidence in hand:

1. **Local worktrees**: `git worktree list --porcelain` from the repo's primary checkout; grep for
   `<plan-identifier>` in the path or branch name.
2. **Local branches**: `git branch --list '*<plan-identifier>*'`.
3. **Remote branches**: `git ls-remote --heads origin '*<plan-identifier>*'` — this finds a pushed
   branch even without a local fetch of that ref.
4. **PRs, open and closed**: `gh pr list --repo <owner>/<repo> --search "<plan-identifier> in:title,body,head" --state all --json number,state,headRefName,mergedAt,url`.
5. **Plan-folder location on `origin/main`**: `git ls-tree -r origin/main --name-only -- 'plans/*<slug>*'` —
   does the folder live in `backlog/`, `in-progress/`, or an already-dated `done/` entry?
6. **On any found worktree or branch**: read its copy of `delivery.md` (if present) and record every
   `- [x]` count plus that location's own `git status --porcelain` output. Never assume a found
   worktree is clean just because it exists.

**A3. Persist raw findings to the takeover-report as they're gathered**, not held in memory only —
this file is the recovery point if the session is interrupted mid-discovery, consistent with the
scratchpad-first defensive posture this repo's own incident history recommends for multi-step work in
a shared checkout.
