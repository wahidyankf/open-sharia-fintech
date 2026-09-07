---
description: Policy defining when and how to create Indonesian content in ayokoding-www bilingual platform
when_to_use: Use when deciding what language to write new ayokoding-www content in, or whether an Indonesian translation of existing content is warranted.
---

# Indonesian Content Policy - ayokoding-www

This document defines the policy for Indonesian language content in ayokoding-www, establishing when Indonesian content should be created and what types of content are appropriate for Indonesian translation.

## Contents

- [Purpose, Principles, and Scope](./indonesian-content-policy/purpose-principles-and-scope.md) — why English-first exists, the principles it implements, and what's in/out of scope.
- [Indonesian Content Categories](./indonesian-content-policy/indonesian-content-categories.md) — encouraged unique content, allowed strategic translations, and discouraged mirror translations.
- [Decision Tree and Cross-Reference Requirements](./indonesian-content-policy/decision-tree-and-cross-reference-requirements.md) — the language-selection decision tree and mandatory cross-reference links.
- [Agent Guidelines and Migration Notes](./indonesian-content-policy/agent-guidelines-and-migration-notes.md) — how content/validation agents apply this policy, and its 2026-02-07 establishment history.
- [Rationale](./indonesian-content-policy/rationale.md) — why English-first for tutorials, and why unique Indonesian content is encouraged.
- [Examples](./indonesian-content-policy/examples.md) — three worked examples of compliant and non-compliant content creation.
- [Quality Checklist and References](./indonesian-content-policy/quality-checklist-and-references.md) — pre-publication checklist and related conventions/agents.

## Core Policy: English-First for Technical Tutorials

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
