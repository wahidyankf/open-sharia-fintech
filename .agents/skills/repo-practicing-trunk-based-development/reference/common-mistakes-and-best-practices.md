# Trunk-Based Development — Common Mistakes and Best Practices

## Common Mistakes

### ❌ Mistake 1: Creating unnecessary branches

**Wrong thinking**: "I'll create a branch just to be safe"

**Right thinking**: "Can I use a feature flag? If yes, use a short-lived `worktree-to-pr` branch
and integrate it promptly into `main`"

### ❌ Mistake 2: Long-lived branches (> 1 day)

**Wrong**: Branch open for weeks accumulating changes

**Right**: Short-lived, single-purpose `worktree-to-pr` branches integrated promptly into `main`;
experimental branches remain time-bounded

### ❌ Mistake 3: Treating environment branches as development branches

**Wrong**: `git commit` directly to `prod-ayokoding-www`

**Right**: Merge into `main` through the resolved delivery mode; let CI/CD deploy to the environment
branch

### ❌ Mistake 4: Large, infrequent commits

**Wrong**: One commit bundles independent purposes, or many tiny commits split one purpose's
required completion artifacts

**Right**: After explicit authorization, compose the fewest build-valid, independently reviewable,
and revertible commits; use no fixed line-count or commits-per-day quota

### ❌ Mistake 5: Committing broken code to main

**Wrong**: Push commits that fail tests "I'll fix it later"

**Right**: Every commit passes tests (use pre-push hooks)

## Best Practices

### TBD Checklist

Before pushing a delivery branch, or using an explicitly eligible direct-main mode:

- [ ] The user explicitly authorized the named change set before staging or committing
- [ ] Boundaries are the fewest that remain build-valid, reviewable, and revertible
- [ ] PR boundaries follow natural cohesive seams, never LOC or file counts
- [ ] Commit is atomic (complete, working unit)
- [ ] Required tests, docs, specs, references, migrations, and mirrors stay with their purpose
- [ ] Tests pass for this commit
- [ ] Commit message follows Conventional Commits
- [ ] Resulting `main` state is safe to deploy to production immediately
- [ ] Incomplete behavior is inert behind a temporary production-disabled flag, with both paths
      tested and rollout, rollback, and removal recorded
- [ ] No environment branch commits
- [ ] Working on latest `main` (pulled recently)

### When in Doubt

**Ask these questions**:

1. **Does each proposed boundary pass the thematic test?** → Keep only independently reviewable
   and revertible purposes separate
2. **Is the resulting state production-deployable?** → If no, it cannot merge
3. **Can incomplete behavior be complete-and-inert behind a feature flag?** → If yes, test both
   paths and record rollout, rollback, and removal
4. **Have I declared the mode in the plan?** → If no, the default `worktree-to-pr` applies

**Default to `worktree-to-pr`. Choose a direct-push mode deliberately, and declare it in the plan.**
