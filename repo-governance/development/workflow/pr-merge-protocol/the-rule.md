---
title: "The Rule"
description: The five hardened preconditions that must all hold before an AI agent or automation may merge a pull request.
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
when_to_use: Use immediately before merging any pull request, to confirm all five preconditions hold.
---

# The Rule

**AI agents and automation MUST NOT merge a pull request until the hardened preconditions hold.**

A PR merges only when **all five** hold:

- **(a)** the PR's behavior route is complete — an eligible PR reached the first completed specialist
  cycle with zero code-related MEDIUM/HIGH/CRITICAL findings within the default maximum of seven,
  while a noneligible PR has recorded classifier evidence and a green
  `.github/workflows/pr-quality-gate.yml` run. A `blocked` route status prevents merge;
- **(b)** 0 code-related CRITICAL, HIGH, and MEDIUM findings are outstanding;
- **(c)** the branch is up-to-date with the latest `origin/main`, brought forward
  **non-destructively** if behind (never a shared-history rewrite);
- **(d)** the route-required quality gate is green: all applicable local and CI gates for an eligible
  PR; `.github/workflows/pr-quality-gate.yml` for a noneligible PR;
- **(e)** the surface-conditional tester gates have been run and their defect findings resolved for
  an eligible PR. A noneligible PR has no reachable behavior and does not run those tester gates.

For every PR merge -- without exception -- the agent must:

1. Confirm all five preconditions hold.
2. Surface the PR status, including which gates passed and how each precondition was satisfied.
3. Execute the merge -- `[AI]` is the default actor.

`[AI]` is the merge actor once the preconditions hold, unless a separate, explicitly authorized
exception says otherwise. This convergence plan has no human review or merge gate.

**Preconditions are evaluated per merge.** Satisfying them for one PR says nothing about the next;
each PR is assessed from zero against the full set.
