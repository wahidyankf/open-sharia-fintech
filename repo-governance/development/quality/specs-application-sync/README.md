---
title: "Specs-Application Sync Convention"
description: "Bidirectional synchronization requirement between specs/ and application code in apps/ and libs/"
when_to_use: "Read this index to find the right Specs-Application Sync Convention child document."
---

# Specs-Application Sync Convention

- [Principles and Conventions Implemented/Respected](./01-principles-and-conventions-implemented-respected.md) — Principles and conventions this convention implements. Use when tracing this convention to the principles/conventions behind it.
- [What Must Stay in Sync](./02-what-must-stay-in-sync.md) — The three artifacts requiring sync: C4 diagrams, Gherkin feature files, and specs/ README files. Use when deciding which spec artifact a code change must also update.
- [When to Check Synchronization](./03-when-to-check-synchronization.md) — The trigger points for verifying specs/ and application code are still in sync. Use when deciding whether a change requires a synchronization check.
- [Decision Guide: Architecture Change vs. Minor Change](./04-decision-guide-architecture-change-vs-minor-change.md) — Table (part 1 of 2) mapping common change types to whether a spec update is required. Use when uncertain whether a REST/tRPC/data-store/app-level change requires a spec update.
- [Decision Guide (continued)](./05-decision-guide-continued.md) — Table (part 2 of 2) mapping common change types to whether a spec update is required. Use when uncertain whether a Next.js/React/app-rename/library-level change requires a spec update.
- [Existing Patterns to Follow](./06-existing-patterns-to-follow.md) — Worked spec-organization patterns for organiclever, ayokoding-www, and CLI apps. Use when structuring specs/ for a new app and want an existing pattern to follow.
- [Examples](./07-examples.md) — PASS/FAIL examples of endpoint, app-removal, bug-fix, and refactor changes against sync obligations. Use when you need a concrete example of a change that does or does not require a spec update.
- [Scope](./08-scope.md) — What this convention applies to, and its boundary with other conventions. Use when checking whether this convention applies to a specific kind of change.
- [Tools and Automation](./09-tools-and-automation.md) — The validators and checks that enforce specs-application sync. Use when locating the automated check for a sync violation.
- [Related Documentation](./10-related-documentation.md) — Cross-references to related structure and testing conventions. Use when you need a related convention on specs structure or testing.
