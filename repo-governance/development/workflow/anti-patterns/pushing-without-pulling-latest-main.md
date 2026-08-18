---
title: "Anti-Pattern: Pushing Without Pulling Latest Main"
description: Pushing without first pulling and rebasing on the latest main causes push rejections and messy merge commits.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when about to push to main without first pulling with rebase, or when configuring the team's pull strategy.
---

# Anti-Pattern: Pushing Without Pulling Latest Main

**Problem**: Pushing to main without first pulling latest changes causes push failures and forced merge situations.

**Bad Example:**

```bash
# You have local commits
git commit -m "feat(api): add endpoint"

# Push directly without pulling
git push origin main

# Push rejected!
# error: failed to push some refs to 'origin'
# hint: Updates were rejected because the remote contains work that you do
# hint: not have locally.

# Now must pull and merge
git pull origin main
# Forced merge situation - conflicts may occur
# Could have been handled more deliberately
```

**Additional Anti-Pattern: Using Merge When Rebase Would Be Cleaner**

```bash
# Small change, no conflicts expected
git commit -m "fix(typo): correct documentation spelling"

# Using merge creates unnecessary merge commit
git pull origin main  # Creates merge commit
git push origin main

# Result: Cluttered history with merge commits for trivial integrations
# git log shows merge commits for every pull
```

**Solution (Recommended for TBD):**

```bash
# You have local commits
git commit -m "feat(api): add endpoint"

# Pull with rebase BEFORE pushing (recommended for TBD)
git pull --rebase origin main
# Replays your commits on top of remote changes
# Linear history, no merge commits

# Now push clean result
git push origin main
# Success! Clean linear history
```

**Alternative Solution (When Merge is Appropriate):**

```bash
# Large divergence or many conflicts expected
git commit -m "feat(api): add endpoint"

# Use merge when safer
git pull origin main  # Merge strategy
# Resolve conflicts in one merge commit

# Push merged result
git push origin main
```

**Additional Anti-Pattern: Not Configuring Pull Strategy**

```bash
# No pull strategy configured - behavior inconsistent
git pull origin main
# Uses default (merge on some systems, rebase on others)
# Team members have different history results
```

**Solution:**

```bash
# Configure pull strategy for main branch
git config branch.main.rebase true

# Now consistent behavior for entire team
git pull origin main  # Always rebases for main branch
```

**Rationale:**

- Prevents push rejection errors
- Allows deliberate conflict resolution locally
- **Rebase creates cleaner linear history for TBD workflow**
- **Reduces merge commit noise in git log**
- **Consistent pull strategy across team**
- Respects Trunk Based Development principles (small, frequent commits integrate cleanly)
- Better collaboration in team environments
- Reduces merge friction
- **Professional appearance with linear commit history**
