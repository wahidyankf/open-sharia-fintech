---
title: "Coverage Progression by Level"
description: "Defines the topic focus, topic list, and example count for beginner, intermediate, and advanced coverage levels."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when deciding which topics belong in the beginner, intermediate, or advanced level of a by-example tutorial."
---

# Coverage Progression by Level

## Beginner (0-40% coverage)

**Focus**: Language/framework fundamentals and core syntax

**Topics**:

- Variable declaration and types
- Control flow (if, loops, switch)
- Functions and methods
- Basic data structures (arrays, slices, maps, structs)
- Error handling basics
- Package/module structure
- Basic testing
- Standard library essentials

**Example count**: 27-30 examples

## Intermediate (40-75% coverage)

**Focus**: Production patterns and framework features

**Topics**:

- Advanced data structures and patterns
- Concurrency primitives
- I/O and networking
- HTTP clients and servers
- Database access patterns
- Testing strategies (integration, mocking)
- Common frameworks and libraries
- Error wrapping and custom errors
- Configuration and environment handling

**Example count**: 20-30 examples (varies by language complexity)

**Rationale for variance**: Some languages have simpler production patterns requiring fewer examples (Java: 20), while others with richer standard libraries need more (Golang, Python: 30).

## Advanced (75-95% coverage)

**Focus**: Expert mastery and optimization

**Topics**:

- Advanced concurrency patterns (pipelines, fan-out/fan-in)
- Performance optimization and profiling
- Reflection and metaprogramming
- Generic programming (where applicable)
- Advanced framework features
- Production deployment patterns
- Observability (metrics, tracing, logging)
- Security patterns
- Internals and debugging
- Best practices synthesis

**Example count**: 25-28 examples
