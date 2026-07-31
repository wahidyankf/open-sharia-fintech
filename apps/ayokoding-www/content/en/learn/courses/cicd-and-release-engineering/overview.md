---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- [Version Control and Git](../version-control-and-git/learning/overview.md) for branches, commits,
  pull requests, and protected mainlines.
- [Containers and Orchestration](../containers-and-orchestration/learning/overview.md) for the images
  and deployments a release pipeline promotes.
- GitHub Actions access in a disposable public repository, Python 3.13, and an editor with YAML and
  Python language support.

## Why this exists

A release is a claim that one specific change is safe for a wider audience. CI/CD makes that claim
repeatable: continuous integration detects incompatible changes early, delivery preserves a promotable
artifact, and progressive deployment limits the blast radius when reality disagrees with a test suite.
This course teaches the pipeline as a reviewed product, not as a collection of opaque automation.

## Scope boundary

This course teaches pipeline design, promotion decisions, release metadata, and deployment safety. It
does not replace the containers course's runtime architecture or the cloud course's infrastructure
provisioning; it connects their verified outputs into a reliable delivery path.

## How this topic is organized

[Learning](./learning/overview.md) develops the concepts and 83 YAML-plus-Python examples from a
self-testing commit through provenance and automated canary analysis. The [capstone](./learning/capstone/overview.md)
combines those practices into a local, credential-free delivery simulation, while [drilling](./drilling/overview.md)
turns the same concepts into active recall and judgment practice.
