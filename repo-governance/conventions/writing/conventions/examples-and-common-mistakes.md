---
description: A worked good-vs-bad example of full convention document structure, plus a table of common authoring mistakes and their fixes.
when_to_use: Use when you need a concrete template to copy or want to check a draft against known authoring pitfalls.
---

# Examples and Common Mistakes

## Examples

### Good Convention Document Structure

```markdown
---
description: Brief, clear description
when_to_use: Use when <the situation this convention governs>.
---

# Example Convention

Clear, concise introduction explaining what and why.

## Purpose

Why this convention exists and what problems it solves.

## Scope

### What This Convention Covers

- Specific topic A
- Specific topic B

### What This Convention Does NOT Cover

- Out-of-scope topic (see Other Convention)

## Standards

### Rule Category 1

Clear, imperative guidance with examples.

### Rule Category 2

More guidance with concrete examples.

## Examples

### Good Examples

Showing correct usage.

### Bad Examples

Showing what to avoid and why.

## References

**Related Conventions:**

- Related Convention

**Agents:**

- `example-agent` - Uses this convention for validation
```

### Bad Convention Document Structure

```markdown
# Some Topic

This is about some stuff.

Here are some rules:

- Do this
- Don't do that

The end.
```

**Problems:**

- FAIL: No frontmatter
- FAIL: No clear purpose or scope
- FAIL: No examples
- FAIL: No references
- FAIL: Vague, unconvincing content
- FAIL: No rationale for rules

## Common Mistakes to Avoid

| Mistake                 | FAIL: Problem                                       | PASS: Solution                                      |
| ----------------------- | --------------------------------------------------- | --------------------------------------------------- |
| **Scope creep**         | Convention tries to cover too many unrelated topics | Define clear scope; split if needed                 |
| **No examples**         | Only abstract rules, no concrete demonstrations     | Add good PASS: and bad FAIL: examples               |
| **Missing rationale**   | Rules without explanation of "why"                  | Explain reasoning, especially for non-obvious rules |
| **Orphaned convention** | Not referenced anywhere, not used by agents         | Ensure integration with agents or processes         |
| **Overlapping scope**   | Duplicates content from other conventions           | Consolidate or clearly delineate boundaries         |
| **Too prescriptive**    | Overly detailed rules for simple topics             | Match detail level to topic complexity              |
| **No cross-references** | Doesn't link to related conventions                 | Add References section with related docs            |
