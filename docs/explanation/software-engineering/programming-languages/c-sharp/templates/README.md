---
title: C# Documentation Templates
description: Reusable templates for C# development patterns in OSE Platform
category: explanation
subcategory: prog-lang
tags:
  - csharp
  - templates
  - programming-languages
created: 2026-04-26
---

# C# Documentation Templates

This directory is reserved for reusable C# documentation templates. It is intentionally empty today, so it does not yet offer a copy-and-adapt starting point.

## Purpose

When templates are added, they will provide a documented starting point for common C# patterns without pretending that an unreviewed snippet is a complete implementation.

## Template Naming Convention

Templates use plain kebab-case filenames (e.g., `value-object.md`). The containing directory (`programming-languages/c-sharp/templates/`) encodes the category.

## Templates

No templates are published in this directory yet. Use the [C# programming-language overview](../README.md) and the relevant architecture standards instead of assuming that the example filenames below already exist.

Candidate templates, once a recurring and reviewed need exists:

- `value-object.md` — record-based value object with validation
- `aggregate-root.md` — aggregate root with domain events
- `minimal-api-endpoint.md` — minimal API endpoint group with filters
- `ef-core-repository.md` — generic EF Core repository with a specification

## Usage

Templates in this directory can be used as:

- Starting points for new implementations
- Reference patterns for code review
- Educational examples in documentation

## Related Documentation

- [C# Programming Language Overview](../README.md) - Language documentation index
- [File Naming Convention](../../../../../../repo-governance/conventions/structure/file-naming.md) - Naming patterns
