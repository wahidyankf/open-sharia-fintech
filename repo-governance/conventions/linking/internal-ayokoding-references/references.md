---
title: "References"
description: Related conventions, principles, and the docs-checker/docs-fixer agents that enforce AyoKoding relative-path linking.
when_to_use: Use when you need to jump from this convention to the broader linking convention, the principles it implements, or the agents that validate it.
category: explanation
subcategory: conventions
tags:
  - linking
  - cross-reference
  - relative-paths
  - portability
  - ayokoding-www
created: 2026-02-07
---

# References

**Related Conventions:**

- [Linking Convention](../../formatting/linking.md) — General markdown linking standards (GitHub-compatible paths with `.md`)
  **Related Principles:**

- [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) — Why explicit relative paths over implicit external URLs
- [Reproducibility First](../../../principles/software-engineering/reproducibility.md) — Why links must work across all environments
- [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md) — One pattern for repository-internal references

**Agents:**

- `docs-checker` - Validates docs/ links follow this convention
- `docs-fixer` - Applies corrections to convert public URLs to relative paths
