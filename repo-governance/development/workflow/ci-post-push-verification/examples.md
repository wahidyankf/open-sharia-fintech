---
title: "Examples"
description: Worked pass/fail examples of CI post-push verification, including how to fix a failure found during verification.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - verification
  - quality-gates
  - workflow
when_to_use: Use when you need a concrete example of correct or incorrect CI post-push verification behaviour.
---

# Examples

## PASS: Correct post-push verification

```
Agent: Pushed feat(organiclever-app-web): update hero section to origin main.

Identifying blast radius: apps/organiclever-app-web/ changed.

Triggering CI:
  gh workflow run organiclever-app-test-local-deploy-stag.yml

Monitoring:
  gh run list --workflow=organiclever-app-test-local-deploy-stag.yml --limit=3
  # [scheduled wakeup after 2 minutes]
  gh run view 12345678 --json conclusion,status,jobs

Result: All steps passed. Work is complete.
```

## FAIL: Declaring done before CI verification

```
Agent: Pushed feat(organiclever-app-web): update hero section to origin main.

Work is complete.
```

No CI verification was performed. This is wrong — the pre-push hook passing is not sufficient.

## FAIL: Skipping CI because pre-push passed

```
Agent: Pre-push hook passed (including affected test:quick with Unit and static coverage).
       CI verification skipped — local gates passed.

Work is complete.
```

The pre-push hook does not run integration tests, E2E tests, or deployment workflows. Skipping CI verification is wrong.

## PASS: Fixing a CI failure discovered during verification

```
Agent: Pushed feat(organiclever-be): update auth endpoint to origin main.

Triggering CI:
  gh workflow run organiclever-app-test-local-deploy-stag.yml

Monitoring: run 12345679 failed — integration test failure in organiclever-be.

Root cause: Database migration step missing from integration test fixture.

Fix:
  git add apps/organiclever-be/tests/fixtures/migration.sql
  git commit -m "fix(organiclever-be): add missing migration fixture for auth integration test"
  git push origin main

Re-triggering CI:
  gh workflow run organiclever-app-test-local-deploy-stag.yml

Result: All steps passed. Work is complete.
```
