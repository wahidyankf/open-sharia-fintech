---
title: "TBD Benefits for This Project"
description: Why TBD helps solo/small teams, scaling the team, and continuous deployment.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when justifying TBD's value for this project's team size or deployment model.
---

# TBD Benefits for This Project

## For Solo/Small Team Development

Even with a small team, TBD provides benefits:

- PASS: **Simplified workflow**: No mental overhead of managing multiple branches
- PASS: **No merge conflicts**: Less time diverged = fewer conflicts
- PASS: **Faster feedback**: CI runs on every commit
- PASS: **Clear history**: Linear commit history is easy to understand
- PASS: **No stale code**: Everything is current

## For Scaling the Team

As the team grows, TBD prevents common scaling problems:

- PASS: **Coordination**: Everyone works on same codebase, sees changes immediately
- PASS: **Onboarding**: Simpler workflow for new contributors
- PASS: **Accountability**: Commits are visible, encouraging quality
- PASS: **Release readiness**: `main` is always releasable

## For Continuous Deployment

TBD enables automated deployment:

- PASS: **Deployment from `main`**: Every commit can deploy to staging
- PASS: **Feature flags**: Control production rollouts without branches
- PASS: **Rapid fixes**: Hotfixes commit to `main` and deploy immediately
- PASS: **Rollback**: Revert commit or toggle flag off
