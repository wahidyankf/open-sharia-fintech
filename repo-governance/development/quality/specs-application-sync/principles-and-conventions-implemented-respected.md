---
title: "Principles and Conventions Implemented/Respected"
description: "Principles and conventions this convention implements."
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
when_to_use: "Use when tracing this convention to the principles/conventions behind it."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Documentation First](../../../principles/content/documentation-first.md)**: Specs are living documentation of system behavior and architecture. Allowing them to drift from reality turns them into misleading artifacts rather than authoritative sources of truth. Keeping them current is an instance of treating documentation as a first-class deliverable, not an afterthought.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The system's architecture and behavior should be fully legible from the repository. When C4 diagrams or Gherkin feature files diverge from the actual implementation, the system's behavior becomes implicit — knowable only by reading source code. Synchronization keeps behavior explicit.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Stale specs are a symptom of treating spec updates as optional. This convention addresses the root cause by making synchronization a mandatory part of every relevant change, not a periodic cleanup task.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Where synchronization can be enforced automatically — such as Nx cache inputs that include Gherkin specs, or `rhino-cli specs coverage` for CLI apps — automation is preferred. Manual checking is reserved for architectural changes that require human judgment.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Three-Level Testing Standard](.././three-level-testing-standard.md)**: All three test levels (unit, integration, E2E) consume Gherkin feature files from `specs/`. If feature files do not reflect current API behavior, tests consuming those specs validate the wrong contract.

- **[BDD Spec-to-Test Mapping](../../infra/bdd-spec-test-mapping.md)**: The mandatory 1:1 mapping between CLI commands and feature file `@tags` requires that specs and code evolve together. Adding a command without a spec, or removing a command without removing its spec, violates this mapping.
