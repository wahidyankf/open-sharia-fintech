---
description: "Defines the by-concept directory structure, file naming pattern, and concept-hierarchy section organization."
when_to_use: "Read when creating or naming the beginner, intermediate, and advanced files for a new By-Concept tutorial."
---

# File Naming and Organization

## Directory Structure

```
content/
└── en/
    └── learn/
        └── software-engineering/
            └── programming-language/
                └── {language}/
                    └── tutorials/
                        └── by-concept/
                            ├── _index.md          # Landing page
                            ├── beginner.md        # Sections 1-25 (0-40%)
                            ├── intermediate.md    # Sections 26-45 (40-75%)
                            └── advanced.md        # Sections 46-60 (75-95%)
```

## File Naming Pattern

- `beginner.md`: Always named "Beginner" (weight: 10000000)
- `intermediate.md`: Always named "Intermediate" (weight: 10000001)
- `advanced.md`: Always named "Advanced" (weight: 10000002)

## Section Organization

**Sections are NOT numbered** (unlike by-example examples which are numbered 1-85)

**Sections are organized by concept hierarchy**:

- Main Concept (H2)
  - Subsection 1 (H3)
  - Subsection 2 (H3)
  - Code examples within subsections

**Rationale**: Concept-driven learning groups related topics hierarchically, not sequentially.
