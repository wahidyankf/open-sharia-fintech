---
description: Who is responsible for CI post-push verification, and which shortcuts are explicitly forbidden.
when_to_use: Use when checking whether an agent or workflow step owes CI verification, or whether an action being considered is a forbidden shortcut.
---

# Agent Responsibilities and Forbidden Actions

## Agent Responsibilities

| Agent / Workflow        | Responsibility                                                                                                                                                                                  |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| All AI agents           | After pushing app or lib code changes to the delivery target (PR branch or `origin main`, per the declared mode), trigger and monitor all relevant CI workflows before declaring work complete. |
| plan-execution workflow | CI post-push verification is a required final step in any delivery that includes app or lib changes. It is not optional.                                                                        |
| Developer (human)       | Same requirement as agents — trigger and verify CI workflows before declaring work done.                                                                                                        |

## Forbidden Actions

The following actions are explicitly forbidden under this convention:

- Declaring work "done" before all relevant CI workflows pass.
- Skipping CI verification because "the pre-push hook passed."
- Assuming a scheduled CI run will catch issues without performing explicit verification.
- Treating a CI failure discovered after verification as someone else's problem to fix.
