---
description: The per-agent responsibility table — plan-maker, plan-checker, plan-quality-gate, and the plan-execution workflow — for applying this convention.
when_to_use: Use when identifying which agent owns a specific responsibility under the Git Push Default Convention.
---

# Agent Responsibilities

| Agent                                       | Responsibility                                                                                                                                                                              |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan-maker`                                | Applies `worktree-to-pr` by default; adds a justified `## Delivery Mode` field only when overriding it.                                                                                     |
| `plan-checker`                              | Flags delivery checklists that assume direct push without a declared override, and mis-tagged `[HUMAN]`/`[AI]` git-mechanical steps.                                                        |
| `plan-quality-gate`                         | Corrects mode-mismatched checklists and retags mis-tagged git-mechanical steps.                                                                                                             |
| plan-execution workflow                     | Resolves the delivery mode once at Step 0 via the three-tier precedence; pushes to the resolved integration target; rebases to maintain linear history; fixes preexisting mismatches found. |
| plan-execution workflow in worktree context | Same as above — worktree execution is one axis of the mode, not the whole mode; resolves per the precedence, not by inference from context.                                                 |
