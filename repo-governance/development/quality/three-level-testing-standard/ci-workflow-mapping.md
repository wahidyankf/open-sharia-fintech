---
title: "CI Workflow Mapping"
description: "Which CI job runs which test level."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-03-13
when_to_use: "Use to locate a test level's CI job."
---

# CI Workflow Mapping

The following table maps GitHub Actions workflows to the test levels they execute:

| Workflow                | lint | test:unit        | specs:coverage | test:integration | test:e2e | When          |
| ----------------------- | ---- | ---------------- | -------------- | ---------------- | -------- | ------------- |
| Pre-push hook           | Yes  | Via `test:quick` | Yes            | No               | No       | Every push    |
| PR quality gate         | Yes  | Via `test:quick` | No             | No               | No       | Every PR      |
| `test-and-deploy-*.yml` | Yes  | Via `test:quick` | Yes            | Yes              | Yes      | CRON 2x daily |

`lint` (including static a11y checks via oxlint jsx-a11y plugin for TypeScript UI projects) runs in all three enforcement gates: the pre-push hook, the PR quality gate, and Test CI workflows. `specs:coverage` runs in the pre-push hook and all Test CI workflows, ensuring every Gherkin step has a matching step definition. The pre-push hook intentionally omits integration and E2E tests. These tests require Docker infrastructure (PostgreSQL, running servers) and are too slow and environment-dependent to run on every push. The PR quality gate omits `specs:coverage` because it targets only the fast `test:quick` path used for merge checks. The scheduled `test-and-deploy-*.yml` workflows cover integration, E2E, and specs:coverage on a regular cadence for production apps.
