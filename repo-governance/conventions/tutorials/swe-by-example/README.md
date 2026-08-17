---
title: "By-Example Tutorial Convention"
description: "Standards for creating code-first by-example tutorials with 95% coverage, self-contained examples, and educational annotations"
when_to_use: "Read this index to find the right By-Example Tutorial Convention child document."
---

# By-Example Tutorial Convention

- [Purpose and Structure Integration with General Tutorial Standards](./01-purpose-and-structure-integration.md) — Read first when you need to understand why by-example tutorials exist and how their structure maps onto the general tutorial structure.
- [Purpose and Structure Integration](./01b-inherited-and-specialized-requirements.md) — You need the checklist of general tutorial standards a by-example tutorial must inherit, plus the extra requirements specific to by-example.
- [Core Characteristics](./02-core-characteristics.md) — You need the baseline definition of what makes a by-example tutorial code-first, its coverage target, and its example-count range.
- [Core Features First](./03-core-features-first-why.md) — Deciding whether an example should teach a language/framework primitive or an external library, and why that ordering matters.
- [Core Features First](./03b-core-features-first-what-to-prioritize.md) — You need the concrete checklist of what counts as a core/built-in feature to teach first for a given language, framework, or platform.
- [Core Features First](./04-core-features-first-what-to-avoid.md) — Writing or reviewing a beginner example to check it does not prematurely introduce a framework, library, or auto-magic tool.
- [Core Features First](./05-core-features-first-when.md) — Deciding at which coverage level (beginner/intermediate/advanced) an external dependency is finally permitted and how to introduce it.
- [Core Features First](./05b-core-features-first-implementation-by-level.md) — Deciding exactly how much core-feature purity vs external tooling is expected at a specific coverage level (beginner/intermediate/advanced).
- [Core Features First](./06-core-features-first-java-reference-and-validation.md) — You need a concrete worked example of core-features-first applied across levels, or the exact criteria the checker agent validates.
- [Core Features First](./07-core-features-first-comparison-json-and-state.md) — You need worked PASS/FAIL comparison snippets for teaching JSON processing or React state management progressively.
- [Core Features First](./07b-core-features-first-comparison-http-di-and-integration.md) — You need worked PASS/FAIL comparison snippets for teaching HTTP clients or dependency injection progressively, or how this principle relates to other conventions.
- [Example Structure](./08-example-structure-explanation-and-diagram.md) — Writing the brief explanation or diagram portion of an example, or when you need the annotation density requirement before writing annotated code.
- [Example Structure](./09-example-structure-annotated-code-reference.md) — You need a worked reference for measuring annotation density on a real code block, or the required-annotations and code-organization checklists.
- [Example Structure](./10-example-structure-takeaway-and-why-it-matters.md) — Writing the closing Key Takeaway or Why It Matters sections of an example, or checking their length and content requirements.
- [Complete Example Structure (Production Reference)](./11-complete-example-structure-reference.md) — You need a single complete worked example showing all five parts assembled together, to model a new example against.
- [Self-Containment Rules by Level](./12-self-containment-rules-by-level.md) — Deciding how much a given example may assume from earlier examples, or when checking whether a cross-reference is acceptable.
- [Self-Containment Rules](./13-per-example-annotation-density-measurement.md) — Validating or creating example content, to confirm density must be checked per example and not averaged across a file.
- [Self-Containment Rules](./14-where-to-place-extensive-explanations.md) — An annotation is getting too long or explanatory, to decide whether that content belongs in the code block or in a text section instead.
- [Annotation Patterns Reference](./15-annotation-patterns-reference.md) — Writing `// =>` style annotations for outputs, state, collections, or goroutine/channel concurrency and you need a worked pattern to follow.
- [Mermaid Diagram Guidelines](./16-mermaid-diagram-guidelines.md) — Deciding whether an example needs a diagram, which diagram type to use, or which colors are permitted.
- [Coverage Progression by Level](./17-coverage-progression-by-level.md) — Deciding which topics belong in the beginner, intermediate, or advanced level of a by-example tutorial.
- [File Naming and Organization](./18-file-naming-and-directory-structure.md) — Scaffolding a new by-example tutorial's directory/files, or when writing the Examples by Level bullet list on overview.md.
- [Examples-by-Level Section](./19-examples-by-level-slug-algorithm-and-numbering.md) — You need to compute a github-slugger anchor by hand, justify why the Examples by Level section exists, or determine sequential example numbering across levels.
- [Frontmatter Requirements](./20-frontmatter-requirements-and-quality-checklist.md) — Publishing by-example content, to confirm frontmatter is complete and every quality checklist item is satisfied.
- [Quality Checklist](./20b-quality-checklist-continued.md) — Publishing by-example content, alongside the Coverage/Self-Containment/Code Quality checklist, to confirm educational value, diagram, and structure requirements are satisfied.
- [Validation and Enforcement](./21-validation-enforcement-and-relationship-to-other-types.md) — You need to know exactly what the automated checker validates, how the quality-gate workflow runs, or how by-example compares to other tutorial types.
- [Cross-Language Consistency](./22-cross-language-consistency-and-standards-summary.md) — Creating by-example tutorials for a new language, to know what must match across languages and what is allowed to vary, plus the target numbers to hit.
- [Scope and Related References](./23-scope-and-related-references.md) — You need to confirm whether a topic falls inside this convention's scope, or need links to the related agents/workflows/skills that implement it.
- [Multiple Code Blocks Pattern](./24-multiple-code-blocks-pattern-structure-and-anti-pattern.md) — An example compares multiple approaches or libraries, to structure it as separate code blocks with text between them instead of one dense block.
- [Multiple Code Blocks Pattern](./25-multiple-code-blocks-correct-pattern.md) — You need a concrete worked example of the correct multiple-code-blocks pattern to model a comparison example against.
- [Multiple Code Blocks Pattern](./26-multiple-code-blocks-when-to-split.md) — Reviewing a single code block that mixes languages, alternatives, or excessive comparison comments, to decide whether it must be split.
- [Multiple Code Blocks Pattern](./27-multiple-code-blocks-usage-and-density-measurement.md) — Deciding whether an example needs multiple code blocks, how to slot them into the five-part format, or how to measure density across blocks.
