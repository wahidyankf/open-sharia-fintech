---
description: Why this convention exists, the principles it implements, and what it covers versus what it explicitly does not cover
when_to_use: Read this when you need the rationale for splitting programming-language documentation between docs/explanation/ and ayokoding-www, or to confirm whether a topic is in scope.
---

# Principles, Purpose, and Scope

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Clear separation of concerns prevents confusion about where content belongs. One source for learning (ayokoding-www), one source for OSE Platform style (docs/explanation/)

- **[Documentation First](../../../principles/content/documentation-first.md)**: Explicit prerequisite knowledge statements ensure developers know where to learn languages before applying OSE Platform styles. Documentation acknowledges the educational foundation

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Required prerequisite statements make dependencies explicit. No assumption that developers already know languages - we tell them where to learn

## Purpose

This convention prevents duplication and confusion by defining:

- **What belongs in `docs/explanation/software-engineering/programming-languages/{language}/`**: Repository-specific style guides, coding standards, and conventions
- **What belongs in ayokoding-www**: Educational programming language content (0-95% coverage, by-example, in-practice, tutorials)
- **How to link between them**: Explicit prerequisite knowledge statements

This separation follows the **DRY principle** (Don't Repeat Yourself) - educational content lives in ONE place (ayokoding-www), style guides live in ANOTHER place (docs/explanation/), and they reference each other.

## Scope

### What This Convention Covers

- Scope boundaries for `docs/explanation/software-engineering/programming-languages/{language}/`
- Scope boundaries for ayokoding-www learning content
- Required prerequisite knowledge statements
- Linking patterns between educational and style guide content
- Content organization for all programming languages in the repository

### What This Convention Does NOT Cover

- **How to write educational content** - Covered in tutorial conventions ([Programming Language Content Standard](../../tutorials/programming-language-content.md), [By Example Tutorial](../../tutorials/swe-by-example.md))
- **How to write style guides** - Covered in [Content Quality Principles](../../writing/quality.md)
- **Diátaxis framework application** - Covered in [Diátaxis Framework Convention](../diataxis-framework.md)
- **ayokoding-www content conventions** - Covered in [Programming Language Content Standard](../../tutorials/programming-language-content.md)
