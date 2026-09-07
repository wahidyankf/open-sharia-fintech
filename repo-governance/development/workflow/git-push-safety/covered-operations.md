---
description: The table of git push operations that require explicit, per-instance user approval before an agent may run them.
when_to_use: Use when deciding whether a specific push command or its aliased/scripted equivalent needs approval before running.
---

# Covered Operations

The following operations require explicit, per-instance user approval:

| Operation                       | Why it is destructive or safety-bypassing                                                                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `git push --force`              | Overwrites the remote branch tip, permanently discarding any remote commits not present locally. Teammates lose pushed work without warning.                                                     |
| `git push --force-with-lease`   | Safer than `--force` but still rewrites history. The lease check can silently succeed when a teammate's push arrived before the lease was refreshed, making it unreliable as a safety guarantee. |
| `git push --no-verify`          | Skips all git hooks on the push side, bypassing `typecheck`, `lint`, and `test:quick` quality gates. Broken code can reach the remote and block CI.                                              |
| Any combination of the above    | The risks compound; combined flags require the same explicit approval.                                                                                                                           |
| Aliased or scripted equivalents | Any shell alias, npm script, Makefile target, or CI step that invokes the above flags is subject to the same rule. The mechanism does not change the requirement.                                |
