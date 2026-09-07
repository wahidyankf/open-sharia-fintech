---
description: Foundational tutorials (initial setup, quick start) and the code-first by-example track, the first two of five mandatory Full Set Tutorial Package components.
when_to_use: Use when defining or reviewing the foundational tutorials or the by-example track of a language's Full Set Tutorial Package.
---

# The Full Set Tutorial Package Components: Foundational Tutorials and By-Example Track

A complete programming language on ayokoding-www requires **all 5 mandatory components**:

## Component 1-2: Foundational Tutorials (Mandatory)

**Files**: `initial-setup.md`, `quick-start.md` at root level

**Coverage**: 0-30% cumulative

**Purpose**: Prerequisites for both learning tracks

**Initial Setup (0-5%)**:

- Installation instructions (platform-specific)
- Version verification
- First "Hello, World!" program
- Basic tool setup (compiler/interpreter, package manager)

**Quick Start (5-30%)**:

- 8-12 core concepts in order of importance
- Mermaid learning path diagram
- Runnable code for each touchpoint
- Links to by-example Beginner for rapid pickup

## Component 3: By-Example Track (Mandatory - PRIORITY)

**Location**: `by-example/` folder with 3 files

**Coverage**: 95% through 75-85 annotated code examples

**Priority**: **First learning track** - prioritized for fast learning ("move fast")

**Purpose**: Rapid language pickup through heavily annotated code examples

**Characteristics:**

- **Code-first approach** with minimal prose
- **75-85 heavily annotated examples** achieving 95% coverage
- **Self-contained examples** runnable without dependencies
- **Educational comments** showing outputs, states, intermediate values
- **Mermaid diagrams** when appropriate for concept relationships
- **Five-part structure** per example: brief explanation, optional diagram, heavily commented code, key takeaway

**Target Audience:**

- Experienced developers (seasonal programmers, software engineers)
- Already know at least one programming language well
- Want quick language pickup without extensive narrative
- Prefer learning through working code
- Need 95% coverage efficiently

**File Structure:**

```
by-example/
├── _index.md        # Navigation hub
├── overview.md      # Explains code-first approach
├── beginner.md      # Examples 1-25 (basics: syntax, control flow, functions)
├── intermediate.md  # Examples 26-50 (data structures, OOP/functional, modules)
└── advanced.md      # Examples 51-75 (concurrency, metaprogramming, internals)
```

**Content Requirements:**

See [By Example Tutorial Convention](../swe-by-example.md) for complete by-example standards including:

- Five-part example structure
- Self-containment rules
- Educational comment standards (`// =>` notation)
- Coverage progression (0-40%, 40-75%, 75-95%)
- Mermaid diagram usage

**NOT a replacement for:**

- By-concept tutorials (which provide deep explanations for complete beginners)
- Quick Start (which is 5-30% coverage touchpoints)
- Cookbook (which is problem-solving oriented, not learning-oriented)
