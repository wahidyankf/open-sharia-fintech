---
title: "Anti-Pattern: Long-Lived Feature Branches"
description: Feature branches lasting weeks cause merge conflicts and integration delays, and the fix that avoids them.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when tempted to keep a feature branch open for more than a day or two instead of shipping in small integrated phases.
---

# Anti-Pattern: Long-Lived Feature Branches

**Problem**: Feature branches lasting weeks cause merge conflicts and integration delays.

**Bad Example:**

```bash
# Create feature branch
git checkout -b feature/user-dashboard

# Work for 3 weeks on branch
# ... hundreds of commits ...

# Try to merge - MASSIVE CONFLICTS!
git checkout main
git pull origin main
git merge feature/user-dashboard
# 200 conflicts in 50 files!
```

**Solution:**

```bash
# Split the work into phases. Each phase gets its own short-lived branch and PR,
# and lands within a day or two -- the default `worktree-to-pr` mode.
git worktree add worktrees/dashboard-widget -b dashboard-widget

# Commit an internally complete increment; the production-disabled flag controls exposure
git commit -m "feat(dashboard): add user widget (flag OFF)"
git push origin dashboard-widget
gh pr create --draft --base main
# ... review cycle + CI, then merge. Next phase gets a fresh branch and PR.

# Enable when ready
# config: ENABLE_USER_DASHBOARD=true
```

Under a declared direct-push mode the same shape applies without the branch and PR — commit and
`git push origin main` daily. Either way the fix is the same: **integrate internally complete,
production-deployable increments frequently**. Incomplete behaviour stays inert behind a temporary
production-disabled flag; both paths pass and rollout, rollback, and removal are recorded.

**Rationale:**

- Frequent integration prevents conflicts — the branch's _lifespan_ is the problem, not its existence
- Each branch is single-purpose and disposable, so it never diverges far from `main`
- Feature flags control visibility of complete, tested increments, removing the reason to hold work back
- Faster feedback
