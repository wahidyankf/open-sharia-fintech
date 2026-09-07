---
description: "Defines the 1.0-2.25 comment-per-code-line density target and the `// =>` output-annotation pattern for By-Concept code blocks."
when_to_use: "Read when annotating code examples in a By-Concept tutorial and verifying comment density meets the standard."
---

# Annotation Density Standards

**CRITICAL REQUIREMENT: Annotation Density Standard**

- **Density target**: 1.0-2.25 lines of comment for every line of code (same as by-example)
- **Simple code**: 1 line of annotation per code line
- **Complex code**: 2-2.25 lines of annotation per code line
- **Focus**: Concise explanations that scale naturally with code complexity

**Annotation Quality Over Quantity**:

- Each line of code gets 1-2 lines explaining what it does and why
- Simple lines get brief explanations, complex lines get detailed breakdowns
- Annotations remain focused without repetitive patterns

**Output Annotation Pattern**

Use `// =>` or `# =>` to show outputs, states, and intermediate values:

```python
x = 42                            # => x references integer object 42
                                  # => type(x) is int

y = x * 2                         # => y is 84 (x unchanged at 42)
                                  # => Multiplication creates new object

print(y)                          # => Output: 84
```

## Where to Place Extensive Explanations

**CRITICAL**: Code block annotations should focus on WHAT the code does. Extensive WHY explanations go in narrative sections.

**Code block purpose** (inside ` ```language ` fence):

- Show WHAT each line does: `x := 10 // => x is now 10 (type: int)`
- Show return values: `result := fn() // => result is "output" (string)`
- Show state changes: `counter++ // => counter is now 5`
- Show outputs: `fmt.Println(x) // => Output: 10`

**Narrative section purpose** (before/after code blocks):

- WHY this concept matters
- HOW it works internally
- WHEN to use this pattern
- Production relevance and comparisons
- Trade-offs and alternatives
