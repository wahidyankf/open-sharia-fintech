---
title: "Scope and Pre-Push Hook Coverage"
description: What kinds of pushes this convention applies to, what it excludes, and how it complements the pre-push hook.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - verification
  - quality-gates
  - workflow
when_to_use: Use when deciding whether a push requires CI post-push verification, or checking what the pre-push hook already covers.
---

# Scope and Pre-Push Hook Coverage

## When This Convention Applies

This convention applies after **any** push that touches the following, regardless of whether the target is a PR branch or `origin main`:

- App source code under `apps/`
- Library source code under `libs/`
- CI workflow files under `.github/workflows/`
- Contract specs under `specs/` (blast radius extends to all apps consuming the contract)
- Configuration files that affect build or test behavior (`nx.json`, `tsconfig.base.json`, `package.json`, etc.)

## When This Convention Does NOT Apply

This convention does not apply to pushes that exclusively touch:

- `docs/` — documentation only, no app behavior impact
- `repo-governance/` — governance only, no app behavior impact
- `plans/` — planning documents only
- `generated-reports/` — audit reports only
- `social-media-posts/` — social content only
- `.claude/agents/`, `.claude/skills/` — agent/skill definitions only, no app code impact

The pre-push hook (typecheck, lint, test:quick, specs:coverage) already validates these changes sufficiently.

## What the Pre-Push Hook Covers vs. What This Convention Covers

| Quality Gate              | Pre-Push Hook | CI Post-Push Verification |
| ------------------------- | ------------- | ------------------------- |
| Typecheck                 | Yes           | Yes (as part of CI)       |
| Lint                      | Yes           | Yes (as part of CI)       |
| Unit tests (`test:quick`) | Yes           | Yes (as part of CI)       |
| Integration tests         | No            | Yes                       |
| E2E tests                 | No            | Yes                       |
| Deployment workflows      | No            | Yes                       |
| Spec coverage             | Yes           | Yes (as part of CI)       |

The pre-push hook is fast and local. CI workflows are comprehensive and environment-representative. Both are required.
