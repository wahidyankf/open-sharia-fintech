---
name: repo-practicing-trunk-based-development
description: Trunk Based Development workflow - all development on main branch with small frequent commits, minimal branching, and continuous integration. Covers when branches are justified (exceptional cases only), commit patterns, feature flag usage for incomplete work, environment branch rules (deployment only), and AI agent default behavior (the repo-wide default delivery mode is `worktree-to-pr` -- a short-lived plan branch in a disposable worktree pushed to a draft PR; direct push to main remains available as an explicit selection). Essential for understanding repository git workflow and keeping branches short-lived
---

# Trunk Based Development Skill

## Purpose

This Skill provides comprehensive guidance on **Trunk Based Development (TBD)** - the git workflow used throughout this repository: small, frequent commits integrated continuously into `main` through short-lived, single-purpose branches. The repo-wide default delivery mode is `worktree-to-pr`; direct commit to `main` remains available as an explicitly declared mode.

**When to use this Skill:**

- Planning git workflow for new features
- Deciding whether to create a branch
- Understanding when branches are justified
- Managing incomplete work using feature flags
- Navigating environment branches (deployment only)
- Creating plans with git workflow specifications
- Implementing AI agent default behaviors

## Core Concepts

### What is Trunk Based Development?

**Trunk Based Development (TBD)** is a git workflow where:

- **All work converges on `main`** (the "trunk") — one integration target, no long-lived parallel lines
- **Small, frequent commits** integrated continuously, many times a day
- **Short-lived branches** - single-purpose, landed within 1-2 days; TBD forbids _long-lived_ branches, not branches
- **Feature flags** for incomplete work, so nothing needs an open branch to stay hidden
- **Continuous integration** enabled by that frequent landing

In this repo the default shape is `worktree-to-pr`: a short-lived plan branch in a disposable
worktree, pushed to a draft PR, merged once the hardened preconditions hold. Committing straight to
`main` is the `worktree-to-origin-main` / `main-to-origin-main` modes — fully supported, explicitly
declared.

### Why TBD?

**Benefits**:

- **Reduced merge conflicts**: Small commits integrate continuously
- **Faster feedback**: Changes visible immediately
- **Simpler workflow**: No complex branching strategies
- **Better collaboration**: Everyone works on latest code
- **Easier rollback**: Small commits easier to revert than large branches

**Tradeoffs**:

- **Requires discipline**: Commits must be small and safe
- **Needs feature flags**: Hide incomplete work behind flags
- **Depends on CI/CD**: Automated tests prevent breakage
- **Cultural shift**: Teams used to long-lived branches must adapt

## Delivery Modes: How Work Reaches `main`

### Default Behavior

**Work happens on short-lived branches that integrate into `main` continuously.** TBD's defining tenet is avoiding _long-lived_ branches, not avoiding branches: a short-lived branch reviewed via PR is a recognized TBD flavor, and it is this repo's default (`worktree-to-pr`). Direct commit to `main` remains fully supported for small, well-understood changes via the `worktree-to-origin-main` and `main-to-origin-main` modes.

**Standard workflow** (the default `worktree-to-pr` mode):

```bash
# 1. Provision a disposable worktree on a plan-scoped branch
git worktree add worktrees/<plan-identifier> -b <plan-identifier>
cd worktrees/<plan-identifier>

# 2. Make changes
# (edit files)

# 3. Commit frequently
git add [files]
git commit -m "feat(component): add feature X"

# 4. Push to the plan branch and open a draft PR
git push origin <plan-identifier>
gh pr create --draft --base main

# 5. Repeat steps 2-4; drive the PR green through the review cycle and CI,
#    then merge once the hardened preconditions hold ([AI] by default)
```

Under a declared direct-push mode the same loop applies without steps 1 and 4 — commit on `main` and
`git push origin main`.

> **Reading the examples below**: later examples in this document focus on their own topic (commit
> granularity, feature flags, branch lifespan) and write the push as `git push origin <plan-branch>`.
> Substitute `git push origin main` when a direct-push mode is the declared Delivery Mode. The push
> target follows the mode; it is never the point the example is making.

**AI agents assume `worktree-to-pr` by default** unless a plan or invocation explicitly selects another delivery mode. Resolve the mode by three-tier precedence: invocation argument > plan `## Delivery Mode` field > repo default.

### When a Direct-Push Mode Is Appropriate

Select `worktree-to-origin-main` or `main-to-origin-main` — pushing straight to `main` with no PR —
for changes that are small, well-understood, and safe to integrate immediately:

- **Small bug fixes** where the failure and the fix are both obvious
- **Small, safe refactors** with existing test coverage
- **Documentation** and **configuration** touch-ups
- **Dependency updates** that pass the full gate locally

**Key principle**: the direct-push modes trade review for speed. Choose them when the change is small
enough that the trade is obviously worth it — and declare the mode explicitly in the plan, since it is
a deliberate departure from the `worktree-to-pr` default rather than the assumed path.

## Keeping Branches Short-Lived

### What TBD Actually Forbids

TBD forbids **long-lived** branches, not branches. A plan branch that opens, integrates, and is
deleted within a day or two is fully consistent with TBD; a branch that accumulates weeks of work is
the anti-pattern. Under the `worktree-to-pr` default, each branch is single-purpose and disposable —
one branch, one worktree, one PR, deleted at the cleanup gate.

Branch lifespan discipline still applies with full force:

**1. Experimental Work (High Risk)**

- **Definition**: Unproven ideas, may be abandoned
- **Duration**: Days to weeks (not months)
- **Example**: Exploring new framework, prototyping radical redesign
- **Note**: an experimental branch is still short-lived — abandon or land it, do not let it drift

**2. External Contributions**

- **Definition**: Pull requests from external contributors
- **Duration**: Until review complete
- **Example**: Open source PR from community member
- **Note**: fork + PR is the only external path; maintainers review it like any other PR

**3. Compliance/Audit Requirements**

- **Definition**: Regulatory need for branch-based approval
- **Duration**: Until approval granted
- **Example**: Financial system change requiring dual approval
- **Note**: this is the case where a plan legitimately opts into a `[HUMAN]` merge gate

**4. Parallel Maintenance Versions**

- **Definition**: Supporting multiple major versions simultaneously
- **Duration**: Ongoing (release branches)
- **Example**: Supporting v1.x while developing v2.x
- **Note**: release branches are the one sanctioned long-lived exception

### Declaring the Delivery Mode

A plan branch needs no justification — it is the default. What a plan **must** declare is its
Delivery Mode, which determines where the work lands:

```yaml
delivery-mode: worktree-to-pr # or worktree-to-origin-main | main-to-origin-main | main-to-pr
worktree: "worktrees/[plan-identifier]"
branch: "[plan-identifier]"
```

For the categories above that go beyond an ordinary plan branch (experimental, compliance, parallel
maintenance versions), state the expected lifespan and the landing strategy alongside the mode, since
those are the cases where a branch risks outliving its plan.

### ❌ NOT Justified Reasons to Let a Branch Live Long

A plan branch is expected. What is **not** justified is letting one run long — these reasons do not
excuse a branch that outlives its plan:

- **"Feature in progress"** → Use feature flags and merge the incomplete-but-hidden work
- **"Might break things"** → Use automated tests and the PR quality gates
- **"Working on it for a week"** → Break the plan into phases; each phase gets its own branch and PR
- **"Multiple people on feature"** → Split into independent DAG nodes, one branch each
- **"Want to keep it separate"** → Preference is not justification

**Key principle**: branches are short-lived and single-purpose. Integration frequency is what TBD
protects — the PR is a review buffer, never a parking space.

## Feature Flags for Incomplete Work

### What are Feature Flags?

**Feature flags** (feature toggles) are runtime switches that enable/disable features without code changes.

**Purpose**: Hide incomplete work on `main` until ready for users.

### Basic Pattern

```javascript
// Define feature flag (in config or env vars)
const FEATURE_FLAGS = {
  newCheckout: false, // Feature under development
  betaAnalytics: true, // Feature in beta testing
};

// Use flag to conditionally enable feature
function renderCheckout() {
  if (FEATURE_FLAGS.newCheckout) {
    return <NewCheckoutFlow />; // New implementation
  } else {
    return <OldCheckoutFlow />; // Stable implementation
  }
}
```

### Feature Flag Lifecycle

**1. Development Phase** (flag = false):

- Commit new code to `main` with flag disabled
- Code deployed but not executed
- Safe to push incomplete work

**2. Testing Phase** (flag = true for testers):

- Enable flag for internal testing
- Users don't see changes yet
- Iterate based on feedback

**3. Release Phase** (flag = true for everyone):

- Enable flag for all users
- Feature now live
- Monitor for issues

**4. Cleanup Phase** (remove flag):

- After stability confirmed, remove flag and old code
- Simplify codebase
- One path remains

### Feature Flag Best Practices

**DO**:

- Use flags for multi-day features
- Keep flags simple (boolean toggles)
- Document flag purpose and timeline
- Remove flags after feature stable (don't accumulate)
- Test both paths (flag on and off)

**DON'T**:

- Use flags for trivial single-commit changes
- Create complex flag hierarchies
- Keep flags indefinitely (technical debt)
- Forget to test flag-disabled path
- Use flags as permanent configuration

## Environment Branches

### What are Environment Branches?

This repository has **environment-specific branches** for deployment:

- `prod-ayokoding-www` - Production deployment for ayokoding.com
- `prod-ose-www` - Production deployment for oseplatform.com

### Critical Rules

**❌ NEVER commit directly to environment branches**

- Environment branches are **deployment targets**, not development branches
- Changes flow: `main` → CI/CD → environment branch (automated)
- Manual commits to environment branches break deployment pipeline

**✅ Only CI/CD writes to environment branches**

- Deployment automation merges from `main`
- Environment-specific configs applied during deployment
- Tags created on environment branches to track releases

**Workflow**:

```
Developer commits to main → CI/CD tests → CI/CD deploys to environment branch
```

### Environment Branch Naming

**Pattern**: `prod-[app-name]`

**Examples**:

- `prod-ayokoding-www`
- `prod-ose-www`

**Rationale**: Clear, explicit, unambiguous naming prevents accidental commits.

## AI Agent Default Behavior

### Delivery Mode in Plans

**Default assumption**: every plan uses `worktree-to-pr` unless it declares another mode.

**Plan field** (in `delivery.md`, alongside `## Worktree`):

```yaml
delivery-mode: worktree-to-pr # worktree-to-origin-main | main-to-origin-main | main-to-pr
```

**If omitted**: agents resolve by three-tier precedence — invocation argument > plan field >
default `worktree-to-pr`. Never silently coerce an invalid non-empty value; ask instead.

**If a direct-push mode is selected**: state why, since it trades away the review buffer:

```yaml
delivery-mode: main-to-origin-main
rationale: "Single-line doc fix; full gate passes locally; no review value in a PR"
```

### Agent Behavior Rules

**When creating plans**:

- `plan-maker` defaults to `worktree-to-pr` and emits the worktree, PR, review-cycle, and merge steps
- Tags every git-mechanical step `[AI]` — worktree create/remove and the push
- Tags the merge `[AI]` by default; emits a `[HUMAN]` merge step only where the plan opts into that gate

**When executing work**:

- The executor provisions the worktree and works on the plan branch, not on `main`
- Pushes to the PR branch as `[AI]`; opening a draft PR is expected, not exceptional
- Merges once the five hardened preconditions hold, unless the plan declared a `[HUMAN]` gate

**When validating plans**:

- Checkers validate steps against the plan's **declared** Delivery Mode, not against a fixed default
- A PR step under a `*-to-pr` mode is correct; a PR step under a direct-push mode is a finding
- A `[HUMAN]`-tagged merge step is valid where the plan opts in — never "corrected" to `[AI]`

## Common Patterns

### Pattern 1: Multi-Day Feature Development

**Scenario**: Feature takes 3 days to complete

**✅ Correct approach (TBD with feature flags)**:

```
Day 1:
- Add feature flag (disabled)
- Commit basic infrastructure
- Push to <plan-branch>; open a draft PR; land it once green

Day 2:
- Implement core logic (behind flag)
- Commit
- Push to <plan-branch>; land it once green

Day 3:
- Complete feature (behind flag)
- Test internally with flag enabled
- Enable flag for all users
- Push to <plan-branch>; land it once green
```

Each day's work lands on its own short-lived branch and PR — the flag, not an open branch, is what
hides the half-built feature. Under a declared direct-push mode, substitute `git push origin main`
for the branch-and-PR step; the daily-integration shape is identical either way.

**❌ Wrong approach (long-lived branch)**:

```
Day 1-3:
- Create feature branch
- Accumulate changes
- Risk merge conflicts
- Delayed integration
```

### Pattern 2: Experimental Work

**Scenario**: Testing new framework (may be abandoned)

**✅ Correct approach (short-lived experimental branch)**:

```yaml
git-workflow: "Branch: experimental-graphql"
branch-justification: |
  **Category**: Experimental
  **Reason**: Evaluating GraphQL vs REST, may reject GraphQL
  **Duration**: 1 week evaluation
  **Merge Strategy**: Merge to main if adopted, delete if rejected
```

**Workflow**:

```bash
# Day 1-7: Experiment on branch
git checkout -b experimental-graphql
# (exploration work)

# Day 7: Decision made
# If adopting: push the branch and land it through a PR
git push origin experimental-graphql
gh pr create --draft --base main
# ... review cycle + CI, then squash/rebase merge (never a local `git merge`,
# which would break linear history)
git branch -d experimental-graphql

# If rejecting: Delete branch
git branch -D experimental-graphql
```

### Pattern 3: External Contribution

**Scenario**: Open source contributor submits PR

**✅ Correct approach (PR branch from fork)**:

```
1. Contributor forks repo
2. Contributor creates branch in fork
3. Contributor opens PR to main
4. Maintainer reviews PR
5. Maintainer merges to main (if approved)
6. Contributor's branch deleted after merge
```

**Key**: Branch is in fork, not main repo. Main repo stays clean.

## Commit Patterns in TBD

### Small, Frequent Commits

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

### Atomic Commits

**Definition**: Each commit is a complete, working unit

**Rules**:

- ✅ Commit compiles and passes tests
- ✅ Commit includes related changes only
- ✅ Commit message describes change clearly
- ❌ Commit breaks build (fails tests)
- ❌ Commit mixes unrelated changes
- ❌ Commit message is vague

### Conventional Commits

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

## PR Is the Default; Direct Push Is an Explicit Selection

**The repo-wide default delivery mode is `worktree-to-pr`.** Work happens on a short-lived plan
branch inside a disposable worktree, is pushed to a draft PR opened against `main`, and is driven
through the review cycle and CI to a fully green state before it merges.

### Resolving the Delivery Mode

Apply three-tier precedence:

1. **Invocation argument** — the user or calling context named a mode explicitly
2. **Plan field** — the plan's `## Delivery Mode` section declares one
3. **Default** — `worktree-to-pr`

Never silently coerce an invalid non-empty value; treat it as a question for the user instead.

### What This Means for Plans

**Plan delivery checklists SHOULD include the PR steps** under the two `*-to-pr` modes — opening the
draft PR, running the PR-Review Maker→Fixer Cycle, and the merge step itself. What they must not
contain is a `[HUMAN]` "review the diff and approve push" gate: pushing to a PR branch is not a
merge, and the push is always `[AI]`.

### What This Means for AI Agents

**Default to a plan branch and a draft PR** (`gh pr create --draft --base main …`). Push to the PR
branch as `[AI]`. The merge is a separate step and is **`[AI]` by default** too, once the five
hardened preconditions hold; a `[HUMAN]` merge gate applies only where a plan's own step says so
explicitly, and that opt-in must be left intact rather than "corrected".

Selecting a direct-push mode is legitimate but deliberate — it belongs in the plan's declared
Delivery Mode, not inferred from context.

See [Git Push Default Convention](../../../repo-governance/development/workflow/git-push-default.md)
and [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) for
complete rules and edge cases.

## References

**Primary Convention**: [Trunk Based Development Convention](../../../repo-governance/development/workflow/trunk-based-development.md)

**Related Conventions**:

- [Git Push Default Convention](../../../repo-governance/development/workflow/git-push-default.md) - The PR-branch-as-default push target, and the direct-push modes as explicit selections
- [Commit Message Convention](../../../repo-governance/development/workflow/commit-messages.md) - Conventional Commits format
- [Implementation Workflow](../../../repo-governance/development/workflow/implementation.md) - Development workflow stages
- [Plans Organization](../../../repo-governance/conventions/structure/plans.md) - Git workflow in plans

**Related Skills**:

- `plan-writing-gherkin-criteria` - Writing testable acceptance criteria for TBD workflow
- `repo-understanding-repository-architecture` - Understanding repository structure and principles

---

This Skill packages critical Trunk Based Development workflow knowledge for maintaining simple, effective git practices. For comprehensive details, consult the primary convention document.
