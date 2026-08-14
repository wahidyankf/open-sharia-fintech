---
title: "GitHub Actions Conventions — Reusable Workflows and CRON Scheduling"
description: Reusable workflow structure and the staggered CRON tracks.
category: explanation
subcategory: development
tags: [ci-cd, github-actions]
created: 2026-03-31
when_to_use: Use when writing a reusable workflow or scheduling a CRON job.
---

# GitHub Actions Conventions — Reusable Workflows and CRON Scheduling

## Reusable Workflows

Reusable workflows live in `.github/workflows/_reusable-{purpose}.yml` and are called via
`workflow_call`. They contain the actual job definitions (checkout, setup, test execution, artifact
upload). Per-variant test workflows stay thin (~40 lines) by calling these reusable workflows with
variant-specific inputs.

**Examples**:

```
.github/workflows/_reusable-www-test-local-deploy.yml
.github/workflows/_reusable-app-test-local-deploy-stag.yml
.github/workflows/_reusable-app-test-stag.yml
.github/workflows/_reusable-be-build-deploy.yml
```

## CRON Schedule

Scheduled service workflows run twice daily aligned to WIB (UTC+7). The app tier uses a
**staggered** schedule — `*-app-test-local-deploy-stag` fires first to produce the staging deploy,
then `*-app-test-stag` fires **2.5 hours later** once Vercel and coralpolyp have
settled. The www tier is independent and runs after both app-tier passes.

`*-be-build-deploy-stag` is **not** scheduled — it fires on push to the `stag-*-be` branch, which
the `*-app-test-local-deploy-stag` deploy job force-pushes on success.

| Pipeline                       | WIB           | UTC           | Rationale                                                           |
| ------------------------------ | ------------- | ------------- | ------------------------------------------------------------------- |
| `*-app-test-local-deploy-stag` | 03:00 / 15:00 | 20:00 / 08:00 | Earliest — produces the staging deploy the later stag-gate verifies |
| `*-app-test-stag`              | 05:30 / 17:30 | 22:30 / 10:30 | **+2.5 h** after staging, so Vercel + coralpolyp have rolled out    |
| `*-www-test-local-deploy-prod` | 06:00 / 18:00 | 23:00 / 11:00 | Independent of the app tier (direct www test → prod deploy)         |

## 5-Track Parallel CRON

Each scheduled test run executes five parallel tracks:

| Track | Nx Target / Command             | Notes                                                                               |
| ----- | ------------------------------- | ----------------------------------------------------------------------------------- |
| 1     | `lint`                          | Static analysis across all affected projects (includes static a11y for UI projects) |
| 2     | `typecheck`                     | Type verification                                                                   |
| 3     | `test:quick`                    | Unit tests + coverage validation                                                    |
| 4     | `specs:coverage`                | Validates Gherkin step coverage for all apps and E2E runners                        |
| 5     | `test:integration` → `test:e2e` | Sequential: integration then E2E per service                                        |

Tracks 1–4 run in parallel. Track 5 sequences integration before E2E within each service but
services themselves run in parallel across matrix entries.
