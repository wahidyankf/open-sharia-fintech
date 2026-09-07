---
title: By-Concept Tutorial Convention
description: Standards for creating comprehensive concept-driven tutorials with 95% coverage, heavily annotated code, and rich diagrams
when_to_use: Use when authoring, reviewing, or scoping a By-Concept (narrative-driven) tutorial for any language or framework.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-concept
  - education
  - narrative-driven
created: 2026-01-30
---

# By-Concept Tutorial Convention

This convention extends the [Tutorials Convention](../tutorials/general.md) for the By Concept tutorial type: narrative-driven learning through comprehensive concept explanations, heavily annotated code, and rich diagrams achieving 95% coverage. The sections below have moved into [`by-concept/`](./by-concept/) — read them in order for the full convention.

## Contents

1. [Purpose](./by-concept/purpose.md) — Why the By-Concept tutorial type exists and who it targets.
2. [Structure Integration with General Tutorial Standards](./by-concept/structure-integration.md) — How By-Concept adapts the general tutorial structure.
3. [Core Characteristics](./by-concept/core-characteristics.md) — The concept-driven approach, 95% coverage target, and 40-60 section count.
4. [Section Structure: Title, Diagram, and Narrative (Parts 1-3)](./by-concept/section-structure-parts-1-3.md) — The opening parts of the six-part concept-section structure.
5. [Section Structure: Heavily Annotated Code Examples (Part 4)](./by-concept/section-structure-part-4-code.md) — The annotated-code part of the six-part concept-section structure.
6. [Section Structure: Key Takeaway and Why It Matters (Parts 5-6)](./by-concept/section-structure-parts-5-6-takeaway-why.md) — The closing parts of the six-part concept-section structure.
7. [Complete Section Example: Goroutines and Concurrency](./by-concept/complete-example-goroutines.md) — A worked reference example's title, diagram, narrative, and code.
8. [Complete Section Example: Key Takeaway and Analysis](./by-concept/complete-example-key-takeaway-analysis.md) — The same example's key takeaway, why-it-matters, and part-by-part analysis.
9. [Annotation Density Standards](./by-concept/annotation-density-standards.md) — The 1.0-2.25 comment-density target and output-annotation pattern.
10. [Mermaid Diagram Guidelines](./by-concept/mermaid-diagram-guidelines.md) — When to include diagrams and the color-blind friendly palette.
11. [Coverage Progression by Level](./by-concept/coverage-progression-by-level.md) — Topic and section-count expectations per level.
12. [File Naming and Organization](./by-concept/file-naming-and-organization.md) — Directory structure and file naming pattern.
13. [Quality Checklist](./by-concept/quality-checklist.md) — The pre-publish checklist across coverage, code, narrative, diagrams, and structure.
14. [Validation and Enforcement](./by-concept/validation-and-enforcement.md) — Automated validation and the quality-gate workflow.
15. [Relationship to Other Tutorial Types](./by-concept/relationship-to-other-tutorial-types.md) — How By-Concept compares to the other tutorial types.
16. [Cross-Language Consistency](./by-concept/cross-language-consistency.md) — What must stay consistent versus what may vary across languages.
17. [Production-Validated Standards Summary](./by-concept/production-validated-standards-summary.md) — Condensed numeric targets and current production gaps.
18. [Principles Implemented/Respected](./by-concept/principles-implemented-respected.md) — The repository principles this convention implements.
19. [Scope](./by-concept/scope.md) — What this convention covers, does not cover, and where it applies.
20. [Related Documentation](./by-concept/related-documentation.md) — Links to By-Example, Naming, Content Quality, and Diagrams conventions.

## Related Documentation

- [By-Example Tutorial Convention](../tutorials/swe-by-example.md): Code-first alternative achieving same 95% coverage
- [Tutorial Naming Convention](../tutorials/naming.md): Tutorial type definitions and naming standards
- [Tutorials Convention](../tutorials/general.md): Base tutorial standards that by-concept inherits

## Frontmatter Requirements

### Beginner/Intermediate/Advanced Pages

```yaml
---
title: "Beginner" | "Intermediate" | "Advanced"
date: YYYY-MM-DDTHH:MM:SS+07:00
weight: 10000000 | 10000001 | 10000002
description: "Comprehensive {Language} tutorial covering {coverage}% with hands-on exercises"
tags: ["language-tag", "tutorial", "by-concept", "level-tag", "topic-tags"]
---
```
