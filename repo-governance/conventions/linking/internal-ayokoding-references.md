---
description: Standards for linking from docs/ to apps/ayokoding-www/ content using relative paths instead of public web URLs
when_to_use: Use when linking from docs/ to educational content in apps/ayokoding-www/ and unsure whether to use a relative path or a public URL.
---

# Internal AyoKoding Reference Links Convention

This document defines standards for linking from documentation in `docs/` to educational content in `apps/ayokoding-www/` using repository-relative paths instead of public web URLs. This ensures links work during local development, testing, and remain portable across environments.

## In This Convention

- [Principles Implemented/Respected](./internal-ayokoding-references/principles-implemented-respected.md) — The three software-engineering principles this convention implements
- [Purpose](./internal-ayokoding-references/purpose.md) — Why this convention exists
- [Scope](./internal-ayokoding-references/scope.md) — What this convention covers and excludes
- [Standards](./internal-ayokoding-references/standards.md) — The core rule, path-calculation method, path examples, language selection, and link-text guidelines
- [Examples](./internal-ayokoding-references/examples.md) — Four worked before/after examples
- [Enforcement](./internal-ayokoding-references/enforcement.md) — Manual review, CI validation, and agent validation
- [Edge Cases and Special Considerations](./internal-ayokoding-references/edge-cases-and-special-considerations.md) — When public URLs are correct, Indonesian-language content, path migrations

## Path Verification Checklist

Before committing documentation with AyoKoding references:

- [ ] All AyoKoding links use relative paths (no `https://ayokoding.com/...`)
- [ ] Path depth matches file location in docs/ hierarchy
- [ ] Paths use `/en/` language directory (not `/id/`)
- [ ] Paths point to existing directories in apps/ayokoding-www/content/
- [ ] Link text is descriptive and context-appropriate
- [ ] Links tested locally (navigate in file explorer or markdown preview)

## Real-World Context

**Historical issue:** This convention was created after discovering 50+ instances where public web links (`https://ayokoding.com/...`) were incorrectly used instead of relative paths in Java, Spring Framework, and Spring Boot explanation documentation.

**Impact:** These external URLs created false external dependencies for repository-internal content, breaking offline development workflows and obscuring the repository structure.

**Resolution:** Systematic replacement of all `https://ayokoding.com/` URLs in docs/explanation/ with correct relative paths following this convention.

## References

**Related Conventions:**

- [Linking Convention](../formatting/linking.md) — General markdown linking standards (GitHub-compatible paths with `.md`)
  **Related Principles:**

- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — Why explicit relative paths over implicit external URLs
- [Reproducibility First](../../principles/software-engineering/reproducibility.md) — Why links must work across all environments
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — One pattern for repository-internal references

**Agents:**

- `docs-checker` - Validates docs/ links follow this convention
- `docs-fixer` - Applies corrections to convert public URLs to relative paths

## References

**Related Conventions:**

- [Linking Convention](../formatting/linking.md) — General markdown linking standards (GitHub-compatible paths with `.md`)
  **Related Principles:**

- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — Why explicit relative paths over implicit external URLs
- [Reproducibility First](../../principles/software-engineering/reproducibility.md) — Why links must work across all environments
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — One pattern for repository-internal references

**Agents:**

- `docs-checker` - Validates docs/ links follow this convention
- `docs-fixer` - Applies corrections to convert public URLs to relative paths
