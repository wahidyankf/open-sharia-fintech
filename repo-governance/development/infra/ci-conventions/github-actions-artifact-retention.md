---
title: "Artifact Retention"
description: Every upload-artifact step must declare retention-days, because the inherited default bills storage.
category: explanation
subcategory: development
tags: [ci-cd, github-actions, cost]
created: 2026-09-01
when_to_use: Use when a workflow step uploads a build artifact or test report.
---

# Artifact Retention

**Every `actions/upload-artifact` step must declare an explicit `retention-days`.**

A step that omits it inherits the repository default. GitHub ships that default at **90 days**,
and the value is invisible at the point of use — nothing in the workflow file reveals how long the
upload will be billed. Retention is therefore a required, reviewable declaration, not an inherited
default.

The cost is multiplicative, not additive: retained bytes are `size x runs-per-day x
retention-days`. A 38 MB scratch binary uploaded by a PR gate that runs 30 times a day holds
**~100 GB** at 90-day retention. The account-wide Actions storage quota is measured in fractions of
a gigabyte, so a single undeclared step can exhaust it on its own while every individual upload
still looks harmless in review.

Choose the window by what the artifact is _for_:

| Artifact role                                 | Window               |
| --------------------------------------------- | -------------------- |
| Intra-run scratch consumed by a later job     | `1`                  |
| Test report or trace read when triage happens | `7`                  |
| Anything longer                               | Justify in a comment |

Only **private** repositories consume the billed quota — public-repository Actions storage is
free. Do not treat a public repository as an exemption: workflows are copied between repositories,
and this repository's `pr-quality-gate.yml` is mirrored into a private sibling where the same step
does bill.

## Enforcement

The `artifact-retention` gate (`scripts/verify-artifact-retention.sh`) fails any
`upload-artifact` step with no `retention-days` in its step block. It runs on `pre-commit` for
changed workflow files and across all workflows in CI. Attributing `retention-days` to the correct
step matters: a value on a _later_ step does not satisfy an earlier one.

The repository default is a backstop, not the control. Set it to a short window
(`PUT /repos/{owner}/{repo}/actions/permissions/artifact-and-log-retention`), because it also caps
**log** retention, which this gate cannot see and which bills at the same rate.
