# Pattern 1: Direct Force-Push Workflow

Used by agents whose Target Parameters name a single `prod-*` branch with no staging gate.
Substitute that agent's branch name for `$PROD_BRANCH` below.

## Step 1: Validate Current Branch

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Must be on main branch. Currently on: $CURRENT_BRANCH"
  exit 1
fi
```

## Step 2: Check for Uncommitted Changes

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "Uncommitted changes detected. Commit or stash changes first."
  git status --short
  exit 1
fi
```

## Step 3: Force Push to Production

```bash
git push origin main:$PROD_BRANCH --force

echo "Deployed successfully!"
echo "Vercel will automatically build from $PROD_BRANCH branch"
```

## Vercel Integration

**Build Trigger**: Automatic on push. **No Local Build**: Vercel handles all build operations —
never run a local build before this push. **Trunk-Based Development**: per
`repo-practicing-trunk-based-development`, all development happens on `main`; the production branch
is deployment-only, never committed to directly.

## Why Force Push Is Safe

`$PROD_BRANCH` is a deployment-only branch. It must always be an exact copy of `main` — force-push is
the correct operation, not a hazard, for this specific branch.

## Common Issues

### Issue 1: Not on Main Branch

```bash
git checkout main
```

### Issue 2: Uncommitted Changes

```bash
git add -A && git commit -m "commit message"
# OR
git stash
```

### Issue 3: Behind Remote

```bash
git pull origin main
```

After a successful push, proceed to
[Post-Deploy Verification](./post-deploy-verification-vercel-mcp.md) — the push alone is not
evidence the build succeeded.
