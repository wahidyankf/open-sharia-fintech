---
title: "Default Branch and Working on Main Directly"
description: The trunk is main with no develop/release/hotfix branches, and the classic direct-commit-to-trunk shape (not executable in ose-public).
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when explaining why there is no develop/release/hotfix branch, or when illustrating the classic direct-commit-to-main TBD shape.
---

# Default Branch and Working on Main Directly

## Default Branch: `main`

- **The trunk is `main`**: All development happens on `main` branch
- **No `develop` branch**: We don't use GitFlow or similar multi-branch strategies
- **No release branches**: Releases are tagged commits on `main`
- **No hotfix branches**: Hotfixes commit directly to `main` (or very short-lived branches)

## Working on `main` Directly

> This subsection describes TBD's classic direct-commit-to-trunk shape — one of the two direct-push
> delivery modes named in this repo's vocabulary (`worktree-to-origin-main`, `main-to-origin-main`).
> This repository's own **repo-wide default** is the short-lived-branch-via-PR shape (`worktree-to-pr`)
> — see [Default Push and Worktree Execution](./08-default-push-and-worktree-execution.md#default-push-and-worktree-execution) below.
>
> **Per-repository restriction (independent of the shape described here)**: in `ose-public`,
> `main` is branch-protected against direct pushes — including for admins — so
> **neither direct-push mode has an executable path there at all**. In
> `ose-private`, both remain available only for infrastructure-as-code plans. See
> [Plans Organization Convention §Per-Repository Delivery Mode Restrictions](../../../conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
> for the full rule. The PASS example immediately below is therefore **not executable in this repo
> (`ose-public`)** — it is retained as illustrative TBD vocabulary and remains genuinely runnable only
> for `ose-private` infrastructure-as-code plans.

PASS (only where the per-repository restriction above does not block it — not currently `ose-public`):
**You should commit directly to `main` when**:

- Change is small and well-tested
- You're confident tests will pass
- Change won't break others' work
- Feature flags hide incomplete functionality
- You can commit and push multiple times per day

**Example workflow**:

```bash
# Work on main branch
git checkout main
git pull origin main

# Make small change
# ... edit files ...

# Test locally
npm test

# Commit directly to main
git add .
git commit -m "feat(auth): add email validation helper"
git push origin main

# CI runs automatically
# Change is now visible to entire team
```
