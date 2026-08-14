# Trunk-Based Development — Commit Patterns

## Small, Frequent Commits

**Target**: Multiple commits per day, each < 200 lines changed

**Rationale**: Small commits are:

- Easier to review
- Easier to revert
- Easier to understand in git history
- Lower risk of conflicts

**Example workflow**:

```bash
# Commit 1: Add data model
git add src/models/user.ts
git commit -m "feat(models): add User data model"
git push origin <plan-branch>

# Commit 2: Add repository interface
git add src/repositories/user-repository.ts
git commit -m "feat(repositories): add UserRepository interface"
git push origin <plan-branch>

# Commit 3: Add service layer
git add src/services/user-service.ts
git commit -m "feat(services): add UserService with CRUD operations"
git push origin <plan-branch>
```

**NOT**:

```bash
# Bad: One massive commit after 3 days
git add src/*
git commit -m "feat(user): add complete user management system"
git push origin <plan-branch>
```

## Atomic Commits

**Definition**: Each commit is a complete, working unit

**Rules**:

- ✅ Commit compiles and passes tests
- ✅ Commit includes related changes only
- ✅ Commit message describes change clearly
- ❌ Commit breaks build (fails tests)
- ❌ Commit mixes unrelated changes
- ❌ Commit message is vague

## Conventional Commits

This repository enforces Conventional Commits format:

```
<type>(<scope>): <description>

type: feat | fix | docs | style | refactor | test | chore
scope: component/module being changed
description: brief summary of change
```

**Examples**:

```bash
feat(auth): add JWT token validation
fix(api): handle null response from external service
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
test(user): add integration tests for user service
```
