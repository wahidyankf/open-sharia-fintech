---
title: "PASS: Best Practices"
description: Practices for minimal viable examples, multiple entry points, learn-more links, and complete levels.
category: explanation
subcategory: principles
tags:
  - principles
  - progressive-disclosure
  - user-experience
created: 2025-12-15
when_to_use: Use as a checklist when writing layered, audience-aware documentation.
---

# PASS: Best Practices

## 1. Start with Minimal Viable Example

**Hello World first**:

```typescript
// PASS: Simplest possible example
console.log("Hello, World!");
```

**Then add complexity**:

```typescript
// Next step: Add type safety
const message: string = "Hello, World!";
console.log(message);
```

## 2. Provide Multiple Entry Points

**For different audiences**:

```markdown
- **New to React?** Start with [Quick Start Tutorial](./react-quick-start.md)
- **Experienced developer?** See [API Reference](./react-api.md)
- **Migrating from Vue?** Read [Migration Guide](./migrate-from-vue.md)
```

## 3. Use "Learn More" Links

**Basic content with optional depth**:

```markdown
API authentication uses OAuth 2.0. [Learn more about OAuth 2.0](./oauth2.md)
```

**Not** embedding OAuth explanation in basic tutorial.

## 4. Layer Complexity in Sections

**Structure documentation progressively**:

```markdown
## Basic Configuration

Simple options most users need.

## Advanced Configuration

Optional optimization and edge cases.

## Expert Configuration

Internals and customization.
```

## 5. Create Complete Levels

**Each level is self-contained**:

- PASS: Beginner tutorial teaches 0-60% completely
- PASS: Beginner can build real projects with 60% knowledge
- PASS: Intermediate builds on beginner (not replacement)

**Not**:

- FAIL: Beginner tutorial leaves gaps
- FAIL: Must read intermediate to be productive
