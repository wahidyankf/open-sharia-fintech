---
description: Standards for referencing dynamic collections (agents, principles, conventions, practices, skills) in documentation without hardcoding counts that become stale
when_to_use: Use when writing a sentence, layer description, index summary, or directory-tree comment that mentions how many agents, skills, conventions, principles, practices, or workflows exist.
---

# Dynamic Collection References Convention

This convention defines how to reference dynamic collections in documentation. A dynamic collection is any group whose membership changes over time as items are added or removed. Hardcoding a count for such a collection creates a maintenance burden: every addition or removal requires finding and updating every document that mentions the count. Instead, reference collections by name and link, letting readers find the current count themselves.

## Contents

- [Purpose, Principles, and Scope](./dynamic-collection-references/purpose-principles-and-scope.md) — why hardcoded counts are a problem, the principles this convention implements, and what is in/out of scope.
- [Standards (Rules 1-4)](./dynamic-collection-references/standards-rules-1-to-4.md) — never hardcode counts, layer descriptions, index summaries, and directory tree comments.
- [Standards (Rules 5-7)](./dynamic-collection-references/standards-rules-5-to-7.md) — where counts are acceptable, the index-as-source-of-truth rule, and the amendment numeric-sweep rule.
- [Examples and Special Considerations](./dynamic-collection-references/examples-and-special-considerations.md) — before/after conversions, the pattern-recognition list, and edge cases (index footers, workflow counts).

## Tools, Automation, and References

### Tools and Automation

The following agents check and enforce this convention:

- **rules-checker** - Validates repository-wide consistency including hardcoded counts
- **rules-propagation** - Applies fixes for governance violations including count removal

### References

**Related Conventions:**

- [Content Quality Principles](./quality.md) — Universal quality standards; accuracy is a quality requirement
- [Conventions Writing Convention](./conventions.md) — Meta-convention for writing convention documents

**Related Development Practices:**

- [AI Agents Convention](../../development/agents/ai-agents.md) — Defines how agents are structured and maintained

**Agents:**

- `rules-maker` - Creates governance documents following this convention
- `rules-checker` - Validates convention compliance across the repository
- `rules-propagation` - Fixes convention violations
