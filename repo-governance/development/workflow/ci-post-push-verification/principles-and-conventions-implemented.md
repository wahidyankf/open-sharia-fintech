---
description: The principles and companion conventions that CI post-push verification respects.
when_to_use: Use when tracing why CI post-push verification exists back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: The GitHub CI workflows exist to catch what the pre-push hook cannot — integration failures, E2E regressions, and deployment breakage. This convention ensures those automated checks are actively invoked rather than passively awaited.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: A failing CI workflow after a push is not "CI's problem." It is a sign that the work is incomplete. This convention treats CI failure as an unresolved root cause, not a background concern to defer.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Verification must be explicit. Assuming CI will pass, or that a scheduled run will catch issues, substitutes an implicit hope for a deliberate check. This convention requires the verification step to be performed, not assumed.

## Conventions Implemented/Respected

This practice implements/respects the following development practices:

- **[CI Blocker Resolution Convention](../../quality/ci-blocker-resolution.md)**: When a CI workflow fails after push, the failure is treated as a CI blocker. Investigate the root cause and fix it properly per that convention. Never defer or bypass.

- **[Trunk Based Development Convention](../../workflow/trunk-based-development.md)**: TBD requires that `main` is always in a releasable state. Work that breaks CI would leave `main` unreleasable once it lands. This convention closes that gap by mandating verification after every push — on the PR branch under the default `worktree-to-pr`, which catches the breakage _before_ it can reach `main`, and on `main` itself under the direct-push modes, where there is no earlier checkpoint.

- **[Git Push Default Convention](../../workflow/git-push-default.md)**: The default integration target is a PR branch (`worktree-to-pr`); the direct-push modes remain available where a plan declares them. Under the direct-push modes there is no PR review buffer at all, so CI post-push verification is the only mechanism that catches what the pre-push hook missed; under `worktree-to-pr` it is what makes the PR green before the merge preconditions can hold.
