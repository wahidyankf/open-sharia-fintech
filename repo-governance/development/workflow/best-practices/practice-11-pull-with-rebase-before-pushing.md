---
title: "Practice 11: Pull with Rebase Before Pushing"
description: Always pull latest changes from remote main before pushing, preferring rebase for clean linear history in Trunk Based Development.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use immediately before pushing to main, to pull the latest remote changes with rebase first.
---

# Practice 11: Pull with Rebase Before Pushing

**Principle**: Always pull latest changes from remote main before pushing, preferring rebase for clean linear history in Trunk Based Development.

**Default Strategy: Rebase**

For Trunk Based Development with small, frequent commits, rebase creates cleaner linear history:

**Good Example (Rebase):**

```bash
# Work completed locally with commits
git status
# On branch main
# Your branch is ahead of 'origin/main' by 1 commit

# Pull with rebase BEFORE pushing (recommended for TBD)
git pull --rebase origin main

# If there are remote changes, Git replays your commits on top
# Linear history: no merge commits

# Review the result
git log --oneline --graph -10

# Now push your changes
git push origin main
# Success! Clean linear history preserved
```

**Bad Example:**

```bash
# Work completed locally
git push origin main

# Push rejected!
# error: failed to push some refs to 'origin'
# hint: Updates were rejected because the remote contains work that you do
# hint: not have locally. This is usually caused by another repository pushing
# hint: to the same ref.

# Now forced to pull and resolve
git pull origin main
# Merge required - could have been avoided!
```

**Rationale for Rebase-First Approach:**

- **Linear history**: No merge commits cluttering git log in TBD workflow
- **Cleaner visualization**: `git log --oneline` shows straight line of development
- **Better for TBD**: Small, frequent commits integrate cleanly without merge noise
- **Easier bisect**: `git bisect` works better with linear history
- **Simpler to understand**: Each commit applies directly on top of previous
- **Professional appearance**: Enterprise projects favor linear commit history
