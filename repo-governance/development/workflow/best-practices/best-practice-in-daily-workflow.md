---
description: A worked start-of-day-to-push walkthrough using rebase, including what to do when a conflict appears.
when_to_use: Use as a concrete daily-workflow template combining rebase config, pulling, committing, and pushing.
---

# Best Practice in Daily Workflow

**Start of day workflow with rebase:**

```bash
# Configure main branch for rebase (one-time setup)
git config branch.main.rebase true

# Start of day: Get latest with rebase
git checkout main
git pull origin main  # Automatically rebases due to config

# Make changes
# ... work work work ...

# Commit locally
git add .
git commit -m "feat(auth): add validation"

# Before pushing: Pull with rebase again (main may have advanced)
git pull origin main  # Automatically rebases due to config

# Review history (should be linear)
git log --oneline --graph -10

# Push your changes
git push origin main
# Success! Linear history maintained
```

**When conflicts appear:**

```bash
# Pull with rebase
git pull origin main

# Conflict in one file
# Resolve conflict, then:
git add <resolved-file>
git rebase --continue

# If conflicts too complex:
git rebase --abort
git pull origin main  # Use merge instead
```
