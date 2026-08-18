---
title: "Purpose"
description: "Why this convention exists."
category: explanation
subcategory: development
tags:
  - testing
  - git
  - test-fixtures
  - isolation
  - regression
  - safety
  - defense-in-depth
created: 2026-07-19
when_to_use: "Use when orienting to why git-fixture isolation is required."
---

# Purpose

Fixtures and tests that build throwaway git repositories are common across this polyglot
monorepo -- CLI integration tests exercising `git` plumbing, unit tests verifying repository-root
resolution, BDD scenario runners that construct scratch repos as test data. Every one of these
shells out to a real `git` binary. `git` was designed to discover the repository it should
operate on by walking upward from the current working directory (or by following `GIT_DIR`),
which is exactly the right default for a human sitting in a terminal and exactly the wrong
default for a concurrent test process whose current working directory is process-global, shared,
mutable state.

This convention exists so that a bug in test concurrency, a stray `TMPDIR` misconfiguration, or a
forgotten `.env()` call can **never** result in a `git` command executing against the real
repository -- not "usually won't," not "shouldn't," but structurally cannot, because every layer
of ambient repository resolution has been closed off in code, and any residual escape trips a
loud, immediate failure before a single write happens.
