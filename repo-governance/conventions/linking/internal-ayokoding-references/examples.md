---
title: "Examples"
description: Four worked examples of converting public AyoKoding URLs to correct relative repository paths, including a multi-link learning-resources block.
when_to_use: Use when you want a concrete before/after example to copy while fixing or writing an AyoKoding cross-reference.
category: explanation
subcategory: conventions
tags:
  - linking
  - cross-reference
  - relative-paths
  - portability
  - ayokoding-www
created: 2026-02-07
---

# Examples

## Example 1: Java Documentation Cross-Reference

**Context:** docs/explanation/software-engineering/programming-languages/java/README.md references AyoKoding Java tutorials

**Scenario:** Pointing readers to comprehensive Java learning content

❌ **WRONG:**

```markdown
For hands-on Java tutorials, see our [Java learning path](https://ayokoding.com/en/learn/software-engineering/programming-languages/java/).
```

✅ **CORRECT:**

```markdown
For hands-on Java tutorials, see our [Java learning path](../../../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/java/).
```

## Example 2: Spring Framework Reference

**Context:** docs/explanation/software-engineering/platform-web/tools/jvm-spring/README.md references AyoKoding Spring content

**Scenario:** Directing readers to framework tutorials

❌ **WRONG:**

```markdown
Learn Spring Framework basics at [ayokoding.com](https://ayokoding.com/en/learn/software-engineering/platform-web/tools/jvm-spring/).
```

✅ **CORRECT:**

```markdown
Learn Spring Framework basics in our [comprehensive Spring tutorial series](../../../../../../apps/ayokoding-www/content/en/learn/software-engineering/platforms/web/tools/jvm-spring/).
```

## Example 3: Spring Boot Deep Dive

**Context:** docs/explanation/software-engineering/platform-web/tools/jvm-spring-boot/README.md references Spring Boot tutorials

**Scenario:** Cross-referencing detailed Spring Boot educational content

❌ **WRONG:**

```markdown
Check out our [Spring Boot tutorials](https://ayokoding.com/en/learn/software-engineering/platform-web/tools/jvm-spring-boot/) for practical examples.
```

✅ **CORRECT:**

```markdown
Check out our [Spring Boot tutorials](../../../../../../apps/ayokoding-www/content/en/learn/software-engineering/platforms/web/tools/jvm-spring-boot/) for practical examples.
```

## Example 4: Multiple Cross-References in One Document

**Context:** docs/explanation/software-engineering/programming-languages/java/README.md references multiple AyoKoding sections

**Scenario:** Comprehensive navigation to related educational content

✅ **CORRECT:**

```markdown
## Learning Resources

This documentation provides reference material for Java in the open-sharia-enterprise project. For comprehensive learning content, explore:

- **[Java Fundamentals](../../../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/java/)** - Core language concepts, syntax, and basic programming
- **[Spring Framework](../../../../../../apps/ayokoding-www/content/en/learn/software-engineering/platforms/web/tools/jvm-spring/)** - Dependency injection, AOP, and enterprise patterns
- **[Spring Boot](../../../../../../apps/ayokoding-www/content/en/learn/software-engineering/platforms/web/tools/jvm-spring-boot/)** - Rapid application development with Spring ecosystem
```
