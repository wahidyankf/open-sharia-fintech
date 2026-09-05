---
title: "Licensing Overview and Scope"
description: Why the repository uses a single per-directory MIT licensing strategy and which licensing decisions this convention governs versus leaves to other policy.
when_to_use: Read this before deciding what license text to apply to a new directory or evaluating why the repository does not use a dual-license or per-app-varying model.
category: explanation
subcategory: conventions
tags:
  - licensing
  - structure
  - mit
  - per-directory
created: 2026-04-04
---

# Licensing Overview and Scope

This is the learning-side entry point for the [Per-Directory Licensing Convention](../licensing.md):
why the repository standardized on one license, and precisely which decisions this convention
covers.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Each application directory contains its own LICENSE file, making licensing terms immediately
  visible without requiring readers to trace inheritance from the root.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: A
  single MIT license throughout eliminates the dual-license split model and the "HOW vs WHAT"
  distinction. Simpler licensing reduces contributor friction and legal overhead.

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: MIT removes all
  restrictions for contributors, learners, and downstream consumers. Anyone can use, modify,
  and redistribute any part of the repository without restriction.

## Purpose

This convention establishes clear rules for which license applies to which code in the
repository. All code is MIT. The per-directory LICENSE file structure is retained as a future
escape hatch — if a specific directory ever needs different terms, the mechanism exists without
requiring a root LICENSE change.

## Scope

### What This Convention Covers

- License type selection for new applications, libraries, and directories
- Per-directory LICENSE file placement rules
- Copyright notice format
- Root LICENSE fallback behaviour

### What This Convention Does NOT Cover

- Third-party dependency license compliance (e.g., LGPL, Apache 2.0 obligations)
- Contributor License Agreements (CLAs)
- Trademark or patent policies
