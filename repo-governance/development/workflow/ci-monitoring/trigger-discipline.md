---
title: "Trigger Discipline"
description: Rules preventing redundant concurrent CI runs — never trigger the same workflow more than once every 10 minutes.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use before triggering a CI workflow, to confirm no run for it is already active.
---

# Trigger Discipline

Triggering the same workflow repeatedly before prior runs complete multiplies API quota consumption (setup calls, list calls, view calls per run) and risks concurrency cancellation — where GitHub's `concurrency` group cancels an in-progress run when a new one is queued, sending both to a non-green terminal state.

**Rules:**

1. Never trigger the same workflow more than once every 10 minutes.
2. Before triggering, check whether a run is already in progress:

   ```bash
   # Check for an active run before triggering
   gh run list --workflow=<workflow-file> --limit=1 --json status --jq '.[0].status'
   # If status is "in_progress" or "queued", do NOT trigger again
   ```

3. If a run was cancelled by a concurrency group, wait for the currently-running run to reach a terminal state before deciding whether to trigger again.
4. In plan execution, if CI was triggered for a push and the run is still in progress, schedule a wakeup and poll the existing run with `gh run view <id> --json status,conclusion` — do not trigger a new run.
