---
title: "Core Features First: Why It Matters"
description: "Explains why by-example tutorials must teach core/built-in features before external dependencies, and the production impact of that ordering."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when deciding whether an example should teach a language/framework primitive or an external library, and why that ordering matters."
---

# Core Features First: Why It Matters

**Core Principle**: By-example tutorials MUST prioritize core/built-in/primitive features over external dependencies, abstractions, and third-party tools when teaching ANY technology (programming languages, frameworks, platforms).

## Why This Matters

Teaching core features first:

- **Establishes fundamental understanding** before abstractions and extensions
- **Keeps examples runnable** without dependency management (npm install, pip install, etc.)
- **Reduces maintenance burden** - no version conflicts, breaking API changes from third-party tools
- **Teaches portable knowledge** - core feature skills transfer across all projects using that technology
- **Enables immediate experimentation** - learners can run code without setup
- **Builds mental models** - understanding primitives reveals when abstractions add value

**Production impact**: Understanding core capabilities prevents unnecessary dependencies and abstractions. Developers who learn JSON processing with standard library (Java's `java.util.json`) understand fundamentals before reaching for Jackson. Those who learn React state with `useState` make informed decisions about when Redux/Zustand add value. Engineers who understand Spring Core DI recognize when Spring Boot auto-configuration helps vs hinders debugging.
