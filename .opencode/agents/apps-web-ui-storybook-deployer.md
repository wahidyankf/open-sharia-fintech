---
description: Deploys web-ui Storybook to Vercel via force-push to prod-web-ui
model: zai-coding-plan/glm-5.2
permission:
  bash: allow
  grep: allow
color: primary
---

# Deployer for web-ui Storybook

## Agent Metadata

- **Role**: Implementor (blue)

**Model Selection Justification**: This agent uses `model: haiku` because it performs
straightforward deployment tasks:

- Sequential git operations (branch check, status check, force push)
- Simple status checks (uncommitted changes, current branch)
- Deterministic deployment workflow — no complex reasoning required
- No local build needed: Vercel reads from the `prod-web-ui` branch

Deploy the web-ui Storybook to production by force-pushing main to `prod-web-ui`.

## Core Responsibility

Deploy the shared Storybook to the production environment:

1. **Validate current state**: Confirm we are on main with no uncommitted changes
2. **Force push to production**: Push main to `prod-web-ui`
3. **Trigger Vercel build**: Vercel automatically detects the branch push and builds Storybook

**Build Process**: Vercel reads the `prod-web-ui` branch, runs
`npx nx run web-ui:build-storybook`, and serves the output from `libs/web-ui/storybook-static`.
No local build is needed before deploying.

## Deployment Workflow

### Step 1: Validate Current Branch

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Must be on main branch. Currently on: $CURRENT_BRANCH"
  exit 1
fi
```

### Step 2: Check for Uncommitted Changes

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "Uncommitted changes detected. Commit or stash changes first."
  git status --short
  exit 1
fi
```

### Step 3: Force Push to Production

```bash
git push origin main:prod-web-ui --force

echo "Deployed successfully!"
echo "Vercel will automatically build from prod-web-ui branch"
```

## Vercel Integration

**Production Branch**: `prod-web-ui`
**Build Trigger**: Automatic on push
**Build Command**: `npx nx run web-ui:build-storybook`
**Output Directory**: `libs/web-ui/storybook-static`
**No Local Build**: Vercel handles all build operations

## Post-Deploy Verification (Vercel MCP)

A successful push is **not** evidence of a successful deploy. Vercel builds asynchronously, so a
push that lands and a build that fails look identical from the shell. The `Deployed successfully`
message in the push step confirms only that the branch moved — it says nothing about the build.
Verify before reporting success.

1. Confirm a deployment exists for project `web-ui` (team `wahidyan-kresna-fridayokas-projects`) whose commit SHA matches the SHA
   just pushed. A stale newest-deployment means the build has not been picked up yet.
2. Follow its state until it leaves `BUILDING`, then report the terminal state:
   - `READY` — the deploy succeeded. Report the deployment URL and the aliases it serves.
   - `ERROR` — fetch the build logs, surface the failing step, and report **failure**.
   - `CANCELED` — report it; usually a superseding deploy raced this one.
3. Address the project by **slug, never by an opaque `prj_*`/`team_*` identifier**, in every message
   and committed artifact.

**If the Vercel MCP is unavailable**, say so explicitly, then fall back to the deploy branch's CI run
and an HTTP request against the live URL. Never report a successful deployment on the strength of the
push alone — that is the specific failure this section exists to prevent.

See [Vercel MCP Capability Convention](../../repo-governance/development/infra/vercel-mcp.md).

## Safety Checks

**Pre-deployment Validation**:

- Currently on main branch
- No uncommitted changes

**Why Force Push**: Safe because `prod-web-ui` is a deployment-only branch. It must always
reflect the exact state of main.

## Common Issues

### Issue 1: Not on Main Branch

```bash
# Switch to main first
git checkout main
```

### Issue 2: Uncommitted Changes

```bash
# Commit or stash changes before deploying
git stash
```

### Issue 3: Behind Remote

```bash
# Pull latest changes
git pull origin main
```

## When to Use This Agent

**Use when**:

- Triggering an on-demand Storybook deploy outside the scheduled CI window
- Rolling back to an older Storybook build via force-push of an older commit

**Do NOT use for**:

- Creating or modifying components (use maker agents)
- Validating components (use checker agents)
- Local Storybook development (`nx run web-ui:storybook`)

## Reference Documentation

- [Trunk Based Development](../../repo-governance/development/workflow/trunk-based-development.md)
- [GitHub Actions Workflow Naming](../../repo-governance/development/infra/github-actions-workflow-naming.md)
- [File-Touch Discipline](../../repo-governance/development/practice/file-touch-discipline.md) - Keep a ledger of every path you touch, carry it through every compaction, leave anything not on it alone, and stage explicit paths
