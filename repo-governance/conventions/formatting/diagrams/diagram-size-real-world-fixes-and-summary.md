---
title: "Diagram Size and Splitting: Real-World Fixes and Summary"
description: "Shows real-world before/after examples of splitting oversized diagrams, plus a summary of the guidance."
when_to_use: "Use when you want worked before/after examples of diagram splitting, or a quick summary of the rule."
category: explanation
subcategory: conventions
tags:
  - diagrams
  - mermaid
  - ascii-art
  - visualization
  - conventions
  - accessibility
  - color-blindness
created: 2025-11-24
---

# Diagram Size and Splitting: Real-World Fixes and Summary

## Real-World Fixes

**Example 1: Sealed Classes (Before)**

Combined hierarchy + pattern matching:

```mermaid
graph TD
    Shape --> Circle
    Shape --> Rectangle
    Shape --> Triangle

    S[switch#40;shape#41;] --> Switch[Pattern Match]
    Switch --> |Circle| C[Handle Circle]
    Switch --> |Rectangle| R[Handle Rectangle]
    Switch --> |Triangle| T[Handle Triangle]
```

**Example 1: Sealed Classes (After)**

**Sealed Class Hierarchy:**

```mermaid
graph TD
    Shape[Shape<br/>sealed interface] --> Circle
    Shape --> Rectangle
    Shape --> Triangle
```

**Pattern Matching Switch:**

```mermaid
graph TD
    A[switch#40;shape#41;] --> B{Type?}
    B -->|Circle| C[area = π × r²]
    B -->|Rectangle| D[area = w × h]
    B -->|Triangle| E[area = ½ × b × h]
```

**Example 2: Concurrent Collections (Before)**

Combined BlockingQueue + ConcurrentHashMap:

```mermaid
graph TD
    BQ[BlockingQueue] --> Put[put#40;#41;]
    Put --> Take[take#40;#41;]

    CHM[ConcurrentHashMap] --> PutIfAbsent
    PutIfAbsent --> Compute
    Compute --> Merge
```

**Example 2: Concurrent Collections (After)**

**BlockingQueue (Producer-Consumer):**

```mermaid
graph TD
    Producer --> |put#40;item#41;| Queue[BlockingQueue]
    Queue --> |take#40;#41;| Consumer
    Queue --> |Blocks if full| Producer
    Consumer --> |Blocks if empty| Queue
```

**ConcurrentHashMap (Atomic Operations):**

```mermaid
graph TD
    A[putIfAbsent#40;k,v#41;] --> B{Key exists?}
    B -->|No| C[Insert value]
    B -->|Yes| D[Return existing]
```

## Summary

**Golden Rules**:

1. **One concept per diagram** - Each diagram explains one idea
2. **Limit branching** - Maximum 3-4 branches per level
3. **No subgraphs** - Use separate diagrams with headers instead
4. **Descriptive headers** - Add `**Concept Name:**` above each diagram
5. **Mobile-first** - Ensure readability on narrow screens

This prevents "too small" diagram issues and improves mobile user experience.
