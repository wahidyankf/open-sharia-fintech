---
title: "Convention Document Structure — Recommended and Optional Sections"
description: The recommended Examples, Comparison Tables, Special Considerations, Tools and Automation, and References sections, plus the optional Quick Reference/Migration Guide/FAQ/Rationale sections.
when_to_use: Use when deciding whether to add optional or recommended sections to a convention document beyond the required minimum.
category: explanation
subcategory: conventions
tags:
  - meta
  - conventions
  - standards
  - documentation
created: 2025-12-07
---

# Convention Document Structure — Recommended and Optional Sections

This page continues [Required Sections](./document-structure-required-sections.md) with the sections that are recommended, then optional, for a convention document.

## Recommended Sections

### 7. Examples Section (H2)

```markdown
## Examples

### Good Examples

Concrete examples showing correct usage

### Bad Examples

Concrete examples showing what to avoid (with explanations)
```

**Value:** Examples make abstract rules concrete and immediately actionable.

### 8. Comparison Tables

Use tables to contrast approaches:

```markdown
| Scenario  | PASS: Correct | FAIL: Incorrect | Why         |
| --------- | ------------- | --------------- | ----------- |
| Example 1 | Good way      | Bad way         | Explanation |
```

### 9. Edge Cases / Special Considerations (H2)

```markdown
## Special Considerations

Address nuanced scenarios, exceptions, or edge cases.
```

### 10. Tools and Automation (H2)

```markdown
## Tools and Automation

Reference agents or tools that enforce or assist with this convention:

- **agent-name** - What it does related to this convention
```

### 11. References Section (H2)

```markdown
## References

**Related Conventions:**

- Convention Name — How it relates

**External Resources:**

- [Resource Name](https://example.com) - Why it's relevant

**Agents:**

- `agent-name` - How it uses this convention
```

**Purpose:** Help readers discover related content and understand the convention's ecosystem.

## Optional Sections

- **Quick Reference** - Checklists or TL;DR summaries
- **Migration Guide** - How to adopt this convention in existing content
- **FAQ** - Common questions (use sparingly; prefer clear standards)
- **Rationale** - Deeper explanation of design decisions (for complex conventions)
