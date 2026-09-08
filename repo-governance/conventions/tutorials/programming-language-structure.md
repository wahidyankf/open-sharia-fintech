---
description: "Dual-path tutorial organization pattern for programming language education with by-concept and by-example learning tracks"
when_to_use: Use when creating, auditing, or restructuring a programming language's Full Set Tutorial Package directory structure on ayokoding-www.
---

# Programming Language Tutorial Structure Convention

**Defines the dual-path tutorial directory organization for programming language content on ayokoding-www.**

This convention standardizes how programming language tutorials are organized as a **Full Set Tutorial Package** with 5 mandatory components: foundational tutorials (initial-setup, quick-start), two complementary learning tracks (narrative-driven by-concept and code-first by-example, both achieving 95% coverage), and practical cookbook for problem-solving. All 5 components are required for complete language content. The sections below have moved into [`programming-language-structure/`](./programming-language-structure/) — read them in order for the full convention.

## Contents

1. [Principles, Purpose, and Scope](./programming-language-structure/principles-purpose-and-scope.md) — The content principles this convention implements, why it exists, and what it applies to.
2. [Directory Structure Pattern](./programming-language-structure/directory-structure-pattern.md) — Directory trees for dual-path and single-path languages.
3. [Full Set Components: Foundational and By-Example](./programming-language-structure/full-set-components-foundational-and-by-example.md) — Components 1-3: foundational tutorials and the by-example track.
4. [Full Set Components: By-Concept and Cookbook](./programming-language-structure/full-set-components-by-concept-and-cookbook.md) — Components 4-5: the by-concept track and the cookbook.
5. [Foundational Tutorials at Root](./programming-language-structure/foundational-tutorials-at-root.md) — Why Initial Setup and Quick Start stay at the tutorials root.
6. [Navigation Ordering](./programming-language-structure/navigation-ordering.md) — Required order of paths in tutorials navigation.
7. [Navigation Pattern: Weight Values](./programming-language-structure/navigation-weight-values.md) — The level-based weight-value system for tutorial folders and files.
8. [Full Set Completeness and Content Requirements](./programming-language-structure/completeness-and-content-requirements.md) — The completeness checklist plus frontmatter, link, overview, and index requirements.
9. [Examples](./programming-language-structure/examples.md) — Worked Java (dual-path) and Kotlin (single-path) examples.
10. [Validation](./programming-language-structure/validation.md) — Automated checkers and the manual verification checklist.
11. [Common Mistakes](./programming-language-structure/common-mistakes.md) — Five common structural mistakes with FAIL/PASS examples.
12. [Migration Guide](./programming-language-structure/migration-guide.md) — Six-step walkthrough for completing a Full Set Tutorial Package.
13. [Tutorial Folder Arrangement Standard](./programming-language-structure/tutorial-folder-arrangement-standard.md) — The manual, weight-ordered arrangement standard across all content types.

## Related Conventions

- **[Programming Language Content Standard](../tutorials/programming-language-content.md)** - Universal content architecture for programming languages (5 tutorial levels, coverage philosophy, quality metrics, pedagogical patterns)
- **[By Example Tutorial Convention](../tutorials/swe-by-example.md)** - Complete standards for creating code-first by-example tutorials (five-part structure, self-containment, educational comments, coverage progression)
- **[Tutorial Naming Convention](../tutorials/naming.md)** - Tutorial type definitions (Initial Setup, Quick Start, Beginner, Intermediate, Advanced coverage percentages)
- **[Content Quality Principles](../writing/quality.md)** - Universal markdown quality standards (active voice, heading hierarchy, accessibility)
- **[Diátaxis Framework](../structure/diataxis-framework.md)** - Documentation categorization (tutorials vs how-to vs reference vs explanation)

## Version History

- **v1.0** (2025-12-27): Initial convention based on Java/Elixir/Golang dual-path implementations and Kotlin/Python/Rust single-path implementations
