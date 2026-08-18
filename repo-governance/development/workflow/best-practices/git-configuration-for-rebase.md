---
title: "Git Configuration for Rebase"
description: Three ways to configure git to pull with rebase by default — branch-specific, global, or explicit flag.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when setting up a repository or global git config so pulls rebase by default instead of merging.
---

# Git Configuration for Rebase

**Option 1: Configure main branch only (RECOMMENDED)**

```bash
# Make main branch always use rebase for pulls
git config branch.main.rebase true

# Verify configuration
git config branch.main.rebase
# Output: true

# Now `git pull` on main automatically rebases
git pull origin main  # Automatically uses --rebase
```

**Why branch-specific is recommended**: Predictable for main branch (TBD), but merge is still default for other branches.

**Option 2: Global configuration (all branches)**

```bash
# Make rebase default for all branches in this repository
git config pull.rebase true

# Or globally for all repositories
git config --global pull.rebase true

# Now all `git pull` commands use rebase by default
git pull origin main  # Automatically rebases
```

**Why global might be too aggressive**: Some branches (experimental, external PRs) may benefit from merge commits.

**Option 3: Explicit flag (most explicit)**

```bash
# Always specify strategy explicitly
git pull --rebase origin main  # Rebase
git pull origin main           # Merge (default)

# Add shell alias for convenience
git config --global alias.pr 'pull --rebase'
git pr origin main  # Shorthand for pull --rebase
```

**Recommendation**: Start with Option 1 (branch-specific for main), then expand to Option 2 if team is comfortable.
