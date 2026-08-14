---
title: "When Branches Are Appropriate"
description: Five natural-fit cases for a branch — code review, spikes, external contributors, compliance, environment branches.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when deciding whether a situation warrants a branch, or why prod-ayokoding-www is TBD-compliant.
---

# When Branches Are Appropriate

Under the repo-wide `worktree-to-pr` default, a short-lived branch is the norm for routine development,
not an exception carved out from an otherwise branchless workflow. The cases below describe situations
where a branch (via a plan's `worktree-to-pr` mode, or an external fork) has always been the natural
fit -- they remain equally valid today, just no longer framed as rare deviations:

## Code Review Requirement

If your team/organization mandates peer review via Pull Requests:

- PASS: **Create branch** for PR workflow
- PASS: **Get review within 24 hours** (not days)
- PASS: **Merge immediately** after approval
- PASS: **Delete branch** right after merge

**Minimize branch lifespan**: The goal is still rapid integration.

## Experimental/Spike Work

When exploring a new approach with high uncertainty:

- PASS: **Create branch** for experimentation
- PASS: **Set time limit** (e.g., "1 day to spike this approach")
- PASS: **Decision point**: Keep and merge, or discard entirely
- PASS: **Don't let spikes become features**: Decide quickly

## External Contributors

When accepting contributions from outside the team:

- PASS: **Fork + PR workflow** is standard
- PASS: **Review and merge quickly** to reduce staleness
- PASS: **Guide contributor** to make small, focused PRs

## Regulatory/Compliance

If industry regulations require documented review:

- PASS: **Use branches + PRs** for audit trail
- PASS: **Still minimize branch lifespan** (review quickly)
- PASS: **Automate compliance checks** in CI

## Environment/Deployment Branches

**Long-lived environment branches are explicitly allowed in TBD.** These are NOT feature branches.

Environment branches serve deployment purposes, not feature isolation:

- PASS: **Production branches**: Trigger deployment to production environment
- PASS: **Staging branches**: Trigger deployment to staging environment
- PASS: **Environment-specific configuration**: Different settings per environment

**Key distinction**: Environment branches reflect deployment state, not development work.

**Example in this repository: `prod-ayokoding-www`**

The `apps/ayokoding-www/` project uses a production deployment branch:

- **Branch**: `prod-ayokoding-www`
- **Purpose**: Triggers automatic deployment to ayokoding.com via Vercel
- **Location**: Deploys `apps/ayokoding-www/` (Next.js 16 application)
- **Workflow** (automated):
  1. All development happens in `main`
  2. The `ayokoding-www-test-local-deploy-prod.yml` GitHub Actions workflow runs at 6 AM and 6 PM WIB, detects changes in `apps/ayokoding-www/`, builds, then force-pushes `main` to `prod-ayokoding-www`
  3. Push to `prod-ayokoding-www` triggers production deployment via Vercel
- **Important**: Never commit directly to `prod-ayokoding-www` outside the CI automation

**Why this is TBD-compliant**:

- Development still happens on `main` (trunk)
- No feature isolation in branches
- `prod-ayokoding-www` is a deployment trigger, not a development workspace
- Changes flow from `main` to `prod-ayokoding-www`, never the reverse
- Consistent with TBD principles: environment branches are for release management, not feature development

**Reference**: [TrunkBasedDevelopment.com - Branch for Release](https://trunkbaseddevelopment.com/branch-for-release/) explicitly describes release branches as acceptable in TBD.
