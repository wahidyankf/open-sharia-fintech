---
description: Before any task, including a purely conversational one, open the harness's native task list and keep it continuously in sync with actual progress
when_to_use: Use whenever you're about to start work with 3 or more distinct steps, or work spanning multiple files or phases, before you touch the first file.
---

# Task List Discipline

Before any task — including a purely conversational one — create, update, or adjust the harness's native task list, then keep it continuously in sync with actual progress. A task list that lags behind reality is a defect, not a detail.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Creating a task list before starting multi-step work forces deliberate scoping. It surfaces assumptions, identifies dependencies, and reveals missing context before execution begins — not mid-way through.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: A task list makes the work plan explicit and shared. Progress, remaining work, and newly discovered tasks are visible rather than held in the agent's context window as implicit state that degrades with distance.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Keeping the task list current in the harness's native task list automates progress tracking. It replaces ad-hoc mental bookkeeping with a durable, queryable record.

- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: A task list layers complexity appropriately: start with the known steps, then add newly-discovered follow-up tasks as they surface. Complexity accretes in the list, not in the agent's informal prose output.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: This document follows active voice, proper heading hierarchy, and accessible examples throughout.

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: This document uses a lowercase kebab-case filename consistent with repository naming rules.

The following structural convention also informs this practice:

- **[Plans Convention](../../conventions/structure/plans.md)**: That convention governs plan-file delivery checklists (the checklist living inside `delivery.md` or a plan document). This practice governs the live working task list for everyday multi-step execution. Both require continuous sync; they serve different scopes.

## Contents

- [Purpose and Scope](./task-list-discipline/purpose-and-scope.md) — the two failure modes this practice prevents, and what it covers.
- [Standards 1-5](./task-list-discipline/standards-1-to-5.md) — create the list first, mark in-progress/completed accurately, add discovered tasks, one task per outcome.
- [Standard 6 — Idle-Polling Status Heartbeat](./task-list-discipline/standard-6.md) — the five-minute heartbeat required only while the main thread is otherwise idle and polling non-CI background work.
- [Standard 7 — Continuation State](./task-list-discipline/standard-7-continuation-state.md) — preserve and reconcile active user-established repository-rule decisions.
- [Anti-Patterns](./task-list-discipline/anti-patterns.md) — five common failure patterns and their fixes.
- [For AI Agents and Related Documentation](./task-list-discipline/for-ai-agents-and-related-documentation.md) — the five-point agent checklist and links to related conventions.
