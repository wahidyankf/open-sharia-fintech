---
title: F# Documentation Templates
description: Reusable templates for F# development patterns in OSE Platform
category: explanation
subcategory: prog-lang
tags:
  - fsharp
  - templates
  - programming-languages
created: 2026-03-09
---

# F# Documentation Templates

This directory is reserved for reusable F# documentation templates. It is intentionally empty today, so it does not yet offer a copy-and-adapt starting point.

## Purpose

When templates are added, they will provide a documented starting point for common F# patterns without pretending that an unreviewed snippet is a complete implementation.

## Template Naming Convention

Templates use plain kebab-case filenames (e.g., `giraffe-handler.md`). The containing directory (`programming-languages/f-sharp/templates/`) encodes the category.

## Templates

No templates are published in this directory yet. Use the [F# programming-language overview](../README.md) and the relevant architecture standards instead of assuming that the example filenames below already exist.

Candidate templates, once a recurring and reviewed need exists:

- `giraffe-handler.md` — Giraffe `HttpHandler` composition pattern
- `result-railway.md` — railway-oriented programming with `Result`
- `expecto-suite.md` — Expecto test module structure
- `discriminated-union-domain.md` — domain modeling with discriminated unions
- `mailboxprocessor-actor.md` — `MailboxProcessor` actor pattern

## Usage

Templates in this directory can be used as:

- Starting points for new implementations
- Reference patterns for code review
- Educational examples in documentation

## Related Documentation

- [F# Programming Language Overview](../README.md) - Language documentation index
- [File Naming Convention](../../../../../../repo-governance/conventions/structure/file-naming.md) - Naming patterns
