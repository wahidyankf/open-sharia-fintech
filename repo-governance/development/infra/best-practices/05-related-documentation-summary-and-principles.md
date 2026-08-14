---
title: "Related Documentation, Summary, and Principles"
description: Lists related documentation, summarizes the ten infrastructure best practices, and states the principles and conventions this guidance implements.
category: explanation
subcategory: development
tags: [infrastructure, best-practices, summary]
created: 2026-05-12
when_to_use: Use when looking for related documentation links, a quick recap of all ten best practices, or the principles/conventions this document implements.
---

# Related Documentation, Summary, and Principles

## Related Documentation

- [Temporary Files Convention](../temporary-files.md) - Complete temporary file standards
- [Acceptance Criteria Convention](../acceptance-criteria.md) - Gherkin acceptance criteria guide
- [Anti-Patterns](../anti-patterns.md) - Common mistakes to avoid
- [Explicit Over Implicit Principle](../../../principles/software-engineering/explicit-over-implicit.md) - Why clear organization matters

## Summary

Following these best practices ensures:

1. Use designated temporary directories
2. Follow standardized report naming
3. Write reports progressively
4. Generate real UUIDs and timestamps
5. Use scope-based execution tracking
6. Write Gherkin acceptance criteria
7. Require Write and Bash tools for reports
8. Pair audit and fix reports correctly
9. Clean up temporary files periodically
10. Document temporary file purposes

Infrastructure built following these practices is organized, traceable, testable, and maintainable.

## Principles Implemented/Respected

- **Explicit Over Implicit**: Clear file organization, standardized naming
- **Automation Over Manual**: Progressive report writing, automated tracking
- **Simplicity Over Complexity**: Two directories for all temporary files

## Conventions Implemented/Respected

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Report files follow standardized naming with UUID chains and timestamps
- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Clear, structured documentation of infrastructure practices
- **[Dynamic Collection References Convention](../../../conventions/writing/dynamic-collection-references.md)**: Avoid hardcoded counts in report descriptions
