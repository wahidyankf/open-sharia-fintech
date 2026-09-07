---
description: "Standards for linking from docs/ to apps/ayokoding-www/ content using relative paths instead of public web URLs"
when_to_use: "Read this index to find the right Internal AyoKoding Reference Links Convention child document."
---

# Internal AyoKoding Reference Links Convention

- [Principles Implemented/Respected](./principles-implemented-respected.md) — The three software-engineering principles this AyoKoding-linking convention implements — Explicit Over Implicit, Reproducibility First, Simplicity Over Complexity. Use when you need to justify why this convention prefers relative repository paths over public URLs in terms of the repository's core principles.
- [Purpose](./purpose.md) — Why this convention exists — preventing broken AyoKoding links across offline, CI/CD, and cloned-repository development contexts. Use when you want to understand what problem this linking convention solves before applying it to a new document.
- [Scope](./scope.md) — What this convention covers (docs/ to apps/ayokoding-www/ relative linking) and what it explicitly excludes. Use when checking whether a specific linking scenario falls inside or outside this convention's coverage.
- [Standards](./standards.md) — The core rule, pattern recognition, path-calculation method, common path examples, language selection, and link-text guidelines for AyoKoding relative-path linking. Use when writing or reviewing a link from docs/ to apps/ayokoding-www/ and you need the exact relative-path rule and examples.
- [Examples](./examples.md) — Four worked examples of converting public AyoKoding URLs to correct relative repository paths, including a multi-link learning-resources block. Use when you want a concrete before/after example to copy while fixing or writing an AyoKoding cross-reference.
- [Enforcement](./enforcement.md) — How this convention is enforced — manual PR review, a future automated CI link check, and docs-checker agent validation. Use when setting up or reviewing enforcement for AyoKoding link correctness (PR review checklist, CI script, or agent rules).
- [Edge Cases and Special Considerations](./edge-cases-and-special-considerations.md) — When public ayokoding.com URLs are the correct choice, how to reference Indonesian-language content, and how to handle AyoKoding path migrations. Use when a linking situation doesn't fit the standard docs/-to-relative-path rule — public-facing content, Indonesian content, or a directory reorganization.
