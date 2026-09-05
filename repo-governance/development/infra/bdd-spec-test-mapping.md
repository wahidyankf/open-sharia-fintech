---
title: "BDD Spec-to-Test Mapping"
description: "Compatibility entry point for canonical recursive Gherkin corpus and adapter mapping"
category: explanation
subcategory: development
tags: [bdd, gherkin, testing]
created: 2026-03-06
when_to_use: "Use when tracing an older BDD mapping reference to the canonical repository standard."
---

# BDD Spec-to-Test Mapping

## Principles Implemented/Respected

- [Automation over Manual](../../principles/software-engineering/automation-over-manual.md) — the
  canonical mapping is validated instead of maintained as a second manual registry.
- [Explicit over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — each
  project role declares the adapters it owns.

## Conventions Implemented/Respected

- [Specs Directory Structure](../../conventions/structure/specs-directory-structure.md) — owners use
  one recursively discovered canonical corpus.
- [Repository Working Language](../../conventions/writing/repository-working-language.md) — active
  repository-authored identifiers use `behaviour`.

The canonical [Behaviour-Driven Development standard](../behaviour-driven-development.md) replaces
the former CLI-specific filename/tag registry and demo-backend mapping rules. All owners now expose
one recursively discovered Gherkin corpus. Unit, Integration, and E2E adapters map that corpus by
project-role applicability, not by a central Rhino registry or fixed filename convention.

This entry point remains only to preserve discoverability from older guidance. New documentation
must link directly to the canonical standard.
