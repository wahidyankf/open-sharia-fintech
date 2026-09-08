---
description: Why Initial Setup and Quick Start live at the tutorials root instead of being nested inside a learning path.
when_to_use: Use when deciding where initial-setup.md and quick-start.md belong in a language's tutorials/ tree.
---

# Foundational Tutorials at Root

**CRITICAL**: Initial Setup and Quick Start remain at tutorials root level (NOT nested in by-concept or by-example).

**Rationale:**

- **Prerequisites for both paths**: Both by-concept and by-example assume working environment
- **Common entry point**: All learners need installation and basic verification
- **Accessibility**: Root placement signals "start here" before choosing learning path
- **Clarity**: Avoids duplication across paths

**Files:**

```
tutorials/
├── initial-setup.md   # 0-5% coverage: Installation, verification, Hello World
└── quick-start.md     # 5-30% coverage: Core concepts touchpoints
```

**Coverage:**

- **Initial Setup (0-5%)**: Get language working on learner's system
  - Installation instructions (platform-specific)
  - Version verification
  - First "Hello, World!" program
  - Basic tool setup (compiler/interpreter, package manager)
- **Quick Start (5-30%)**: Learn enough to explore independently
  - 8-12 core concepts in order of importance
  - Mermaid learning path diagram
  - Runnable code for each touchpoint
  - Links to by-example Beginner for fast pickup
