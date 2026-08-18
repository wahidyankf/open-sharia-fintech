---
title: "Dynamic Collection References Convention"
description: Standards for referencing dynamic collections (agents, principles, conventions, practices, skills) in documentation without hardcoding counts that become stale
when_to_use: Use when writing a sentence, layer description, index summary, or directory-tree comment that mentions how many agents, skills, conventions, principles, practices, or workflows exist.
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - maintenance
  - collections
created: 2026-02-22
---

# Dynamic Collection References Convention

This convention defines how to reference dynamic collections in documentation. A dynamic collection is any group whose membership changes over time as items are added or removed. Hardcoding a count for such a collection creates a maintenance burden: every addition or removal requires finding and updating every document that mentions the count. Instead, reference collections by name and link, letting readers find the current count themselves.

## Contents

- [Purpose, Principles, and Scope](./dynamic-collection-references/purpose-principles-and-scope.md) — why hardcoded counts are a problem, the principles this convention implements, and what is in/out of scope.
- [Standards (Rules 1-4)](./dynamic-collection-references/standards-rules-1-to-4.md) — never hardcode counts, layer descriptions, index summaries, and directory tree comments.
- [Standards (Rules 5-7)](./dynamic-collection-references/standards-rules-5-to-7.md) — where counts are acceptable, the index-as-source-of-truth rule, and the amendment numeric-sweep rule.
- [Examples and Special Considerations](./dynamic-collection-references/examples-and-special-considerations.md) — before/after conversions, the pattern-recognition list, and edge cases (index footers, workflow counts).
- [Tools, Automation, and References](./dynamic-collection-references/tools-automation-and-references.md) — enforcing agents and links to related conventions.
