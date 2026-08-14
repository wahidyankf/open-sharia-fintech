---
title: "Completeness Checklist"
description: "The checklist to verify a git fixture implements all six layers."
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
when_to_use: "Use before landing a new git-fixture test, to verify full isolation."
---

# Completeness Checklist

Before landing a test fixture that shells out to `git` to build a throwaway repository, verify:

- [ ] `GIT_CEILING_DIRECTORIES` is set to the fixture's temp root (Standard 1)
- [ ] `GIT_DIR` is set explicitly; no `git` invocation in the fixture relies on
      `current_dir()`/process CWD to select the repository (Standard 2). `GIT_WORK_TREE` is optional
      and must be **absent** for `git worktree add` and the escape guard.
- [ ] `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null` are set (Standard 3)
- [ ] A pre-write escape guard runs before every write command, comparing canonicalized
      `git rev-parse --show-toplevel` output against the intended tempdir, panicking/failing loud
      on mismatch (Standard 4)
- [ ] Every `git` subprocess's exit status is checked via `status.success()` or the language
      equivalent -- not inferred from a bare `.expect()`/try-catch around the spawn call alone
      (Standard 5)
- [ ] Anyone diagnosing a failing instance of this fixture does so in a throwaway clone, never the
      primary/real worktree (Standard 6 -- a process discipline, not a code check)
