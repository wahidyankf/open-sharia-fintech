---
title: "Learning Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

This track treats a release pipeline as a chain of evidence: each gate makes one safety claim before
the next audience receives the change. The worked examples pair GitHub Actions YAML with fully typed
Python so delivery policy and executable verification remain readable, reviewable, and runnable.

## Concepts

- **co-01–co-08**: continuous integration, continuous delivery and deployment, pipeline stages,
  fail-fast checks, acceptance gates, trunk-based development, and the GitFlow caveat.
- **co-09–co-18**: GitHub Actions workflow structure, matrices, dependencies, cache, artifacts,
  required checks, environments, secrets, OIDC, reusable workflows, and composite actions.
- **co-19–co-29**: semantic versioning, conventional commits, automation, publishing, deployment
  strategies, toggles, rollback, pipeline as code, quality gates, and provenance.
- **co-30–co-34**: DORA metrics, runner boundaries, affected CI, progressive delivery, and automated
  canary analysis.

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Daily Merge and Self-Testing Build](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-1-daily-merge-and-self-testing-build)
- [Example 2: Keep the Mainline Green](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-2-keep-the-mainline-green)
- [Example 3: Keep Software Releasable](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-3-keep-software-releasable)
- [Example 4: Continuous Delivery Versus Deployment](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-4-continuous-delivery-versus-deployment)
- [Example 5: Automatic Deployment After Green](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-5-automatic-deployment-after-green)
- [Example 6: Order a Deployment Pipeline](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-6-order-a-deployment-pipeline)
- [Example 7: Fail Fast in the Commit Stage](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-7-fail-fast-in-the-commit-stage)
- [Example 8: Block Promotion on Acceptance Failure](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-8-block-promotion-on-acceptance-failure)
- [Example 9: Use a Single Trunk](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-9-use-a-single-trunk)
- [Example 10: Identify GitFlow Branch Roles](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-10-identify-gitflow-branch-roles)
- [Example 11: Apply the GitFlow Continuous-Delivery Caveat](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-11-apply-the-gitflow-continuous-delivery-caveat)
- [Example 12: Run a Minimal GitHub Actions Workflow](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-12-run-a-minimal-github-actions-workflow)
- [Example 13: Use Push and Pull-Request Triggers](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-13-use-push-and-pull-request-triggers)
- [Example 14: Choose Run or Uses](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-14-choose-run-or-uses)
- [Example 15: Select a Hosted Runner](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-15-select-a-hosted-runner)
- [Example 16: Set Up Python Before Tests](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-16-set-up-python-before-tests)
- [Example 17: Test a Python Version Matrix](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-17-test-a-python-version-matrix)
- [Example 18: Control Matrix Fail-Fast Behavior](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-18-control-matrix-fail-fast-behavior)
- [Example 19: Sequence Jobs with Needs](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-19-sequence-jobs-with-needs)
- [Example 20: Cache Dependency Inputs](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-20-cache-dependency-inputs)
- [Example 21: Branch on a Cache Hit](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-21-branch-on-a-cache-hit)
- [Example 22: Upload a Build Artifact](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-22-upload-a-build-artifact)
- [Example 23: Download a Build Artifact](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-23-download-a-build-artifact)
- [Example 24: Require a Green Status Check](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-24-require-a-green-status-check)
- [Example 25: Choose a Semantic Version Increment](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-25-choose-a-semantic-version-increment)
- [Example 26: Compare Pre-release Precedence](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-26-compare-pre-release-precedence)
- [Example 27: Write a Conventional Commit](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-27-write-a-conventional-commit)
- [Example 28: Mark a Breaking Conventional Commit](/en/learn/courses/cicd-and-release-engineering/learning/beginner#example-28-mark-a-breaking-conventional-commit)

### Intermediate (Examples 29–55)

- [Example 29: Map Conventional Commits to SemVer](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-29-map-conventional-commits-to-semver)
- [Example 30: Protect a Production Environment](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-30-protect-a-production-environment)
- [Example 31: Wait for Deployment Approval](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-31-wait-for-deployment-approval)
- [Example 32: Inject a Secret Safely](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-32-inject-a-secret-safely)
- [Example 33: Mask a Sensitive Value](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-33-mask-a-sensitive-value)
- [Example 34: Request a Short-Lived OIDC Token](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-34-request-a-short-lived-oidc-token)
- [Example 35: Call a Reusable Workflow](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-35-call-a-reusable-workflow)
- [Example 36: Factor a Composite Action](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-36-factor-a-composite-action)
- [Example 37: Pass a Secret to a Reusable Workflow](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-37-pass-a-secret-to-a-reusable-workflow)
- [Example 38: Publish a Release Tag](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-38-publish-a-release-tag)
- [Example 39: Generate a Changelog](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-39-generate-a-changelog)
- [Example 40: Automate the Release Decision](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-40-automate-the-release-decision)
- [Example 41: Publish an npm Package](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-41-publish-an-npm-package)
- [Example 42: Push a Container Image](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-42-push-a-container-image)
- [Example 43: Gate on Lint](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-43-gate-on-lint)
- [Example 44: Gate on Pyright](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-44-gate-on-pyright)
- [Example 45: Gate on Coverage](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-45-gate-on-coverage)
- [Example 46: Scan with CodeQL](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-46-scan-with-codeql)
- [Example 47: Review Dependency Updates](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-47-review-dependency-updates)
- [Example 48: Review Pipeline as Code](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-48-review-pipeline-as-code)
- [Example 49: Compare a Jenkinsfile](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-49-compare-a-jenkinsfile)
- [Example 50: Assess a Self-Hosted Runner](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-50-assess-a-self-hosted-runner)
- [Example 51: Avoid Public-Repository Runner Exposure](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-51-avoid-public-repository-runner-exposure)
- [Example 52: Run Affected Monorepo CI](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-52-run-affected-monorepo-ci)
- [Example 53: Select Affected Base and Head](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-53-select-affected-base-and-head)
- [Example 54: Assert Required Checks in Python](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-54-assert-required-checks-in-python)
- [Example 55: Order Gates for Fast Feedback](/en/learn/courses/cicd-and-release-engineering/learning/intermediate#example-55-order-gates-for-fast-feedback)

### Advanced (Examples 56–83)

- [Example 56: Switch Blue-Green Traffic](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-56-switch-blue-green-traffic)
- [Example 57: Roll Back Blue-Green Traffic](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-57-roll-back-blue-green-traffic)
- [Example 58: Shift Canary Traffic Gradually](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-58-shift-canary-traffic-gradually)
- [Example 59: Target a Canary Cohort](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-59-target-a-canary-cohort)
- [Example 60: Roll Back a Bad Canary Automatically](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-60-roll-back-a-bad-canary-automatically)
- [Example 61: Practice Progressive Delivery](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-61-practice-progressive-delivery)
- [Example 62: Choose Rollback or Fix Forward](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-62-choose-rollback-or-fix-forward)
- [Example 63: Use a Release Toggle](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-63-use-a-release-toggle)
- [Example 64: Use an Experiment Toggle](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-64-use-an-experiment-toggle)
- [Example 65: Use an Operations Toggle](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-65-use-an-operations-toggle)
- [Example 66: Use a Permission Toggle](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-66-use-a-permission-toggle)
- [Example 67: Route Toggles in Typed Python](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-67-route-toggles-in-typed-python)
- [Example 68: Record SLSA Provenance](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-68-record-slsa-provenance)
- [Example 69: Sign a Container Image](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-69-sign-a-container-image)
- [Example 70: Verify a Container Signature](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-70-verify-a-container-signature)
- [Example 71: Gate on Provenance Verification](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-71-gate-on-provenance-verification)
- [Example 72: Measure Deployment Frequency](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-72-measure-deployment-frequency)
- [Example 73: Measure Change Lead Time](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-73-measure-change-lead-time)
- [Example 74: Measure Change Failure Rate](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-74-measure-change-failure-rate)
- [Example 75: Measure Failed-Deployment Recovery Time](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-75-measure-failed-deployment-recovery-time)
- [Example 76: Report DORA Metrics in Python](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-76-report-dora-metrics-in-python)
- [Example 77: Promote One Immutable Artifact](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-77-promote-one-immutable-artifact)
- [Example 78: Wire a Commit-to-Production Pipeline](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-78-wire-a-commit-to-production-pipeline)
- [Example 79: Evaluate Gate Cost](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-79-evaluate-gate-cost)
- [Example 80: Preview the CI/CD Capstone](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-80-preview-the-ci-cd-capstone)
- [Example 81: Analyze an Argo Rollouts Canary](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-81-analyze-an-argo-rollouts-canary)
- [Example 82: Drive a Flagger Progressive Delivery](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-82-drive-a-flagger-progressive-delivery)
- [Example 83: Choose a Progressive Delivery Strategy](/en/learn/courses/cicd-and-release-engineering/learning/advanced#example-83-choose-a-progressive-delivery-strategy)
