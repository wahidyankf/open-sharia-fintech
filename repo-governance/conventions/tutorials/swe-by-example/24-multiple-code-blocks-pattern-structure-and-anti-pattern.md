---
title: "Multiple Code Blocks Pattern: Structure, Benefits, and the Anti-Pattern"
description: "Introduces the multiple-code-blocks pattern for comparisons, its structure and benefits, and the anti-pattern of cramming comparisons into a single over-commented block."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when an example compares multiple approaches or libraries, to structure it as separate code blocks with text between them instead of one dense block."
---

# Multiple Code Blocks Pattern: Structure, Benefits, and the Anti-Pattern

**CRITICAL NEW RULE**: Examples comparing multiple approaches, libraries, or implementations should use MULTIPLE CODE BLOCKS with markdown text between them, NOT cramming all explanations into comments within a single code block.

## Pattern Structure

When demonstrating alternatives or comparisons:

1. **Brief explanation** (markdown text) - What are we comparing and why
2. **Code Block 1**: Approach A with minimal annotations (1.0-2.25 density)
3. **Explanation of Approach A** (markdown text) - WHY this approach, trade-offs
4. **Code Block 2**: Approach B with minimal annotations (1.0-2.25 density)
5. **Explanation of Approach B** (markdown text) - WHY this approach, trade-offs
6. **Comparison/Summary** (markdown text) - When to use each

## Benefits

- **Syntax highlighting works properly** - Each block gets correct language highlighting
- **Code is copy-paste runnable** - No need to extract from comment-heavy blocks
- **Clear separation of WHAT vs WHY** - Code shows WHAT (with state annotations), text explains WHY
- **Each code block maintains density target** - 1.0-2.25 annotations per code line per block
- **Better scannability** - Readers can quickly compare code side-by-side

## Anti-Pattern: Single Block with Excessive Comments

**BAD EXAMPLE** (violates density target and readability):

```java
// Library A approach - low-level API
import lib.A;
// => Uses library A
// => Requires manual configuration
// => Low-level API but powerful
// => More complex but flexible
ClassA a = new ClassA();
// => Creates instance of ClassA
// => Parameter 1: configuration object
// => Parameter 2: callback handler
// => This approach gives you full control

// Library B approach - high-level API
import lib.B;
// => Uses library B
// => Automatic configuration
// => High-level API but limited
// => Simpler but less flexible
ClassB b = ClassB.create();
// => Creates instance via factory method
// => No parameters needed (auto-configured)
// => This approach is easier but less powerful
```

**Problems**:

- Single code block has excessive comments (density > 2.5)
- Syntax highlighting broken (imports mixed with comments)
- Code not runnable (two incompatible approaches in one block)
- Hard to scan (comments overwhelm code)
- Explanations buried in code instead of structured text
