---
title: "Before Merging"
description: The full (a)-(e) precondition checklist an agent must confirm immediately before merging, and why the list is spelled out in full rather than abbreviated.
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
when_to_use: Use as the final checklist immediately before executing a PR merge.
---

# Before Merging

Before merging, the agent must confirm **all five** hardened preconditions (a)-(e) hold, as stated in
[The Rule](./the-rule.md#the-rule) above and defined normatively in
[the PR Review Quality Gate](../../../workflows/pr/pr-review-quality-gate/hardened-merge-preconditions-a-e.md).
Do not substitute the shorter list that used to live here.

1. **(a)** The route is complete: eligible review reached its clean exit within its configured ceiling;
   noneligible review has classification evidence plus a green `pr-quality-gate.yml` run. `blocked`
   never merges.
2. **(b)** 0 code-related CRITICAL, HIGH, and MEDIUM findings outstanding, verified against the PR's
   own diff rather than against thread-resolution state.
3. **(c)** The branch is non-destructively up to date with the target branch (no merge conflicts).
4. **(d)** The route-required quality gate is green as of the PR's current head: all applicable
   gates for eligible work, or the named `pr-quality-gate.yml` workflow for noneligible work.
5. **(e)** Eligible surface tester gates have run and their findings are resolved. A noneligible
   route is explicitly exempt because its classifier evidence shows no reachable behavior.

> **Why this list is spelled out in full.** It previously carried only three items — CI completed,
> review comments checked, branch up to date — because it ran immediately before a **human approval
> prompt**, and the human was the backstop for whatever the list omitted. Now that `[AI]` merges by
> default, that backstop is gone and this is the last checklist an autonomous merge passes through.
> An enumeration that was merely incomplete has become the thing standing in for a reviewer. Any
> future edit must keep it congruent with (a)-(e); never shorten it.
