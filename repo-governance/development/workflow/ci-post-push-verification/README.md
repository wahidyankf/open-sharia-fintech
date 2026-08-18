---
title: "CI Post-Push Verification Convention"
description: "After pushing app or library code, manually trigger all related GitHub CI workflows and verify they pass before considering the work complete."
when_to_use: "Read this index to find the right CI Post-Push Verification Convention child document."
---

# CI Post-Push Verification Convention

- [Principles and Conventions Implemented](./principles-and-conventions-implemented.md) — The principles and companion conventions that CI post-push verification respects. Use when tracing why CI post-push verification exists back to the principles and conventions it respects.
- [The Rule and Workflow Mapping](./the-rule-and-workflow-mapping.md) — The four required steps after pushing app or lib code, and which CI workflow to trigger per changed app. Use when you need the exact steps to verify CI after a push, or need to know which workflow file covers a changed app.
- [Monitoring and Commands](./monitoring-and-commands.md) — How to monitor CI without exhausting the GitHub API rate limit, and the reference command set. Use when polling a CI run's status, or when you need the exact gh commands for triggering and checking a workflow.
- [Scope and Pre-Push Hook Coverage](./scope-and-pre-push-hook-coverage.md) — What kinds of pushes this convention applies to, what it excludes, and how it complements the pre-push hook. Use when deciding whether a push requires CI post-push verification, or checking what the pre-push hook already covers.
- [Agent Responsibilities and Forbidden Actions](./agent-responsibilities-and-forbidden-actions.md) — Who is responsible for CI post-push verification, and which shortcuts are explicitly forbidden. Use when checking whether an agent or workflow step owes CI verification, or whether an action being considered is a forbidden shortcut.
- [Examples](./examples.md) — Worked pass/fail examples of CI post-push verification, including how to fix a failure found during verification. Use when you need a concrete example of correct or incorrect CI post-push verification behavior.
