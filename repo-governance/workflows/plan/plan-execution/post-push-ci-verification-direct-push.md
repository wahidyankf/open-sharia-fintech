---
title: "Post-Push CI Verification — Direct-Push Modes"
description: Defines how execution monitors and resolves failures for GitHub Actions workflows triggered on a direct push to origin main.
when_to_use: Use when monitoring CI after a push under worktree-to-origin-main or main-to-origin-main.
---

# Post-Push CI Verification — Direct-Push Modes

**Continues** [Post-Push CI Verification — Overview and Monitoring Tool](./post-push-ci-verification-overview.md).

**Orchestrator action — `worktree-to-origin-main` / `main-to-origin-main` (direct push to `origin main`)**:

1. Identify which GitHub Actions workflows were triggered by the push
2. Find the run ID: `gh run list --workflow=<workflow-file> --limit=3`
3. Monitor to completion using the correct approach for the job duration:
   - **Standard jobs (10–35 min, required default)**: `ScheduleWakeup(delaySeconds=120)` (2 min), check with one `gh run view <run-id> --json conclusion,status,jobs`, repeat every 2-5 min until complete
   - **Short jobs (<5 min only)**: `gh run watch <run-id>` — do NOT use for 20–35 min CI jobs
   - Never use `gh run watch` on jobs expected to take 20–35 min — it polls every ~3s and exhausts API quota
4. If ANY workflow fails:
   - Pull failure logs and diagnose the root cause: `gh run view <run-id> --log-failed`
   - Fix locally (including preexisting CI failures — Iron Rule 3)
   - Run local quality gates again (Step 2b)
   - Push fix commit
   - Monitor CI again with `ScheduleWakeup` + single `gh run view` (or `gh run watch` if <5 min)
5. Repeat until ALL GitHub Actions workflows pass with zero failures
6. Do NOT proceed to the next delivery phase until CI is fully green
7. If rate-limited (HTTP 403 from `gh`): stop all `gh` calls immediately, use `ScheduleWakeup(delaySeconds=2100)` (35 min) to resume after the rolling window clears — do NOT spin in a retry loop
