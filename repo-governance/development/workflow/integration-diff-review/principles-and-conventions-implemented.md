---
description: The principles and companion conventions the integration diff review convention implements and respects.
when_to_use: Use when tracing why integration diff review exists back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Resuming
  work on autopilot immediately after an integration operation is the opposite of understanding before
  acting. This convention inserts a mandatory understanding step between "the integration succeeded"
  and "continue the task."

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Bugs introduced by
  an unreviewed rebase/pull surface later as confusing test failures or silent semantic breakage, far
  from their true cause. Reviewing the diff at the moment of integration catches the cause immediately,
  not downstream.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: "The
  merge was clean" is an implicit, git-mechanical signal. This convention requires an explicit,
  read-the-diff judgment call about semantic impact, which git's conflict detection cannot make.

## Conventions Implemented/Respected

- **[No Destructive Git Operations Convention](../no-destructive-git-operations.md)**: That convention
  governs which local operations are safe to run. This convention governs what to do with the
  operation's _result_ once it has run — the two are companions, not overlapping.

- **[Bare-Repo Base-Worktree Landing Method](../bare-repo-landing-method.md)**: Fast-forwarding local
  `main` after a sibling worktree has pushed ahead is itself an integration event in scope of this
  convention — the incoming commits must be read, not just fast-forwarded past.

- **[Agent Workflow Orchestration](../../agents/agent-workflow-orchestration.md)**: The same-machine
  assumption means other agents' pushes can land on the branch you are rebasing onto or pulling from
  at any time. This convention is the required response the moment that happens.
