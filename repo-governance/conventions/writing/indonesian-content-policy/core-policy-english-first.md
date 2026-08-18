---
title: "Indonesian Content Policy — Core Policy: English-First for Technical Tutorials"
description: The critical rule that ayokoding-www is English-first for technical tutorials, its rationale, and which content types it applies to.
when_to_use: Use when deciding what language to write a new technical tutorial or programming-language content page in.
category: explanation
subcategory: conventions
tags:
  - ayokoding-www
  - indonesian
  - bilingual
  - content-policy
  - translation
created: 2026-02-07
---

# Core Policy: English-First for Technical Tutorials

**CRITICAL RULE**: ayokoding-www is **English-first** for technical tutorials and programming language content.

**Rationale**:

1. **Resource Efficiency**: Translating technical tutorials doubles maintenance burden
2. **Quality Degradation**: Translated tutorials often become outdated as English originals update
3. **Programming Reality**: Most programming resources, documentation, and communities use English
4. **Indonesian Value Focus**: Indonesian content should provide unique value, not mirror English content

**Applies to**:

- Programming language tutorials (Golang, Java, TypeScript, Python, Kotlin, Rust, Elixir, etc.)
- Software engineering concepts and patterns
- Framework and library tutorials
- Tool usage guides
- Technical reference materials

**Example** (English tutorial, no Indonesian mirror):

```
content/en/learn/swe/programming-languages/golang/
├── _index.md
├── overview.md
├── tutorials/
│   ├── by-example/
│   │   ├── beginner.md
│   │   ├── intermediate.md
│   │   └── advanced.md
│   └── by-concept/
│       └── comprehensive.md

NO Indonesian mirror at:
content/id/belajar/swe/programming-languages/golang/
(unless explicitly requested)
```
