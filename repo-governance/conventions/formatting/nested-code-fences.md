---
title: "Nested Code Fence Convention"
description: Standards for properly nesting code fences when documenting markdown structure within markdown content
when_to_use: Use when a markdown example itself needs to show a fenced code block, and the outer/inner fence depth must be chosen correctly.
category: explanation
subcategory: conventions
tags:
  - markdown
  - code-fences
  - nesting
  - syntax
  - documentation
created: 2025-12-23
---

# Nested Code Fence Convention

This convention defines how to properly nest code fences when documenting markdown structure within markdown content. Understanding the correct nesting pattern prevents rendering bugs that break markdown formatting.

## In This Convention

- [Purpose, Scope, and the Orphaned Fence Problem](./nested-code-fences/purpose-scope-and-the-orphaned-fence-problem.md) — Principles, scope, and how an orphaned closing fence breaks rendering
- [Fence Depth Rules and Complete Nesting Examples](./nested-code-fences/fence-depth-rules-and-complete-nesting-examples.md) — The 4-backtick outer / 3-backtick inner rule and three worked examples
- [Validation Checklist and Troubleshooting](./nested-code-fences/validation-checklist-and-troubleshooting.md) — Pre-commit checklist and symptom-based rendering troubleshooting
- [Testing, Integration, and Related Conventions](./nested-code-fences/testing-integration-and-related-conventions.md) — How to test nested fences and how this convention relates to others
- [Examples in Documentation Types and References](./nested-code-fences/examples-in-documentation-types-and-references.md) — Tutorial, how-to, and reference examples, plus spec references

## Common Mistakes and How to Fix Them

### Mistake 1: Extra Closing Fence

**Broken**:

`````markdown
````markdown
#### Example

```javascript
code here
```
````

```← ORPHANED! Breaks rendering

```
`````

**Fixed**:

`````markdown
````markdown
#### Example

```javascript
code here
```
````
`````

**Fix**: Remove the orphaned closing fence after the proper 4-backtick closure.

### Mistake 2: Wrong Fence Depth

**Broken** (using 3 backticks for outer fence):

`````markdown
````markdown
#### Example

```javascript
code here
```
````
`````

```

```

``````

**Problem**: Parser can't distinguish outer from inner fences. Rendering is unpredictable.

**Fixed** (using 4 backticks for outer fence):

`````markdown
````markdown
### Example

```javascript
code here
```
``````

``````

## Mistake 3: Mismatched Fence Pairs

**Broken**:

`````markdown
`````markdown
### Example

`````javascript
code here
````   ← WRONG! Closes with 4 backticks (should be 3)
````   ← WRONG! Extra 4-backtick fence
``````

```

```

**Fixed**:

`````markdown
````markdown
### Example

```javascript
code here
```
````
`````

**Fix**: Each fence pair must use same depth (3-3 or 4-4, not 3-4).
