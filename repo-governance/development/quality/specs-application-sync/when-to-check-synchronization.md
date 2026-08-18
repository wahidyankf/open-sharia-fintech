---
title: "When to Check Synchronization"
description: "The trigger points for verifying specs/ and application code are still in sync."
category: explanation
subcategory: development
tags:
  - specs
  - architecture
  - c4-diagrams
  - gherkin
  - synchronization
  - quality
created: 2026-03-24
when_to_use: "Use when deciding whether a change requires a synchronization check."
---

# When to Check Synchronization

Check and update specs in the same commit as the application change for:

- Adding, removing, or renaming an application (`apps/`, `libs/`)
- Changing framework or runtime technology for an existing application
- Adding or removing a REST endpoint, tRPC procedure, GraphQL resolver, or equivalent API surface
- Adding or removing a major UI page or route
- Introducing a new data store or removing an existing one
- Adding or removing an external integration that appears in the C4 context or container diagram
- Adding or removing a CLI command (covered by mandatory `rhino-cli specs coverage`)
- Changing deployment target in a way that creates a new architectural boundary

Do **not** update specs for:

- Bug fixes that do not change the observable API contract (the behavior described in specs was already the intended behavior)
- Styling changes, layout adjustments, or purely visual changes with no behavioral impact
- Internal refactors that do not change public interfaces, API contracts, or architectural boundaries
- Dependency version upgrades that do not change behavior visible to consumers
- Performance optimizations with unchanged interfaces
- Test-internal changes (renaming a test helper, restructuring mocks) that do not change what is tested
