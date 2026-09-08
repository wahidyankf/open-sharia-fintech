---
description: Rebase rather than merge before every push, and never let a merge commit reach main or a PR branch.
when_to_use: Use before pushing when the remote may have moved forward since the last pull or push.
---

# Standard 4: Maintain Linear History Before Pushing

Before pushing — whether to a PR branch or to `origin main` — ensure the local branch has a linear
history with respect to its remote counterpart. If the remote has moved forward since the last pull or
push, rebase rather than merge:

```bash
# If remote has new commits since last pull, rebase first
git pull --rebase origin <target-branch>
# If commits landed, complete Integration Diff Review before continuing
# Then push
git push origin <target-branch>
```

When the pull introduces commits absent from the pre-pull branch, the
[Integration Diff Review Convention](../integration-diff-review.md) requires a full-diff impact
checkpoint and any invalidated verification rerun before the push.

Never create merge commits when pushing to `main` or to a PR branch. A merge commit in the history
violates this standard. If a merge commit appears locally, squash or rebase it before pushing. When a
PR is ready to land, prefer GitHub's squash or rebase merge over a local `git merge` — the
[PR Merge Protocol](../pr-merge-protocol.md) governs that final step.
