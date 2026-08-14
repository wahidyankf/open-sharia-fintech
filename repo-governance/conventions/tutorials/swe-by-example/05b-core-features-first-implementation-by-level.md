---
title: "Core Features First: Implementation by Coverage Level"
description: "Shows how core-features-first applies concretely across beginner, intermediate, and advanced coverage levels."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when deciding exactly how much core-feature purity vs external tooling is expected at a specific coverage level (beginner/intermediate/advanced)."
---

# Core Features First: Implementation by Coverage Level

## Implementation in Coverage Levels

**Beginner (0-40% coverage)**:

- **100% core features** - Zero external dependencies or abstractions
- **Languages**: Language syntax, core types, standard library modules
- **Frameworks**: Framework primitives and built-in features
- **Platforms**: Built-in capabilities and native APIs
- Examples run immediately with base technology installed

**Intermediate (40-75% coverage)**:

- **Primarily core features** with selective external tool/abstraction introduction
- Introduce production-critical frameworks/libraries when teaching architecture patterns
- Always explain WHY core features alone insufficient
- **Language example**: Teach basic HTTP with `java.net.http`, then Spring WebClient for reactive patterns
- **React example**: Teach state with `useState`/`useReducer`, then Redux for complex global state
- **Spring example**: Teach DI with Spring Core, then Spring Boot for deployment patterns

**Advanced (75-95% coverage)**:

- **Mixed core features and external tools** - Production ecosystem
- Focus on when to choose external tools vs core features
- Compare performance, complexity, maintenance trade-offs
- **Language example**: `ExecutorService` vs Kotlin Coroutines vs Project Loom
- **React example**: `useState` + Context vs Redux vs Zustand vs Jotai
- **Node.js example**: `http.createServer` vs Express vs Fastify performance comparison
