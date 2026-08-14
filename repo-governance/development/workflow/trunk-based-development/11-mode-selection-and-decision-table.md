---
title: "Mode Selection Does Not Depend on Execution Context Alone"
description: Why work location and integration target are independent axes, plus a decision table resolving the delivery mode for common situations.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when unsure which delivery mode applies to a given situation, or explaining why worktree usage alone doesn't determine it.
---

# Mode Selection Does Not Depend on Execution Context Alone

Running from inside a git worktree does not, by itself, force a PR -- a plan may still declare
`worktree-to-origin-main` and push directly. Conversely, running from the primary checkout does not
force direct push either -- `main-to-pr` uses the primary checkout while still routing through a PR.
Work location (worktree vs. primary checkout) and integration target (PR vs. direct push) are
independent axes; the active mode is whichever the three-tier precedence resolves to (invocation
argument > plan field > default `worktree-to-pr`), never inferred from execution context alone.

## Decision Table

| Situation                               | Resolved Delivery Mode (absent an explicit override)    |
| --------------------------------------- | ------------------------------------------------------- |
| Routine development, no mode specified  | `worktree-to-pr` (repo-wide default)                    |
| Plan declares `worktree-to-origin-main` | Worktree work location, direct push to `origin main`    |
| Plan declares `main-to-origin-main`     | Primary checkout, direct push to `origin main`          |
| Plan declares `main-to-pr`              | Primary checkout, PR opened against `main`              |
| Invocation argument names a valid mode  | The named mode overrides the plan field and the default |
| External contribution                   | Fork + PR (follows the `*-to-pr` review/merge protocol) |
