---
description: The narrative-driven by-concept track and the practical cookbook, the remaining two of five mandatory Full Set Tutorial Package components.
when_to_use: Use when defining or reviewing the by-concept track or the cookbook of a language's Full Set Tutorial Package.
---

# The Full Set Tutorial Package Components: By-Concept Track and Cookbook

## Component 4: By-Concept Track (Mandatory)

**Location**: `by-concept/` folder with 3 files

**Coverage**: 95% through narrative-driven tutorials

**Purpose**: Deep understanding through comprehensive narrative-driven tutorials ("learn deep")

**Characteristics:**

- **Comprehensive explanations** with rationale and context
- **Progressive examples** building on previous concepts
- **Diagrams and visualizations** for complex concepts
- **0-95% coverage** through three levels (beginner 0-40%, intermediate 40-75%, advanced 75-95%)
- **Methodical learning** for deep foundation

**Target Audience:**

- Complete beginners to programming
- Developers wanting deep language understanding
- Learners who prefer narrative explanations
- Building production-ready skills

**File Structure:**

```
by-concept/
├── _index.md        # Navigation hub
├── overview.md      # Explains narrative-driven approach
├── beginner.md      # Fundamentals with detailed explanations (0-40%)
├── intermediate.md  # Production patterns with context (40-75%)
└── advanced.md      # Expert mastery with internals (75-95%)
```

**Content Requirements:**

See [Programming Language Content Standard](../programming-language-content.md) for complete pedagogical requirements including:

- Front hooks ("Want to..." opening paragraphs)
- Learning path visualizations (Mermaid diagrams)
- Prerequisites sections
- Progressive disclosure patterns
- Runnable code examples
- Hands-on exercises
- Cross-references

## Component 5: Cookbook (Mandatory)

**Location**: `cookbook/` folder (NEW LOCATION - moved from how-to/)

**Purpose**: Practical problem-solving recipes

**Structure**:

- 30+ recipes organized by category
- Problem → Solution → How It Works pattern
- Copy-paste ready code examples

**Organization**:

- Can use single file (`cookbook.md`) or multiple files by category
- Positioned at weight 1000002 (after by-example, before initial-setup)

**Why in tutorials/ folder now**:

- Part of complete educational package
- Complements both learning tracks
- Used alongside tutorials (not separate reference)
