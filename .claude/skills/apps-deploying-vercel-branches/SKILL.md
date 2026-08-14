---
name: apps-deploying-vercel-branches
description: Shared deployment procedure for the `*-deployer` agent family — force-pushing an environment branch that Vercel (or a GitHub Actions workflow) builds from. Covers three patterns (direct force-push, scheduled staging workflow, scheduled test-only workflow) plus the shared Vercel MCP post-deploy verification protocol. Use when authoring or invoking any `apps-*-deployer` agent.
---

# Deploying Vercel Branches Skill

## Purpose

Every `apps-*-deployer` agent in this repo ships a frontend by moving an environment branch, never
by running a local build. This skill holds the procedure once so each deployer agent's own file
only needs to state its target-specific values (branch name, project slug, workflow file).

## The Three Patterns

1. **Direct force-push** (`reference/01-direct-force-push-workflow.md`) — validate `main`, force-push
   straight to a `prod-*` branch Vercel watches. Used by production sites with no staging gate.
2. **Scheduled staging workflow** (`reference/02-scheduled-staging-workflow.md`) — trigger a GitHub
   Actions workflow that runs the full local-stack test suite, then force-pushes `stag-*` branches
   itself. Used by app groups with a staging tier.
3. **Scheduled test-only workflow** (`reference/03-scheduled-test-only-workflow.md`) — trigger a
   GitHub Actions workflow that only runs tests; no deploy target exists yet. Used where staging/prod
   infrastructure is not provisioned.

All three share `reference/04-post-deploy-verification-vercel-mcp.md` — the Vercel MCP protocol that
confirms a build actually succeeded, since a successful push is not evidence of a successful deploy.

## How a Deployer Agent Uses This Skill

The agent's own file states which pattern applies and its target parameters (branch, project slug,
team, workflow filename). It then points its `## Required Reading` section at this skill's
`reference/` directory instead of repeating the procedure inline.

## References

- [Vercel MCP Capability Convention](../../../repo-governance/development/infra/vercel-mcp.md)
- [Trunk Based Development](../../../repo-governance/development/workflow/trunk-based-development.md)
- [GitHub Actions Workflow Naming](../../../repo-governance/development/infra/github-actions-workflow-naming.md)
