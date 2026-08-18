---
title: "When to Use Merge vs Rebase"
description: Rebase is the default for daily TBD workflow; five conditions where merge is the safer choice instead.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when deciding whether to pull with rebase or merge for a specific situation.
---

# When to Use Merge vs Rebase

## Default: Use Rebase

**For normal Trunk Based Development workflow**:

```bash
# Daily workflow with rebase (RECOMMENDED)
git pull --rebase origin main
git push origin main
```

**When rebase is ideal**:

- Small, frequent commits (TBD standard workflow)
- Few local commits (1-3 commits)
- Working on main branch
- No conflicts expected
- Clean linear history desired
- Normal day-to-day development

## When to Use Merge Instead

**Switch to merge when you encounter:**

**1. Heavy conflicts** - Easier to resolve all conflicts at once:

```bash
# Many conflicts during rebase? Abort and merge instead
git rebase --abort
git pull origin main  # Uses merge
# Resolve all conflicts in one merge commit
```

**2. Large divergence** - Many commits on both sides:

```bash
# You have 10 local commits, remote has 15 new commits
# Rebase would require resolving conflicts 10+ times
git pull origin main  # Merge is safer here
```

**3. Preserve parallel work timing** - Want to show work happened in parallel:

```bash
# Documenting simultaneous development by multiple developers
git pull origin main  # Merge preserves parallel history
```

**4. Safety preference** - When unsure, merge is safer:

```bash
# Unsure about conflicts or impact?
git pull origin main  # Merge doesn't rewrite history
```

**5. Already pushed commits** - NEVER rebase commits others have pulled:

```bash
# CRITICAL: If you've pushed and others pulled, ONLY merge
git pull origin main  # Never rebase shared commits!
```
