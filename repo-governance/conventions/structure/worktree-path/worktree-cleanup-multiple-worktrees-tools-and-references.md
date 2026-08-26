---
title: "Worktree Path: Cleanup, Multiple Worktrees, Tools, and References"
description: The worktree removal procedure and AI/HUMAN tagging rule, the multiple-concurrent-worktrees layout, the tools that interact with this convention, and related convention/documentation links
when_to_use: Read this when removing a worktree, tagging worktree-related delivery checklist steps, or looking up a related convention or reference.
category: explanation
subcategory: conventions
tags:
  - worktree
  - git
  - repository-structure
  - claude
  - hooks
created: 2026-05-03
---

# Worktree Path: Cleanup, Multiple Worktrees, Tools, and References

## Worktree Cleanup

When removing a worktree:

1. Resolve the exact path from the plan's Provisioned Worktree Identity, then reconcile it with
   `git worktree list --porcelain`. Inventory every plan-created and current branch from the Delivery
   Branch Inventory and `git -C <exact-path> branch --show-current`; a missing identity, path
   conflict, or unclassified branch blocks removal.
2. For each inventoried branch, prove its PR merged, or for a direct-push entry prove its recorded
   commit reached `origin/main` and no PR remains open. Do not use `origin/main` ancestry for a
   squash-merged PR branch.
3. Verify the exact worktree is clean and idle (`git -C <exact-path> status --porcelain`) and every
   inventoried branch has no unpushed commit.
4. When every check passes, immediately run non-force `git worktree remove <exact-path>`, then the
   canonical [branch cleanup](../../../development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md).
   `git worktree prune` may follow. If any check or removal fails, retain the worktree, preserve the
   evidence, and escalate; never force removal or prompt for an otherwise eligible exact plan path.

For plan worktrees, the [plan-execution workflow](../../../workflows/plan/plan-execution.md) performs
this cleanup immediately when that repo's delivery is confirmed. It never removes a root, wildcard,
identity-unknown, or another actor's worktree.

**Plan delivery checklist tagging**: when any of these three commands — `git worktree add`, the push (to the PR branch under the default `worktree-to-pr`, or `git push origin main` under a direct-push mode), or `git worktree remove` — appear as steps in a plan delivery checklist, they MUST be tagged `[AI]`. Tagging them `[HUMAN]` incorrectly creates a hand-off gate where none exists. See [Plans Organization Convention §Executor Tagging](../plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule) and the [Git Push Default Convention](../../../development/workflow/git-push-default.md) for the canonical rule statement and FAIL/PASS examples.

## Multiple Worktrees

The pattern supports multiple concurrent worktrees:

```
worktrees/
├── feature-auth/
├── bugfix-session-timeout/
└── experiment-new-api/
```

## Tools and Automation

Reference agents or tools that interact with this convention:

- **WorktreeCreate hook** (`.claude/hooks/worktree-create.sh`) — Routes `claude --worktree` to custom path
- **repo-rules-checker** — Validates worktree-related rules and gitignore compliance

## References

**Related Conventions:**

- [File Naming Convention](../file-naming.md) — Kebab-case file naming standards

**Related Documentation:**

- [AGENTS.md](../../../../AGENTS.md) — agent configuration
- [Repository Governance Architecture](../../../repository-governance-architecture.md) — Six-layer governance hierarchy
