---
title: "The Rule and Workflow Mapping"
description: The four required steps after pushing app or lib code, and which CI workflow to trigger per changed app.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - verification
  - quality-gates
  - workflow
when_to_use: Use when you need the exact steps to verify CI after a push, or need to know which workflow file covers a changed app.
---

# The Rule and Workflow Mapping

After pushing app or library code — to the PR branch under `*-to-pr` modes, or to `origin main` under the direct-push modes — you MUST:

1. **Identify which apps and libs were changed.** Use `git diff HEAD~1 --name-only` or `nx affected --base=HEAD~1` to determine the blast radius.
2. **Trigger the relevant CI workflows.** Use `gh workflow run` for each workflow that covers the changed apps or libs.
3. **Monitor until completion.** Use `gh run list` to find the run ID, then schedule a wakeup and make one `gh run view <run-id>` call every 2 minutes. Never use `gh run watch`.
4. **If any workflow fails**, investigate the root cause and fix it per the [CI Blocker Resolution Convention](../../quality/ci-blocker-resolution.md). Do not declare the work done until all relevant workflows pass.

## Workflow Mapping

| App(s) Changed                                              | Workflow to Trigger                           |
| ----------------------------------------------------------- | --------------------------------------------- |
| `apps/ayokoding-www/`                                       | `ayokoding-www-test-local-deploy-prod.yml`    |
| `apps/ose-www/`                                             | `ose-www-test-local-deploy-prod.yml`          |
| `apps/organiclever-app-web/`, `apps/organiclever-be/`       | `organiclever-app-test-local-deploy-stag.yml` |
| `libs/`, shared infrastructure, or cross-cutting governance | All workflows for apps in blast radius        |

When a change touches shared code (a lib, a shared type, a contract), trigger every workflow for every app that imports that code — not just the app most obviously related to the change.
