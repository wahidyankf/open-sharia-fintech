---
description: Worked complete-structure and navigation examples for a dual-path language (Java) and a single-path language (Kotlin).
when_to_use: Use when you need a concrete worked example of tutorials/ structure and navigation for a dual-path or single-path language.
---

# Examples

## Example 1: Java (Dual-Path Language)

**Complete Structure:**

```
java/tutorials/
├── _index.md                # "Tutorials" (weight: 100002)
├── by-concept/
│   ├── _index.md            # "By Concept" (weight: 1000000)
│   ├── overview.md          # "Overview" (weight: 10000000)
│   ├── beginner.md          # "Beginner Tutorial" (weight: 10000001)
│   ├── intermediate.md      # "Intermediate Tutorial" (weight: 10000002)
│   └── advanced.md          # "Advanced Tutorial" (weight: 10000003)
├── by-example/
│   ├── _index.md            # "By Example" (weight: 1000001)
│   ├── overview.md          # "Overview" (weight: 10000000)
│   ├── beginner.md          # "Beginner Examples" (weight: 10000001)
│   ├── intermediate.md      # "Intermediate Examples" (weight: 10000002)
│   └── advanced.md          # "Advanced Examples" (weight: 10000003)
├── initial-setup.md         # "Initial Setup" (weight: 1000002)
└── quick-start.md           # "Quick Start" (weight: 1000003)
```

**Navigation (`tutorials/_index.md`):**

```markdown
---
title: Tutorials
weight: 100002
---

- [By Concept](/en/learn/software-engineering/programming-language/java/tutorials/by-concept)
- [By Example](/en/learn/software-engineering/programming-language/java/tutorials/by-example)
- [Initial Setup](/en/learn/software-engineering/programming-language/java/tutorials/initial-setup)
- [Quick Start](/en/learn/software-engineering/programming-language/java/tutorials/quick-start)
```

## Example 2: Kotlin (Single-Path Language)

**Complete Structure:**

```
kotlin/tutorials/
├── _index.md                # "Tutorials" (weight: 100002)
├── by-concept/
│   ├── _index.md            # "By Concept" (weight: 1000000)
│   ├── overview.md          # "Overview" (weight: 10000000)
│   ├── beginner.md          # "Beginner Tutorial" (weight: 10000001)
│   ├── intermediate.md      # "Intermediate Tutorial" (weight: 10000002)
│   └── advanced.md          # "Advanced Tutorial" (weight: 10000003)
├── initial-setup.md         # "Initial Setup" (weight: 1000001)
└── quick-start.md           # "Quick Start" (weight: 1000002)
```

**Navigation (`tutorials/_index.md`):**

```markdown
---
title: Tutorials
weight: 100002
---

- [By Concept](/en/learn/software-engineering/programming-language/kotlin/tutorials/by-concept)
- [Initial Setup](/en/learn/software-engineering/programming-language/kotlin/tutorials/initial-setup)
- [Quick Start](/en/learn/software-engineering/programming-language/kotlin/tutorials/quick-start)
```

**Note**: When Kotlin gains by-example path, `initial-setup.md` weight changes from 1000001 to 1000002, `quick-start.md` from 1000002 to 1000003.
