---
description: "Shows worked PASS/FAIL comparisons of core-features-first vs framework-first teaching for HTTP clients and Spring dependency injection, and ties the principle to related conventions."
when_to_use: "Read when you need worked PASS/FAIL comparison snippets for teaching HTTP clients or dependency injection progressively, or how this principle relates to other conventions."
---

# Core Features First: Comparison for HTTP Clients and DI, and Principle Integration

## Comparison: Core Features vs External Tools (continued)

**Teaching HTTP Clients (Language)**:

```markdown
## PASS: Progressive Approach

### Example 18: HTTP GET with HttpClient (Beginner)

Java 11+ provides `java.net.http.HttpClient` for synchronous and asynchronous HTTP...

### Example 45: Reactive HTTP with WebClient (Advanced)

Spring WebClient enables reactive streaming for high-throughput services...
Trade-off: Added complexity (Project Reactor) justified when handling >10K requests/sec
```

```markdown
## FAIL: Framework-First Approach

### Example 18: HTTP with OkHttp (Beginner)

OkHttp is popular for HTTP requests...
(External dependency before teaching standard library capabilities)
```

**Teaching Dependency Injection (Spring)**:

```markdown
## PASS: Progressive Approach

### Example 8: Dependency Injection with Spring Core (Beginner)

Spring Core `@Component` and `@Autowired` enable dependency injection...

### Example 32: Spring Boot Auto-Configuration (Intermediate)

Spring Boot auto-configures beans based on classpath and properties...
Trade-off: Convenience vs explicit control. Use when defaults match requirements.
Builds on explicit DI from Example 8.
```

```markdown
## FAIL: Auto-Magic First Approach

### Example 8: Spring Boot Application (Beginner)

Spring Boot automatically configures everything...
(Learner doesn't understand DI mechanism before seeing auto-magic!)
```

## Integration with Other Principles

This principle aligns with:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Start with simplest viable approach (core features)
- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: Core features work without dependency installation
- **[Progressive Disclosure](../../../principles/content/progressive-disclosure.md)**: Teach fundamentals (core features) before advanced abstractions (external tools)
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Explicit about when and why external dependencies/abstractions introduced
