---
title: "Principles Implemented/Respected"
description: "Principles this convention implements."
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
when_to_use: "Use to trace this convention's principle rationale."
---

# Principles Implemented/Respected

This convention implements the following core principles:

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Checking a
  `git` subprocess's exit status is a natural, necessary first response to a fixture-escape
  symptom -- but it treats "the command failed" as the only failure mode. The motivating incident's
  `git` commands never failed; they succeeded against the wrong repository, which exit-status
  checking cannot detect even in principle. A fix that only catches command failure, not command
  success-against-the-wrong-target, addresses a symptom, not the cause. This convention names the
  real cause (ambient, CWD-dependent git repository discovery) and closes it structurally.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Ambient git repository discovery -- walking up from the process's current working directory
  until a `.git` is found -- is the implicit mechanism this convention forbids. Every fixture
  must state explicitly, via environment variables, which repository it targets. Nothing about
  which repository a git fixture touches should ever depend on which directory a process happened
  to be in when the command ran.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: A fixture
  whose correctness depends on the process-global current working directory is non-deterministic
  under concurrency -- the exact failure mode this convention exists to prevent. A fixture that
  fully specifies its target repository via `GIT_DIR`/`GIT_WORK_TREE`/`GIT_CEILING_DIRECTORIES`
  behaves identically regardless of how many other tests, threads, or scenarios are running
  concurrently.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  The pre-write escape guard (Standard 4) is an automated, fail-loud check that runs before every
  write operation -- it does not depend on a human noticing that a fixture "looks risky." A
  reviewer or checker agent can grep for the required isolation environment variables and the
  guard call, rather than manually auditing every fixture's control flow for CWD-dependence.
