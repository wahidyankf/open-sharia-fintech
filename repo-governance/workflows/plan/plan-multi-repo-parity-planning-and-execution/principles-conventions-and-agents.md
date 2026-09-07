---
title: "Principles, Conventions, and Agents"
description: Lists the principles and conventions this composite implements, and the agents it delegates to across its planning and execution phases.
when_to_use: Use when auditing this workflow's governance alignment or looking up which agent performs a given phase.
---

# Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Three hard-gated grills make every cross-repo decision and every operational execution decision
  explicit before work proceeds.
- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**:
  Survey → matrix → grill → research → grill → author → gate → grill → execute is deliberate
  sequencing by construction.
- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  The full idea-to-archived-parity lifecycle runs as one orchestration instead of four manual
  hand-offs.
- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: The execution
  phase inherits plan-execution's fix-all-issues-including-preexisting rule in every repo.
- **[No Time Estimates](../../../principles/content/no-time-estimates.md)**: Describes outcomes and
  gates, never durations.

## Conventions Implemented/Respected

- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: Fixed mature core,
  one reader-led technical form, `in-progress` staging, worktree specification, executor tagging,
  and phase gates are enforced through the nested workflows.
- **[Worktree Path Convention](../../../conventions/structure/worktree-path.md)** and
  **[Worktree Toolchain Initialization](../../../development/workflow/worktree-setup.md)**: Every
  worktree lands at `worktrees/<name>/` and is initialized with the two-step toolchain sequence.
- **[Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md)**:
  All three grill sessions present 2-4 concrete options per question; open-ended questions are
  forbidden.
- **[Commit Messages Convention](../../../development/workflow/commit-messages.md)**: Conventional
  Commits, thematic splits, in every repo.
- **[CI Monitoring Convention](../../../development/workflow/ci-monitoring.md)**: Post-push CI
  verification in the execution phase uses scheduled wake-ups, never tight-loop polling.
- **[Linking Convention](../../../conventions/formatting/linking.md)**: GitHub-compatible markdown
  links with `.md` extensions throughout.
- **[Plans Organization Convention §Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)**:
  each repo's plan resolves its own delivery mode independently in the execution phase (Step 4),
  distinct from this composite's own planning-phase `mode` input (Step 1).

## Agents

- [plan-maker](../../../../.claude/agents/plan/plan-maker.md) — authors each repo's plan (planning phase)
- [plan-checker](../../../../.claude/agents/plan/plan-checker.md) /
  the [plan-quality-gate](../plan-quality-gate.md) itself — one gate run per plan (planning phase)
- [web-researcher](../../../../.claude/agents/web/web-researcher.md) — conditional research
  (planning phase)
- [plan-execution-checker](../../../../.claude/agents/plan/plan-execution-checker.md) — independent
  validation per repo (execution phase)
- [repo-setup-manager](../../../../.claude/agents/repo/repo-setup-manager.md) — Phase 0 environment setup
  and baseline per repo (execution phase)
