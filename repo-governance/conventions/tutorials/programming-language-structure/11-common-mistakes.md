---
title: "Common Mistakes"
description: Five common tutorial-structure mistakes, each with a FAIL example and the corrected PASS version.
when_to_use: Use when reviewing a tutorial structure for common structural mistakes before or during a PR.
category: explanation
subcategory: conventions
tags:
  - programming-languages
  - tutorials
  - ayokoding-www
  - education
  - structure
created: 2025-12-27
---

# Common Mistakes

FAIL: **Mistake 1: Nesting foundational tutorials in by-concept/**

```
# WRONG!
by-concept/
├── initial-setup.md   # Should be at tutorials/ root
└── quick-start.md     # Should be at tutorials/ root
```

PASS: **Correct: Foundational at root**

```
# RIGHT!
tutorials/
├── by-concept/
├── initial-setup.md   # At root - prerequisite for both paths
└── quick-start.md     # At root - prerequisite for both paths
```

---

FAIL: **Mistake 2: Wrong navigation order**

```markdown
# WRONG! Setup/quick-start before learning paths

- [Initial Setup](/en/.../initial-setup)
- [Quick Start](/en/.../quick-start)
- [By Concept](/en/.../by-concept)
- [By Example](/en/.../by-example)
```

PASS: **Correct: Learning paths first**

```markdown
# RIGHT! Learning path choice comes first

- [By Concept](/en/.../by-concept)
- [By Example](/en/.../by-example)
- [Initial Setup](/en/.../initial-setup)
- [Quick Start](/en/.../quick-start)
```

---

FAIL: **Mistake 3: Using relative paths**

```markdown
# WRONG! Relative paths break from different page contexts

- [Beginner](by-concept/beginner)
- [Examples](./by-example/beginner)
```

PASS: **Correct: Absolute paths**

```markdown
# RIGHT! Absolute paths work from any context

- [Beginner](/en/learn/software-engineering/programming-language/java/tutorials/by-concept/beginner)
- [Examples](/en/learn/software-engineering/programming-language/java/tutorials/by-example/beginner)
```

---

FAIL: **Mistake 4: Creating by-example before by-concept**

```
# WRONG! By-example created first
java/tutorials/
├── by-example/          # Created first
└── initial-setup.md     # Missing by-concept/
```

PASS: **Correct: By-example prioritized first**

```
# RIGHT! By-example first (move fast), then by-concept (learn deep) - both mandatory
java/tutorials/
├── by-example/          # Component 3 - PRIORITY (mandatory)
├── by-concept/          # Component 4 (mandatory)
├── cookbook/            # Component 5 (mandatory)
├── initial-setup.md     # Component 1 (mandatory)
└── quick-start.md       # Component 2 (mandatory)
```

---

FAIL: **Mistake 5: Missing overview.md files**

```
# WRONG! No overview explaining learning approach
by-concept/
├── _index.md
├── beginner.md          # Missing overview.md
├── intermediate.md
└── advanced.md
```

PASS: **Correct: Overview explains path**

```
# RIGHT! Overview sets expectations
by-concept/
├── _index.md
├── overview.md          # Explains narrative-driven approach
├── beginner.md
├── intermediate.md
└── advanced.md
```
