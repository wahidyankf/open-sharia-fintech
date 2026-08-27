---
title: "Post-Push CI Verification — Overview and Monitoring Tool"
description: Defines when Post-Push CI Verification applies and the required ScheduleWakeup-based monitoring tool and cadence.
when_to_use: Use when deciding which monitoring tool and poll cadence to use for CI after a push.
---

# Post-Push CI Verification — Overview and Monitoring Tool

After every push, verify every GitHub Actions workflow triggered on the resolved delivery mode's target — `origin main` for the direct-push modes (`worktree-to-origin-main`, `main-to-origin-main`), the PR branch for the `*-to-pr` modes (`worktree-to-pr`, `main-to-pr`).

**Phase 0 never reaches this step**: it pushes nothing (Step 2b), so it triggers no CI run and there is nothing to verify. Skip straight from the Phase 0 gate to Phase 1.

**An intermediate phase reaches this step only in the direct-push modes.** Under a `*-to-pr` mode, a phase that is not its delivery unit's **boundary** has opened no PR, so there is no PR CI to verify — proceed to the next phase after its gate is green. The PR-branch verification below binds at delivery boundaries.

**Monitoring tool**: Schedule a wakeup every 2 minutes, then make one `gh run view` (direct-push modes) or `gh pr checks` (`*-to-pr` modes) status read. Never use `gh run watch` or tight polling, regardless of expected job duration. See [CI Monitoring Convention](../../../development/workflow/ci-monitoring.md) for trigger discipline and rate-limit recovery procedures.
