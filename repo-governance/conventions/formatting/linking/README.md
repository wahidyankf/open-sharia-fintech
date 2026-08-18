---
title: "Documentation Linking Convention"
description: "Standards for linking between documentation files in open-sharia-enterprise"
when_to_use: "Read this index to find the right Documentation Linking Convention child document."
---

# Documentation Linking Convention

- [Purpose, Scope, and Why GitHub-Compatible Links](./purpose-scope-and-why-github-compatible-links.md) — Defines what the Linking Convention covers, the principles it implements, and why the repository standardizes on GitHub-compatible relative markdown links. Use when you need to understand why this repository avoids wiki-style links or what the linking convention covers.
- [Link Syntax, Examples, and Correct Usage](./link-syntax-examples-and-correct-usage.md) — The required markdown link syntax and key rules, worked examples by file location, correct-vs-incorrect link examples, and external link formatting. Use when writing a link in documentation and you need the exact syntax or a worked example for your file's location.
- [Nested Directory Linking](./nested-directory-linking.md) — How to calculate the correct number of ../ segments for a relative link based on file nesting depth, with a depth reference table and worked patterns. Use when writing a relative link between files at different nesting depths and you need to count the correct number of ../ segments.
- [Anchors, Images, and Link Validation](./anchors-images-and-link-validation.md) — Anchor-link syntax and slug validation rules, image link syntax, and the pre-commit link verification checklist. Use when linking to a heading within a page, embedding an image, or verifying links before committing.
- [When to Link Rule References: Formatting and Examples](./when-to-link-rule-references-formatting-and-examples.md) — The two-tier formatting rule for referencing repository rules — markdown link on first mention, inline code on subsequent mentions — with correct and incorrect examples. Use when writing prose that references a vision, principle, convention, development practice, or workflow document more than once in a section.
- [When to Link Rule References: Exclusions](./when-to-link-rule-references-exclusions.md) — The cases where the two-tier link-then-inline-code formatting rule does not apply, and how the docs-checker agent validates the requirement. Use when deciding whether a rule reference inside a code block, quote, file path, or naming discussion is exempt from the two-tier formatting rule.
