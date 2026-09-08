---
description: The three software-engineering principles this AyoKoding-linking convention implements — Explicit Over Implicit, Reproducibility First, Simplicity Over Complexity.
when_to_use: Use when you need to justify why this convention prefers relative repository paths over public URLs in terms of the repository's core principles.
---

# Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Uses explicit relative file paths instead of implicit external URLs. When a docs/ file references ayokoding-www content, the relative path `../../../../../apps/ayokoding-www/content/en/learn/...` makes the relationship explicit and visible. No hidden assumptions about domain availability or DNS resolution.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: Relative paths work consistently across all environments (local development, CI/CD, offline testing, cloned repositories). External URLs depend on network availability, domain ownership, and DNS configuration. Relative paths eliminate these external dependencies for reproducible local builds.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: One linking pattern works everywhere in the repository. No special cases for "internal but looks external" links. No need to configure domain mappings or link rewriting. Just count the directory levels and use relative paths.
