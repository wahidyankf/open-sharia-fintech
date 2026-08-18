---
title: "Integration Diff Review Convention"
description: Read the full incoming diff and assess its impact on in-flight work whenever foreign commits land on the current branch.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - rebase
  - merge
  - review
created: 2026-08-06
when_to_use: Use immediately after a rebase, pull, merge, cherry-pick, or fast-forward lands commits you did not author.
---

# Integration Diff Review Convention

Any operation that brings commits from another branch or remote into the branch you are currently
working on — `git rebase`, `git pull`, `git merge`, `git cherry-pick`, or a fast-forward of local
`main` after a sibling worktree pushed ahead of it — changes the ground you are standing on. A clean
merge with zero textual conflicts is not evidence that the incoming changes are safe to ignore. Before
continuing the interrupted work, you MUST read the incoming diff in full and think hard about what
changed and what it means for what you were doing — not just check that git reports no conflict markers.

## Contents

- [Principles and Conventions Implemented](./integration-diff-review/principles-and-conventions-implemented.md) — Why this convention exists and its companion conventions.
- [The Rule and Reading Checklist](./integration-diff-review/the-rule-and-reading-checklist.md) — The five-step rule, and what to look for in the diff.
- [Commands and Agent Responsibilities](./integration-diff-review/commands-and-agent-responsibilities.md) — The exact commands per operation, and who is responsible.
- [Forbidden Actions and Examples](./integration-diff-review/forbidden-actions-and-examples.md) — What violates this convention, with worked pass/fail examples.

## Related Documentation

- [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md) — the
  companion convention for which local git operations are safe to run at all.
- [Agent Workflow Orchestration](../agents/agent-workflow-orchestration.md) — the same-machine
  assumption that makes concurrent, unreviewed integration events likely.
- [CI Post-Push Verification Convention](../workflow/ci-post-push-verification.md) — the parallel
  post-push discipline: verify after you push out, review after you pull in.
