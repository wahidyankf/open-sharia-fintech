---
title: "GitHub Environment Key Registry"
description: The table of which vars./secrets. keys each named GitHub environment ({group}-app-local, {group}-app-staging) holds, and the rule for omitting an empty environment.
when_to_use: Use when adding a new GitHub Environment secret or var, or checking which environment a CI job should read a key from.
category: explanation
subcategory: conventions
tags:
  - security
  - secrets
  - env-files
  - guard-env-file-access
  - naming
  - reproducibility
created: 2026-06-10
---

# GitHub Environment Key Registry

Each `environment:` named by the pipeline holds exactly the keys that stage's jobs read, split into
non-secret `vars.` and secret `secrets.`. Values are placeholders or secrets only in-repo (created
by wire-vercel):

| Environment               | `vars.`                 | `secrets.`                        | Read by                                |
| ------------------------- | ----------------------- | --------------------------------- | -------------------------------------- |
| `{group}-app-local`       | _(none — compose-only)_ | local-CI secrets, if any          | `_reusable-app-test-local-deploy-stag` |
| `{group}-app-staging`     | `WEB_BASE_URL`          | `VERCEL_AUTOMATION_BYPASS_SECRET` | `_reusable-app-test-stag`              |
| _(www has no GitHub Env)_ | —                       | —                                 | www e2e runs entirely on local compose |

If `{group}-app-local` holds no secrets after wire-vercel completes, **omit the `environment:` key**
rather than bind an empty environment.
