# Common Development Workflow — Git Workflow

## Trunk Based Development

**Core Principle**: All development happens on `main` branch

**Branch Strategy**:

- **Default branch**: `main` (all development work)
- **Environment branches**: `prod-*` (deployment only, never commit directly)
- **No feature branches**: Commit small changes frequently to main
- **No long-lived branches**: Keep changes integrated

**Why Trunk Based Development?**

- Reduces merge conflicts (no long-lived branches)
- Encourages small, incremental changes
- Faster feedback loop
- Simplifies deployment pipeline

## Conventional Commits Format

**Pattern**: `<type>(<scope>): <description>`

**Required Format**:

- **type**: Category of change (see types below)
- **scope**: Optional but recommended (component/module affected)
- **description**: Imperative mood ("add" not "added"), no period at end

**Commit Types**:

- **feat**: New feature or capability
- **fix**: Bug fix
- **docs**: Documentation changes only
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code restructuring (no feature change, no bug fix)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build, packaging, or compiler configuration
- **chore**: Dependency updates and repository housekeeping
- **ci**: CI/CD pipeline changes
- **revert**: Reverting previous commit

**Examples**:

```bash
feat(auth): add OAuth2 login support
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
test(auth): add integration tests for login flow
```

**Split Commits by Domain**:

- Different types → separate commits
- Different scopes → separate commits
- Different concerns → separate commits

**Example** (wrong):

```bash
git commit -m "feat(auth): add login + fix(api): fix bug + docs: update readme"
```

**Example** (correct):

```bash
git commit -m "feat(auth): add OAuth2 login support"
git commit -m "fix(api): handle null response in user endpoint"
git commit -m "docs(readme): update installation instructions"
```

## Git Discipline

**CRITICAL**: Never stage or commit unless explicitly instructed by user

**Default Behavior**:

- Do NOT run `git add` automatically
- Do NOT run `git commit` automatically
- User must explicitly request commits

**Commit Permission**:

- One-time only (not continuous)
- User says "commit these changes" → you commit once
- User does NOT say "commit everything I ask you to do" → don't assume

**Why This Matters**:

- User controls git history
- Prevents unwanted commits
- User decides commit boundaries
- Respects user's workflow preferences
