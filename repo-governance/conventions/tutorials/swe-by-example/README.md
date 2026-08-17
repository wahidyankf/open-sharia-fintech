---
title: "By-Example Tutorial Convention"
description: "Standards for creating code-first by-example tutorials with 95% coverage, self-contained examples, and educational annotations"
when_to_use: "Read this index to find the right By-Example Tutorial Convention child document."
---

# By-Example Tutorial Convention

- [Purpose and Structure Integration with General Tutorial Standards](./01-purpose-and-structure-integration.md) — Defines the purpose of by-example tutorials and how their structure adapts and
- [Purpose and Structure Integration: Inherited and Specialized Requirements](./01b-inherited-and-specialized-requirements.md) — Lists the general tutorial standards by-example tutorials inherit, and the specialized requirements
- [Core Characteristics](./02-core-characteristics.md) — Defines the three core characteristics of by-example tutorials: code-first approach, 95% coverage
- [Core Features First: Why It Matters](./03-core-features-first-why.md) — Explains why by-example tutorials must teach core/built-in features before external dependencies, and
- [Core Features First: What to Prioritize](./03b-core-features-first-what-to-prioritize.md) — Lists which core/built-in features to prioritize for programming languages, frameworks, and platforms,
- [Core Features First: What to Avoid Initially](./04-core-features-first-what-to-avoid.md) — Catalogs premature abstraction/extension anti-patterns for languages, frameworks, and platforms, with paired FAIL/PASS
- [Core Features First: When to Introduce Dependencies](./05-core-features-first-when.md) — Defines the permitted exceptions for introducing external dependencies/abstractions and how to mark
- [Core Features First: Implementation by Coverage Level](./05b-core-features-first-implementation-by-level.md) — Shows how core-features-first applies concretely across beginner, intermediate, and advanced coverage levels.
- [Core Features First: Java Reference Implementation and Validation Criteria](./06-core-features-first-java-reference-and-validation.md) — Uses the Java by-example tutorial as a worked reference for core-features-first, and
- [Core Features First: Comparison for JSON Processing and State Management](./07-core-features-first-comparison-json-and-state.md) — Shows worked PASS/FAIL comparisons of core-features-first vs framework-first teaching for JSON processing
- [Core Features First: Comparison for HTTP Clients and DI, and Principle Integration](./07b-core-features-first-comparison-http-di-and-integration.md) — Shows worked PASS/FAIL comparisons of core-features-first vs framework-first teaching for HTTP clients
- [Example Structure: Brief Explanation, Diagram, and Annotation Density Standard](./08-example-structure-explanation-and-diagram.md) — Defines Parts 1 and 2 of the mandatory five-part example format (brief
- [Example Structure: Part 3 Annotated Code Reference Example](./09-example-structure-annotated-code-reference.md) — Provides a production-quality reference example of heavily annotated code with measured density,
- [Example Structure: Key Takeaway and Why It Matters](./10-example-structure-takeaway-and-why-it-matters.md) — Defines Parts 4 and 5 of the mandatory five-part example format: the
- [Complete Example Structure (Production Reference)](./11-complete-example-structure-reference.md) — Walks through a full production reference example (Golang Hello World) demonstrating all
- [Self-Containment Rules by Level](./12-self-containment-rules-by-level.md) — Defines the self-containment requirements for beginner, intermediate, and advanced examples, and the
- [Self-Containment Rules: Per-Example Annotation Density Measurement](./13-per-example-annotation-density-measurement.md) — Clarifies that annotation density is measured per individual example rather than as
- [Self-Containment Rules: Where to Place Extensive Explanations](./14-where-to-place-extensive-explanations.md) — Defines the split between what belongs inside code-block annotations (WHAT) versus markdown
- [Annotation Patterns Reference](./15-annotation-patterns-reference.md) — Reference patterns for annotating output, state changes, collections, and concurrency using the
- [Mermaid Diagram Guidelines](./16-mermaid-diagram-guidelines.md) — Defines when to include diagrams, the target diagram frequency, diagram types by
- [Coverage Progression by Level](./17-coverage-progression-by-level.md) — Defines the topic focus, topic list, and example count for beginner, intermediate,
- [File Naming and Organization: Directory Structure and Naming](./18-file-naming-and-directory-structure.md) — Defines the directory structure, file naming pattern, and the start of the
- [Examples-by-Level Section: Slug Algorithm and Example Numbering](./19-examples-by-level-slug-algorithm-and-numbering.md) — Details the github-slugger algorithm for anchor generation, why the Examples by Level
- [Frontmatter Requirements and Quality Checklist](./20-frontmatter-requirements-and-quality-checklist.md) — Specifies the required frontmatter fields for overview and level pages, plus the
- [Quality Checklist: Educational Value, Diagrams, and Structure](./20b-quality-checklist-continued.md) — Continues the pre-publish quality checklist with the educational value, diagrams, and structure
- [Validation and Enforcement, and Relationship to Other Tutorial Types](./21-validation-enforcement-and-relationship-to-other-types.md) — Lists what the checker agent automatically validates and production validation results, the
- [Cross-Language Consistency, Standards Summary, and Principles](./22-cross-language-consistency-and-standards-summary.md) — Defines what must stay consistent vs vary across languages, summarizes the production-validated
- [Scope and Related References](./23-scope-and-related-references.md) — States what by-example convention covers and does not cover, and links to
- [Multiple Code Blocks Pattern: Structure, Benefits, and the Anti-Pattern](./24-multiple-code-blocks-pattern-structure-and-anti-pattern.md) — Introduces the multiple-code-blocks pattern for comparisons, its structure and benefits, and the
- [Multiple Code Blocks Pattern: The Correct Pattern](./25-multiple-code-blocks-correct-pattern.md) — Shows the correct multiple-code-blocks pattern for a two-library comparison, with trade-off text
- [Multiple Code Blocks Pattern: When to Split Code Blocks](./26-multiple-code-blocks-when-to-split.md) — Lists the indicators that signal a code block should be split into
- [Multiple Code Blocks Pattern: Usage, Five-Part Integration, and Density Measurement](./27-multiple-code-blocks-usage-and-density-measurement.md) — Defines when to use vs avoid multiple code blocks, how the pattern
