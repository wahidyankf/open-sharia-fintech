---
title: "Multiple Code Blocks Pattern: Usage, Five-Part Integration, and Density Measurement"
description: "Defines when to use vs avoid multiple code blocks, how the pattern integrates with the five-part format, and how density is measured per code block."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when deciding whether an example needs multiple code blocks, how to slot them into the five-part format, or how to measure density across blocks."
---

# Multiple Code Blocks Pattern: Usage, Five-Part Integration, and Density Measurement

## When to Use Multiple Code Blocks

**Use multiple code blocks when**:

- Comparing different libraries (Library A vs Library B)
- Showing alternative implementations (approach 1 vs approach 2)
- Demonstrating evolution (before refactoring → after refactoring)
- Illustrating different language features (for loop vs stream API)
- Contrasting patterns (PASS: GOOD vs FAIL: BAD examples)

**Still use single code block when**:

- Showing one approach with progressive state changes
- Demonstrating linear execution flow
- Building up a single concept step by step
- Code doesn't involve comparisons or alternatives

## Integration with Five-Part Format

When using multiple code blocks within an example:

1. **Brief Explanation** - Introduce the comparison
2. **Diagram (optional)** - Show conceptual difference if helpful
3. **Multiple Annotated Code Blocks** - Each approach as separate block with text between
4. **Key Takeaway** - Summarize when to use each approach
5. **Why It Matters** - Production implications of the choice

## Annotation Density Measurement

**IMPORTANT**: Density is measured PER CODE BLOCK when using multiple blocks:

- Code Block 1 (Approach A): Should have 1.0-2.25 density
- Code Block 2 (Approach B): Should have 1.0-2.25 density
- Text sections between blocks: Do NOT count toward density

**Example measurement**:

```
Code Block 1: 5 code lines, 6 annotation lines = 1.2 density
Text Section: 3 sentences of explanation (NOT counted)
Code Block 2: 4 code lines, 8 annotation lines = 2.0 density
Overall: Both blocks meet 1.0-2.25 target
```
