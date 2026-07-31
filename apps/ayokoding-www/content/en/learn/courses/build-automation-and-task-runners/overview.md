---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Prior topics**: [Just Enough Bash](../just-enough-bash/learning/overview.md), [Version Control
  and Git](../version-control-and-git/learning/overview.md), and [Just Enough
  TypeScript](../just-enough-typescript/learning/overview.md).
- **Tools**: GNU Make, just, Node.js with npm, and optionally Bazel plus Gradle. Each worked artifact
  is local and uses only a temporary directory beneath its own example.

## Why this exists

Typing a build, test, and packaging sequence by hand hides its dependencies and eventually drifts.
This course teaches you to declare artifacts and inputs so a runner can name repeatable work and a
build system can rebuild only what changed.

Make is timestamp-driven, just and npm scripts are command runners, and Bazel plus Gradle model
content-fingerprinted work with caching. The practical choice follows the project: use a clear recipe
alias first, then adopt a stronger dependency model when incorrect or expensive rebuilds become real.

## How this topic is organized

- **[Learning](./learning/overview.md)**: 80 self-contained examples, from Make rules to a multi-tool
  capstone.
- **[Drilling](./drilling/overview.md)**: recall prompts, judgment exercises, and runnable practice.

Next: [Learning Overview](./learning/overview.md) →
