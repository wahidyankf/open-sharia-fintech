---
title: "Multiple Code Blocks Pattern: The Correct Pattern"
description: "Shows the correct multiple-code-blocks pattern for a two-library comparison, with trade-off text between blocks and a benefits summary."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when you need a concrete worked example of the correct multiple-code-blocks pattern to model a comparison example against."
---

# Multiple Code Blocks Pattern: The Correct Pattern

**GOOD EXAMPLE** (maintains density, clear structure):

**Brief explanation**: Compare two libraries for HTTP client implementation - Library A offers low-level control while Library B provides convenience.

**Approach A: Library A (Low-Level Control)**

```java
import lib.A;

ClassA client = new ClassA();
// => Creates client instance
// => Requires manual configuration

client.configure(config);
// => Applies configuration
// => Sets timeout, headers, etc.

Response response = client.execute(request);
// => Executes HTTP request
// => Returns response object
```

**Library A Trade-offs**: Provides fine-grained control over connection pooling, retry logic, and request lifecycle. Requires manual configuration but enables advanced use cases like custom authentication schemes and request interceptors. Best for complex production systems needing precise control.

**Approach B: Library B (High-Level Convenience)**

```java
import lib.B;

ClassB client = ClassB.create();
// => Creates auto-configured client
// => Sensible defaults applied

Response response = client.get(url);
// => Executes GET request
// => Returns response object
```

**Library B Trade-offs**: Prioritizes developer experience with automatic configuration and fluent API. Limited customization options but handles 80% of use cases. Best for rapid prototyping and simple integrations.

**Comparison Summary**: Use Library A when you need complete control over HTTP behaviour (custom protocols, advanced retry logic, connection management). Use Library B for standard REST API consumption where defaults suffice. Library A has steeper learning curve but scales to complex requirements.

**Benefits of this approach**:

- **Each code block**: ~1.5 density (3 annotations for 2 code lines)
- **Syntax highlighting**: Works correctly for each block
- **Runnable code**: Each block is independently executable
- **Structured explanations**: WHY and trade-offs in text sections
- **Easy comparison**: Readers can see code side-by-side
