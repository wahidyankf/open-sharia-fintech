---
title: "Post-Push CI Verification — Overview and Monitoring Tool"
description: Defines when Post-Push CI Verification applies and the required ScheduleWakeup-based monitoring tool and cadence.
when_to_use: Use when deciding which monitoring tool and poll cadence to use for CI after a push.
---

# Post-Push CI Verification — Overview and Monitoring Tool

After every push, verify every GitHub Actions workflow triggered on the resolved delivery mode's target — `origin main` for the direct-push modes (`worktree-to-origin-main`, `main-to-origin-main`), the PR branch for the `*-to-pr` modes (`worktree-to-pr`, `main-to-pr`).

**Phase 0 never reaches this step**: it pushes nothing (Step 2b), so it triggers no CI run and there is nothing to verify. Skip straight from the Phase 0 gate to Phase 1.

**An intermediate phase reaches this step only in the direct-push modes.** Under a `*-to-pr` mode, a phase that is not its delivery unit's **boundary** has opened no PR, so there is no PR CI to verify — proceed to the next phase after its gate is green. The PR-branch verification below binds at delivery boundaries.

**Monitoring tool**: The required default for standard CI jobs (10–35 min) is `ScheduleWakeup` + a single `gh run view` (direct-push modes) or `gh pr checks` (`*-to-pr` modes) call on wakeup (2 API calls total per run). Use `gh run watch <run-id>` (or tight polling of `gh pr checks`) only if the job is expected to complete in under 5 minutes — both poll every ~3 s and exhaust the GitHub API rate limit (5,000 req/hour) on any job longer than ~5 min. Manual tight-loop polling without a sleep interval is also **forbidden**. See [CI Monitoring Convention](../../../development/workflow/ci-monitoring.md) for required tooling, minimum poll intervals, trigger discipline, and rate-limit recovery procedures.
