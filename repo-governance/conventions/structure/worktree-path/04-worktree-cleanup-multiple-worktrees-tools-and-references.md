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

1. Verify nothing is uncommitted or unpushed: `git -C worktrees/<name> status --porcelain` must be empty, and the worktree HEAD must be an ancestor of `origin/main`
2. Remove the worktree: `git worktree remove worktrees/<name>` (preferred over `rm -rf`, which leaves a stale registration)
3. Prune any stale references: `git worktree prune`
4. Optionally remove the branch: `git branch -d <name>` (safe delete; only succeeds when fully merged)

For plan worktrees, the [plan-execution workflow](../../../workflows/plan/plan-execution.md) performs this cleanup automatically after a plan is archived and pushed — but ALWAYS prompts the user for confirmation first. Worktrees are never deleted silently.

**Plan delivery checklist tagging**: when any of these three commands — `git worktree add`, the push (to the PR branch under the default `worktree-to-pr`, or `git push origin main` under a direct-push mode), or `git worktree remove` — appear as steps in a plan delivery checklist, they MUST be tagged `[AI]`. Tagging them `[HUMAN]` incorrectly creates a hand-off gate where none exists. See [Plans Organization Convention §Executor Tagging](../plans/17-executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule) and the [Git Push Default Convention](../../../development/workflow/git-push-default.md) for the canonical rule statement and FAIL/PASS examples.

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
