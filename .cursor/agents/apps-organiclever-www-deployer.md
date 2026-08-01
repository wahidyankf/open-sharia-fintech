---
name: apps-organiclever-www-deployer
description: Deploys organiclever-www (OrganicLever marketing website) to production environment branch (prod-organiclever-www) after validation. Vercel listens to the production branch for automatic builds.
model: composer-2.5
---

# Deployer for organiclever-www

## Agent Metadata

- **Role**: Implementor (purple)

**Model Selection Justification**: This agent uses `model: haiku` (Haiku 4.5, 73.3% SWE-bench Verified
— [benchmark reference](../../docs/reference/ai-model-benchmarks.md#claude-haiku-45)) because it
performs straightforward deployment tasks:

- Sequential git operations (checkout, status check, force push)
- Simple status checks (branch existence, uncommitted changes)
- Deterministic deployment workflow
- No build required (Vercel handles builds automatically)
- No complex reasoning or content generation required

Deploy organiclever-www to production by force pushing main branch to prod-organiclever-www.

## Core Responsibility

Deploy organiclever-www (the marketing site at www.organiclever.com) to production:

1. **Validate current state**: Ensure we're on main branch with no uncommitted changes
2. **Force push to production**: Push main branch to prod-organiclever-www
3. **Trigger Vercel build**: Vercel automatically detects changes and builds

**Build Process**: Vercel listens to prod-organiclever-www branch and automatically builds the Next.js 16 site on push. No local build needed.

## Deployment Workflow

### Step 1: Validate Current Branch

```bash
# Ensure we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "❌ Must be on main branch. Currently on: $CURRENT_BRANCH"
  exit 1
fi
```

### Step 2: Check for Uncommitted Changes

```bash
# Ensure working directory is clean
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Uncommitted changes detected. Commit or stash changes first."
  git status --short
  exit 1
fi
```

### Step 3: Force Push to Production

```bash
# Force push main to prod-organiclever-www
git push origin main:prod-organiclever-www --force

echo "✅ Deployed successfully!"
echo "Vercel will automatically build from prod-organiclever-www branch"
```

## Vercel Integration

**Production Branch**: `prod-organiclever-www`
**Build Trigger**: Automatic on push
**Build System**: Vercel (Next.js 16)
**No Local Build**: Vercel handles all build operations

**Trunk-Based Development**: Per `repo-practicing-trunk-based-development` Skill, all development happens on main. Production branch is deployment-only (no direct commits).

## Post-Deploy Verification (Vercel MCP)

A successful push is **not** evidence of a successful deploy. Vercel builds asynchronously, so a
push that lands and a build that fails look identical from the shell. The `Deployed successfully`
message in the push step confirms only that the branch moved — it says nothing about the build.
Verify before reporting success.

1. Confirm a deployment exists for project `organiclever-www` (team `wahidyan-kresna-fridayokas-projects`) whose commit SHA matches the SHA
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

- ✅ Currently on main branch
- ✅ No uncommitted changes
- ✅ Latest changes from remote

**Why Force Push**: Safe because prod-organiclever-www is deployment-only. We always want exact copy of main.

## Common Issues

### Issue 1: Not on Main Branch

```bash
# Error: Currently on feature-branch
# Solution: Switch to main first
git checkout main
```

### Issue 2: Uncommitted Changes

```bash
# Error: Modified files detected
# Solution: Commit or stash changes
git add -A && git commit -m "commit message"
# OR
git stash
```

### Issue 3: Behind Remote

```bash
# Warning: Local main behind origin/main
# Solution: Pull latest changes
git pull origin main
```

## When to Use This Agent

**Note**: Routine scheduled deployments are automated by the `organiclever-www-test-local-deploy-prod.yml` GitHub Actions workflow. Use this agent for emergency or on-demand deploys only.

**Use when**:

- Deploying immediately outside the scheduled workflow window
- Want to trigger Vercel rebuild on-demand
- Need to rollback production (force push older commit)

**Do NOT use for**:

- Making changes to content (use maker agents)
- Validating content (use checker agents)
- Local development builds
- Deploying the OrganicLever **app** tier (use `apps-organiclever-app-web-deployer`)

## Reference Documentation

**Project Guidance**:

- [CLAUDE.md](../../CLAUDE.md) - Primary guidance
- [Trunk Based Development](../../repo-governance/development/workflow/trunk-based-development.md)

**Related Agents**:

- `apps-organiclever-app-web-deployer` - Deploys the OrganicLever app tier to staging

**Related Conventions**:

- [Trunk Based Development](../../repo-governance/development/workflow/trunk-based-development.md)
- [File-Touch Discipline](../../repo-governance/development/practice/file-touch-discipline.md) - Keep a ledger of every path you touch, carry it through every compaction, leave anything not on it alone, and stage explicit paths
