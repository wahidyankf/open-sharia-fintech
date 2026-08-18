---
title: "Quality Standards"
description: "Defines the recipe completeness checklist, code quality standards, and annotation density target for cookbook recipes."
when_to_use: "Read when verifying a recipe's completeness, code quality, and annotation density before publishing."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - cookbook
  - education
  - problem-solving
  - recipes
created: 2026-01-30
---

# Quality Standards

## Recipe Completeness Checklist

Each recipe MUST have:

- ✅ Clear problem statement (1-3 sentences)
- ✅ Complete solution code (copy-paste ready)
- ✅ Code annotations (0.5-1.5 per line)
- ✅ How It Works explanation (2-4 paragraphs)
- ✅ Common Pitfalls list (3-5 items)
- ✅ Related Recipes links (2-4 items)
- ✅ Self-contained (all imports, no external dependencies on other recipes)

## Code Quality Standards

- **Runnable**: Code must work as-is (not pseudocode)
- **Production-ready**: Use real error handling, not TODO comments
- **Idiomatic**: Follow language conventions and best practices
- **Minimal**: Solve the problem without extra complexity
- **Annotated**: Use `// =>` or `# =>` for state/output annotations

## Annotation Density

**Target**: 0.5-1.5 comment lines per code line

**Rationale**: Cookbook code is copy-paste oriented, so annotations focus on "what this does" rather than educational "why we need this". Lighter annotation than by-example (1-2.25) but still helpful.

**Examples**:

```go
// GOOD: Concise annotation focused on action
file, err := os.Open(filepath)  // => Open file for reading
```

```go
// TOO MUCH: Over-explaining (by-example style, not cookbook style)
file, err := os.Open(filepath)  // => Open file for reading
                                // => os.Open returns (*File, error)
                                // => File is a handle to the opened file
                                // => We'll use this to create a CSV reader
```

```go
// TOO LITTLE: No annotation (reader must infer)
file, err := os.Open(filepath)
```
