# Trunk-Based Development — Common Mistakes and Best Practices

## Common Mistakes

### ❌ Mistake 1: Creating unnecessary branches

**Wrong thinking**: "I'll create a branch just to be safe"

**Right thinking**: "Can I use feature flags? If yes, work on main"

### ❌ Mistake 2: Long-lived branches (> 1 day)

**Wrong**: Branch open for weeks accumulating changes

**Right**: Short-lived experimental branches (< 1 week) or work on main

### ❌ Mistake 3: Treating environment branches as development branches

**Wrong**: `git commit` directly to `prod-ayokoding-www`

**Right**: Commit to `main`, let CI/CD deploy to environment branch

### ❌ Mistake 4: Large, infrequent commits

**Wrong**: One commit after 3 days with 1000 lines changed

**Right**: 10-15 small commits over 3 days, each < 200 lines

### ❌ Mistake 5: Committing broken code to main

**Wrong**: Push commits that fail tests "I'll fix it later"

**Right**: Every commit passes tests (use pre-push hooks)

## Best Practices

### TBD Checklist

Before pushing to `main`:

- [ ] Commit is small (< 200 lines changed)
- [ ] Commit is atomic (complete, working unit)
- [ ] Tests pass for this commit
- [ ] Commit message follows Conventional Commits
- [ ] Feature incomplete? Hidden behind feature flag
- [ ] No environment branch commits
- [ ] Working on latest `main` (pulled recently)

### When in Doubt

**Ask these questions**:

1. **Can I break this into smaller commits?** → If yes, do it
2. **Is the change small and obviously safe?** → If yes, a direct-push mode is a reasonable choice
3. **Can I hide incomplete work behind a feature flag?** → If yes, do so regardless of mode
4. **Have I declared the mode in the plan?** → If no, the default `worktree-to-pr` applies

**Default to `worktree-to-pr`. Choose a direct-push mode deliberately, and declare it in the plan.**
