---
description: Defines what the Nested Code Fence Convention covers, the principles it implements, and how an orphaned closing fence breaks markdown rendering.
when_to_use: Use when you need to understand why nested code fences need special handling or what this convention covers.
---

# Purpose, Scope, and the Orphaned Fence Problem

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Explicitly documents nesting depth rules and fence pairing requirements. Makes the implicit markdown parsing behaviour explicit through clear examples.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Uses a simple depth rule (outer = 4 backticks, inner = 3 backticks) that's easy to remember and apply consistently.

## Purpose

This convention establishes the pattern for nesting code fences when documenting markdown structure. It prevents orphaned fence syntax that breaks rendering by using 4 backticks for outer fences and 3 for inner fences, ensuring markdown examples display correctly.

## Scope

### What This Convention Covers

- **Nested fence syntax** - 4 backticks outer, 3 backticks inner
- **When to nest** - Documenting markdown structure, code blocks, or fence syntax
- **Nesting depth** - How deep nesting can go (rarely beyond 2 levels)
- **Language hints** - How to specify syntax highlighting for nested blocks

### What This Convention Does NOT Cover

- **Regular code blocks** - Single-level code blocks use standard 3 backticks
- **Code quality** - This is about markdown syntax, not code content
- **Platform shortcodes** - Platform-specific alternatives (different syntax)

## Scope

This convention applies to markdown content in:

- **docs/** - Documentation showing markdown examples
- **Next.js sites** - Content demonstrating markdown structure (ayokoding-www, ose-www)
- **plans/** - Planning documents with markdown examples
- **Repository root files** - README.md, CONTRIBUTING.md when documenting markdown

**Universal Application**: Any markdown file that shows "how to write markdown" needs nested code fences.

## The Problem: Orphaned Closing Fences

When documenting markdown structure (showing "how to write markdown"), we need to display code fences within code fences. Incorrect nesting breaks rendering:

**Broken Structure** (causes rendering bugs):

`````markdown
````markdown
### Example: Code Block

**Code**:

```javascript
const x = 5;
```
````

**Summary**: This demonstrates...

```← EXTRA CLOSING FENCE (orphaned - breaks rendering)

```
`````

**Result**: Text after the orphaned fence shows as literal markdown (`**bold**` not rendered as **bold**).

**Why it breaks**: Markdown parser sees the orphaned ``` and treats remaining content as literal code, not formatted markdown.
