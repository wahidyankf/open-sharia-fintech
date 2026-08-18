---
title: "Diagram Size and Splitting: Why It Matters and When to Split"
description: "Explains why oversized diagrams are a problem, what makes a diagram too small/dense, and when to split it."
when_to_use: "Use when a diagram feels cluttered or hard to read and you're deciding whether it needs to be split."
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

# Diagram Size and Splitting: Why It Matters and When to Split

**CRITICAL RULE**: Split complex diagrams into multiple focused diagrams for mobile readability.

## Why This Matters

Large diagrams with multiple concepts, many branches, or subgraphs render too small on mobile devices (narrow screens) and become difficult to read. Mobile-first design requires each diagram to be simple enough to display clearly on small screens.

## Problem: Diagrams That Become Too Small

**Symptoms**:

- Diagram contains multiple distinct concepts in one visualization
- More than 4-5 branches from a single node (renders wide and small)
- Using `subgraph` syntax for comparisons (e.g., "Eager vs Lazy")
- Combining different aspects of a feature (hierarchy + usage pattern)

**Real-world examples of diagrams that were too small**:

1. **Java Example 43 (Sealed Classes)**: Combined sealed class hierarchy + pattern matching switch in one diagram
2. **Java Example 36 (Concurrent Collections)**: Combined BlockingQueue + ConcurrentHashMap in one diagram
3. **Kotlin Example 30 (Structured Concurrency)**: Combined hierarchy + cancellation propagation in one diagram
4. **Kotlin Example 34 (Flow Operators)**: Combined transform + buffer + conflate in one diagram
5. **Kotlin Example 38 (Sequences)**: Used subgraphs for Eager vs Lazy comparison
6. **Kotlin Example 43 (Operator Overloading)**: 7 operator types branching from one central node

## Solution: Split Into Focused Diagrams

**One Concept Per Diagram**: Each diagram should explain one idea, pattern, or workflow.

## When to Split

**SPLIT when you have**:

- Multiple distinct concepts in one diagram
- More than 4-5 branches from a single node
- `subgraph` syntax (replace with separate diagrams)
- A vs B comparisons (split into A diagram and B diagram)
- Workflow with multiple stages (split into stage-specific diagrams)

**KEEP as one diagram when**:

- Simple linear flow (3-4 steps)
- Single concept with minimal branching
- Diagram is already focused and readable on mobile
