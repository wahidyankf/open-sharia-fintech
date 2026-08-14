# organiclever-www — Vercel Deployment

## Production Branch

**Branch**: `prod-organiclever-www` → [https://www.organiclever.com/](https://www.organiclever.com/)
**Purpose**: Deployment-only branch that Vercel monitors
**Build System**: Vercel (Next.js auto-detected, no `builds` array needed)
**Security Headers**: Configured in `vercel.json`

## vercel.json Configuration

```json
{
  "version": 2,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    }
  ]
}
```

## Deployment Process

**Step 1: Validate Current State**

```bash
# Ensure on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "❌ Must be on main branch"
  exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Uncommitted changes detected"
  exit 1
fi
```

**Step 2: Force Push to Production**

```bash
# Deploy to production
git push origin main:prod-organiclever-www --force
```

**Step 3: Vercel Auto-Build**

Vercel automatically:

- Detects push to prod-organiclever-www branch
- Pulls latest code
- Builds Next.js 16 application
- Deploys to https://www.organiclever.com/

## Why Force Push

**Safe for deployment branches**:

- prod-organiclever-www is deployment-only (no direct commits)
- Always want exact copy of main branch
- Trunk-based development: main is source of truth
