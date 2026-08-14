---
title: "Standard 4: Maintain Linear History Before Pushing"
description: Rebase rather than merge before every push, and never let a merge commit reach main or a PR branch.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - push
  - trunk-based-development
  - ai-agents
created: 2026-04-25
when_to_use: Use before pushing when the remote may have moved forward since the last pull or push.
---

# Standard 4: Maintain Linear History Before Pushing

Before pushing — whether to a PR branch or to `origin main` — ensure the local branch has a linear
history with respect to its remote counterpart. If the remote has moved forward since the last pull or
push, rebase rather than merge:

```bash
# If remote has new commits since last pull, rebase first
git pull --rebase origin <target-branch>
# Then push
git push origin <target-branch>
```

Never create merge commits when pushing to `main` or to a PR branch. A merge commit in the history
violates this standard. If a merge commit appears locally, squash or rebase it before pushing. When a
PR is ready to land, prefer GitHub's squash or rebase merge over a local `git merge` — the
[PR Merge Protocol](../pr-merge-protocol.md) governs that final step.
