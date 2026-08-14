---
title: "The Sixteen Rules (11-14)"
description: "Rules 11-14: deploy config as code, distinguishing assertions, checkbox lockstep, clean re-entry."
category: explanation
subcategory: development
tags:
  - quality
  - planning
  - ui
  - verification
  - testing
  - deployment
created: 2026-06-19
when_to_use: "Use when executing or verifying a UI plan against rules 11-14."
---

# The Sixteen Rules (11-14)

1. **(Verification) Deploy configuration is code — validate it in the plan.** Gap: a production
   deploy failed because `vercel.json`'s `buildCommand` still pointed at a moved file path; nothing
   tested it, so a green local build produced a broken Vercel build. Apply: any plan that
   moves/renames files includes a deploy-config sweep (`vercel.json`, Dockerfiles, CI
   `buildCommand`s) and a real post-deploy smoke test of the live URL — not just local gates.

2. **(Execution) Prefer assertions that distinguish correct from buggy; pick fixtures that exercise
   the branch.** (Sharpens Rule 5.) A presence-only assertion passes under inverted logic; a
   fixture that trivially satisfies the threshold never exercises the split. Author the test to
   fail when the logic inverts, and probe the data to choose an input that genuinely splits the
   set.

3. **(Process) Keep delivery checkboxes in lockstep with execution (Atomic Sync Ritual).** Gap:
   items were implemented but recorded in a separate as-built log instead of ticking the matching
   boxes, so a phase _looked_ unfinished and needed a later reconciliation pass. Apply: tick the
   box the moment the item lands; if you must record as-built, reconcile the boxes in the **same**
   commit — never leave them divergent.

4. **(Process) A feature reopened after archival needs a clean re-entry, not silent edits on
   `main`.** Gap: a post-archival fix round ran directly on `main` (the worktree was already
   removed) under a tight feedback loop. Apply: reopen the plan first (move it back to
   `plans/in-progress/`, re-provision the worktree) so the work has a home and the trunk stays
   clean; plan-execution documents this "reopen" entry path.
